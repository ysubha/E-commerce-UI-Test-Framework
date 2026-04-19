import json
import os.path

import allure
import pytest


# LESSON: 💳 4. Checkout Flow (End-to-End)
# Checkout Step One
#   Proceed to checkout with items in cart
#   Checkout with valid user information
@allure.feature('Checkout')
@allure.story('Valid checkout flow')
def test_positive_case_of_checkout_with_cart_items(checkout_overview1_fixture):
    checkout_overview1_fixture.fill_personal_info_details("User", "Name", "123456")
    checkout_overview1_fixture.go_to_checkout_overview_page2()


# LESSON: 💳 4. Checkout Flow (End-to-End)
# Checkout with empty first name
# Checkout with empty last name
# Checkout with empty postal code
# Verify proper error messages for each field
# TODO: move to utils/data_loader.py
def load_user_details_and_errors_list_from_json():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_file = os.path.join(base_dir, "../data", "checkout_user_details.json")
    with open(data_file) as data_file_obj:
        return json.load(data_file_obj)['user_details_and_errors']


@allure.feature('Checkout')
@allure.story('Checkout error validations')
@pytest.mark.parametrize("user", load_user_details_and_errors_list_from_json())
def test_negative_case_of_checkout_errors_with_cart_items(checkout_overview1_fixture, user):
    checkout_overview1_fixture.fill_personal_info_details(user["first_name"], user["last_name"], user["postal_code"])
    checkout_overview1_fixture.submit_and_validate_error(user["error_code"])
    checkout_overview1_fixture.clear_personal_info_details()
