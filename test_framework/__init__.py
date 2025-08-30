## `test_framework/__init__.py`

"""python_linux_test_platform (package: test_framework)

Modules (high level):
- serial_talker: transport abstraction (mock, serial, ssh/serial prompt rough-in)
- mock_serial_device: simulated DUT (ping, voltage, temp, current, status, reset)
- checkers: range validation helpers
- report: test result recorder with CSV/JSON export and live log streaming
- shell: interactive CLI with set_uut/save
- test_runner: orchestrates smoke test, writes per-UUT artifacts
- shell_cli / runner_cli / demo_showcase: console entry points
- backends: serial_prompt_talker, ssh_prompt_talker (rough-in)
"""
__all__ = [
    "serial_talker",
    "mock_serial_device",
    "checkers",
    "report",
    "shell",
    "test_runner",
]
