"""Command-line interface for TCGA Pathology Explorer."""

import typer

from pathology_explorer.ingestion import gdc_client

app = typer.Typer(help="Explore TCGA pathology data.")


@app.callback()
def main() -> None:
    """Explore TCGA pathology data."""


@app.command()
def hello() -> None:
    """Confirm that the CLI is installed and working."""
    typer.echo("TCGA Pathology Explorer is ready.")


@app.command()
def slides(
    project: str = typer.Option(..., "--project", help="GDC project ID."),
    size: int = typer.Option(5, "--size", help="Maximum number of files."),
) -> None:
    """List slide-image files for a GDC project."""
    response = gdc_client.query_slide_images(project_id=project, size=size)

    for hit in response["data"]["hits"]:
        case_ids = ", ".join(case["case_id"] for case in hit.get("cases", []))
        typer.echo(f"File name: {hit['file_name']}")
        typer.echo(f"File ID: {hit['file_id']}")
        typer.echo(f"Case ID: {case_ids or 'N/A'}")
        typer.echo()


if __name__ == "__main__":
    app()
