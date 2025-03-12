# DICE Command Line Interface (CLI)

[![Actions Status][actions-badge]][actions-link]
[![Documentation Status][rtd-badge]][rtd-link]
[![Code style: black][black-badge]][black-link]

[![PyPI version][pypi-version]][pypi-link]
[![PyPI platforms][pypi-platforms]][pypi-link]

[actions-badge]:            https://github.com/uobdic/dice-cli/workflows/CI/badge.svg
[actions-link]:             https://github.com/uobdic/dice-cli/actions
[black-badge]:              https://img.shields.io/badge/code%20style-black-000000.svg
[black-link]:               https://github.com/psf/black
[pypi-link]:                https://pypi.org/project/dice-cli/
[pypi-platforms]:           https://img.shields.io/pypi/pyversions/dice-cli
[pypi-version]:             https://badge.fury.io/py/dice-cli.svg
[rtd-badge]:                https://readthedocs.org/projects/dice-cli/badge/?version=latest
[rtd-link]:                 https://dice-cli.readthedocs.io/en/latest/?badge=latest

## Installation

The best way to install `dice-cli` is via `pipx`.
This will setup a separate `virtualenv` for `dice-cli` preventing interference with your normal Python setup.

```bash
pipx install dice-cli
```

For tab-completion of the DICE CLI, you can run

```bash
dice --install-completion
```

which will install the completion for your shell.

Should you be using a "non-standard" shell, you can check what will be installed through

```bash
dice --show-completion
```


## Development

### Development cycle

`dice-cli` has a direct, tight dependency on [dice-lib](https://github.com/uobdic/dice-lib).
New features are usually developed within `dice-cli` first, and then common functionality is moved to `dice-lib`.

### Code layout

CLI commands are currently grouped into two categories: `admin` and `user`.
All categories, except for `user` need to be placed in their respective folders.
Each category should use its own logging and error handling to allow for individual tuning.

Main commands are implemented directly into `<category>/__init__.py`, e.g. `dice admin scan_groups_and_users`, while subcommands should be placed in `<category>/<command>/__init__.py`, e.g. `dice job why_is_my_job_not_running`.

Should a command require extensive logic, it should be placed in its own file , e.g. `admin/_print_used_id_ranges.py`. This will be the main point of change when things move to `dice-lib`.

Snapshot (2022.02.17):

```bash
src/dice_cli/
├── __init__.py
├── _io
│   ├── __init__.py
│   └── _csv.py
├── admin # `dice admin` category
│   ├── __init__.py
│   ├── _print_unused_id_ranges.py # main command functionality for `dice admin print_unused_id_ranges`
│   ├── _print_used_id_ranges.py
│   ├── _scan_groups_and_users.py
│   └── report # all `dice admin report` commands
│       ├── __init__.py
│       ├── __pycache__
│       ├── _consistency_check_grid.py
│       ├── _inventory.py
│       ├── _network.py
│       └── _storage.py
├── benchmark
│   ├── __init__.py
├── docs
│   ├── __init__.py
├── fs # user command example: `dice fs`
│   ├── __init__.py
│   └── _copy_from_local.py
├── info
│   ├── __init__.py
├── job
│   ├── __init__.py
├── logger.py
├── main.py
└── py.typed
```

### Local installation

```bash
conda create -n dice python=3.8
conda activate dice
# make sure to have the latst pip
pip install -U pip
# install dice-cli
pip install -e .
```
