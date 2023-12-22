from driver_init import init_driver
import selenium


def func(x):
    return x + 1


def test_answer():
    assert init_driver() != 'something'
