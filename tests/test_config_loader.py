import json
import pathlib

from config_loader import load_config

CONFIG_CONTENT = {
    "seed_url": "https://ruscorpora.ru/search",
    "x_paths":
    {
        "search_input": "//*[@id='lexgramm-search-panel']/div[4]/div/div/button[1]",
        "word_elements": ".hit.word",
        "lemma": "/html/body/div[6]/div/div/div/div[1]/div[2]/div[1]/table/tr[2]/td[2]/span[1]/i",
        "grammar": "/html/body/div[6]/div/div/div/div[1]/div[2]/div[1]/table/tr[3]/td[2]/span/i",
        "syntax_features_option":
        [
            "/html/body/div[6]/div/div/div/div[1]/div[2]/div[4]/table/tr[1]/td[2]/span",
            "/html/body/div[6]/div/div/div/div[1]/div[2]/div[3]/table/tr[1]/td[2]/span/i",
            "/html/body/div[6]/div/div/div/div[1]/div[2]/div[2]/table/tr[1]/td[2]/span/i"
        ],
        "modal_close": "/html/body/div[6]/div/div/div/div[1]/div[1]/button",
        "next_page_button": ".ant-pagination-next:not(.ant-pagination-disabled)"
    },
    "timeout": 15
}

FILE_PATH = pathlib.Path('test.json')

def test_config_loader():
    with open(FILE_PATH, 'w') as f:
        json.dump(CONFIG_CONTENT, f)
    assert load_config(str(FILE_PATH)) == CONFIG_CONTENT
    pathlib.Path.unlink(FILE_PATH)

def test_config_correctness():
    config_path = pathlib.Path(__file__).parent.parent / 'scrapper_config.json'
    with open(config_path) as f:
        content = json.load(f)
    assert content['timeout'] < 60
    assert content['timeout'] > 0