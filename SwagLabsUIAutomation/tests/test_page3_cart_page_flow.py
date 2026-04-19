import allure
import pytest


# LESSON: 🧺 3. Cart Functionality
# Persistence
#   Verify cart items persist after page refresh
#   Verify cart items persist after navigating back and forth
@pytest.mark.integration 
@allure.feature("Cart")
@allure.story('Cart persistence on refresh')
def test_dashboard_page_refresh(dashboard_fixture):
    item_name_list = ["Sauce Labs Onesie", "Sauce Labs Bike Light"]
    dashboard_fixture.add_item_to_cart(item_name_list)
    dashboard_fixture.reload_dashboard()
    dashboard_fixture.verify_items_are_added_to_inventory(item_name_list)
    cart_pg = dashboard_fixture.go_to_cart()
    cart_pg.verify_cart_items(item_name_list)


@pytest.mark.integration 
@allure.feature("Cart")
@allure.story('Cart persistence on navigation')
def test_dashboard_to_cart_navigation_back_and_forth(dashboard_fixture):
    item_name_list = ["Sauce Labs Onesie", "Sauce Labs Bike Light", "Sauce Labs Backpack"]
    dashboard_fixture.add_item_to_cart(item_name_list)
    cart_obj = dashboard_fixture.go_to_cart()
    cart_obj.verify_cart_items(item_name_list)
    cart_obj.go_back_to_dashboard()
    dashboard_fixture.verify_items_are_added_to_inventory(item_name_list)
