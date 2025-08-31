from __future__ import annotations
import os
from typing import Callable, Dict, Tuple, Optional

try:
    import readline  # history on most Unix systems
except Exception:
    readline = None

from .serial_talker import SerialTalker
from .report import Report

class BotDiagsShell:
    """Interactive diagnostic shell.
    - Executes commands through SerialTalker
    - Logs every command to TestReport
    - 'set_uut' to set UUT ID, 'save' to export artifacts
    """

    def __init__(self, *, mode: str = "mock", uut_id: Optional[str] = None, **talker_kwargs):
        self.talker = SerialTalker(mode=mode, **talker_kwargs)
        self.report = Report(uut_id=uut_id)
        self.commands: Dict[str, Callable[[str], Tuple[str, str]]] = {
            "ping": lambda _: self.talker.ping(),
            "read_voltage": lambda _: self.talker.read_voltage(),
            "read_temperature": lambda _: self.talker.read_temperature(),
            "read_current": lambda _: self.talker.read_current(),
            "read_status": lambda _: self.talker.read_status(),
            "reset_device": lambda _: self.talker.reset_device(),
            "set_uut": self._cmd_set_uut,
            "save": self._cmd_save,
            "help": self._cmd_help,
            "exit": self._cmd_exit,
            "quit": self._cmd_exit,
        }
        self._running = True
        self._hist_file = os.path.expanduser("~/.botdiags_history")
        if readline:
            try:
                readline.read_history_file(self._hist_file)
            except Exception:
                pass

    # --- builtin commands ---
    def _cmd_help(self, _: str):
        cmds = ", ".join(sorted(self.commands.keys()))
        return ("OK", f"commands: {cmds}\n  set_uut <ID>  | save <dir>")

    def _cmd_exit(self, _: str):
        self._running = False
        return ("OK", "bye")

    def _cmd_set_uut(self, args: str):
        uut = args.strip()
        if not uut:
            return ("ERROR", "usage: set_uut <UUT_ID>")
        self.report.set_meta(uut_id=uut)
        return ("OK", f"uut_id set to {uut}")

    def _cmd_save(self, args: str):
        directory = args.strip() or "./results"
        subdir = f"{directory}/{self.report.uut_id or 'UUT-UNKNOWN'}/{self.report.session_id}"
        self.report.export_artifacts(subdir)
        return ("OK", f"saved JSON/CSV to {subdir}")

    # --- main loop helpers ---
    def execute_command(self, line: str):
        parts = line.strip().split()
        if not parts:
            return ("OK", "")
        cmd, *args = parts
        handler = self.commands.get(cmd.lower())
        if not handler:
            return ("ERROR", f"unknown command: {cmd}")
        status, output = handler(" ".join(args))
        self.report.log_result(
            cmd,
            status,
            output=output if status == "OK" else None,
            error=None if status == "OK" else output,
        )
        return (status, output)

    def run(self):
        print("Bot Diagnostic Shell. Type a command (or 'help', 'exit').")
        while self._running:
            try:
                line = input("botdiags$ ").strip()
            except EOFError:
                break
            if not line:
                continue
            status, output = self.execute_command(line)
            if output:
                print(output)
        if self.report.records:
            print(f"Recorded {len(self.report.records)} steps.")
        if readline:
            try:
                readline.write_history_file(self._hist_file)
            except Exception:
                pass
        self.talker.close()