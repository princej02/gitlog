import typer

app = typer.Typer()


@app.command()
def version() -> None:
    print("GitLog Version 0.1.0")
