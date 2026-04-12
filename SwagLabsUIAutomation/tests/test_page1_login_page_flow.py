import json
import os
import time
import pytest
from playwright.sync_api import expect

from SwagLabsUIAutomation.pageObjects.login import LoginPage

# def test_ete_ui_flow_process(login):
#     dashboard_obj = login.login_using_valid_credentials("standard_user", "secret_sauce")
#     item_name_list = ["Sauce Labs Onesie", "Sauce Labs Bike Light", "Sauce Labs Backpack"]
#     dashboard_obj.add_item_to_cart(item_name_list)
#     cart_obj = dashboard_obj.go_to_cart()
#     cart_obj.verify_cart_items()

# LESSON: 🔐 1. LOGIN MODULE (HIGH PRIORITY)
# Positive Scenarios - Login with following credentials : "standard_user", "problem_user credentials", "performance_glitch_user" credentials"
# Positive Scenarios - Verify user is redirected to inventory page after successful login
# Positive Scenarios - Verify session persists on page refresh
base_dir = os.path.dirname(os.path.abspath(__file__))
data_file = os.path.join(base_dir, "../data", "login_credentials.json")
with open(data_file) as login_credential_obj:
    test_data = json.load(login_credential_obj)
    valid_user_credentials_list = test_data['valid_user_credentials']
    invalid_user_credentials_list = test_data['invalid_user_credentials']

@pytest.mark.parametrize('login_credentials_list',valid_user_credentials_list)
def test_positive_case_for_login_credentials(login_fixture,login_credentials_list):
    dashboard_obj = login_fixture.login_using_valid_credentials(login_credentials_list['username'], login_credentials_list['user_password'])
    dashboard_obj.reload_dashboard()
    dashboard_obj.dashboard_visibility()

def test_positive_case_for_problem_user_login_credentials(login_fixture):
    dashboard_obj = login_fixture.login_using_valid_credentials("problem_user", "secret_sauce")
    dashboard_obj.reload_dashboard()
    dashboard_obj.dashboard_visibility()
    dashboard_obj.check_product_image_source()

# LESSON: 🔐 1. LOGIN MODULE (HIGH PRIORITY)
# Negative Scenarios - Login with :
#       1,2) invalid username | invalid password
#       3,4) empty username & password  | empty username only
#       5) empty password only
# Negative Scenarios - Verify error message text and UI styling
# Negative Scenarios - Verify error disappears after correcting input

@pytest.mark.parametrize("username,password",[("WRONG_CREDENTIALS","secret_sauce"),("standard_user", "WRONG_CREDENTIALS")])
@pytest.mark.no_reset
def test_negative_case_for_login_with_invalid_credentials(login_fixture, username, password):
    error_message = "Epic sadface: Username and password do not match any user in this service"
    login_fixture.login_and_expect_error(username, password, error_message)

@pytest.mark.parametrize("username,password",[("",""),("","secret_sauce")])
@pytest.mark.no_reset
def test_negative_case_for_login_with_missing_credentials(login_fixture, username, password):
    error_message = "Epic sadface: Username is required"
    login_fixture.login_and_expect_error(username, password, error_message)

@pytest.mark.parametrize("username,password",[("standard_user","")])
@pytest.mark.no_reset
def test_negative_case_for_login_with_missing_password_credentials(login_fixture, username, password):
    error_message = "Epic sadface: Password is required"
    error_locator = login_fixture.login_and_expect_error(username, password, error_message)
    login_fixture.login_using_valid_credentials("standard_user", "secret_sauce")
    expect(error_locator).not_to_be_visible() # Negative Scenarios - Verify error disappears after correcting input