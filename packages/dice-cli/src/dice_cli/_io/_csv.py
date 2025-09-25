from __future__ import annotations

import csv
from pathlib import Path
from typing import Any


def read_ints_from_csv(filename: Path, fieldname: str) -> list[int]:
    """
    Reads data from CSV file and converts {fieldname} to int.
    Returned data is sorted
    """
    with Path(filename).open() as f:
        reader = csv.DictReader(f, delimiter=",", quotechar='"')
        data = [int(row[fieldname]) for row in reader]
        data.sort()
    return data


def write_list_data_as_dict_to_csv(
    data: list[dict[str, Any]], fieldnames: list[str], output_file: Path
) -> None:
    with Path(output_file).open("w") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

    
def write_list_data_to_csv(
    data: list[Any], fieldnames: list[str], output_file: Path
) -> None:
    with Path(output_file).open("w") as f:
        writer = csv.writer(f)
        writer.writerow(fieldnames)
        writer.writerows(data)


def read_list_data_from_csv(filename: Path) -> list[dict[str, Any]]:
    with Path(filename).open() as f:
        reader = csv.DictReader(f, delimiter=",", quotechar='"')
        return list(reader)
