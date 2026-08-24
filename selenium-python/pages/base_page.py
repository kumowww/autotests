from selenium.webdriver.common.by import By
from selenium_python.pages.base_page import BasePage

def test_homepage_title(driver):
    page = BasePage(driver)
    page.open("https://example.com")
    header = page.find((By.TAG_NAME, "h1"))
    assert "Example Domain" in header.text