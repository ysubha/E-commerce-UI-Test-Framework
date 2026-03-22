

class OrderSuccessPage:

    def __init__(self,page):
        self.page = page

    def logout(self):
        self.page.locator("#react-burger-menu-btn").click()
        self.page.locator("a#logout_sidebar_link").click()

        from SwagLabsUIAutomation.pageObjects.login import LoginPage
        return LoginPage(self.page)