"""Pytest configuration file that defines fixtures for WebDriver and page objects, and a hook for taking screenshots on test failure"""

import os
import pytest
import logging

from time import time
from datetime import datetime

from pytest import FixtureRequest, Parser

from selenium import webdriver

from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.chrome.webdriver import WebDriver as ChromeWebDriver
from selenium.webdriver.firefox.webdriver import WebDriver as FireFoxWebDriver

from pages.home_page import HomePage
from pages.careers_page import CareersPage


logger = logging.getLogger(__name__)

def pytest_addoption(parser: Parser):
    parser.addoption("--browser", action="store", default="chrome", help="chrome or firefox")
    parser.addoption("--headless", action="store_true", help="Run in headless mode")

# Define a fixture for the WebDriver that initializes the driver based on the command line options
@pytest.fixture(scope="function")
def driver(request: FixtureRequest):
    browser_name = request.config.getoption("browser")
    headless = request.config.getoption("headless")

    if browser_name == "chrome":
        options = ChromeOptions()
        if headless: options.add_argument("--headless=new")
        logger.info(f"Initializing Chrome WebDriver with headless={headless}")
        driver: ChromeWebDriver = webdriver.Chrome(options=options)
    elif browser_name == "firefox":
        options = FirefoxOptions()
        if headless: options.add_argument("-headless")
        logger.info(f"Initializing Firefox WebDriver with headless={headless}")
        driver: FireFoxWebDriver = webdriver.Firefox(options=options)

    driver.maximize_window()
    yield driver
    driver.quit()

# Define fixtures for the Home Page
@pytest.fixture()
def home_page(driver):
    return HomePage(driver)

# Define fixtures for the Careers Page
@pytest.fixture()
def careers_page(driver):
    return CareersPage(driver)

# for failed tests, take a screenshot and save it with the test name and timestamp
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    current_time = datetime.fromtimestamp(time()).strftime('%Y-%m-%d_%H-%M-%S')
    rep = outcome.get_result()
    if rep.when == "call" and rep.failed:
        try:
            screenshot_dir = "screenshots"
            os.makedirs(screenshot_dir, exist_ok=True)
            file_path = f"{screenshot_dir}/{item.name}_{current_time}.png"
            driver = item.funcargs['driver']
            logger.info(f"Saving screenshot for failed test: {item.name}")
            driver.save_screenshot(file_path)
            logger.info(f"[SCREENSHOT] Saved to: {file_path}")
        except Exception as e:
            logger.error(f"Fail to take screenshot: {e}")
