import socket
from typing import List, Tuple

from dice_cli.logger import admin_logger


def _dns_report(hosts: List[str]) -> Tuple[List[str], List[Tuple[str, str, str]]]:
    result = []
    headers = [
        "fqdn",
        "ipv4",
        "ipv6",
    ]
    for host in hosts:
        fqdn = socket.getfqdn(host)
        ipv4 = socket.gethostbyname(host)
        try:
            ipv6 = socket.getaddrinfo(host, None, socket.AF_INET6)[0][4][0]
        except socket.gaierror:
            admin_logger.warning("Unabled to find IPv6 address for %s", host)
            ipv6 = "---"
        host_info = (fqdn, ipv4, ipv6)
        admin_logger.debug(f"{host} | {host_info}")
        result.append(host_info)

    return headers, result
