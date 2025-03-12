import typer

from ..logger import user_logger

app = typer.Typer(help="DICE job commands")


@app.command()
def why_is_my_job_not_running(job_id: str = typer.Argument(..., help="Job ID")) -> None:
    """
    Logs the reason why a job is not running
    """
    user_logger.info(f"Job {job_id} is not running")
    user_logger.warning("Not implemented yet")
