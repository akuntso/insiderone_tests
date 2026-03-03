"""BasePage class that provides common methods for interacting with web pages using Selenium WebDriver"""
import logging

from selenium.webdriver.chrome.webdriver import WebDriver as ChromeWebDriver
from selenium.webdriver.firefox.webdriver import WebDriver as FirefoxWebDriver

from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement

from .home_page_locator import HomePageLocator
from .careers_qa_page_locators import CareersQALocator


class BasePage:
    def __init__(self, driver: ChromeWebDriver | FirefoxWebDriver):
        self.driver = driver
        # Set an implicit wait for the driver to handle dynamic content loading
        self.wait = WebDriverWait(driver, 30)
        # Initialize locators and logger
        self.home_locator = HomePageLocator
        # Initialize the locator for the careers QA page
        self.careers_qa_locator = CareersQALocator
        self.logger = logging.getLogger(__name__)


    def find(self, locator: tuple[str, str]) -> WebElement:
        """Finds an element using the provided locator

        :returns WebElement: the found element
        """
        try:
            self.logger.info(f'Finding element with locator: {locator}')
            return self.wait.until(EC.presence_of_element_located(locator))
        except:
            raise TimeoutException(f'Element with locator {locator} not found')

    def click(self, locator: tuple[str, str]) -> None:
        """Clicks on an element using the provided locator"""

        self.logger.info(f'Clicking element with locator: {locator}')
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    def handle_cookies(self, action: str = "accept") -> None:
        """Handles cookies dialog by accepting or declining cookies based on the provided action

        :param action: "accept" to accept cookies, "decline" to decline cookies
        """
        try:
            self.logger.info("Checking for cookies dialog...")
            self.find(self.home_locator.COOKIES_DIALOG)
            if action == "accept":
                self.logger.info("Accepting cookies...")
                self.click(self.home_locator.COOKIES_ACCEPT_BTN)
            elif action == "decline":
                self.click(self.home_locator.COOKIES_DECLINE_BTN)
        except:
            self.logger.info("Cookies dialog not found, proceeding without handling cookies")
