from playwright.sync_api import expect
from SwagLabsUIAutomation.pageObjects.checkout_overview1 import CheckoutOverview1


class Cart:
    def __init__(self, page):
        self.page = page

    def remove_cart_items(self, products_list):
        for product_name in products_list:
            cart_item = self.page.locator(".cart_item").filter(has_text=product_name)
            expect(cart_item).to_be_visible()
            cart_item.get_by_role("button", name="Remove").click()

    def verify_cart_is_empty(self):
        expect(self.page.locator(".cart_item")).to_have_count(0)

    def go_back_to_dashboard(self):
        self.page.get_by_role("button", name="Continue Shopping").click()
        expect(self.page.get_by_text("Products")).to_be_visible()

    def verify_cart_items(self, products_list):
        for product_name in products_list:
            cart_item = self.page.locator(".cart_item").filter(has_text=product_name)
            expect(cart_item).to_be_visible()

    def go_to_checkout_overview_page1(self):
        self.page.get_by_role('button', name='Checkout').click()
        expect(self.page.get_by_text("Checkout: Your Information")).to_be_visible()
        return CheckoutOverview1(self.page)

    def logout(self):
        self.page.locator("#react-burger-menu-btn").click()
        self.page.locator("a#logout_sidebar_link").click()
        expect(self.page.locator("#login-button")).to_be_visible()
