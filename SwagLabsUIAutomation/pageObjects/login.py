from playwright.sync_api import expect
from .dashboard import Dashboard


class LoginPage:
    def __init__(self, page):
        self.page = page

    def navigation(self):
        self.page.goto('https://www.saucedemo.com/')

    def login_page_verification(self):
        expect(self.page).to_have_url('https://www.saucedemo.com/')
        expect(self.page.locator('.login_logo')).to_have_text('Swag Labs')
        expect(self.page.locator('#login-button')).to_be_visible()

    def verify_dashboard_not_accessible_after_logout(self):
        self.page.goto('https://www.saucedemo.com/inventory.html')
        expect(self.page).to_have_url('https://www.saucedemo.com/')
        expect(self.page.locator('#login-button')).to_be_visible()
        expect(self.page.locator("h3[data-test='error']")).to_have_text(
            "Epic sadface: You can only access '/inventory.html' when you are logged in.")

    def verify_app_pages_not_accessible_without_login(self, url, error_code):
        self.page.goto(url)
        expect(self.page).to_have_url('https://www.saucedemo.com/')
        expect(self.page.locator('#login-button')).to_be_visible()
        expect(self.page.locator("h3[data-test='error']")).to_have_text(error_code)

    def verify_back_navigation_blocked(self):
        self.page.go_back()
        expect(self.page).to_have_url('https://www.saucedemo.com/')

    def login_using_valid_credentials(self, username, password):
        self.page.get_by_placeholder('Username').clear()
        self.page.get_by_placeholder('Password').clear()
        self.page.get_by_placeholder('Username').fill(username)
        self.page.get_by_placeholder('Password').fill(password)
        self.page.locator('#login-button').click()

        expect(self.page).to_have_url('https://www.saucedemo.com/inventory.html')

        dashboard_obj = Dashboard(self.page)
        return dashboard_obj

    # Negative Scenarios

    def login_and_expect_error(self, username, password, expected_error):
        username_locator = self.page.get_by_placeholder('Username')
        password_locator = self.page.get_by_placeholder('Password')

        username_locator.clear()
        username_locator.fill(username)
        password_locator.clear()
        password_locator.fill(password)

        self.page.locator('#login-button').click()
        error_locator = self.page.locator("h3[data-test='error']")
        expect(error_locator).to_be_visible()  # Negative Scenarios - Verify error message text and UI styling
        expect(error_locator).to_have_text(
            expected_error)  # Negative Scenarios - Verify error message text and UI styling
        return error_locator
