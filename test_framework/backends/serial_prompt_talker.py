from __future__ import annotations
import re, time
from typing import Tuple
import serial  # requires pyserial

class SerialPromptTalker:
    """Drive an interactive prompt over a serial port.

    Rough-in: minimal robust logic to:
      - open serial, wait for prompt
      - send commands, read until prompt returns
      - parse out echoed command + trailing prompt
    Returns ("OK"|"ERROR", "body") with a naive OK heuristic.
    """

    def __init__(self, port: str, baud: int = 115200, prompt: str = r"Diags\$ ", timeout: float = 3.0):
        self._ser = serial.Serial(port, baudrate=baud, timeout=0)  # non-blocking
        self._prompt_re = re.compile(prompt.encode())
        self._timeout = timeout
        self._wait_for_prompt()

    def _read_until(self, pattern: re.Pattern, timeout: float) -> bytes:
        buf = b""
        end = time.time() + timeout
        while time.time() < end:
            chunk = self._ser.read(4096)
            if chunk:
                buf += chunk
                if pattern.search(buf):
                    return buf
            else:
                time.sleep(0.02)
        raise TimeoutError("prompt timeout")

    def _wait_for_prompt(self):
        self._read_until(self._prompt_re, self._timeout)

    def send(self, command: str) -> Tuple[str, str]:
        self._ser.write((command.strip() + "\r\n").encode())
        out = self._read_until(self._prompt_re, self._timeout)
        text = out.decode(errors="replace")
        # strip echoed command and trailing prompt lines
        lines = [ln for ln in text.splitlines() if ln.strip() and not self._prompt_re.search(ln.encode())]
        if lines and lines[0].strip() == command.strip():
            lines = lines[1:]
        body = "\n".join(lines).strip()
        status = "OK" if body and "error" not in body.lower() else "ERROR"
        return (status, body)

    def close(self):
        try:
            self._ser.close()
        except Exception:
            pass