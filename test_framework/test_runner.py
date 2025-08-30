from __future__ import annotations
import os
from typing import Optional
from .serial_talker import SerialTalker
from .checkers import check_voltage_str, check_temperature_str, check_current_str
from .report import TestReport

def run_smoke_tests(
    *,
    mode: str = "mock",
    uut_id: str = "UUT-001",
    out_root: str = "./results",
    **talker_kwargs,
):
    """Run a fixed sequence of tests using the given transport mode."""
    talker = SerialTalker(mode=mode, **talker_kwargs)
    report = TestReport(uut_id=uut_id)

    # Prepare run directory + live log (tail -f friendly)
    out_dir = os.path.join(out_root, uut_id, report.session_id)
    os.makedirs(out_dir, exist_ok=True)
    report.attach_live_log(os.path.join(out_dir, "live.log"))

    # 1) ping
    s, out = talker.ping()
    report.log_result("ping", s, output=out if s == "OK" else None, error=None if s == "OK" else out)

    # 2) voltage (12.0 - 13.0 V)
    s, out = talker.read_voltage()
    ok = s == "OK" and check_voltage_str(out, 12.0, 13.0)
    report.log_result("read_voltage", "OK" if ok else "ERROR", output=out if ok else None, error=None if ok else f"out-of-range: {out}")

    # 3) temperature (20 - 40 C)
    s, out = talker.read_temperature()
    ok = s == "OK" and check_temperature_str(out, 20.0, 40.0)
    report.log_result("read_temperature", "OK" if ok else "ERROR", output=out if ok else None, error=None if ok else f"out-of-range: {out}")

    # 4) current (0.5 - 2.0 A)
    s, out = talker.read_current()
    ok = s == "OK" and check_current_str(out, 0.5, 2.0)
    report.log_result("read_current", "OK" if ok else "ERROR", output=out if ok else None, error=None if ok else f"out-of-range: {out}")

    # 5) status
    s, out = talker.read_status()
    report.log_result("read_status", s, output=out if s == "OK" else None, error=None if s == "OK" else out)

    # 6) reset
    s, out = talker.reset_device()
    report.log_result("reset_device", s, output=out if s == "OK" else None, error=None if s == "OK" else out)

    talker.close()
    report.export_artifacts(out_dir)

    overall_ok = all(r["status"] == "OK" for r in report.records)
    return report, overall_ok, out_dir

if __name__ == "__main__":
    rpt, ok, out_dir = run_smoke_tests(mode="mock", uut_id="UUT-001")
    print(f"Ran {len(rpt.records)} steps. All good? {ok}")
    print(f"Artifacts saved to: {out_dir}")