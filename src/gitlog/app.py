from collections import Counter
from datetime import datetime, timedelta
from pathlib import Path

import typer
from git import BadName, Commit, InvalidGitRepositoryError, Repo
from rich import box
from rich.console import Console
from rich.table import Table


def check_path(path: Path) -> tuple[bool, str]:
    try:
        repo = Repo(path)
    except InvalidGitRepositoryError:
        return False, "No git repository in the chosen path"

    if repo.bare:
        return False, "Repository is bare"

    try:
        _ = repo.head.commit
    except (ValueError, BadName):
        return False, "Repository has no commits"

    return True, ""


def print_summary(commits: list[Commit]) -> None:
    total_commits = len(commits)

    # unique contributors (ordered)
    contributors = list(
        dict.fromkeys(
            commit.author.name
            for commit in commits
            if commit.author and commit.author.name
        )
    )

    changed_files: list[str] = []
    for commit in commits:
        changed_files.extend(str(path) for path in commit.stats.files.keys())

    unique_files = set(changed_files)

    commit_freq = Counter(
        commit.author.name for commit in commits if commit.author and commit.author.name
    )

    table = Table(title="Git Commit Summary", box=box.ROUNDED)

    table.add_column(
        f"Commits ({total_commits})", justify="right", style="cyan", no_wrap=True
    )
    table.add_column("Contributors", style="magenta")
    table.add_column("files", style="red")
    table.add_column("Frequency", style="green")

    for commit in commits:
        table.add_row(
            str(commit), str(contributors), str(unique_files), str(commit_freq.total())
        )

    console = Console()
    console.print(table)


def process_summary(path: Path, days: int) -> None:
    now = datetime.now()
    cutoff = now - timedelta(days)
    ok, message = check_path(path)

    if ok:
        repo = Repo(path)
        commits = [
            commit
            for commit in repo.iter_commits(all=True)
            if datetime.fromtimestamp(commit.committed_date) >= cutoff
        ]
        print_summary(commits)
    else:
        typer.echo(message, err=True)
        raise typer.Exit(code=1)


app = typer.Typer()


@app.command()
def main(
    path: Path = typer.Argument(default=".", help="Path to the git repo"),
    days: int = typer.Option(default=7, help="Controls how far back to look."),
) -> None:
    process_summary(path, days)
