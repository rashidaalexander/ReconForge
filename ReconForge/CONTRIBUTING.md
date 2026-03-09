# Contributing

Thanks for your interest in ReconForge.

## Development setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
pytest
```

## Guidelines

- Keep modules passive and safe by default.
- Add tests for new functionality.
- Document architectural changes in `docs/adr/`.
