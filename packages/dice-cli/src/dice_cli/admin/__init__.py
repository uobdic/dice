import typer

from . import (
    _print_unused_id_ranges,
    _print_used_id_ranges,
    _scan_groups_and_users,
    deploy,
    investigate,
    report,
)

app = typer.Typer(help="DICE admin commands")
app.add_typer(deploy.app, name="deploy")
app.add_typer(investigate.app, name="investigate")
app.add_typer(report.app, name="report")


@app.command()
def scan_groups_and_users() -> None:
    _scan_groups_and_users.main()


@app.command()
def print_used_id_ranges(
    user_file: str = typer.Argument(..., help="CSV file containing users"),
    group_file: str = typer.Argument(..., help="CSV file containing groups"),
) -> None:
    _print_used_id_ranges.main(user_file, group_file)


@app.command()
def print_unused_id_ranges(
    user_file: str = typer.Argument(..., help="CSV file containing users"),
    group_file: str = typer.Argument(..., help="CSV file containing groups"),
) -> None:
    _print_unused_id_ranges.main(user_file, group_file)
