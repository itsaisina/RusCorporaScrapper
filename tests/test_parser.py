"""
Tests for parser abstraction
"""

import time
import unittest
from pathlib import Path
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config.config_loader import load_config
from custom_parser import Parser
from driver_init import init_driver


class TestParser(unittest.TestCase):
    """
    A class to test the functionality of the Parser class.
    """

    driver = None
    config = None

    @classmethod
    def setUpClass(cls):
        """
        Set up the test environment before running tests.
        """
        current_dir = Path(__file__).parent
        config_path = current_dir / "../config/scrapper_config.json"
        cls.config = load_config(config_path.resolve())
        cls.driver = init_driver(cls.config.get("headless", True))
        cls.wait = WebDriverWait(cls.driver, cls.config.get("timeout", 10))
        cls.driver.get(
            'https://ruscorpora.ru/results?search=CtgBErQBCrEBChMKCWRpc2'
            'FtYm1vZBIGCgRtYWluChcKB2Rpc3Rtb2QSDAoKd2l0aF96ZXJvcxKAAQorC'
            'gNsZXgSJAoi0LDQutGB0LjQvtC80LDRgtC40LfQuNGA0L7QstCw0YLRjAoKC'
            'gRmb3JtEgIKAAoLCgVncmFtbRICCgAKCQoDc2VtEgIKAAoVCgdzZW0tbW9kE'
            'goKCHNlbXpzZW14CgkKA3N5bhICCgAKCwoFZmxhZ3MSAgoAKhgKCAgAEAoYM'
            'iAKEAUgAEAFagQwLjk1eAAyAggBOgEBMAE='
        )
        cls.parser = Parser(cls.driver, cls.config)

    def setUp(self):
        """
        Set up each test case.
        """
        hit_word_elements = self.wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".hit.word")))
        self.driver.execute_script(
            "arguments[0].scrollIntoView(true);", hit_word_elements[0])
        time.sleep(2)
        self.driver.execute_script(
            "arguments[0].click();", hit_word_elements[0])

    def test_extract_context(self):
        """
        Test extracting context from a web element.
        """
        expected_context = \
            ('Выделен и аксиоматизирован собственный дедуктивно замкнутый фрагмент логики '
             'доказательств LP С.Н.Иванова, достаточный для реализации модальной логики T. '
             '(В.Н.Иванов)')
        context = self.parser.extract_context(1)
        self.assertEqual(context, expected_context)

    def test_extract_lemma(self):
        """
        Test extracting lemma from the current page.
        """
        expected_lemma = 'аксиоматизировать'
        lemma = self.parser.extract_lemma()
        self.assertEqual(lemma, expected_lemma)

    def test_extract_grammar(self):
        """
        Test the extraction of grammatical information from the current page.
        """
        expected_grammar = \
            ('глагол, краткая форма, мужской, причастие, '
             'страдательный, совершенный, прошедшее, '
             'единственное, переходный')
        grammar = self.parser.extract_grammar()
        self.assertEqual(grammar, expected_grammar)

    def test_extract_syntax_features(self):
        """
        Test the extraction of syntax features from the current page.
        """
        expected_syntax_features = \
            'сочиненный элемент , главная клауза, глагольная клауза, есть зависимые'
        syntax_features = self.parser.extract_syntax_features()
        self.assertEqual(syntax_features, expected_syntax_features)

    def test_extract_lemma_wrong_xpath(self):
        """
        Test the extraction of lemma with an incorrect XPath
        to ensure it handles errors properly.
        """
        original_xpath = self.parser.config["x_paths"]["lemma"]
        self.parser.config["x_paths"]["lemma"] = \
            '/html/body/div[106]/div/div/div/div[1]/div[2]/div[1]/table/tr[2]/td[2]/span[1]/i'
        lemma = self.parser.extract_lemma()
        self.assertIsNone(lemma)
        self.parser.config["x_paths"]["lemma"] = original_xpath

    def test_extract_grammar_wrong_xpath(self):
        """
        Verify how the parser behaves when extracting grammar with an incorrect XPath.
        """
        original_xpath = self.parser.config["x_paths"]["grammar"]
        self.parser.config["x_paths"]["grammar"] = \
            '/html/body/div[106]/div/div/div/div[1]/div[2]/div[1]/table/tr[2]/td[2]/span[1]/i'
        grammar = self.parser.extract_grammar()
        self.assertIsNone(grammar)
        self.parser.config["x_paths"]["grammar"] = original_xpath

    def test_extract_syntax_features_wrong_xpath(self):
        """
        Test the extraction of syntax features with an incorrect XPath to check error handling.
        """
        original_xpath = self.parser.config["x_paths"]["syntax_features_option"]
        self.parser.config["x_paths"]["syntax_features_option"] = \
            ['/html/body/div[106]/div/div/div/div[1]/div[2]/div[1]/table/tr[2]/td[2]/span[1]/i']
        syntax_features = self.parser.extract_syntax_features()
        self.assertIsNone(syntax_features)
        self.parser.config["x_paths"]["syntax_features_option"] = original_xpath

    def set_down(self):
        """
        Clean up the web page after each test by closing any open modal or pop-up.
        """
        close_button = self.driver.find_element(
            By.CSS_SELECTOR, "button.info-modal__close")
        self.driver.execute_script("arguments[0].click();", close_button)

    def test_extract_context_no_element(self):
        """
        Test context extraction when no relevant web element is available on the page.
        """
        self.driver.get('https://ruscorpora.ru/search')
        context = self.parser.extract_context(1)
        self.driver.get(
            'https://ruscorpora.ru/results?search=CtgBErQBCrEBChMKCWRpc2'
            'FtYm1vZBIGCgRtYWluChcKB2Rpc3Rtb2QSDAoKd2l0aF96ZXJvcxKAAQorC'
            'gNsZXgSJAoi0LDQutGB0LjQvtC80LDRgtC40LfQuNGA0L7QstCw0YLRjAoKC'
            'gRmb3JtEgIKAAoLCgVncmFtbRICCgAKCQoDc2VtEgIKAAoVCgdzZW0tbW9kE'
            'goKCHNlbXpzZW14CgkKA3N5bhICCgAKCwoFZmxhZ3MSAgoAKhgKCAgAEAoYM'
            'iAKEAUgAEAFagQwLjk1eAAyAggBOgEBMAE='
        )
        self.assertIsNone(context)

    def test_extract_lemma_no_element(self):
        """
        Verify lemma extraction behavior when no relevant web element is present on the page.
        """
        self.driver.get('https://ruscorpora.ru/search')
        lemma = self.parser.extract_lemma()
        self.driver.get(
            'https://ruscorpora.ru/results?search=CtgBErQBCrEBChMKCWRpc2'
            'FtYm1vZBIGCgRtYWluChcKB2Rpc3Rtb2QSDAoKd2l0aF96ZXJvcxKAAQorC'
            'gNsZXgSJAoi0LDQutGB0LjQvtC80LDRgtC40LfQuNGA0L7QstCw0YLRjAoKC'
            'gRmb3JtEgIKAAoLCgVncmFtbRICCgAKCQoDc2VtEgIKAAoVCgdzZW0tbW9kE'
            'goKCHNlbXpzZW14CgkKA3N5bhICCgAKCwoFZmxhZ3MSAgoAKhgKCAgAEAoYM'
            'iAKEAUgAEAFagQwLjk1eAAyAggBOgEBMAE='
        )
        self.assertIsNone(lemma)

    def test_extract_grammar_no_element(self):
        """
        Test grammar extraction with no relevant web element present on the page.
        """
        self.driver.get('https://ruscorpora.ru/search')
        grammar = self.parser.extract_grammar()
        self.driver.get(
            'https://ruscorpora.ru/results?search=CtgBErQBCrEBChMKCWRpc2'
            'FtYm1vZBIGCgRtYWluChcKB2Rpc3Rtb2QSDAoKd2l0aF96ZXJvcxKAAQorC'
            'gNsZXgSJAoi0LDQutGB0LjQvtC80LDRgtC40LfQuNGA0L7QstCw0YLRjAoKC'
            'gRmb3JtEgIKAAoLCgVncmFtbRICCgAKCQoDc2VtEgIKAAoVCgdzZW0tbW9kE'
            'goKCHNlbXpzZW14CgkKA3N5bhICCgAKCwoFZmxhZ3MSAgoAKhgKCAgAEAoYM'
            'iAKEAUgAEAFagQwLjk1eAAyAggBOgEBMAE='
        )
        self.assertIsNone(grammar)

    def test_extract_syntax_features_no_element(self):
        """
        Evaluate the extraction of syntax features when no relevant element is available.
        """
        self.driver.get('https://ruscorpora.ru/search')
        syntax_features = self.parser.extract_syntax_features()
        self.driver.get(
            'https://ruscorpora.ru/results?search=CtgBErQBCrEBChMKCWRpc2'
            'FtYm1vZBIGCgRtYWluChcKB2Rpc3Rtb2QSDAoKd2l0aF96ZXJvcxKAAQorC'
            'gNsZXgSJAoi0LDQutGB0LjQvtC80LDRgtC40LfQuNGA0L7QstCw0YLRjAoKC'
            'gRmb3JtEgIKAAoLCgVncmFtbRICCgAKCQoDc2VtEgIKAAoVCgdzZW0tbW9kE'
            'goKCHNlbXpzZW14CgkKA3N5bhICCgAKCwoFZmxhZ3MSAgoAKhgKCAgAEAoYM'
            'iAKEAUgAEAFagQwLjk1eAAyAggBOgEBMAE='
        )
        self.assertIsNone(syntax_features)

    @classmethod
    def tearDownClass(cls):
        """
        Clean up after all tests are run.
        """
        cls.driver.quit()
