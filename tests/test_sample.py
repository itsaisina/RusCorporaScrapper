from driver_init import init_driver


def func(x):
    return x + 1


def test_answer():
    import selenium
    assert init_driver() != 'something'
