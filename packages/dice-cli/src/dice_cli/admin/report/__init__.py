from pathlib import Path
from typing import List, Optional, cast

import pandas as pd
import typer
from dice_lib.date import current_formatted_date
from tabulate import tabulate

from dice_cli._io import (
    read_list_data_from_csv,
    write_list_data_as_dict_to_csv,
    write_list_data_to_csv,
)
from dice_cli.logger import admin_logger

from ._inventory import COLUMNS as INVENTORY_COLUMNS
from ._inventory import _inventory_from_network_report
from ._storage import generate_storage_report

app = typer.Typer(help="Commands for report creation")

# U = TypeVar("U")
# def optional_to_strict(optional: Optional[U]) -> U:
#     if optional is None:
#         raise ValueError("Value is None")
#     return cast(U, optional)


@app.command()
def storage(
    paths: List[Path] = typer.Argument(...),
    output_file: Optional[Path] = typer.Option(
        None,
        "-o",
        "--output",
        help="Output file",
    ),
    resolve_usernames: bool = typer.Option(False, "--resolve-usernames"),
    print_to_console: bool = typer.Option(
        False, "--print", help="Print to console instead of output file"
    ),
    no_summary: bool = typer.Option(False, "--no-summary", help="Do not print summary"),
) -> None:
    """
    Generate a report of the storage usage of the given paths.

    :param paths: The paths to generate the report for.
    :param output_file: The file to write the report to.
    :param resolve_usernames: Whether to resolve usernames to their real names.
    """
    if not output_file and not print_to_console:
        today = current_formatted_date()
        output_file = Path(f"/tmp/{today}_dice_admin_storage_report.csv")

    headers, report = generate_storage_report(paths, resolve_usernames)
    if not print_to_console:
        write_list_data_to_csv(report, headers, cast(Path, output_file))
        admin_logger.info(f"Report saved to {output_file}")
    else:
        admin_logger.info(tabulate(report, headers=headers, tablefmt="psql"))

    if no_summary:
        # TODO: move functionality to separate function
        # Produce summary for the top 5 users
        # sort by "Size [B]" descending
        df = pd.DataFrame(report, columns=headers)
        df["Size [B]"] = df["Size [B]"].astype(int)
        df = df.sort_values(by=["Size [B]"], ascending=False)
        df["Size [human-readable]"] = df["Size [human-readable]"].astype(str)

        admin_logger.info("Summary for top 5 users:")
        admin_logger.info(
            tabulate(
                df.head(5),  # type: ignore[arg-type]
                headers=headers,
                tablefmt="psql",
                showindex=False,
            )
        )


@app.command()
def consistency_check_grid(
    grid_endpoint: str = typer.Argument(...),
    storage_endpoint: str = typer.Argument(...),
    output_file: Optional[Path] = typer.Option(
        None,
        "-o",
        "--output",
        help="Output file",
    ),
) -> None:
    """
    Generate a consistency check report for a grid endpoint and the underlying storage.

    :param grid_endpoint: The grid endpoint to generate the report for.
    :param storage_endpoint: The storage endpoint to generate the report for.
    :param output_file: The file to write the report to.
    """
    admin_logger.warning(":construction: Work in progress :construction:")


@app.command()
def network(
    ip_network: str = typer.Argument(...),
    output_file: Optional[Path] = typer.Option(
        None,
        "-o",
        "--output",
        help="Output file",
    ),
    print_to_console: bool = typer.Option(
        False, "--print", help="Print to console instead of output file"
    ),
) -> None:
    """
    Generate a report of the devices connected to the specified network.

    :param ip_network: The network to generate the report for, e.g. 10.129.5.0/24
    :param output_directory: The directory to write the report to.
    """
    if not output_file and not print_to_console:
        today = current_formatted_date()
        output_file = Path(f"/tmp/{today}_dice_admin_network_report.csv")

    admin_logger.warning(":construction: Work in progress :construction:")
    from ._network import _scan_network

    all_hosts = _scan_network(ip_network)
    hosts_without_dns = [host for host in all_hosts if host["fqdn"] == "N/A"]
    admin_logger.info(f"Found {len(all_hosts)} hosts")
    admin_logger.info(f"Found {len(hosts_without_dns)} hosts without DNS")
    for host in hosts_without_dns:
        admin_logger.warning(f"{host} is active but has no DNS")
    if output_file:
        write_list_data_as_dict_to_csv(
            all_hosts,
            ["fqdn", "ipv4", "status"],
            output_file,
        )
        admin_logger.info(f"Report saved to {output_file}")


