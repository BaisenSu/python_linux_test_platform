from __future__ import annotations
import argparse, os
from .shell import BotDiagsShell

def main():
    p = argparse.ArgumentParser(description="Bot diagnostics interactive shell")
    p.add_argument("--mode", default="mock", choices=["mock", "serial", "serial_prompt", "ssh_prompt"])
    p.add_argument("--uut", default=None, help="UUT ID (optional)")
    # serial args
    p.add_argument("--port", default=None)
    p.add_argument("--baud", type=int, default=115200)
    # common
    p.add_argument("--timeout", type=float, default=3.0)
    p.add_argument("--prompt", default=r"Diags\$ ")
    # ssh args
    p.add_argument("--host", default=None)
    p.add_argument("--user", default=None)
    p.add_argument("--password", default=os.environ.get("DIAG_PASS"))
    p.add_argument("--key", dest="key_filename", default=None)
    args = p.parse_args()

    talker_kwargs = dict(
        port=args.port, baud=args.baud, timeout=args.timeout,
        host=args.host, user=args.user, password=args.password,
        key_filename=args.key_filename, prompt=args.prompt
    )

    sh = BotDiagsShell(mode=args.mode, uut_id=args.uut, **talker_kwargs)
    sh.run()