# tcga-pathology-explorer

A minimal command-line application scaffold for a future TCGA pathology explorer.
No TCGA or GDC functionality is implemented yet.

## Development setup

Create and activate a virtual environment, then install the project and its
development tools in editable mode:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

Run the placeholder command:

```bash
pathology-explorer hello
```

Run the checks:

```bash
pytest
ruff check .
ruff format --check .
```
