from driver_init import init_driver
from selenium import webdriver


def test_driver_init():
    assert isinstance(init_driver(), webdriver.Chrome)
