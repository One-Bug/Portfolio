from bank import value


def test_bank():
    assert value("Hello") == 0


def test_bank1():
    assert value("Hey") == 20


def test_bank2():
    assert value("Sup") == 100
