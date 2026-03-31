from datetime import datetime, timedelta
from pathlib import Path

from rich.console import Console
from rich.table import Table

import typer
from git import Repo, Commit


def check_path(path: Path) -> bool:
    repo = Repo(path)
    check = False

    if repo is None:
        print("No current git directory in chosen path")
        return check
    elif repo.head.commit is None:
        print("No commits in range")
        return check
    else:
        check = True
        return check


def print_summary(commits: list[Commit]) -> None:

    total_commits = len(commits)
    contributors = ''.join(map(str, [str(commit.author.name) for commit in commits]))
    changed_files = []
    commit_freq = 0

    table = Table(title="Summary")

    table.add_column("Commits", justify="right", style="cyan", no_wrap=True)
    table.add_column("Contributors", style="magenta")
    table.add_column("files", style="red")
    table.add_column("Frequency", style="green")

    for commit in commits:
        table.add_row(str(commit), contributors, str(commit.committed_date), str(commit.tree.abspath))

    console = Console()
    console.print(table)

def process_summary(path: Path, days: int):
    now = datetime.now()
    cutoff = now - timedelta(days)

    if check_path(path) is True:
        repo = Repo(path)
        commits = [commit for commit in repo.iter_commits(all=True) if datetime.fromtimestamp(commit.committed_date) >= cutoff]
        print_summary(commits)
    else:
        raise typer.Exit()

app = typer.Typer()

@app.command()
def main(
    path: Path = typer.Argument(default=".", help="Path to the git repo"),
    days: int = typer.Option(default=7, help="Controls how far back to look."),
) -> None:
   process_summary(path, days)

