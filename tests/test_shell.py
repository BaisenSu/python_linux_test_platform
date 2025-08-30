from test_framework.shell import BotDiagsShell

def test_shell_executes_and_logs_and_save(tmp_path):
    sh = BotDiagsShell(mode="mock", uut_id="UUT-A")
    assert sh.execute_command("help")[0] == "OK"
    assert sh.execute_command("ping")[0] == "OK"
    assert sh.execute_command("read_voltage")[0] == "OK"

    s, out = sh.execute_command(f"save {tmp_path}")
    assert s == "OK"
    assert "saved JSON/CSV" in out
    assert len(sh.report.records) >= 2