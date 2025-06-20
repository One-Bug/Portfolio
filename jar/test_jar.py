from jar import Jar
import pytest


def test_init():
    jar = Jar()
    assert jar.capacity == 12
    with pytest.raises(ValueError):
        assert Jar(-3)


def test_str():
    jar = Jar()
    assert str(jar) == ""
    jar.deposit(1)
    assert str(jar) == "🍪"
    jar.deposit(11)
    assert str(jar) == "🍪🍪🍪🍪🍪🍪🍪🍪🍪🍪🍪🍪"


def test_deposit():
    jar = Jar()
    jar.deposit(12)
    assert jar.size == 12
    with pytest.raises(ValueError):
        assert jar.deposit(1)


def test_withdraw():
    jar = Jar()
    jar.deposit(12)
    jar.withdraw(12)
    assert jar.size == 0
    with pytest.raises(ValueError):
        assert jar.withdraw(1)
