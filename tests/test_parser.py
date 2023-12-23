import time
import unittest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pathlib import Path
from config.config_loader import load_config
from custom_parser import Parser
from driver_init import init_driver


class TestParser(unittest.TestCase):
    def setUpClass(self):
        current_dir = Path(__file__).parent
        config_path = current_dir / "../config/scrapper_config.json"
        self.config = load_config(config_path.resolve())
        self.driver = init_driver(self.config.get("headless", True))
        self.wait = WebDriverWait(self.driver, self.config.get("timeout", 15))
        self.driver.get(
            'https://ruscorpora.ru/results?search=CtgBErQBCrEBChMKCWRpc2FtYm1vZBIGCgRtYWluChcKB2Rpc3Rtb2QSDAoK'
            'd2l0aF96ZXJvcxKAAQorCgNsZXgSJAoi0LDQutGB0LjQvtC80LDRgtC40LfQuNGA0L7QstCw0YLRjAoKCgRmb3Jt'
            'EgIKAAoLCgVncmFtbRICCgAKCQoDc2VtEgIKAAoVCgdzZW0tbW9kEgoKCHNlbXpzZW14CgkKA3N5bhICCgAKCwoF'
            'ZmxhZ3MSAgoAKhgKCAgAEAoYMiAKEAUgAEAFagQwLjk1eAAyAggBOgEBMAE='
        )
        self.parser = Parser(self.driver, self.config)

    def setUp(self):
        hit_word_elements = self.wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".hit.word")))
        self.driver.execute_script(
            "arguments[0].scrollIntoView(true);", hit_word_elements[0])
        time.sleep(2)
        self.driver.execute_script(
            "arguments[0].click();", hit_word_elements[0])

    def test_extract_context(self):
        expected_context = \
            ('Выделен и аксиоматизирован собственный дедуктивно замкнутый фрагмент логики '
             'доказательств LP С.Н.Иванова, достаточный для реализации модальной логики T. '
             '(В.Н.Иванов)')
        context = self.parser.extract_context(1)
        self.assertEqual(context, expected_context)

    def test_extract_lemma(self):
        expected_lemma = 'аксиоматизировать'
        lemma = self.parser.extract_lemma()
        self.assertEqual(lemma, expected_lemma)

    def test_extract_grammar(self):
        expected_grammar = \
            ('глагол, краткая форма, мужской, причастие, '
             'страдательный, совершенный, прошедшее, '
             'единственное, переходный')
        grammar = self.parser.extract_grammar()
        self.assertEqual(grammar, expected_grammar)

    def test_extract_syntax_features(self):
        expected_syntax_features = \
            'сочиненный элемент , главная клауза, глагольная клауза, есть зависимые'
        syntax_features = self.parser.extract_syntax_features()
        self.assertEqual(syntax_features, expected_syntax_features)

    def test_extract_lemma_wrong_xpath(self):
        original_xpath = self.parser.config["x_paths"]["lemma"]
        self.parser.config["x_paths"]["lemma"] = \
            '/html/body/div[106]/div/div/div/div[1]/div[2]/div[1]/table/tr[2]/td[2]/span[1]/i'
        lemma = self.parser.extract_lemma()
        self.assertIsNone(lemma)
        self.parser.config["x_paths"]["lemma"] = original_xpath

    def test_extract_grammar_wrong_xpath(self):
        original_xpath = self.parser.config["x_paths"]["grammar"]
        self.parser.config["x_paths"]["grammar"] = \
            '/html/body/div[106]/div/div/div/div[1]/div[2]/div[1]/table/tr[2]/td[2]/span[1]/i'
        grammar = self.parser.extract_grammar()
        self.assertIsNone(grammar)
        self.parser.config["x_paths"]["grammar"] = original_xpath

    def test_extract_syntax_features_wrong_xpath(self):
        original_xpath = self.parser.config["x_paths"]["syntax_features_option"]
        self.parser.config["x_paths"]["syntax_features_option"] = \
            ['/html/body/div[106]/div/div/div/div[1]/div[2]/div[1]/table/tr[2]/td[2]/span[1]/i']
        syntax_features = self.parser.extract_syntax_features()
        self.assertIsNone(syntax_features)
        self.parser.config["x_paths"]["syntax_features_option"] = original_xpath

    def setDown(self):
        close_button = self.driver.find_element(
            By.CSS_SELECTOR, "button.info-modal__close")
        self.driver.execute_script("arguments[0].click();", close_button)

    def test_extract_context_no_element(self):
        self.driver.get('https://ruscorpora.ru/search')
        context = self.parser.extract_context(1)
        self.assertIsNone(context)

    def test_extract_lemma_no_element(self):
        self.driver.get('https://ruscorpora.ru/search')
        lemma = self.parser.extract_lemma()
        self.assertIsNone(lemma)

    def test_extract_grammar_no_element(self):
        self.driver.get('https://ruscorpora.ru/search')
        grammar = self.parser.extract_grammar()
        self.assertIsNone(grammar)

    def test_extract_syntax_features_no_element(self):
        self.driver.get('https://ruscorpora.ru/search')
        syntax_features = self.parser.extract_syntax_features()
        self.assertIsNone(syntax_features)

    def tearDownClass(self):
        self.driver.quit()


if __name__ == '__main__':
    unittest.main()
