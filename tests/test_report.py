import json, csv
from test_framework.report import TestReport

def test_report_records_and_exports(tmp_path):
    r = TestReport(uut_id="UUT-XYZ", session_id="S1")
    r.log_result("ping", "OK", output="pong")
    r.log_result("read_voltage", "ERROR", error="timeout")

    out_dir = tmp_path / "artifacts"
    r.export_artifacts(str(out_dir), basename="run")

    data = json.loads((out_dir / "run.json").read_text())
    assert len(data) == 2 and data[0]["uut_id"] == "UUT-XYZ"

    rows = list(csv.DictReader(open(out_dir / "run.csv")))
    assert len(rows) == 2
    