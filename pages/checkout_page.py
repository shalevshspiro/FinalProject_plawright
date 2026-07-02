from pages.basepage import BasePage


class Checkout_Page(BasePage):
    # --- לוקייטורים של שדות הטופס ---
    EMAIL_FIELD = "#sylius_shop_checkout_address_customer_email"
    FIRST_NAME_FIELD = "#sylius_shop_checkout_address_billingAddress_firstName"
    LAST_NAME_FIELD = "#sylius_shop_checkout_address_billingAddress_lastName"
    COMPANY_FIELD = "#sylius_shop_checkout_address_billingAddress_company"
    STREET_FIELD = "#sylius_shop_checkout_address_billingAddress_street"
    COUNTRY_SELECT = "#sylius_shop_checkout_address_billingAddress_countryCode"
    CITY_FIELD = "#sylius_shop_checkout_address_billingAddress_city"
    POST_CODE_FIELD = "#sylius_shop_checkout_address_billingAddress_postcode"
    PHONE_FIELD = "#sylius_shop_checkout_address_billingAddress_phoneNumber"
    NEXT_BTN = ".flex-sm-row.gap-2 button"
    BACK_BTN = ".btn-light.btn-icon"
    DHL_BTN = "[value='dhl_express']"
    CASH_PAY_BTN = "[value='cash_on_delivery']"
    NEXT_CASH_BTN = "[type='submit']"

    # --- לוקייטורים לאימותים (Asserts) ---
    ERROR_INFO = ".invalid-feedback.d-block"
    SUCCESS_INFO = "[name='sylius_shop_checkout_select_shipping'] h5"
    SUCCESS_DHL = "[name='sylius_shop_checkout_select_payment']"
    SUCCESS_CASH = "[name='sylius_checkout_complete']"

    def __init__(self, page):
        super().__init__(page)

    def fill_info_checkout(self, email, first_name, last_name, company, street, country, city, postcode, phone):
        # הגדרת לוקייטור לשדה האימייל
        email_field = self.page.locator(self.EMAIL_FIELD)

        try:
            # פליירייט ימתין מקסימום 3 שניות לראות אם שדה המייל גלוי (מתאים למשתמש אורח)
            email_field.wait_for(state="visible", timeout=3000)
            email_field.fill(email)
        except:
            print("User is already logged in (Email field is hidden), skipping email input.")
        self.fill_text(self.FIRST_NAME_FIELD, first_name)
        self.fill_text(self.LAST_NAME_FIELD, last_name)
        self.fill_text(self.COMPANY_FIELD, company)
        self.fill_text(self.STREET_FIELD, street)
        self.select_by_value(self.COUNTRY_SELECT, country)
        self.fill_text(self.CITY_FIELD, city)
        self.fill_text(self.POST_CODE_FIELD, postcode)
        self.fill_text(self.PHONE_FIELD, phone)
        self.click(self.NEXT_BTN)

    def click_back(self):
        self.click(self.BACK_BTN)
    def choose_dhl(self):
        self.click(self.DHL_BTN)
        self.click(self.NEXT_BTN)
    def choose_cash(self):
        self.click(self.CASH_PAY_BTN)
        self.click(self.NEXT_BTN)


    # --- (Assertions)

    def verify_saved_checkout_fields(self, expected_email, expected_city):
        self.verify_input_value(self.EMAIL_FIELD, expected_email)
        self.verify_input_value(self.CITY_FIELD, expected_city)

    def success_info(self):
        return self.is_visible(self.SUCCESS_INFO)

    def error_info(self):
        return self.is_visible(self.ERROR_INFO)

    def success_dhl(self):
        return self.is_visible(self.SUCCESS_DHL)
    def success_cash(self):
        return self.is_visible(self.SUCCESS_CASH)