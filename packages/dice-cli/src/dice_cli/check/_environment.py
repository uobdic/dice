from enum import Enum
from typing import Dict, List

from prettytable import PrettyTable


class EnvironmentScope(str, Enum):
    hdfs = "hdfs"
    python = "python"
    cpp = "c++"
    java = "java"
    everything = "everything"


class EnvironmentStatus(str, Enum):
    ok = "OK"
    warning = "warning"
    error = "error"
    missing = "missing"


ENV_PATTERNS: Dict[EnvironmentScope, List[str]] = {
    EnvironmentScope.hdfs: ["hdfs", "hadoop", "java"],
    EnvironmentScope.python: ["python", "conda"],
    EnvironmentScope.cpp: ["gcc", "cmake"],
    EnvironmentScope.java: ["java"],
}


def get_env_for_scope(scope: EnvironmentScope) -> Dict[str, str]:
    import os

    env_vars = os.environ.copy()
    if scope == EnvironmentScope.everything:
        return env_vars

    patterns = ENV_PATTERNS[scope]
    return {
        name: value
        for name, value in env_vars.items()
        if any(pattern.lower() in name.lower() for pattern in patterns)
    }


def check_env_entry(name: str, value: str) -> EnvironmentStatus:
    # TODO: add hints if things deviate from /etc/dice/config.yaml
    if value is None or value == "":
        return EnvironmentStatus.missing
    return EnvironmentStatus.ok


def prepare_table(env_vars: Dict[str, str]) -> PrettyTable:
    headers = ["Name", "Value", "Status"]
    rows = []
    for name, value in env_vars.items():
        status = check_env_entry(name, value)
        if ":" in value and len(value) > 50:
            value = "\n".join(value.split(":"))
        rows.append([name, value, status.value])

    table = PrettyTable(headers)
    table.align["Name"] = "l"
    table.align["Value"] = "l"
    table.align["Status"] = "r"
    table.sortby = "Name"
    table.add_rows(rows)
    table.padding_width = 1

    return table
