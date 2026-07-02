from pages.basepage import BasePage


class RegisterPage(BasePage):
    FIRST_NAME_FIELD = "#sylius_shop_customer_registration_firstName"
    LAST_NAME_FIELD = "#sylius_shop_customer_registration_lastName"
    EMAIL_FIELD = "#sylius_shop_customer_registration_email"
    PHONE_FIELD = "#sylius_shop_customer_registration_phoneNumber"
    CHECKBOX_NEWSLETTER = ".form-check-input"
    PASSWORD_FIELD = "#sylius_shop_customer_registration_user_plainPassword_first"
    VERIFICATION_FIELD = "#sylius_shop_customer_registration_user_plainPassword_second"
    CREATE_BTN = "#register-button"
    SIGN_IN_BTN = ".min-vh-100 > div:nth-child(5)  a"

    #assert
    SUCCESS_MSG = ".h2"
    NON_SUCCESS_MSG = ".invalid-feedback.d-block"


    def __init__(self, page):
        super().__init__(page)

    def register(self, first_name, last_name, email, phone_number, password,password_confirmation):
        self.fill_text(self.FIRST_NAME_FIELD, first_name)
        self.fill_text(self.LAST_NAME_FIELD, last_name)
        self.fill_text(self.EMAIL_FIELD, email)
        self.fill_text(self.PHONE_FIELD, phone_number)
        self.fill_text(self.PASSWORD_FIELD, password)
        self.fill_text(self.VERIFICATION_FIELD, password_confirmation)
        self.click(self.CREATE_BTN)

    def goto_sign_in(self):
        self.click(self.SIGN_IN_BTN)

    def check_newsletter(self):
        self.click(self.CHECKBOX_NEWSLETTER)

    #assert
    def is_register_success_visible(self):
        return self.get_text(self.SUCCESS_MSG)
    def is_non_success_msg(self):
        return self.is_visible(self.NON_SUCCESS_MSG)