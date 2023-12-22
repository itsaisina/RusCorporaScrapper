from typing import Optional, Dict
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException


class Parser:
    """
    A class used to parse web elements on a page using Selenium.
    """

    def __init__(self, driver: WebDriver, config: Dict):
        """
        Initializes the Parser with a WebDriver and configuration.

        Args:
            driver (WebDriver): The WebDriver instance to use.
            config (Dict): A dictionary containing configuration parameters.
        """
        self.driver = driver
        self.config = config
        self.wait = WebDriverWait(driver, config["timeout"])

    def extract_context(self, position: int) -> Optional[str]:
        """
        Extracts the context text of a web element located by a specific position.

        Args:
            position (int): The position of the web element to extract context from.

        Returns:
            Optional[str]: The extracted context text or None if extraction fails.
        """
        context_xpath = (
            f"(//span[@class='hit word'])[position()={position}]"
            "/ancestor::p[contains(@class, 'seq-with-actions')]"
        )
        try:
            return self.wait.until(EC.visibility_of_element_located(
                (By.XPATH, context_xpath))).text
        except Exception as e:
            print(f"Error extracting context: {e}")
            return None

    def extract_lemma(self) -> Optional[str]:
        """
        Extracts the lemma text from the current page.

        Returns:
            Optional[str]: The extracted lemma text or None if extraction fails.
        """
        try:
            return self.wait.until(EC.visibility_of_element_located(
                (By.XPATH, self.config["x_paths"]["lemma"]))).text
        except Exception as e:
            print(f"Error extracting lemma: {e}")
            return None

    def extract_grammar(self) -> Optional[str]:
        """
        Extracts the grammar information from the current page.

        Returns:
            Optional[str]: The extracted grammar information or None if extraction fails.
        """
        try:
            return self.wait.until(EC.visibility_of_element_located(
                (By.XPATH, self.config["x_paths"]["grammar"]))).text
        except Exception as e:
            print(f"Error extracting grammar: {e}")
            return None

    def extract_syntax_features(self) -> Optional[str]:
        """
        Iteratively tries to extract syntax features using different XPaths.

        Returns:
            Optional[str]: The extracted syntax features text or None if all attempts fail.
        """
        for xpath in self.config["x_paths"]["syntax_features_option"]:
            try:
                element_present = EC.presence_of_element_located((By.XPATH, xpath))
                return self.wait.until(element_present).text
            except (NoSuchElementException, TimeoutException):
                continue
        return None
