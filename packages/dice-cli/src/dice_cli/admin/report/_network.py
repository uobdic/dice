import ipaddress
from enum import Enum
from typing import Any, Dict, Generator, List, Optional, Union

from dice_cli.cache import admin_cache
from dice_cli.logger import admin_logger


class HostState(Enum):
    DOWN = "DOWN"
    UP = "UP"


@admin_cache.memoize(expire=60 * 15, tag="_ip_to_fqdn")
def _ip_to_fqdn(
    ip_address: Union[ipaddress.IPv4Address, ipaddress.IPv6Address]
) -> Optional[str]:
    """Uses the Domain Name Service (DNS) to get the Fully Qualified Domain Name (FQDN) for a given IP address."""
    import dns.resolver
    import dns.reversename

    fqdn: Optional[str] = None
    address = dns.reversename.from_address(str(ip_address))
    try:
        fqdn = dns.resolver.query(address, "PTR")[0].to_text()
    except dns.resolver.NXDOMAIN:
        admin_logger.debug(f"No DNS entry for {ip_address}")
        return None

    return str(fqdn)


@admin_cache.memoize(expire=60 * 15, tag="_get_dns_hosts")
def _get_dns_hosts(ip_network: str) -> List[Dict[str, str]]:
    """Collects all DNS records for a given network."""
    network = ipaddress.ip_network(ip_network)
    all_ips = list(network.hosts())
    dns_hosts = []
    dns_entries = [_ip_to_fqdn(ip) for ip in all_ips]

    for entry, ip in zip(dns_entries, all_ips):
        if entry is None:
            continue
        dns_hosts.append({"fqdn": entry, "ipv4": str(ip), "status": HostState.DOWN})

    return dns_hosts


@admin_cache.memoize(expire=60 * 15, tag="_get_all_active_ips")
def _get_all_active_ips(ip_network: str) -> List[Dict[str, str]]:
    import nmap

    admin_logger.debug(f"Scanning network {ip_network}")
    nm = nmap.PortScanner()
    nm.scan(hosts=ip_network, arguments="-sP")
    all_hosts = nm.all_hosts()
    all_ips = [ipaddress.ip_address(h) for h in all_hosts]
    admin_logger.debug(f"Found {len(all_ips)} active IPs in {ip_network}")
    # example = {'hostnames':
    # [
    #     {'name': '<hostname>', 'type': 'PTR'}
    # ],
    # 'addresses': {'ipv4': '<ipv4>'},
    # 'vendor': {},
    # 'status': {'state': 'up', 'reason': 'syn-ack'}
    # }
    result = []
    for host in sorted(all_ips):
        host_info = nm[str(host)]
        if host_info["status"]["state"] != "up":
            continue
        admin_logger.debug(f"{host} | {host_info['status']['state']}")
        result.append(
            dict(
                fqdn=host_info["hostnames"][0]["name"],
                ipv4=host_info["addresses"]["ipv4"],
                status=host_info["status"]["state"],
            )
        )

    return result


def _cleanup_hosts(
    hosts: List[Dict[str, str]]
) -> Generator[Dict[str, str], None, None]:
    for host in hosts:
        if host["fqdn"] is None:
            continue
        if host["ipv4"].endswith(".250"):
            continue
        if host["fqdn"].endswith("."):
            host["fqdn"] = host["fqdn"][:-1]
        yield host


def _scan_network(ip_network: str) -> List[Dict[str, Any]]:
    # get all IP addresses in the network
    # check DNS entries for all IP addresses
    # ping all DNS records
    # check if anything NOT in DNS responds to ping
    dns_hosts: List[Dict[str, str]] = _get_dns_hosts(ip_network)
    all_active_ips = _get_all_active_ips(ip_network)

    active_ips_without_dns = []
    for active_ip in all_active_ips:
        matched_dns_entry = False
        for host in dns_hosts:
            if host["ipv4"] == active_ip["ipv4"]:
                host["status"] = HostState.UP.name
                matched_dns_entry = True
        if not matched_dns_entry:
            active_ips_without_dns.append(active_ip)

    for host in active_ips_without_dns:
        host["fqdn"] = "N/A"
        host["status"] = HostState.UP.name
    dns_hosts.extend(active_ips_without_dns)

    # cleanup
    dns_hosts = [host for host in _cleanup_hosts(dns_hosts)]

    return dns_hosts