@app.command()
def inventory(
    network_report_file: Path = typer.Argument(...),
    output_file: Optional[Path] = typer.Option(
        None,
        "-o",
        "--output",
        help="Output file",
    ),
    print_to_console: bool = typer.Option(
        False, "--print", help="Print to console instead of output file"
    ),
    remote_user: str = typer.Option("root", "--remote-user", help="Remote user"),
) -> None:
    """Generate full inventory report based on network report"""
    if not output_file and not print_to_console:
        today = current_formatted_date()
        output_file = Path(f"/tmp/{today}_dice_admin_inventory_report.csv")

    network_report = read_list_data_from_csv(network_report_file)
    active_hosts = [host for host in network_report if host["status"] == "UP"]
    inventory_report = list(_inventory_from_network_report(active_hosts, remote_user))
    if not print_to_console:
        write_list_data_as_dict_to_csv(
            inventory_report, INVENTORY_COLUMNS, cast(Path, output_file)
        )
        admin_logger.info(f"Report saved to {output_file}")


@app.command()
def dns(
    hosts: List[str] = typer.Argument(...),
    output_file: Optional[Path] = typer.Option(
        None,
        "-o",
        "--output",
        help="Output file",
    ),
    print_to_console: bool = typer.Option(
        False, "--print", help="Print to console instead of output file"
    ),
) -> None:
    """
    Generate a report of the DNS records for the given hosts.

    :param hosts: The hosts to generate the report for.
    :param output_directory: The directory to write the report to.
    """
    if not output_file and not print_to_console:
        today = current_formatted_date()
        output_file = Path(f"/tmp/{today}_dice_admin_dns_report.csv")

    admin_logger.warning(":construction: Work in progress :construction:")
    from ._dns import _dns_report

    headers, dns_report = _dns_report(hosts)
    if not print_to_console:
        write_list_data_to_csv(dns_report, headers, cast(Path, output_file))
        admin_logger.info(f"Report saved to {output_file}")
    else:
        admin_logger.info(
            tabulate(dns_report, headers=headers, tablefmt="github"),
            extra={"markup": False},
        )


@app.command()
def resources(
    host_inventory_file: Path = typer.Argument(...),
    output_file: Optional[Path] = typer.Option(
        None,
        "-o",
        "--output",
        help="Output file",
    ),
    print_to_console: bool = typer.Option(
        False, "--print", help="Print to console instead of output file"
    ),
    group: str = typer.Option(
        "htcondor_workers",
        "--group",
        help="Group of hosts to generate report for",
    ),
) -> None:
    """
    Generate a report of the resources of the given hosts.
    """
    if not output_file and not print_to_console:
        today = current_formatted_date()
        output_file = Path(f"/tmp/{today}_dice_admin_resources_report.csv")

    admin_logger.warning(":construction: Work in progress :construction:")
    from ._resources import _resources_report

    # the inventory file is a csv file with columns defined in _inventory.py
    # we are only interested in the FQDN column for "Description/Purpose"==group
    df = pd.read_csv(host_inventory_file)
    if group == "all":
        hosts = df["FQDN"].tolist()
    else:
        htcondor_workers = df[df["Description/Purpose"] == group]
    hosts = htcondor_workers["FQDN"].tolist()

    headers, resources_report = _resources_report(hosts)
    if not print_to_console:
        write_list_data_to_csv(resources_report, headers, cast(Path, output_file))
        admin_logger.info(f"Report saved to {output_file}")
    else:
        admin_logger.info(
            tabulate(resources_report, headers=headers, tablefmt="github"),
            extra={"markup": False},
        )
