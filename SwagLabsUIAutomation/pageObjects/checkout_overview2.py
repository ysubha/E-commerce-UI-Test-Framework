from playwright.sync_api import expect
from SwagLabsUIAutomation.pageObjects.order_success_page import OrderSuccessPage
from SwagLabsUIAutomation.utils.price_calculator import PriceCalculator


class CheckoutOverview2:

    def __init__(self, page):
        self.page = page

    def verify_if_all_items_are_present_in_checkout_overview(self, detailed_product_list):
        for product in detailed_product_list:
            cart_item = self.page.locator('.cart_item').filter(has_text=product['name'])
            item_name = cart_item.locator('.inventory_item_name')
            item_desc = cart_item.locator('.inventory_item_desc')
            item_price = cart_item.locator('.inventory_item_price')

            expect(item_name).to_contain_text(product['name'])
            expect(item_desc).to_contain_text(product['description'])
            price = f'${product['price']:.2f}'
            expect(item_price).to_contain_text(price)

        price_cal_obj = PriceCalculator()
        net_price = price_cal_obj.calculate_net_price(detailed_product_list)
        tax = price_cal_obj.calculate_tax(net_price)
        total = price_cal_obj.calculate_total(net_price)

        expect(self.page.locator('.summary_subtotal_label')).to_have_text(f'Item total: ${net_price:.2f}')
        expect(self.page.locator('.summary_tax_label')).to_have_text(f'Tax: ${tax:.2f}')
        expect(self.page.locator('.summary_total_label')).to_have_text(f'Total: ${total:.2f}')

    def complete_checkout(self):
        self.page.locator('#finish').click()

    def verify_order_success_post_checkout_completion(self):
        expect(self.page.get_by_text('Thank you for your order!')).to_be_visible()
        expect(self.page.locator('.complete-text')).to_have_text(
            'Your order has been dispatched, and will arrive just as fast as the pony can get there!')
        return OrderSuccessPage(self.page)
