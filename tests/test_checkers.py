from test_framework.checkers import in_range, check_voltage_str, check_temperature_str, check_current_str

def test_in_range():
    assert in_range(5, 0, 10)
    assert not in_range(-1, 0, 10)

def test_voltage_checker():
    assert check_voltage_str("12.5", 12, 13)
    assert not check_voltage_str("11.9", 12, 13)
    assert not check_voltage_str("abc", 12, 13)

def test_temperature_checker():
    assert check_temperature_str("25.0", 20, 30)
    assert not check_temperature_str("100", 20, 30)

def test_current_checker():
    assert check_current_str("1.2", 0.5, 2.0)
    assert not check_current_str("0.1", 0.5, 2.0)