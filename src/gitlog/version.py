import typer

app = typer.Typer()

@app.command()
def version():
    print("GitLog Version 0.1.0")