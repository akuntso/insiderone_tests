# N11 Load Testing with Locust and UI Tests with Pytest and Selenium

This project contains load tests for the N11 website, built using the Locust framework. It also includes UI tests implemented with Pytest and Selenium. The load tests simulate user behavior such as searching for products, applying filters, and navigating through paginated results. The UI tests verify the functionality of specific web pages using page object model.

## Project Structure

*   `load_tests.py`: Contains the Locust load test definitions, including tasks for simulating user interactions with the N11 website.
*   `conftest.py`: Pytest configuration file that defines fixtures for WebDriver, page objects, and a hook for taking screenshots on test failure.
*   `pages/`: Contains page object definitions (e.g., `home_page.py`, `careers_page.py`) used in the UI tests.
*   `screenshots/`: (Automatically Generated) This directory will contain screenshots of failed UI tests.

## Requirements

*   Python 3.6+
*   Locust
*   Selenium
*   Pytest
*   Chrome or Firefox browser

Install the necessary dependencies using pip:

```bash
cd insidreone

python -m venv venv

source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

pip install -r requirements.txt

```

You'll also need to have a compatible WebDriver (chromedriver or geckodriver) installed and available in your system's PATH.  Make sure the WebDriver version matches your browser version.

## Running the Load Tests

To run the load tests, use the following Locust command:

```bash
locust -f load_tests.py -H https://www.n11.com
```

*   `-f load_tests.py`: Specifies the Locustfile to use.
*   `-H https://www.n11.com`: Specifies the host URL to test against the n11 website.

You can also specify the number of users and the hatch rate:

```bash
locust -f load_tests.py -H https://www.n11.com --users 1 --hatch-rate 10
```

*   `--users`: The total number of users to simulate.
*   `--hatch-rate`: The rate at which users are spawned.

Open your browser and navigate to `http://localhost:8089` to access the Locust web interface. From there, you can start and stop the load tests and view real-time statistics.

## Running UI Tests

The project includes UI tests configured with Pytest and Selenium. These tests use page objects defined in the `pages/` directory to interact with the N11 website. Tests are marked like api and ui.

To run the UI tests, use the following command:

```bash
pytest tests/ --browser chrome

pytest tests/ --browser firefox --headless -m ui

pytest tests/ --browser chrome --headless -m api
```

*   `--browser`: Specifies the browser to use (chrome or firefox).
*   `--headless`: Runs the browser in headless mode (no GUI).  Remove this option to see the browser during test execution.
*   `--markers`: Specifies which tests run by marker

### Writing UI Tests

1.  **Create a test file** in the `tests/` directory (e.g., `tests/test_home_page.py`).
2.  **Import the necessary fixtures** (e.g., `home_page`).
3.  **Write your test functions** using the page objects to interact with the website.

Example:

```python
def test_home_page_title(home_page):
    home_page.go_to_home_page()
    assert "n11.com" in home_page.get_title()
```

## Test Details

### Load Tests (Locust)

The `load_tests.py` file defines the `N11SearchUser` class, which represents a simulated user. The class includes several tasks that mimic user behavior on the N11 website:

*   `perform_search`: Searches for a random product from a list of predefined search queries.
*   `perform_search_by_popular`: Searches for a popular product ("valiz").
*   `perform_partly_search`: Searches for a product by a partial name ("iph").
*   `infinite_scroll_pagination`: Simulates infinite scrolling by requesting subsequent pages of search results.
*   `apply_filters`: Applies filters for Brand, Model, and Capacity.
*   `apply_filters_by_prise`: Applies filters for Brand, Model, and Capacity, and price range.
*   `apply_filters_by_prise_from`: Applies filters including a minimum price.
*   `apply_filters_by_prise_to`: Applies filters including a maximum price.

### UI Tests (Pytest and Selenium)

The `conftest.py` file configures the Pytest environment and provides fixtures for WebDriver and page objects. Key features include:

*   WebDriver initialization: Sets up Chrome or Firefox with headless options.
*   Page object fixtures: Provides `home_page` and `careers_page` fixtures for easy access to page objects in tests.
*   Screenshot on failure: Automatically captures screenshots for failed tests and saves them in the `screenshots/` directory.

## Notes

*   Ensure that the N11 website is accessible from your test environment.
*   Adjust the number of users and hatch rate for load tests based on your system's resources and testing goals.
*   Consider adding more sophisticated user behavior to the load tests to simulate real-world scenarios more accurately, such as adding items to cart and proceeding to checkout.
*   The UI tests require the website to be in a specific state. Make sure the test environment is properly configured before running the UI tests. You may need to adjust the tests based on changes to the N11 website.
*   Review the logging output in the console for additional information.
