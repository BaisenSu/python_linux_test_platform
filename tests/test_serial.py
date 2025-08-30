from test_framework.serial_talker import SerialTalker

def test_mock_basic_commands():
    t = SerialTalker(mode="mock")
    assert t.ping()[0] == "OK"
    assert t.read_voltage()[0] == "OK"
    assert t.read_temperature()[0] == "OK"
    assert t.read_current()[0] == "OK"
    assert t.read_status()[0] == "OK"
    assert t.reset_device()[0] == "OK"
    t.close()
    