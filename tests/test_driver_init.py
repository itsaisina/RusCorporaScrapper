"""
Tests for driver_init function
"""
from selenium import webdriver
from driver_init import init_driver


def test_driver_init():
    """
    Tests weather driver_init returns Chrome driver
    Returns:

    """
    assert isinstance(init_driver(), webdriver.Chrome)
