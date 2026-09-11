"""Tests for the minimal GDC API client."""

from typing import Any

import httpx
import pytest

from pathology_explorer.ingestion.gdc_client import (
    GDC_FILES_URL,
    query_slide_images,
)


def test_query_slide_images_sends_expected_request(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    expected_response = {
        "data": {
            "hits": [
                {
                    "file_id": "example-file-id",
                    "file_name": "example.svs",
                    "data_type": "Slide Image",
                }
            ]
        }
    }
    captured_request: dict[str, Any] = {}

    def mock_post(url: str, *, json: dict[str, Any], timeout: float) -> httpx.Response:
        captured_request.update(url=url, json=json, timeout=timeout)
        request = httpx.Request("POST", url)
        return httpx.Response(200, json=expected_response, request=request)

    monkeypatch.setattr(httpx, "post", mock_post)

    result = query_slide_images("TCGA-BRCA", size=3)

    assert result == expected_response
    assert captured_request == {
        "url": GDC_FILES_URL,
        "json": {
            "filters": {
                "op": "and",
                "content": [
                    {
                        "op": "in",
                        "content": {
                            "field": "cases.project.project_id",
                            "value": ["TCGA-BRCA"],
                        },
                    },
                    {
                        "op": "in",
                        "content": {
                            "field": "files.data_type",
                            "value": ["Slide Image"],
                        },
                    },
                ],
            },
            "fields": (
                "file_id,file_name,file_size,data_type,cases.case_id,"
                "cases.submitter_id,cases.project.project_id"
            ),
            "format": "JSON",
            "size": 3,
        },
        "timeout": 30.0,
    }


def test_query_slide_images_raises_for_http_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    request = httpx.Request("POST", GDC_FILES_URL)
    response = httpx.Response(503, request=request)

    def mock_post(url: str, *, json: dict[str, Any], timeout: float) -> httpx.Response:
        return response

    monkeypatch.setattr(httpx, "post", mock_post)

    with pytest.raises(httpx.HTTPStatusError):
        query_slide_images("TCGA-LUAD")
