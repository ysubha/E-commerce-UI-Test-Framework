import allure
import pytest

from SwagLabsUIAutomation.pageObjects.login import LoginPage


# 1. Navigate to saucedemo.com
# 2. Login with standard_user
# 3. Add "Sauce Labs Bike Light" and "Sauce Labs Backpack" to cart
# 4. Go to cart, verify item is there
# 5. Proceed to checkout
# 6. Fill user details using Faker
# 7. Complete order
# 8. Verify success message
@pytest.mark.e2e
@allure.feature('E2E')
@allure.story('Full purchase flow')
def test_e2e_eflow(browser_selection, fake_checkout_user):
    browser_selection.context.clear_cookies()


    item_name_list = ["Sauce Labs Bike Light", "Sauce Labs Backpack"]

    login_obj = LoginPage(browser_selection)
    login_obj.navigation()
    login_obj.login_page_verification()
    username = 'standard_user'
    password = 'secret_sauce'
    dashboard_obj = login_obj.login_using_valid_credentials(username, password)

    dashboard_obj.reload_dashboard()
    dashboard_obj.dashboard_visibility()
    dashboard_obj.add_item_to_cart(item_name_list)
    dashboard_obj.verify_items_are_added_to_inventory(item_name_list)
    dashboard_obj.verify_cart_badge_count(len(item_name_list))
    cart_obj = dashboard_obj.go_to_cart()

    cart_obj.verify_cart_items(item_name_list)
    checkout_overview_page1_obj = cart_obj.go_to_checkout_overview_page1()
    checkout_overview_page1_obj.fill_personal_info_details(fake_checkout_user['first_name'], fake_checkout_user['last_name'], fake_checkout_user['post_code'])
    checkout_overview2_obj = checkout_overview_page1_obj.go_to_checkout_overview_page2()

    checkout_overview2_obj.complete_checkout()
    order_success_page = checkout_overview2_obj.verify_order_success_post_checkout_completion()

    login_obj1 = order_success_page.logout()

    login_obj1.login_page_verification()
    login_obj1.verify_dashboard_not_accessible_after_logout()
    login_obj1.verify_back_navigation_blocked()
