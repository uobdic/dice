import glob
import os
from typing import Any, Callable, Iterator, List, Tuple

import classad
import typer

from dice_cli.logger import admin_logger

app = typer.Typer(help="Commands for investigation")


def _get_condor_startd_history(path_to_condor_log: str) -> Iterator[classad.ClassAd]:
    """Get all the startd history files and return a generator of classads."""

    stard_history_search = os.path.join(path_to_condor_log, "startd_history*")
    startd_history_files = glob.glob(stard_history_search)
    startd_history_files.sort()
    for file_name in startd_history_files:
        with open(file_name) as f:
            lines = f.readlines()
        stop_at = "*** Offset"
        current_ad: List[str] = []
        for line in lines:
            if line.startswith(stop_at):
                ad = "\n".join(current_ad)
                current_ad = []
                yield classad.parseOne(ad)
                continue
            current_ad.append(line)


def filter_ads_for_event(ad: classad.ClassAd, event_time: int) -> bool:
    ten_minutes_in_epoch = 600
    return bool(
        (
            ad["JobStartDate"] < event_time
            or ad["JobStartDate"] < event_time + ten_minutes_in_epoch
        )
        and ad["CompletionDate"] > event_time
    )


def noop(x: Any) -> Any:
    return x


def get_ad_info(
    ads: Iterator[classad.ClassAd], time_fmt_func: Callable[[float], str] = noop
) -> Tuple[List[str], List[List[str]]]:
    info = []
    headers = ["Owner", "ClusterId", "JobStartDate", "CompletionDate"]
    for ad in ads:
        info.append(
            [
                ad["Owner"],
                ad["ClusterId"],
                time_fmt_func(ad["JobStartDate"]),
                time_fmt_func(ad["CompletionDate"]),
            ]
        )
    return headers, info


def print_ad_info(ads: Iterator[classad.ClassAd], output_format: str = "psql") -> None:
    """Print the start and end times of the jobs in the classads."""
    import datetime

    import tabulate

    headers, info = get_ad_info(
        ads,
        time_fmt_func=lambda x: datetime.datetime.fromtimestamp(x).strftime(
            "%Y-%m-%d %H:%M:%S"
        ),
    )
    admin_logger.info(tabulate.tabulate(info, headers=headers, tablefmt=output_format))


@app.command()
def condor_local_history(
    incident_time: int, account: str = "", path_to_condor_log: str = "/var/log/condor"
) -> None:
    """Given an incident time, account (optional), list all jobs that were running at the time of the incident."""
    ads = _get_condor_startd_history(path_to_condor_log)
    if account:
        ads = filter(lambda x: x["Owner"].startswith(account), ads)
    ads = filter(lambda x: filter_ads_for_event(x, incident_time), ads)
    print_ad_info(ads, output_format="psql")
