import csv
from pathlib import Path
from typing import Any, Dict, List


def read_ints_from_csv(filename: Path, fieldname: str) -> List[int]:
    """
    Reads data from CSV file and converts {fieldname} to int.
    Returned data is sorted
    """
    with open(filename) as f:
        reader = csv.DictReader(f, delimiter=",", quotechar='"')
        data = [int(row[fieldname]) for row in reader]
        data.sort()
    return data


def write_list_data_as_dict_to_csv(
    data: List[Dict[str, Any]], fieldnames: List[str], output_file: Path
) -> None:
    with open(output_file, "w") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)


def write_list_data_to_csv(
    data: List[Any], fieldnames: List[str], output_file: Path
) -> None:
    with open(output_file, "w") as f:
        writer = csv.writer(f)
        writer.writerow(fieldnames)
        writer.writerows(data)


def read_list_data_from_csv(filename: Path) -> List[Dict[str, Any]]:
    with open(filename) as f:
        reader = csv.DictReader(f, delimiter=",", quotechar='"')
        data = [row for row in reader]
    return data
