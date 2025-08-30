

CONTRIBUTING.md — how others can work with it

## Dev Setup:
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest -q

Branching & Commits:
Feature branches: feat/<name>; bugfix: fix/<name>
Conventional commits preferred: feat:, fix:, docs:

Tests:
Add/extend tests under tests/ (mock mode only)
Keep tests fast and hermetic (no external devices)

Coding Style:
Python 3.9+ with type hints
Small, documented functions; raise clear exceptions
Docstrings for public functions/classes

Releases:
Bump version in pyproject.toml
python -m build
(Optional) twine check dist/* and upload to internal index

