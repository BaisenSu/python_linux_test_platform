# Software Requirements Specification (SRS)
for **python_linux_test_platform**

## 1. Introduction

**Purpose**  
This project provides a modular Python-based test automation platform.  
It allows a host PC to communicate with a Device Under Test (DUT) via different transports, run diagnostics, and record structured results.

**Scope**  
The platform is intended for hardware test engineers and operators. It supports:
- Mock device simulation (for development and CI)
- Serial line communication (RS232/USB)
- Prompt-based serial/SSH sessions (rough-in backends)
- Automated smoke tests and interactive CLI shell

The package can be installed with `pip`, run on Linux/WSL/Windows, and produce artifacts (JSON, CSV, live logs).

## 2. System Overview

Host PC (Python/Linux) ↔ DUT

- **Host side**: this framework (CLI tools, runners, report system).
- **DUT side**: either a simulated MockDevice or a real device responding to commands.
- **Operator**: runs `botdiags` for interactive testing or `botdiags-runner` for automated testing.

## 3. Functional Requirements

1. **Transport abstraction**
   - Support `mock`, `serial`, `serial_prompt`, `ssh_prompt` modes.
   - All commands return standardized tuple `(status, output)`.

2. **Commands supported**
   - `ping`, `read_voltage`, `read_temperature`, `read_current`, `read_status`, `reset_device`.

3. **Validation**
   - Voltage, temperature, current values validated by range checkers.

4. **Reporting**
   - Log every step with timestamp, UUT ID, session ID.
   - Export JSON and CSV.
   - Live log streaming (`live.log`).

5. **Interactive CLI (`botdiags`)**
   - Operator can send individual commands.
   - `set_uut <ID>` to set metadata.
   - `save <dir>` to export artifacts.

6. **Automated runner (`botdiags-runner`)**
   - Runs fixed sequence of diagnostics.
   - Saves reports in `./results/<UUT>/<SESSION>/`.

7. **Demo showcase (`demo-showcase`)**
   - Prints test run summary in a Rich table.

8. **Packaging**
   - Installable via `pip`.
   - Console scripts available after install.

## 4. Non-Functional Requirements

- **Environment**: Python ≥ 3.9, Linux/WSL, optional Windows.
- **Dependencies**: pyserial, paramiko, rich, pytest (dev).
- **Usability**: simple CLI commands for operators.
- **Maintainability**: modular design (`test_framework` package with submodules).
- **Extensibility**: new backends or commands can be added without breaking CLI.

## 5. System Architecture

test_framework/
├── serial_talker.py # transport abstraction
├── mock_serial_device.py # simulated DUT
├── checkers.py # validators
├── report.py # logging and export
├── shell.py # interactive CLI
├── test_runner.py # automated runner
├── backends/ # serial_prompt and ssh_prompt rough-in
└── cli entrypoints # shell_cli, runner_cli, demo_showcase

- `SerialTalker` selects backend based on mode.
- `TestReport` accumulates results, exports CSV/JSON, streams live logs.
- CLI entry points wrap these components for user-facing tools.


## 6. Interfaces

**CLI commands**  
- `botdiags` — interactive shell.  
- `botdiags-runner` — automated smoke test runner.  
- `demo-showcase` — demo run with Rich table output.  

**Artifacts**  
- JSON: full structured record of steps.  
- CSV: table form.  
- live.log: newline-delimited JSON, tail-able.  


## 7. Verification

- Unit tests with pytest under `tests/`.
- Demo run in mock mode (`demo-showcase`) always passes and produces artifacts.
- Acceptance criteria:
  - `pytest -q` all green.
  - `botdiags-runner` creates reports.
  - `botdiags` can `ping` and `save`.

## 8. Deliverables

- Source code (`test_framework/`, `tests/`).
- `pyproject.toml` (packaging metadata).
- `README.md` (usage instructions).
- `SPECIFICATION.md` (this document).
- `dist/*.whl` when built for release.