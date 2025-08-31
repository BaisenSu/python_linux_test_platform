# python_linux_test_platform

A clean, installable **Linux/Python test automation platform**:
- Modular architecture (transport abstraction, checkers, reporting)
- Interactive CLI shell (`botdiags`) + automated runner (`botdiags-runner`)
- Per-UUT artifacts: `report.json`, `report.csv`, `live.log`
- **Rough-in backends** for SSH prompt and Serial prompt shells (like a `Diags$` device)

## Quick start (dev mode)

python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest -q

Run demos:
botdiags-runner
demo-showcase
botdiags

Artifacts appear under:
./results/<UUT_ID>/<SESSION>/{report.json, report.csv, live.log}

Use different backends (rough-in):
These are rough-in implementations to show structure. They require a real device.

Serial prompt (e.g., RS-232 debug shell with a prompt like Diags$ ):
botdiags --mode serial_prompt --port /dev/ttyUSB0 --baud 115200 --prompt "Diags\\$ "

SSH prompt (device exposes interactive diagnostics shell after login):
botdiags --mode ssh_prompt --host 192.168.1.50 --user diag --password secret \
         --prompt "Diags\\$ "

Tip: Put credentials in env vars instead of CLI:
export DIAG_PASS=secret and run botdiags --mode ssh_prompt --host ... --user ...

Build a wheel (like a LabVIEW installer):
pip install build
python -m build
# dist/python_linux_test_platform-0.1.0-py3-none-any.whl

Install on a clean machine:
python -m venv testenv
source testenv/bin/activate
pip install dist/*.whl
botdiags-runner

Architecture:
serial_talker.py – unified API returning (status, output) with modes:
    mock (default): simulated DUT (safe for tests/demo)
    serial (line-based serial, expects "STATUS|payload")
    serial_prompt (rough-in): interactive prompt over serial
    ssh_prompt (rough-in): interactive prompt over SSH (Paramiko)
report.py – in-memory log + CSV/JSON export + live.log streaming
checkers.py – numeric range validators
shell.py – interactive CLI (botdiags$)
test_runner.py – runs a smoke sequence and writes artifacts

Tests:
Mock-only unit tests:
    pytest -q
They validate:
    basic talker commands (mock)
    checkers
    report export
    shell save command
    Backends are not unit-tested to avoid requiring hardware/hosts.

## Project Documentation
- [SPECIFICATION.md](SPECIFICATION.md) — Software Requirements Specification
- [ARCHITECTURE.md](ARCHITECTURE.md) — Modules & diagrams
- [CONTRIBUTING.md](CONTRIBUTING.md) — How to work on this repo
- [SECURITY.md](SECURITY.md) — Credentials & reporting

🚀 Install & Run
🪟 Windows (PowerShell)
1) Clone
    cd C:\Users\baise\Documents\Python_Projects
    git clone https://github.com/BaisenSu/python_linux_test_platform.git
    cd python_linux_test_platform

2) Create venv (one time per machine)
    python -m venv .venv

3) Activate venv (every session)
    .\.venv\Scripts\Activate

If you see “running scripts is disabled”:
    Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
    # then run activation again

4) Install deps
    pip install -U pip
    pip install -r requirements.txt
    # (devs) pip install -r requirements-dev.txt

5) Run tests (optional)
    pytest -q

6) Run the tools
    python -m test_framework.shell_cli
    python -m test_framework.runner_cli

Notes (Windows)
    Serial ports: use COM3, COM4, … (not /dev/ttyUSB0).
    SSH mode: requires paramiko (already in requirements.txt).
    .sh scripts: won’t run natively; use Python entry points or run via WSL.

🐧 WSL / Linux (Ubuntu)
1) Clone
    cd ~/projects
    git clone https://github.com/BaisenSu/python_linux_test_platform.git
    cd python_linux_test_platform

2) Create venv (one time per machine)
    python3 -m venv .venv

3) Activate venv (every session)
    source .venv/bin/activate

4) Install deps
    pip install -U pip
    pip install -r requirements.txt
    # (devs) pip install -r requirements-dev.txt

5) Run tests (optional)
    pytest -q

6) Run the tools
    python -m test_framework.shell_cli
    python -m test_framework.runner_cli

Notes (WSL/Linux)
    Serial ports: /dev/ttyUSB0, /dev/ttyS0, etc.
    Add permission once: sudo usermod -a -G dialout $USER (then log out/in).
    SSH mode: works with paramiko.
    Mock mode: use mode="mock" in SerialTalker if no hardware.

🔁 Every time you reopen the project

Windows:
    cd C:\Users\baise\Documents\Python_Projects\python_linux_test_platform
    .\.venv\Scripts\Activate

WSL/Linux:
    cd ~/projects/python_linux_test_platform
    source .venv/bin/activate

Then run:
    pytest -q                # optional
    python -m test_framework.shell_cli
    python -m test_framework.runner_cli

📦 Requirements

requirements.txt (runtime):
    rich~=13.7
    pyserial~=3.5
    paramiko~=3.4

requirements-dev.txt (developers):
    -r requirements.txt
    pytest~=8.3

🧯 Troubleshooting
    PowerShell can’t run Activate.ps1: set execution policy (see Windows step 3).
    Missing packages: run pip install -r requirements.txt.
    Serial port not found: confirm device name (Windows: COMx; Linux: /dev/ttyUSB0) and permissions.