from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage


def test_standard_user_can_open_inventory(driver):
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login("standard_user", "secret_sauce")

    title = InventoryPage(driver).wait_until_loaded()

    assert title.text == "Products"
    assert "/inventory.html" in driver.current_url
