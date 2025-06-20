from um import count


def test_um():
    assert count("hello, um, world") == 1
    assert count("um, hello, um, world") == 2
    assert count("um...") == 1
    assert count("yum") == 0
    assert (
        count(
            "Um? Mum? Is this that album where, um, umm, the clumsy alums play drums?"
        )
        == 2
    )
