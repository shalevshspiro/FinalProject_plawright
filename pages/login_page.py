from pages.basepage import BasePage


class LoginPage(BasePage):
    USERNAME_FIELD = "#_username"
    PASSWORD_FIELD = "#_password"
    REMEMBER_ME_BTN = "#_remember_me"
    LOGIN_BTN = "#login-button"
    FORGOT_PASSWORD_BTN = "a[href$='forgotten-password']"
    REST_EMAIL_PASSWORD_FIELD = "#sylius_user_request_password_reset_email"
    REST_BTN= "[type='submit']"


    #assert
    SUCCESS_LOGIN = ".gap-2.align-items-center.ps-2 > span"
    SUCCESS_REST_PASSWORD = ".alert.alert-success.my-2"
    ERROR_LOGIN = ".alert-danger div"




    def __init__(self, page):
        super().__init__(page)

    def login(self, username, password):
        self.fill_text(self.USERNAME_FIELD, username)
        self.fill_text(self.PASSWORD_FIELD, password)
        self.click(self.LOGIN_BTN)

    def forgot_password(self,email):
        self.click(self.FORGOT_PASSWORD_BTN)
        self.fill_text(self.REST_EMAIL_PASSWORD_FIELD, email)
        self.click(self.REST_BTN)



    #assert

    def login_success(self):
        return self.is_visible(self.SUCCESS_LOGIN)

    def rest_password_success(self):
        return self.is_visible(self.SUCCESS_REST_PASSWORD)

    def error_login(self):
        return self.is_visible(self.ERROR_LOGIN)

