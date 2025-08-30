# Architecture: System & code structure

## Module View:
- `test_framework/serial_talker.py`  
  Transport façade; routes to:
  - mock (`MockDevice`)
  - serial (line-based)
  - serial_prompt (rough-in)
  - ssh_prompt (rough-in)
- `test_framework/backends/serial_prompt_talker.py`  
  Minimal prompt driver over serial (rough-in)
- `test_framework/backends/ssh_prompt_talker.py`  
  Minimal prompt driver over Paramiko (rough-in)
- `test_framework/mock_serial_device.py`  
  Simulates a DUT for demos/tests
- `test_framework/checkers.py`  
  Range validators
- `test_framework/report.py`  
  In-memory log + JSON/CSV + live.log
- `test_framework/shell.py`  
  Interactive CLI (commands + `set_uut`, `save`)
- `test_framework/test_runner.py`  
  Smoke sequence orchestration
- `shell_cli.py`, `runner_cli.py`, `demo_showcase.py`  
  Entry points for operators and demos

## Relationships (Mermaid):
flowchart LR
  CLI[botdiags / runner] --> ST[SerialTalker]
  ST -->|mock| MD[MockDevice]
  ST -->|serial| SER[pyserial]
  ST -->|serial_prompt| SP[SerialPromptTalker]
  ST -->|ssh_prompt| SSH[SSHPromptTalker]
  CLI --> RPT[TestReport]
  RUN[test_runner] --> ST
  RUN --> RPT

Error & Status Model:
Every command returns (status, output) where status ∈ {"OK","ERROR"}.
Runner converts numeric strings via checkers and sets ERROR for out-of-range.

Packaging:
pyproject.toml declares metadata, deps, and console scripts.
Build with python -m build → wheel in dist/.

Testing Strategy:
Unit tests in tests/ run on mock only (no hardware dependency).
Backends excluded from tests by design to keep CI deterministic.
