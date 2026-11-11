from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage


USERNAME = "standard_user"
PASSWORD = "secret_sauce"


def test_standard_user_can_log_in(driver):
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login(USERNAME, PASSWORD)

    inventory_title = InventoryPage(driver).wait_until_loaded()

    assert inventory_title.text == "Products"
    assert "/inventory.html" in driver.current_url


def test_invalid_user_sees_login_error(driver):
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login("invalid_user", "invalid_password")

    assert "Username and password do not match" in login_page.wait_for_error().text
