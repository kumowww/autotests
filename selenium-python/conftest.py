import os
import shutil

import pytest
from selenium import webdriver


@pytest.fixture(scope="session")
def driver():
    options = webdriver.ChromeOptions()
    if os.getenv("HEADLESS", "true").lower() in ("true", "1", "yes"):
        options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    chrome_binary = os.getenv("CHROME_BIN") or shutil.which("chromium")
    if chrome_binary:
        options.binary_location = chrome_binary
    browser = webdriver.Chrome(options=options)
    yield browser
    browser.quit()
