"""Tests for the command-line interface."""

from typer.testing import CliRunner

from pathology_explorer.cli import app

runner = CliRunner()


def test_hello() -> None:
    result = runner.invoke(app, ["hello"])

    assert result.exit_code == 0
    assert result.stdout == "TCGA Pathology Explorer is ready.\n"
