import allure
import pytest


# LESSON: 🛒 2. Inventory / Products Page
# UI & Data Validation :
#   Verify product list is displayed
#   Verify each product has: Name, Price, Description, Image, Add to Cart button
#   Verify product count matches expected inventory
@pytest.mark.integration
@allure.feature('Product Catalogue')
@allure.story('Products list displayed')
def test_products_list_displayed(dashboard_fixture, product_details_list_from_json):
    dashboard_fixture.dashboard_visibility()
    dashboard_fixture.validate_product_item_info(product_details_list_from_json[0])
    dashboard_fixture.check_product_count(len(product_details_list_from_json[0]))


# LESSON: 🛒 2. Inventory / Products Page
# Sorting
#   Sort products by Name (A → Z) |  products by Name (Z → A)
#   Sort products by Price (Low → High) | products by Price (High → Low)

sort_strategy = {
    'Name (A to Z)': lambda products_lit: sorted(products_lit, key=lambda product: product['name']),
    'Name (Z to A)': lambda products_lit: sorted(products_lit, key=lambda product: product['name'], reverse=True),
    'Price (low to high)': lambda products_lit: sorted(products_lit, key=lambda product: product['price']),
    'Price (high to low)': lambda products_lit: sorted(products_lit, key=lambda product: product['price'], reverse=True)
}


@pytest.mark.integration
@allure.feature('Product Catalogue')
@allure.story('Product sorting')
@pytest.mark.parametrize('sorting_filter',
                         ['Name (A to Z)', 'Name (Z to A)', 'Price (low to high)', 'Price (high to low)'])
def test_asc_sorting_of_product(dashboard_fixture, product_details_list_from_json, sorting_filter):
    expected_sorted_list = sort_strategy[sorting_filter](product_details_list_from_json[0])
    dashboard_fixture.verify_sorting_of_products_based_on_given_filter(expected_sorted_list, sorting_filter)


# LESSON: 🧺 3. Cart Functionality
# Add single product to cart
# Add multiple products to cart
# Remove product from inventory page
# Remove product from cart page
# Verify cart badge count updates correctly
@pytest.mark.integration
@allure.feature('Cart')
@allure.story('Add single item')
def test_adding_single_product_to_cart(dashboard_fixture):
    item_name_list = ['Sauce Labs Onesie']
    dashboard_fixture.add_item_to_cart(item_name_list)
    dashboard_fixture.verify_items_are_added_to_inventory(item_name_list)
    dashboard_fixture.verify_cart_badge_count(len(item_name_list))


@pytest.mark.integration
@allure.feature('Cart')
@allure.story('Add multiple items')
def test_adding_multiple_products_to_cart(dashboard_fixture):
    item_name_list = ['Sauce Labs Bike Light', 'Sauce Labs Backpack']
    dashboard_fixture.add_item_to_cart(item_name_list)
    dashboard_fixture.verify_items_are_added_to_inventory(item_name_list)
    dashboard_fixture.verify_cart_badge_count(len(item_name_list))


@pytest.mark.integration
@allure.feature('Cart')
@allure.story('Remove from inventory')
def test_remove_product_from_inventory(dashboard_fixture):
    item_name_list = ['Sauce Labs Onesie', 'Sauce Labs Bike Light', 'Sauce Labs Backpack']
    dashboard_fixture.add_item_to_cart(item_name_list)
    dashboard_fixture.verify_items_are_added_to_inventory(item_name_list)
    dashboard_fixture.remove_item_from_cart(item_name_list)
    dashboard_fixture.verify_items_are_removed_from_cart(item_name_list)
    dashboard_fixture.verify_cart_badge_count(0)


@pytest.mark.integration
@allure.feature('Cart')
@allure.story('Remove from cart page')
def test_removal_of_products_from_cart_page(dashboard_fixture):
    item_name_list = ['Sauce Labs Onesie', 'Sauce Labs Bike Light']
    dashboard_fixture.add_item_to_cart(item_name_list)
    dashboard_fixture.verify_items_are_added_to_inventory(item_name_list)
    cart_obj = dashboard_fixture.go_to_cart()
    cart_obj.remove_cart_items(item_name_list)
    cart_obj.verify_cart_is_empty()
