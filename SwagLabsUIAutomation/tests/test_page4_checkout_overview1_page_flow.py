

# LESSON: 💳 4. Checkout Flow (End-to-End)
# Checkout Step One
#   Proceed to checkout with items in cart
#   Checkout with valid user information
def test_positive_case_of_checkout_with_cart_items(checkout_overview1_fixture):
    checkout_overview1_fixture.fill_personal_info_details("User","Name","123456")
    checkout_overview1_fixture.go_to_checkout_overview_page2()

# LESSON: 💳 4. Checkout Flow (End-to-End)
# Checkout with empty first name
# Checkout with empty last name
# Checkout with empty postal code
# Verify proper error messages for each field
def test_negative_case_of_checkout_errors_with_cart_items(checkout_overview1_fixture,user_details_and_errors_list_from_json):
    for user in user_details_and_errors_list_from_json :
        checkout_overview1_fixture.fill_personal_info_details(user["first_name"],user["last_name"],user["postal_code"])
        checkout_overview1_fixture.submit_and_validate_error(user["error_code"])
        checkout_overview1_fixture.clear_personal_info_details()