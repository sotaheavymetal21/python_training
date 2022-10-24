import testing_mod


def test_ok_sample():
    result = testing_mod.add_calc(1, 2)
    assert 4 == result
