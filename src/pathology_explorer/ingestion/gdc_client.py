"""Minimal client for the GDC files endpoint."""

from typing import Any

import httpx

GDC_FILES_URL = "https://api.gdc.cancer.gov/files"


def query_slide_images(project_id: str, size: int = 5) -> dict[str, Any]:
    """Return slide-image file records for a GDC project."""
    filters = {
        "op": "and",
        "content": [
            {
                "op": "in",
                "content": {
                    "field": "cases.project.project_id",
                    "value": [project_id],
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
    }
    payload = {
        "filters": filters,
        "fields": ",".join(
            [
                "file_id",
                "file_name",
                "file_size",
                "data_type",
                "cases.case_id",
                "cases.submitter_id",
                "cases.project.project_id",
            ]
        ),
        "format": "JSON",
        "size": size,
    }

    response = httpx.post(GDC_FILES_URL, json=payload, timeout=30.0)
    response.raise_for_status()
    return response.json()
