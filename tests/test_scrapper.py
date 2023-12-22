from ..scrapper import Scrapper
from ..driver_init import init_driver
from config.config_loader import load_config
from pathlib import Path
import time

CONFIG_PATH = Path(__file__).parent.parent / 'scrapper_config.json'
DRIVER = init_driver()
CONFIG = load_config(CONFIG_PATH)
SCRAPPER = Scrapper(DRIVER, CONFIG)


def test_navigate_to_search_timeout():
    start_time = time.time()
    SCRAPPER.navigate_to_search()
    end_time = time.time()
    assert end_time - start_time > 2


def test_navigate_to_search_return_type():
    res = SCRAPPER.navigate_to_search()
    assert res is None


def test_input_word_type():
    res = SCRAPPER.input_word('word')
    assert res is None


def test_collect_data_type():
    res = SCRAPPER.collect_data('word')
    assert isinstance(res[0], list)
    assert isinstance(res[1], list)


def test_go_to_next_page():
    start_time = time.time()
    res = SCRAPPER.go_to_next_page()
    end_time = time.time()
    time_diff = end_time - start_time
    assert (time_diff > 2 and res is True
            or time_diff < 2 and res is False)


def test_close_driver():
    res = SCRAPPER.close_driver()
    assert res is None
    assert SCRAPPER.driver.service.is_connectable() is False


