import pytest
from working import convert


def test_working():
    assert convert("9 AM to 5 PM") == "09:00 to 17:00"
    assert convert("11 PM to 5:30 AM") == "23:00 to 05:30"
    assert convert("12:30 AM to 12 PM") == "00:30 to 12:00"
    assert convert("1:30 AM to 1:30 PM") == "01:30 to 13:30"


def test_working2():
    with pytest.raises(ValueError):
        convert("9 AM - 5 PM")
    with pytest.raises(ValueError):
        convert("9 am - 5 PM")
    with pytest.raises(ValueError):
        convert("9 AM to 20 PM")
