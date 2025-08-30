from __future__ import annotations

def in_range(value: float, lo: float, hi: float) -> bool:
    """Simple inclusive range check."""
    return lo <= value <= hi

def _parse_float(s: str) -> float:
    """Parse str to float; raises on invalid input."""
    return float(s)

def check_voltage_str(s: str, lo: float, hi: float) -> bool:
    """Return True if s parses to a float within [lo, hi]."""
    try:
        v = _parse_float(s)
    except Exception:
        return False
    return in_range(v, lo, hi)

def check_temperature_str(s: str, lo: float, hi: float) -> bool:
    try:
        t = _parse_float(s)
    except Exception:
        return False
    return in_range(t, lo, hi)

def check_current_str(s: str, lo: float, hi: float) -> bool:
    try:
        a = _parse_float(s)
    except Exception:
        return False
    return in_range(a, lo, hi)