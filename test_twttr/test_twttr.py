from twttr import shorten


def test_shorten():
    assert shorten("twitter") == "twttr"


def test_shorten2():
    assert shorten("twisted1") == "twstd1"


def test_shorten3():
    assert shorten("TWITTER") == "TWTTR"


def test_shorten4():
    assert shorten("TWITTER.") == "TWTTR."
