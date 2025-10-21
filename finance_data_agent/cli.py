import typer
from finance_data_agent.loop import run_factor_loop

app = typer.Typer(help="Finance Data Agent CLI")

@app.command("run")
def run(
    path: str | None = None,
    step_n: int | None = None,
    loop_n: int | None = None,
    timeout: str | None = None,
    checkout: bool = True,
):
    """
    Run the standalone Finance Data Agent loop.
    """
    run_factor_loop(path=path, step_n=step_n, loop_n=loop_n, all_duration=timeout, checkout=checkout)

if __name__ == "__main__":
    app()