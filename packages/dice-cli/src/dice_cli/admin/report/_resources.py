"""
The resource report should provide information on
- purchase date of the host
- storage and CPU capacity
- if the host is still in warranty (assume 5 years for all nodes)
- create a graph of the storage capacity over time
- create a graph of the CPU capacity over time
- overlay the graphs with expected data volume from the experiments
"""

import json
from typing import Any

import pandas as pd

from dice_cli.cache import admin_cache
from dice_cli.logger import admin_logger


def read_lumi_json(file_name: str) -> pd.DataFrame:
    with open(file_name) as f:
        data = json.load(f)
    # lumi json has the form of {"year": [2023, ...], "lumi": [1.2, ...]}
    # create a pandas dataframe from this
    df = pd.DataFrame(data)
    return df


def calculate_cumulative_lumi(df: pd.DataFrame) -> pd.DataFrame:
    # calculate cumulative lumi
    df["cumulative_lumi"] = df["lumi"].cumsum()
    return df


@admin_cache.memoize(expire=60 * 60, tag="resources._resources_report")
def _resources_report(hosts: list[str]) -> tuple[list[str], dict[str, Any]]:
    # 1. read N slots, RAM, storage, and purchase date via DICE API
    # 2. calculate warranty end date - assume 5 years
    # 3. calculate cumulative storage and CPU capacity
    # 4. return the cumulative storage and CPU capacity as a dict
    for host in hosts:
        admin_logger.info(f"Processing host {host}")
        # get the data from the DICE API
        # properties = ["slots", "RAM", "storage", "purchase_date"]
        # property_query = '&'.join(f"property={p}" for p in properties)
        # url = f"http://{host}:4935/host/properties/?{property_query}"
    headers = ["year", "CPU capacity", "storage capacity [TB]"]
    data = {
        "year": [2023, 2024, 2025],
        "CPU capacity": [100, 200, 300],
        "storage capacity [TB]": [10, 20, 30],
    }
    return headers, data


if __name__ == "__main__":
    df = read_lumi_json("lhc_lumi.json")
    df = calculate_cumulative_lumi(df)
    print(df)
