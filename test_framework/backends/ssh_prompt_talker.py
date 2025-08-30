from __future__ import annotations
import re, time
from typing import Tuple
import paramiko  # requires paramiko

class SSHPromptTalker:
    """Drive an interactive diagnostics shell over SSH (PTY channel).

    Rough-in: opens SSH, allocates a PTY, waits for the device prompt,
    sends commands and reads until the next prompt. Returns ("OK"/"ERROR", body).
    """

    def __init__(self, host: str, user: str, password: str | None = None,
                 key_filename: str | None = None, prompt: str = r"Diags\$ ", timeout: float = 5.0):
        self._prompt_re = re.compile(prompt.encode())
        self._timeout = timeout

        self._c = paramiko.SSHClient()
        self._c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self._c.connect(hostname=host, username=user, password=password,
                        key_filename=key_filename, look_for_keys=not password, timeout=timeout)

        self._chan = self._c.invoke_shell(width=120, height=40)
        self._chan.settimeout(timeout)
        self._wait_for_prompt()

    def _read_until(self, pattern: re.Pattern, timeout: float) -> bytes:
        buf = b""
        end = time.time() + timeout
        while time.time() < end:
            if self._chan.recv_ready():
                buf += self._chan.recv(4096)
                if pattern.search(buf):
                    return buf
            else:
                time.sleep(0.02)
        raise TimeoutError("prompt timeout")

    def _wait_for_prompt(self):
        self._read_until(self._prompt_re, self._timeout)

    def send(self, command: str) -> Tuple[str, str]:
        self._chan.send((command.strip() + "\n").encode())
        out = self._read_until(self._prompt_re, self._timeout)
        text = out.decode(errors="replace")
        lines = [ln for ln in text.splitlines() if ln.strip() and not self._prompt_re.search(ln.encode())]
        if lines and lines[0].strip() == command.strip():
            lines = lines[1:]
        body = "\n".join(lines).strip()
        status = "OK" if body and "error" not in body.lower() else "ERROR"
        return (status, body)

    def close(self):
        try:
            self._chan.close()
        finally:
            self._c.close()