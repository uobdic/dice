from pathlib import Path
from typing import Any, List, Tuple

from dice_lib.fs import FSClient
from dice_lib.user import get_user_full_name


def _resolve_usernames_in_report(report: List[Any], fs: FSClient) -> List[Any]:
    new_report = []
    for row in report:
        path = row[0]
        owner = fs.get_owner(path)
        full_name = get_user_full_name(owner)
        new_report.append(row + (owner, full_name))
    return new_report


def generate_storage_report(
    paths: List[Path], resolve_usernames: bool
) -> Tuple[List[str], List[Any]]:
    """
    Generates a storage report for a list of paths.

    :param paths: List of paths to generate a report for.
    :param resolve_usernames: Whether to resolve usernames to full names.
    :return: Tuple of (headers, report)
    """
    fs = FSClient()

    headers = ["Path", "Size [B]", "Size [human-readable]", "Unit [human-readable]"]
    report = fs.size_of_paths([str(path) for path in paths])
    if resolve_usernames:
        headers += ["Owner", "Owner full name"]
        report = _resolve_usernames_in_report(report, fs)

    return headers, report
