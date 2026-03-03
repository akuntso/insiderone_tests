"""Test case for Insider's QA job application flow using pytest and Selenium WebDriver"""

import pytest

from pages.home_page import HomePage
from pages.careers_page import CareersPage

@pytest.mark.ui
def test_insider_qa_flow(home_page: HomePage, careers_page: CareersPage):
    """Test that verifies that the user can navigate to the careers page,
    filter for QA jobs in Istanbul, and view job details

    """
    # Step 1: Home Page
    home_page.open()
    assert "insiderone.com" in home_page.driver.current_url
    assert "Insider" in home_page.driver.title
    assert home_page.is_loaded(), "Home page did not load successfully"
    home_page.handle_cookies()
    # Step 2: Careers Page
    home_page.go_to_careers_qa()
    careers_page.open_qa_jobs()
    careers_page.filter_jobs(location="Istanbul, Turkiye", departament="Quality Assurance")
    position_info = careers_page.get_job_details()
    for info in position_info:
        assert 'Quality Assurance' in info[0], f"Expected 'Quality Assurance' got {info[0]}"
        assert 'Quality Assurance' in info[1], f"Expected 'Quality Assurance' got {info[1]}"
        assert 'Istanbul, Turkiye' in info[2], f"Expected 'Istanbul, Turkiye' got {info[2]}"

    assert careers_page.click_wiev_role_and_verify_redirection(), "Redirect to Lever failed"
