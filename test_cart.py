from selenium.webdriver.common.by import By


class InventoryPage:
    TITLE = (By.CSS_SELECTOR, ".title")
    CART_BADGE = (By.CSS_SELECTOR, ".shopping_cart_badge")

    def __init__(self, driver):
        self.driver = driver

    def title(self):
        return self.driver.find_element(*self.TITLE).text

    def add_to_cart(self, product_slug):
        self.driver.find_element(By.ID, f"add-to-cart-{product_slug}").click()
        return self

    def cart_count(self):
        return self.driver.find_element(*self.CART_BADGE).text
