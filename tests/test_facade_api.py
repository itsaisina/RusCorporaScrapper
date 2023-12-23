"""
Tests for FacadeAPI abstraction
"""
from pathlib import Path
from selenium.webdriver.chrome.webdriver import WebDriver
from config.config_loader import load_config
from scrapper import Scrapper
from facade_api import FacadeAPI


CONFIG_PATH = Path(__file__).parent.parent / 'scrapper_config.json'
CONFIG = load_config(str(CONFIG_PATH))
API = FacadeAPI(str(CONFIG_PATH))


def test_init_completeness():
    """
    Tests weather FacadeAPI contains all attributes
    Returns:

    """
    assert set(API.__dict__.keys()) == {'config', 'driver', 'scrapper'}


def test_init_types():
    """
    Tests weather FacadeAPI attributes have correct types
    Returns:

    """
    assert isinstance(API.config, dict)
    assert isinstance(API.driver, WebDriver)
    assert isinstance(API.scrapper, Scrapper)

def test_process_word():
    """
    Tests weather process_word method returns two lists
    Returns:

    """
    res = API.process_word('азотировать')
    assert isinstance(res[0], list) and isinstance(res[1], list)

def test_close():
    """
    Tests weather close method returns anything
    and weather drive is connected after closing
    Returns:

    """
    assert API.close() is None
    assert API.driver.service.is_connectable() is False
