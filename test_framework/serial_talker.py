from __future__ import annotations
from typing import Tuple, Optional

try:
    import serial  # type: ignore
except Exception:  # pragma: no cover
    serial = None

from .mock_serial_device import MockDevice
from .backends.serial_prompt_talker import SerialPromptTalker
from .backends.ssh_prompt_talker import SSHPromptTalker

class SerialError(Exception):
    """Transport-level error (open failures, misconfig, etc.)."""
    pass

class SerialTalker:
    """Unified transport abstraction with a stable ("OK"/"ERROR", "payload") contract.

    Modes:
      - mock           : local simulated DUT (safe for tests/demo)
      - serial         : plain line-based serial; expects "STATUS|payload" lines
      - serial_prompt  : interactive prompt over serial (rough-in)
      - ssh_prompt     : interactive prompt over SSH (rough-in)
    """

    def __init__(
        self,
        port: Optional[str] = None,
        baud: int = 9600,
        timeout: float = 1.0,
        mode: str = "mock",
        *,
        host: Optional[str] = None,
        user: Optional[str] = None,
        password: Optional[str] = None,
        key_filename: Optional[str] = None,
        prompt: str = r"Diags\$ ",
    ):
        self.mode = mode.lower()
        self.port = port
        self.baud = baud
        self.timeout = timeout
        self.prompt = prompt

        self._ser = None
        self._dev = None
        self._sp = None
        self._ssh = None

        if self.mode == "mock":
            self._dev = MockDevice()

        elif self.mode == "serial":
            if serial is None:
                raise SerialError("pyserial not available; install 'pyserial' or use mode='mock'")
            if not port:
                raise SerialError("port is required for mode='serial'")
            try:
                self._ser = serial.Serial(port, baudrate=baud, timeout=timeout)
            except Exception as exc:  # pragma: no cover
                raise SerialError(f"could not open serial port {port!r}: {exc}")

        elif self.mode == "serial_prompt":
            if not port:
                raise SerialError("port is required for mode='serial_prompt'")
            self._sp = SerialPromptTalker(port=port, baud=baud, prompt=prompt, timeout=timeout)

        elif self.mode == "ssh_prompt":
            if not (host and user):
                raise SerialError("host and user required for mode='ssh_prompt'")
            self._ssh = SSHPromptTalker(host=host, user=user, password=password,
                                        key_filename=key_filename, prompt=prompt, timeout=timeout)
        else:
            raise ValueError("mode must be one of: mock, serial, serial_prompt, ssh_prompt")

    # --- low-level send paths ---
    def _send_serial(self, command: str) -> Tuple[str, str]:
        """Line-based protocol: device returns either 'OK|payload' or 'ERROR|message'."""
        assert self._ser is not None
        cmd = (command.strip() + "\n").encode("utf-8")
        self._ser.write(cmd)
        self._ser.flush()
        line = self._ser.readline().decode("utf-8", errors="replace").strip()
        if not line:
            return ("ERROR", "timeout/no response")
        if "|" in line:
            status, output = line.split("|", 1)
            return (status, output)
        # allow devices that only print payload; assume OK if any content
        return ("OK", line)

    def _send_mock(self, command: str) -> Tuple[str, str]:
        assert self._dev is not None
        try:
            return self._dev.handle(command)
        except Exception as exc:
            return ("ERROR", str(exc))

    def _send_serial_prompt(self, command: str) -> Tuple[str, str]:
        assert self._sp is not None
        return self._sp.send(command)

    def _send_ssh_prompt(self, command: str) -> Tuple[str, str]:
        assert self._ssh is not None
        return self._ssh.send(command)

    # --- public API ---
    def send_command(self, command: str) -> Tuple[str, str]:
        """Send a high-level command string; return ("OK"/"ERROR", "payload")."""
        if not isinstance(command, str) or not command.strip():
            return ("ERROR", "invalid command")
        if self.mode == "serial":
            return self._send_serial(command)
        if self.mode == "serial_prompt":
            return self._send_serial_prompt(command)
        if self.mode == "ssh_prompt":
            return self._send_ssh_prompt(command)
        return self._send_mock(command)

    # Convenience wrappers (thin sugar)
    def ping(self): return self.send_command("ping")
    def read_voltage(self): return self.send_command("read_voltage")
    def read_temperature(self): return self.send_command("read_temperature")
    def read_current(self): return self.send_command("read_current")
    def read_status(self): return self.send_command("read_status")
    def reset_device(self): return self.send_command("reset_device")

    def close(self):
        """Close underlying transport if applicable."""
        try:
            if self._ser is not None:
                self._ser.close()
            if self._sp is not None:
                self._sp.close()
            if self._ssh is not None:
                self._ssh.close()
        except Exception:
            pass