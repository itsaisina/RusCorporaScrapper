"""
Tests for scrapper_config content correctness
"""
import json
import pathlib

CONFIG_PATH = pathlib.Path(__file__).parent.parent / 'scrapper_config.json'


def test_config_completeness():
    """
    Tests weather config contains all necessary fields
    Returns:

    """
    with open(CONFIG_PATH, encoding='utf-8') as f:
        content = json.load(f)
    assert set(content.keys()) == {'timeout', 'x_paths', 'seed_url'}


def test_config_datatypes():
    """
    Tests weather config values have correct types
    Returns:

    """
    with open(CONFIG_PATH, encoding='utf-8') as f:
        content = json.load(f)
    types_mapping = {'seed_url': str, 'x_paths': dict, 'timeout': int}
    for k in content:
        assert isinstance(content[k], types_mapping[k])


def test_paths_completeness():
    """
    Tests weather config x_paths contains all necessary fields
    Returns:

    """
    with open(CONFIG_PATH, encoding='utf-8') as f:
        content = json.load(f)
    assert set(content['x_paths'].keys()) == {
        'syntax_features_option',
        'word_elements',
        'modal_close',
        'next_page_button',
        'grammar',
        'lemma',
        'search_input'}


def test_paths_datatypes():
    """
    Tests weather config x_paths values have correct types
    Returns:

    """
    with open(CONFIG_PATH, encoding='utf-8') as f:
        content = json.load(f)
    for k, v in content['x_paths'].items():
        if k == 'syntax_features_option':
            continue
        assert isinstance(v, str)
    assert isinstance(content['x_paths']['syntax_features_option'], list)


def test_time_out():
    """
    Tests weather timeout is in appropriate interval
    Returns:

    """
    with open(CONFIG_PATH, encoding='utf-8') as f:
        content = json.load(f)
    assert content['timeout'] < 60
    assert content['timeout'] > 0

