"""This module contains the CareersPage class, which represents the careers page of the website"""

import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

from selenium.common.exceptions import TimeoutException

from .base_page import BasePage


class CareersPage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)

    def open_qa_jobs(self) -> None:
        """Clicks on the "See all QA jobs" link and waits for the jobs list to load"""

        self.click(self.careers_qa_locator.SEE_ALL_JOBS)
        try:
            self.logger.info("Waiting for jobs list to load...")
            self.wait.until(EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, "#jobs-list .position-list-item")
            ))
        except TimeoutException:
            raise TimeoutException("Jobs list did not load in 20 seconds, too long wait time")

    def filter_jobs(self, location: str, departament: str) -> None:
        """Selects the specified location and department from the dropdown filters
        and waits for the filtering to take effect

        :param location: the location to filter by (e.g. Istanbul, Turkiye)
        :param departament: the department to filter by (e.g. Quality Assurance)

        """
        # Select location and department from dropdowns
        select_el = self.driver.find_element(*self.careers_qa_locator.LOCATION_FILTER)
        select = Select(select_el)
        self.logger.info(f'Selecting location: {location}')
        select.select_by_visible_text(location)
        select_el = self.driver.find_element(*self.careers_qa_locator.DEPARTMENT_FILTER)
        select = Select(select_el)
        self.logger.info(f'Selecting department: {departament}')
        select.select_by_visible_text(departament)
        time.sleep(5) # for filtering to take effect

    def get_job_details(self) -> list[tuple[str, str, str]]:
        """Fetches position, department and location for each job in the filtered list.

        :returns list: list of tuple with position, department and location for each job

        """
        position_details = []
        # Wait for the job list to be present after filtering
        jobs = self.driver.find_elements(*self.careers_qa_locator.JOB_LIST)
        for job in jobs:
            # Find position, department and location within each job element
            position = job.find_element(*self.careers_qa_locator.POSITION).text
            department = job.find_element(*self.careers_qa_locator.DEPARTMENT).text
            location = job.find_element(*self.careers_qa_locator.lOCATION).text
            position_details.append((position, department, location))

        return position_details

    def click_wiev_role_and_verify_redirection(self) -> bool:
        """Clicks on the "View Role" button and verifies that it redirects to the correct URL

        :returns bool: whether active the current URL after redirection

        """
        self.logger.info('Clicking "View Role" button')
        self.click(self.careers_qa_locator.VIEW_ROLE_BTN)
        self.wait.until(EC.number_of_windows_to_be(2))
        self.logger.info("Switched to new window")
        self.driver.switch_to.window(self.driver.window_handles[1])

        return self.wait.until(EC.url_contains("lever.co"))
