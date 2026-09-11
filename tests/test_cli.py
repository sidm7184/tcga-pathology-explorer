"""Tests for the command-line interface."""

from typer.testing import CliRunner

from pathology_explorer import cli
from pathology_explorer.cli import app

runner = CliRunner()


def test_hello() -> None:
    result = runner.invoke(app, ["hello"])

    assert result.exit_code == 0
    assert result.stdout == "TCGA Pathology Explorer is ready.\n"


def test_slides_calls_client_and_prints_results(monkeypatch) -> None:
    calls = []

    def mock_query_slide_images(project_id: str, size: int):
        calls.append((project_id, size))
        return {
            "data": {
                "hits": [
                    {
                        "file_name": "first-slide.svs",
                        "file_id": "file-1",
                        "cases": [{"case_id": "case-1"}],
                    },
                    {
                        "file_name": "second-slide.svs",
                        "file_id": "file-2",
                        "cases": [{"case_id": "case-2"}],
                    },
                ]
            }
        }

    monkeypatch.setattr(cli.gdc_client, "query_slide_images", mock_query_slide_images)

    result = runner.invoke(app, ["slides", "--project", "TCGA-LGG", "--size", "3"])

    assert result.exit_code == 0
    assert calls == [("TCGA-LGG", 3)]
    assert result.stdout == (
        "File name: first-slide.svs\n"
        "File ID: file-1\n"
        "Case ID: case-1\n"
        "\n"
        "File name: second-slide.svs\n"
        "File ID: file-2\n"
        "Case ID: case-2\n"
        "\n"
    )


def test_slides_uses_default_size(monkeypatch) -> None:
    calls = []

    def mock_query_slide_images(project_id: str, size: int):
        calls.append((project_id, size))
        return {"data": {"hits": []}}

    monkeypatch.setattr(cli.gdc_client, "query_slide_images", mock_query_slide_images)

    result = runner.invoke(app, ["slides", "--project", "TCGA-LGG"])

    assert result.exit_code == 0
    assert calls == [("TCGA-LGG", 5)]
