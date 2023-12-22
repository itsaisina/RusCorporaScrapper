"""
Tests for scrapper abstraction
"""

import time
from pathlib import Path

from scrapper import Scrapper
from driver_init import init_driver
from config.config_loader import load_config


CONFIG_PATH = Path(__file__).parent.parent / 'scrapper_config.json'
DRIVER = init_driver()
CONFIG = load_config(str(CONFIG_PATH))
SCRAPPER = Scrapper(DRIVER, CONFIG)


def test_navigate_to_search_timeout():
    """
    Tests weather navigate_to_search method sleeps
    for 2 seconds
    Returns:

    """
    start_time = time.time()
    SCRAPPER.navigate_to_search()
    end_time = time.time()
    assert end_time - start_time > 2


def test_navigate_to_search_return_type():
    """
    Tests weather navigate_to_search return anything
    Returns:

    """
    assert SCRAPPER.navigate_to_search() is None


def test_input_word_type():
    """
    Tests weather input_word_type return anything
    Returns:

    """
    assert SCRAPPER.input_word('азотировать') is None


def test_collect_data_type():
    """
    Tests weather collect_data return two lists
    Returns:

    """
    res = SCRAPPER.collect_data('азотировать')
    assert isinstance(res[0], list)
    assert isinstance(res[1], list)


def test_go_to_next_page():
    """
    Tests weather go_to_next_page method sleeps for 2 seconds
    and processes a page
    or returns False
    Returns:

    """
    start_time = time.time()
    res = SCRAPPER.go_to_next_page()
    end_time = time.time()
    time_diff = end_time - start_time
    assert (time_diff > 2 and res is True
            or time_diff < 2 and res is False)


def test_close_driver():
    """
    Tests weather close_driver return anything
    and weather drive is connectable after closing
    Returns:

    """
    assert SCRAPPER.close_driver() is None
    assert SCRAPPER.driver.service.is_connectable() is False
