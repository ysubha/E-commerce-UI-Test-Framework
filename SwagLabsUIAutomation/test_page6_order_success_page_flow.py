import pytest


# LESSON: 🔁 5. Navigation & Menu
# Logout from application
# Verify user is redirected to login page after logout
# Verify restricted pages are not accessible after logout
@pytest.mark.no_dashboard_teardown
def test_logout_post_order_completion(order_success_page_fixture):
    login_obj = order_success_page_fixture.logout()

    login_obj.login_page_verification()
    login_obj.verify_dashboard_not_accessible_after_logout()
    login_obj.verify_back_navigation_blocked()

# LESSON: 🔁 5. Navigation & Menu
# Reset app state from menu
# Verify cart is cleared after reset
@pytest.mark.no_dashboard_teardown
def test_reset_app_state(dashboard_fixture,product_details_list_from_json):
    names_list = product_details_list_from_json[1]
    dashboard_fixture.add_item_to_cart(names_list)
    dashboard_fixture.page.locator("#react-burger-menu-btn").click()
    dashboard_fixture.page.locator("a#reset_sidebar_link").click()
    dashboard_fixture.page.locator("button#react-burger-cross-btn").click()
    dashboard_fixture.verify_cart_badge_count(0)
