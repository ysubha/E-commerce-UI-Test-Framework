import allure
import pytest

# LESSON: 🔒 6. Security & Access Control
# Access inventory page without login
# Access cart page without login
# Verify user is redirected to login page for unauthorized access
url_error_code_list = [("https://www.saucedemo.com/inventory.html",
                        "Epic sadface: You can only access '/inventory.html' when you are logged in."),
                       ("https://www.saucedemo.com/cart.html",
                        "Epic sadface: You can only access '/cart.html' when you are logged in."),
                       ("https://www.saucedemo.com/checkout-step-one.html",
                        "Epic sadface: You can only access '/checkout-step-one.html' when you are logged in."),
                       ("https://www.saucedemo.com/checkout-step-two.html",
                        "Epic sadface: You can only access '/checkout-step-two.html' when you are logged in."),
                       ("https://www.sauced"
                        "emo.com/checkout-complete.html",
                        "Epic sadface: You can only access '/checkout-complete.html' when you are logged in.")]

@pytest.mark.integration
@allure.feature('Security')
@allure.story('Unauthorized access to protected pages')
@pytest.mark.parametrize(('web_pg_url', 'error_code'), url_error_code_list)
def test_no_access_to_app_pages_without_login(login_fixture, web_pg_url, error_code):
    login_fixture.verify_app_pages_not_accessible_without_login(web_pg_url, error_code)
    login_fixture.verify_back_navigation_blocked()
