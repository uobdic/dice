""" Collects information about the inventory of the system. """
from typing import Dict, Generator, List

from plumbum import SshMachine
from typer import progressbar

from dice_cli.cache import admin_cache
from dice_cli.logger import admin_logger

COLUMNS = [
    "FQDN",
    "Physical/Virtual",  # --> if virt-what returns 'kvm'
    "Server Active?",
    "CNAMES",  # alternative host names in case of multiple NICs (hostname -A)
    "Hostname",  # short hostname (hostname -s)
    "Operating System",  # cat /etc/redhat-release
    "DNS Suffix",  # domain name (hostname -d)
    "DataCentre",  # --> node_info.data_centre
    "Building",  # --> node_info.building
    "Location",  # --> node_info.location
    "Service Name",  # --> node_info.service_name
    "Owner Team",  # --> node_info.owner_team
    "Description/Purpose",  # puppet role?
    "Comments",  # --> node_info.comments
    "Platform",  # uname -m
    "Puppet Instance-Host Group",  # e.g. puppet manager
    "Is managed by Puppet?",  # --> yes
    "Linked Service TSM",  # --> node_info.linked_service_tsm
    "Owner",  # --> node_info.owner
    "Rack",  # --> node_info.rack
    "position in rack",  # --> node_info.position_in_rack
]


@admin_cache.memoize(expire=60 * 60, tag="inventory._get_host_info")
def _get_host_info(ipv4_address: str, user: str) -> Dict[str, str]:
    admin_logger.debug(f"Getting host info for {ipv4_address}")
    # TODO: find a way to do all below as a single command
    # NOTE: this is a good candidate for the DICE API service
    with SshMachine(ipv4_address, user=user, keyfile=None) as rem:
        puppet_agent = rem["puppet"]["agent"]
        facter = rem["facter"]

        hostname = rem["hostname"]("-s")
        domain = rem["hostname"]("-d")
        cnames = ",".join(set(rem["hostname"]("-A").split(" ")))
        os = rem["cat"]("/etc/redhat-release")
        virtual = rem["virt-what"]()
        platform = rem["uname"]("-m")
        puppet_managed = puppet_agent("--configprint", "server")
        puppet_group = puppet_agent("--configprint", "group")
        role = facter("node_info.role")
        service_name = facter("node_info.service_name")
        owner_team = facter("node_info.owner_team")
        owner = facter("node_info.owner")
        building = facter("node_info.building")
        data_centre = facter("node_info.data_centre")
        location = facter("node_info.location")
        rack = facter("node_info.rack")
        position_in_rack = facter("node_info.position_in_rack")
        comments = facter("node_info.comments")
        linked_service_tsm = facter("node_info.linked_service_tsm")

    return dict(
        hostname=hostname,
        domain=domain,
        cnames=cnames,
        os=os,
        virtual=virtual,
        platform=platform,
        puppet_managed=puppet_managed,
        puppet_group=puppet_group,
        role=role,
        service_name=service_name,
        owner_team=owner_team,
        owner=owner,
        rack=rack,
        position_in_rack=position_in_rack,
        data_centre=data_centre,
        building=building,
        location=location,
        comments=comments,
        linked_service_tsm=linked_service_tsm,
    )


def _inventory_from_network_report(
    network_report: List[Dict[str, str]],
    user: str,
) -> Generator[Dict[str, str], None, None]:
    with progressbar(network_report) as progress:
        # TODO: this loop should by async
        for host in progress:
            try:
                host_info = _get_host_info(host["ipv4"], user)
            except Exception as e:
                admin_logger.error(f"Could not get host info for {host['ipv4']}: {e}")
                # TODO: instead of continue, yield what we can
                # TODO: make host_info into a data class
                continue
            yield {
                "FQDN": host["fqdn"],
                "Physical/Virtual": host_info["virtual"],
                "Server Active?": host["status"] == "UP",
                "CNAMES": host_info["cnames"],
                "Hostname": host_info["hostname"],
                "Operating System": host_info["os"],
                "DNS Suffix": host_info["domain"],
                "DataCentre": host_info["data_centre"],
                "Building": host_info["building"],
                "Location": host_info["location"],
                "Service Name": host_info["service_name"],
                "Owner Team": host_info["owner_team"],
                "Description/Purpose": host_info["role"],
                "Comments": host_info["comments"],
                "Platform": host_info["platform"],
                "Puppet Instance-Host Group": host_info["puppet_managed"],
                "Is managed by Puppet?": host_info["puppet_managed"] != "",
                "Linked Service TSM": host_info["linked_service_tsm"],
                "Owner": host_info["owner"],
                "Rack": host_info["rack"],
                "position in rack": host_info["position_in_rack"],
            }
