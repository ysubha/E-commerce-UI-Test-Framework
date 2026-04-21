from playwright.sync_api import Playwright, expect
from SwagLabsUIAutomation.pageObjects.cart import Cart


class Dashboard:

    def __init__(self, page):
        self.page = page

    def verify_cart_badge_count(self, cart_count: int):
        if cart_count:
            expect(self.page.locator('.shopping_cart_badge')).to_have_text(str(cart_count))
        else:
            expect(self.page.locator('.shopping_cart_badge')).not_to_be_visible()

    def add_item_to_cart(self, item_name_list):
        for item_name in item_name_list:
            order_item = self.page.locator('.inventory_item').filter(has_text=item_name)
            add_to_cart_button = order_item.get_by_role('button', name='Add to cart')
            # expect(add_to_cart_button).to_be_visible()
            add_to_cart_button.click()

    def add_item_to_cart_if_not_added(self, item_name_list):
        for item_name in item_name_list:
            order_item = self.page.locator('.inventory_item').filter(has_text=item_name)
            if order_item.get_by_role('button').text_content() == 'Add to cart':
                order_item.get_by_role('button', name='Add to cart').click()

    def verify_items_are_added_to_inventory(self, item_name_list):
        for item_name in item_name_list:
            expect(self.page.locator('.inventory_item').filter(has_text=item_name).get_by_role('button')).to_have_text(
                'Remove')

    def verify_items_are_removed_from_cart(self, item_name_list):
        for item_name in item_name_list:
            expect(self.page.locator('.inventory_item').filter(has_text=item_name).get_by_role('button')).to_have_text(
                'Add to cart')

    def remove_item_from_cart(self, item_name_list):
        for item_name in item_name_list:
            order_item = self.page.locator('.inventory_item').filter(has_text=item_name)
            remove_from_cart_button = order_item.get_by_role('button', name='Remove')
            remove_from_cart_button.click()

    def go_to_cart(self):
        self.page.locator('.shopping_cart_link').click()
        cart_obj = Cart(self.page)
        return cart_obj

    def reload_dashboard(self):
        self.page.reload()
        expect(self.page.get_by_text('Products')).to_be_visible()

    def check_product_count(self, count):
        expect(self.page.locator('.inventory_item')).to_have_count(count)

    def check_locator_visibility(self, item):
        expect(item).to_be_visible()

    def check_product_image_source(self):
        image = self.page.locator('.inventory_item_img img')
        counts = image.count()
        for i in range(counts):
            image_source = image.nth(i).get_attribute('src')
            assert 'sl-404.168b1cce10384b857a6f.jpg' in image_source, 'Expected broken image for problem_user'

    def logout(self):
        self.page.locator('#react-burger-menu-btn').click()
        self.page.locator('a#logout_sidebar_link').click()
        expect(self.page.locator('#login-button')).to_be_visible()

    def dashboard_visibility(self):
        self.check_locator_visibility(self.page.get_by_text('Products'))
        self.check_locator_visibility(self.page.locator('.inventory_container'))
        self.check_locator_visibility(self.page.locator('.inventory_list'))

    def validate_product_item_info(self, my_item_list):
        for item in my_item_list:
            web_product_item = self.page.locator('.inventory_item').filter(has_text=item['name'])
            web_item_name = web_product_item.locator('.inventory_item_name')
            web_item_price = web_product_item.locator('.inventory_item_price')
            web_item_description = web_product_item.locator('.inventory_item_desc')
            web_item_image = web_product_item.locator('img.inventory_item_img')
            web_item_add_to_cart_button = web_product_item.get_by_role('button', name='Add to cart')

            expect(web_item_name).to_have_text(item['name'])
            expect(web_item_price).to_have_text(f'${item["price"]:.2f}')
            expect(web_item_description).to_have_text(item['description'])
            expect(web_item_image).to_have_attribute('alt', item['name'])
            self.check_locator_visibility(web_item_add_to_cart_button)

    def verify_sorting_of_products_based_on_given_filter(self, my_items_list, sort_option):
        self.page.locator('.product_sort_container').select_option(sort_option)
        expect(self.page.locator('.product_sort_container')).to_contain_text(sort_option)
        web_list = self.page.locator('div.inventory_item')
        count = web_list.count()
        for i in range(count):
            expect(web_list.nth(i).locator('div.inventory_item_name')).to_have_text(my_items_list[i]["name"])
            expected_price = f'${my_items_list[i]["price"]:.2f}'
            expect(web_list.nth(i).locator('div.inventory_item_price')).to_have_text(expected_price)
