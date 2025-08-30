from __future__ import annotations
import random, time

class MockDevice:
    """Simulated DUT: deterministic shape, random-ish values.
    All commands return ("OK"|"ERROR", "payload") to match SerialTalker contract.
    """
    def __init__(self):
        self._start = time.time()

    def _uptime(self) -> float:
        return time.time() - self._start

    def handle(self, command: str):
        cmd = command.strip().lower()
        if cmd == "ping":
            return ("OK", "pong")
        if cmd == "read_voltage":
            return ("OK", f"{round(random.uniform(12.2, 12.8), 3)}")
        if cmd == "read_temperature":
            return ("OK", f"{round(random.uniform(24.0, 30.0), 2)}")
        if cmd == "read_current":
            return ("OK", f"{round(random.uniform(0.8, 1.5), 3)}")
        if cmd == "read_status":
            return ("OK", f"uptime={self._uptime():.1f}s")
        if cmd == "reset_device":
            self._start = time.time()
            return ("OK", "reset")
        return ("ERROR", f"unknown command: {command}")