"""Command-line interface for TCGA Pathology Explorer."""

import typer

app = typer.Typer(help="Explore TCGA pathology data.")


@app.callback()
def main() -> None:
    """Explore TCGA pathology data."""


@app.command()
def hello() -> None:
    """Confirm that the CLI is installed and working."""
    typer.echo("TCGA Pathology Explorer is ready.")


if __name__ == "__main__":
    app()
