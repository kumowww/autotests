import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Settings: change these for your project
BASE_URL = "INSERT_YOUR_SITE_URL"          # e.g. https://example.com
EXPECTED_TITLE = "Expected page title"     # homepage title
SEARCH_QUERY = "INSERT_SEARCH_QUERY"       # text to search

def test_home_page_title(browser):
    browser.get(BASE_URL)
    actual_title = browser.title
    assert actual_title == EXPECTED_TITLE, f"Expected title '{EXPECTED_TITLE}' but got '{actual_title}'"

def test_search(browser):
    browser.get(BASE_URL)

    # Find search input and type the query
    search_input = browser.find_element(By.CSS_SELECTOR, "input[name='q']")
    search_input.send_keys(SEARCH_QUERY)

    # Find search button and click it
    search_button = browser.find_element(By.CSS_SELECTOR, "button[type='submit']")
    search_button.click()

    # Wait for the first search result to appear
    first_result = WebDriverWait(browser, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, ".search-result"))
    )
    assert first_result.is_displayed(), "Search result is not displayed"