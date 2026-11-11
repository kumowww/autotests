from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage


def test_adding_a_product_updates_the_cart_badge(driver):
    LoginPage(driver).open().login("standard_user", "secret_sauce")
    inventory = InventoryPage(driver).add_to_cart("sauce-labs-backpack")
    assert inventory.cart_count() == "1"
