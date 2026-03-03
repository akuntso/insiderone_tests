"""This module contains the locators for the Home Page of the InsiderOne website"""

from selenium.webdriver.common.by import By

class HomePageLocator(object):
    URL = "https://insiderone.com/"
    CAREERS_URL = ("https://insiderone.com/careers/quality-assurance/")
    COOKIES_DIALOG =(By.XPATH, "//h5[contains(text(),'This website uses cookies')]")
    COOKIES_ACCEPT_BTN = (By.ID, "wt-cli-accept-all-btn")
    COOKIES_DECLINE_BTN = (By.ID, "wt-cli-reject-all-btn")
    HEADER = (By.TAG_NAME, "header")
    FOOTER = (By.TAG_NAME, "footer")
    ALL_SECTIONS = (By.CSS_SELECTOR, 'section[class^="homepage"]')

