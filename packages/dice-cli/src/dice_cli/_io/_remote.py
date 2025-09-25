"""
from https://stackoverflow.com/questions/54813894/how-to-download-a-file-with-python-using-tqdm
"""
from __future__ import annotations

import math
from pathlib import Path

import requests
from tqdm import tqdm


def download(url: str, destination: str) -> None:
    r = requests.get(url, stream=True)
    total_size = int(r.headers.get("content-length", 0))
    block_size = 1024
    wrote = 0

    with Path(destination).open("wb") as f:
        progress = tqdm(
            r.iter_content(block_size),
            total=math.ceil(total_size / block_size),
            unit="KB",
            unit_scale=True,
        )
        for data in progress:
            wrote = wrote + len(data)
            f.write(data)
