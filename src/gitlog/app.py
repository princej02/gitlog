import typer

from git import Repo
from pathlib import Path

app = typer.Typer()

@app.command()
def main(
    path: Path = typer.Argument(default=".", help="Path to the git repo"),
    days: int = typer.Option(default=7, help="Controls how far back to look.")
):
    """Analyse git log for a given directory."""
    repo = Repo(path)
    typer.echo(f"Running on {path}, days: {days}")


# check if current dir has git initialised - if it doesn't git init