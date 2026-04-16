import json
import os
import pytest
from playwright.sync_api import Playwright
from SwagLabsUIAutomation.pageObjects.login import LoginPage


def pytest_addoption(parser):
    parser.addoption("--browser_name", action="store", default="chrome", help="Select the browser to open")


@pytest.fixture(scope='function')
def product_details_list_from_json():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_file = os.path.join(base_dir, "../data", "product_details.json")
    with open(data_file) as product_details_obj:
        test_data = json.load(product_details_obj)
        item_details_list = test_data['product_details']
        names_list = test_data['names_list']
        return item_details_list, names_list


@pytest.fixture(scope="function")
def user_details_and_errors_list_from_json():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_file = os.path.join(base_dir, "../data", "checkout_user_details.json")
    with open(data_file) as checkout_user_details_obj:
        test_data = json.load(checkout_user_details_obj)
        checkout_user_list = test_data['user_details_and_errors']
        return checkout_user_list


@pytest.fixture(scope="session")
def browser_selection(playwright: Playwright, request):
    browser_name = request.config.getoption("--browser_name")
    if browser_name == "firefox":
        browser = playwright.firefox.launch(headless=False)
    else:
        browser = playwright.chromium.launch(headless=False)

    context = browser.new_context()
    page = context.new_page()

    yield page
    page.close()
    context.close()
    browser.close()


@pytest.fixture(scope='session')
def login_credentials_from_json():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_file = os.path.join(base_dir, "../data", "login_credentials.json")
    with open(data_file) as login_credential_obj:
        test_data = json.load(login_credential_obj)
        valid_user_credentials_list = test_data['valid_user_credentials']
        invalid_user_credentials_list = test_data['invalid_user_credentials']
        return valid_user_credentials_list, invalid_user_credentials_list


@pytest.fixture(scope="function")
def login_fixture(browser_selection):
    login_obj = LoginPage(browser_selection)
    login_obj.navigation()
    login_obj.login_page_verification()
    yield login_obj


@pytest.fixture(scope="function")
def dashboard_fixture(request, login_fixture):
    dashboard_obj = login_fixture.login_using_valid_credentials("standard_user", "secret_sauce")
    yield dashboard_obj
    if not request.node.get_closest_marker("no_dashboard_teardown"):
        dashboard_obj.page.locator("#react-burger-menu-btn").click()
        dashboard_obj.page.locator("a#reset_sidebar_link").click()
        dashboard_obj.page.locator("button#react-burger-cross-btn").click()


@pytest.fixture(scope="function")
def cart_fixture(dashboard_fixture, product_details_list_from_json):
    dashboard_fixture.add_item_to_cart_if_not_added(product_details_list_from_json[1])
    cart_obj = dashboard_fixture.go_to_cart()
    yield cart_obj


@pytest.fixture(scope="function")
def checkout_overview1_fixture(cart_fixture):
    checkout_overview1_obj = cart_fixture.go_to_checkout_overview_page1()
    yield checkout_overview1_obj


@pytest.fixture(scope="function")
def checkout_overview2_fixture(checkout_overview1_fixture):
    checkout_overview1_fixture.fill_personal_info_details("User", "Name", "123456")
    checkout_overview2_obj = checkout_overview1_fixture.go_to_checkout_overview_page2()
    yield checkout_overview2_obj


@pytest.fixture(scope="function")
def order_success_page_fixture(checkout_overview2_fixture):
    checkout_overview2_fixture.complete_checkout()
    order_success_page_obj = checkout_overview2_fixture.verify_order_success_post_checkout_completion()
    yield order_success_page_obj
