from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class InventoryPage:
    TITLE = (By.CSS_SELECTOR, ".title")

    def __init__(self, driver):
        self.driver = driver

    def wait_until_loaded(self):
        return WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.TITLE)
        )
