from pages.basepage import BasePage


class HomePage(BasePage):
    LOGIN_BTN = "#login-page-button"
    REGISTER_BTN = "#register-page-button"
    HOME_BTN = ".d-inline-block.py-lg-2"
    SHIRT_DROPDOWN = ".w-full.py-0 > div > div:nth-child(1)"
    MEN_SHIRT_BTN = "[href$='shirts/men']"
    DRESS_BTN = "[href$='category/dresses']"
    CART_BTN = ".d-none.d-lg-block.ps-1"
    LOGOUT_BTN = "#logout-button"






    def __init__(self, page):
        super().__init__(page)


    def goto_login(self):
        self.click(self.LOGIN_BTN)

    def goto_register(self):
        self.click(self.REGISTER_BTN)

    def goto_home(self):
        self.click(self.HOME_BTN)

    def goto_dresses(self):
        self.click(self.DRESS_BTN)

    def goto_men(self):
        self.click(self.SHIRT_DROPDOWN)
        self.click(self.MEN_SHIRT_BTN)

    def goto_cart(self):
        self.click(self.CART_BTN)

    def logout(self):
        self.click(self.LOGOUT_BTN)


    #assert
    def logout_success(self):
        return self.is_visible(self.LOGIN_BTN)