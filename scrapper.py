"""
Module for web scraping using Selenium WebDriver.
"""

import time
from typing import Tuple, List, Optional, Dict, Any

from selenium.common import NoSuchElementException, TimeoutException, WebDriverException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from custom_parser import Parser


class Scrapper:
    """
    A class to handle the web scraping process using Selenium WebDriver.

    This class includes methods to navigate to a search page, input a word for searching,
    collect data from the search results, and navigate through the search result pages.
    """

    def __init__(self, driver: WebDriver, config: Dict[str, Any]):
        """
        Initializes the Scrapper with a WebDriver, configuration settings, and a Parser.

        Args:
            driver (WebDriver): The WebDriver instance to use for automation.
            config (Dict[str, Any]): A dictionary containing configuration parameters.
        """
        self.driver = driver
        self.config = config
        self.wait = WebDriverWait(driver, config["timeout"])
        self.parser = Parser(driver, config)

    def navigate_to_search(self):
        """
        Navigates to the initial search URL as defined in the configuration.
        """
        try:
            self.driver.get(self.config["seed_url"])
            time.sleep(2)  # sleep to ensure the page has loaded
        except WebDriverException as e:
            print(f"Error navigating to search page: {e}")

    def input_word(self, word: str):
        """
        Inputs a word into the search field and initiates the search.

        Args:
            word (str): The word to search for.
        """
        try:
            input_element = self.wait.until(
                EC.visibility_of_element_located((By.CLASS_NAME, "the-input__input")))
            input_element.clear()
            input_element.send_keys(word)
            search_button = self.driver.find_element(
                By.XPATH, self.config["x_paths"]["search_input"])
            search_button.click()
        except (NoSuchElementException, TimeoutException, WebDriverException) as e:
            print(f"Error in input_word: {e}")

    def collect_data(self, word: str) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
        """
        Collects data from the search results pages for the given word.

        Args:
            word (str): The word for which to collect data.

        Returns:
            Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
            Collected perfective and imperfective forms data.
        """
        perfective, imperfective = [], []
        page_number = 1
        while True:
            print(f"Processing page: {page_number}")
            try:
                hit_word_elements = self.wait.until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".hit.word")))
                for i, element in enumerate(hit_word_elements, start=1):
                    word_data = self.process_element(element, i)
                    if word_data and "глагол" in word_data['грамматика']:
                        if "несовершенный" in word_data['грамматика']:
                            imperfective.append(word_data)
                        elif "совершенный" in word_data['грамматика']:
                            perfective.append(word_data)
                if not self.go_to_next_page():
                    break
                page_number += 1
            except (NoSuchElementException, TimeoutException, WebDriverException) as e:
                print(f"Error on page {page_number} for '{word}': {e}")
                break
        return perfective, imperfective

    def process_element(self, element, position: int) -> Optional[Dict[str, Any]]:
        """
        Processes a web element to extract data like context, lemma, grammar, and syntax features.

        Args:
            element: The web element to process.
            position (int): The position of the element on the page.

        Returns:
            Optional[Dict[str, Any]]: Extracted data from the element or None if an error occurs.
        """
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        time.sleep(2)
        self.driver.execute_script("arguments[0].click();", element)
        try:
            context_text = self.parser.extract_context(position)
            lemma = self.parser.extract_lemma()
            grammar = self.parser.extract_grammar()
            syntax_features = self.parser.extract_syntax_features()

            close_button = self.driver.find_element(By.CSS_SELECTOR, "button.info-modal__close")
            self.driver.execute_script("arguments[0].click();", close_button)

            return {
                'словоформа': element.text,
                'контекст': context_text,
                'лемма': lemma,
                'грамматика': grammar,
                'синтаксические признаки': syntax_features
            }
        except (NoSuchElementException, TimeoutException, WebDriverException) as e:
            print(f"Error processing element: {e}")
            return None

    def go_to_next_page(self) -> bool:
        """
        Attempts to navigate to the next page of search results.

        Returns:
            bool: True if successfully navigated to the next page, False otherwise.
        """
        try:
            next_page_button = self.driver.find_element(
                By.CSS_SELECTOR, self.config["css_selectors"]["next_page"])
            if next_page_button.is_enabled():
                self.driver.execute_script("arguments[0].click();", next_page_button)
                time.sleep(2)
                return True
            return False
        except (NoSuchElementException, TimeoutException, WebDriverException) as e:
            print(f"Error going to next page: {e}")
            return False

    def close_driver(self):
        """
        Closes the WebDriver, effectively ending the browser session.
        """
        self.driver.quit()
