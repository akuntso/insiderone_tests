"""Locators for the Careers QA page"""

from selenium.webdriver.common.by import By

class CareersQALocator(object):
    SEE_ALL_JOBS = (By.LINK_TEXT, "See all QA jobs")
    JOB_LIST_LOADER = (By.ID, "jobs-list")
    LOCATION_FILTER = (By.ID, "filter-by-location")
    DEPARTMENT_FILTER = (By.ID, "filter-by-department")
    JOB_LIST = (By.CSS_SELECTOR, "#jobs-list .position-list-item")
    POSITION = (By.TAG_NAME, "p")
    DEPARTMENT = (By.TAG_NAME, "span")
    lOCATION = (By.CSS_SELECTOR, "div .position-location")
    VIEW_ROLE_BTN = (By.LINK_TEXT, "View Role")
