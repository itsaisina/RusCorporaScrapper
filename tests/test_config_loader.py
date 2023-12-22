"""
Tests for load_config function
"""
import json
import pathlib
from config.config_loader import load_config

TEST_CONFIG_CONTENT = {"seed_url": "url", "x_paths": ({
                                                          "search_input": "input",
                                                          "word_elements": "element",
                                                          "lemma": "lemma path",
                                                          "grammar": "grammar path",
                                                          "syntax_features_option":
                                                              [
                                                                  "opt 1",
                                                                  "opt 2"
                                                              ],
                                                          "modal_close": "close",
                                                          "next_page_button": "button"
                                                      },), 'timeout': 15}

FILE_PATH = pathlib.Path('test.json')


def test_config_loader():
    """
    Tests weather load_config correctly loads json file
    Returns:

    """
    with open(FILE_PATH, 'w') as f:
        json.dump(TEST_CONFIG_CONTENT, f)
    assert load_config(str(FILE_PATH)) == TEST_CONFIG_CONTENT
    pathlib.Path.unlink(FILE_PATH)