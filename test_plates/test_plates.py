from plates import is_valid


def test_plates():
    assert is_valid("1ABC12") == False


def test_plates1():
    assert is_valid("ABC1123") == False


def test_plates2():
    assert is_valid("A11234") == False


def test_plates3():
    assert is_valid("AB0123") == False


def test_plates4():
    assert is_valid("AB12CD") == False


def test_plates5():
    assert is_valid("AB1 -2") == False


def test_plates6():
    assert is_valid("ABC123") == True
