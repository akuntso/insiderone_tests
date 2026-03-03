"""Home page object model for the website."""

import time

from pages.base_page import BasePage

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


class HomePage(BasePage):


    def __init__(self, driver):
        super().__init__(driver)

    def open(self) -> None:
        """Opens the home page of the website"""
        self.logger.info(f"Opening the home page...{self.home_locator.URL}")
        self.driver.get(self.home_locator.URL)

    def go_to_careers_qa(self) -> None:
        """Navigates to the careers page for quality assurance positions"""
        self.logger.info("Going to carees page for quality assurance...")
        self.driver.get(self.home_locator.CAREERS_URL)

    def is_loaded(self) -> bool:
        """Waits until the home page is fully loaded by checking the document ready state"""
        self.wait.until(lambda d: d.execute_script("return document.readyState") == "complete")
        self.wait.until(EC.visibility_of_element_located(self.home_locator.HEADER))
        self.wait.until(EC.visibility_of_element_located(self.home_locator.FOOTER))
        self.logger.info("Checking visibility of all data sections on the home page...")
        elements = self.driver.find_elements(*self.home_locator.ALL_SECTIONS)
        body = self.driver.find_element(By.TAG_NAME, "body")
        body.send_keys(Keys.END)
        time.sleep(2)

        return all(el.is_displayed() for el in elements) if elements else False
