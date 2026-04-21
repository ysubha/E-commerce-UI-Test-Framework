import json
import os

import allure
import pytest
from playwright.sync_api import expect


# LESSON: 🔐 1. LOGIN MODULE (HIGH PRIORITY)
# Positive Scenarios - Login with following credentials : 'standard_user', 'problem_user credentials', 'performance_glitch_user' credentials'
# Positive Scenarios - Verify user is redirected to inventory page after successful login
# Positive Scenarios - Verify session persists on page refresh

def load_valid_credentials():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_file = os.path.join(base_dir, '../../data', 'login_credentials.json')
    with open(data_file) as f:
        return json.load(f)['valid_user_credentials']

@pytest.mark.integration 
@allure.feature('Login')
@allure.story('Valid login (standard, performance_glitch user)')
@pytest.mark.parametrize('user_credential',load_valid_credentials())
def test_positive_case_for_login_credentials(login_fixture, user_credential):
    dashboard_obj = login_fixture.login_using_valid_credentials(user_credential['username'],
                                                                    user_credential['user_password'])
    dashboard_obj.reload_dashboard()
    dashboard_obj.dashboard_visibility()

@pytest.mark.integration 
@allure.feature('Login')
@allure.story('Valid login problem_user')
def test_positive_case_for_problem_user_login_credentials(login_fixture):
    dashboard_obj = login_fixture.login_using_valid_credentials('problem_user', 'secret_sauce')
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

@pytest.mark.integration 
@allure.feature('Login')
@allure.story('Invalid credentials')
@pytest.mark.parametrize('username,password',
                         [('WRONG_CREDENTIALS', 'secret_sauce'), ('standard_user', 'WRONG_CREDENTIALS')])
@pytest.mark.no_reset
def test_negative_case_for_login_with_invalid_credentials(login_fixture, username, password):
    error_message = 'Epic sadface: Username and password do not match any user in this service'
    login_fixture.login_and_expect_error(username, password, error_message)

@pytest.mark.integration 
@allure.feature('Login')
@allure.story('Missing credentials')
@pytest.mark.parametrize('username,password', [('', ''), ('', 'secret_sauce')])
@pytest.mark.no_reset
def test_negative_case_for_login_with_missing_credentials(login_fixture, username, password):
    error_message = 'Epic sadface: Username is required'
    login_fixture.login_and_expect_error(username, password, error_message)

@pytest.mark.integration 
@allure.feature('Login')
@allure.story('Missing credentials')
@pytest.mark.parametrize('username,password', [('standard_user', '')])
@pytest.mark.no_reset
def test_negative_case_for_login_with_missing_password_credentials(login_fixture, username, password):
    error_message = 'Epic sadface: Password is required'
    error_locator = login_fixture.login_and_expect_error(username, password, error_message)
    login_fixture.login_using_valid_credentials('standard_user', 'secret_sauce')
    expect(error_locator).not_to_be_visible()  # Negative Scenarios - Verify error disappears after correcting input

@pytest.mark.integration 
@allure.feature('Login')
@allure.story('Locked out user')
def test_locked_out_user_cannot_login(login_fixture):
    error_message = 'Epic sadface: Sorry, this user has been locked out.'
    login_fixture.login_and_expect_error('locked_out_user', 'secret_sauce', error_message)