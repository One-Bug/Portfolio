from seasons import minutes
import pytest


def test_season():
    assert (
        minutes("1995-01-01")
        == "Fifteen million, seven hundred eighty-three thousand, eight hundred forty minutes"
    )
    assert (
        minutes("2019-12-04")
        == "Two million, six hundred seventy-five thousand, five hundred twenty minutes"
    )
    assert (
        minutes("1970-01-01")
        == "Twenty-eight million, nine hundred thirty-two thousand, four hundred eighty minutes"
    )


def test_season2():
    with pytest.raises(SystemExit):
        minutes("01-01-1995")
    with pytest.raises(SystemExit):
        minutes("January 1, 1999")
    with pytest.raises(SystemExit):
        minutes("cat")
