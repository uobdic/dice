import typer

from ..logger import user_logger

app = typer.Typer(help="Various benchmarks for DICE")


@app.command()
def run_hepspec06() -> None:
    """Run the hepspec06 benchmark"""
    user_logger.warning("Not implemented yet")


@app.command()
def run_third_party_copy(src: str, dst: str, repeat: int = 10) -> None:
    """Run the third party copy benchmark"""
    user_logger.warning("Not implemented yet")
    # check if cert proxy is available --> if not, create it via voms-proxy-init
    # proxy is in /tmp/x509up_u`id -u`
    # example copy command (enforce HTTPS for dst)
    # gfal-copy -p -v -f -K adler32 --checksum-mode both --copy-mode pull src https://dst
    for n in range(repeat):
        user_logger.info(f"Copy {src} to {dst} ({n+1}/{repeat})")
        # log if success or failure
    # print summary table
    # try to cleanup copied files on dst
    for n in range(repeat):
        user_logger.info(f"Cleanup {dst} ({n+1}/{repeat})")
        # ignore failures
        # gfal-rm davs://dst
