"""Basic sanity checks to verify that K2ephem works.

To run, simply type "py.test".
"""


def test_import():
    """Can we import k2ephem successfully?"""
    import K2ephem


def test_planets():
    """Does k2ephem return the correct campaigns for planets?"""
    from K2ephem import check_target
    # We observed Pluto only in C7
    assert(check_target("999") == [7])
    # Mars is in the field during C9 (and C17)
    assert(9 in check_target("499"))
    # Barentsen is only in the field during C4
    assert(check_target("Barentsen") == [4])
