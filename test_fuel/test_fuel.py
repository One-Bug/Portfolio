from fuel import convert, gauge
import pytest


def test_convert():
    assert convert("1/2") == 50
    assert convert("99/100") == 99
    assert convert("1/100") == 1


def test_gauge():
    assert gauge(99) == "F"
    assert gauge(50) == "50%"
    assert gauge(1) == "E"


def test_ValueError():
    with pytest.raises(ValueError):
        convert("2/1")


def test_ZeroDivisionError():
    with pytest.raises(ZeroDivisionError):
        convert("1/0")



