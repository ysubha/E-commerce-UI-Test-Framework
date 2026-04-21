from playwright.sync_api import expect
from SwagLabsUIAutomation.pageObjects.checkout_overview2 import CheckoutOverview2


class CheckoutOverview1:

    def __init__(self, page):
        self.page = page

    def fill_personal_info_details(self, first_name, last_name, postal_code):
        self.page.get_by_placeholder('First Name').fill(first_name)
        self.page.get_by_placeholder('Last Name').fill(last_name)
        self.page.get_by_placeholder('Zip/Postal Code').fill(postal_code)

    def go_to_checkout_overview_page2(self):
        self.page.locator('#continue').click()
        expect(self.page.get_by_text('Checkout: Overview')).to_be_visible()
        checkout_overview2_obj = CheckoutOverview2(self.page)
        return checkout_overview2_obj

    def submit_and_validate_error(self, error_code):
        self.page.locator('#continue').click()
        expect(self.page.locator('h3[data-test="error"]')).to_have_text(error_code)
        expect(self.page.get_by_text('Checkout: Your Information')).to_be_visible()

    def clear_personal_info_details(self):
        self.page.get_by_placeholder('First Name').clear()
        self.page.get_by_placeholder('Last Name').clear()
        self.page.get_by_placeholder('Zip/Postal Code').clear()
