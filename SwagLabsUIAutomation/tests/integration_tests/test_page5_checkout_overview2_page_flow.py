import allure
import pytest


# LESSON: 💳 4. Checkout Flow (End-to-End)
# Checkout Overview
#   Verify selected products appear in checkout overview
#   Verify item total calculation
#   Verify tax calculation
#   Verify total price calculation
@pytest.mark.integration 
@allure.feature('Checkout')
@allure.story('Complete overview validation')
def test_positive_checkout_overview_flow(checkout_overview2_fixture, product_details_list_from_json):
    detailed_products_list = product_details_list_from_json[0]
    checkout_overview2_fixture.verify_if_all_items_are_present_in_checkout_overview(detailed_products_list)


# LESSON:💳 4. Checkout Flow (End-to-End)
# Completion
#   Complete checkout successfully
#   Verify success message after order completion
#   Verify user is redirected to confirmation page
@pytest.mark.integration 
@allure.feature('Checkout')
@allure.story('Complete order')
def test_positive_complete_order_flow(checkout_overview2_fixture, product_details_list_from_json):
    # names_list = product_details_list_from_json[1]
    checkout_overview2_fixture.complete_checkout()
    checkout_overview2_fixture.verify_order_success_post_checkout_completion()
