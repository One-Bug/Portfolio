from numb3rs import validate

def test_numb3rs():
    assert validate("192.168.0.1") == True


def test_numb3rs1():
    assert validate("275.3.6.28") == False
    assert validate("255.403.6.28") == False


def test_numb3rs2():
    assert validate("cat") == False
