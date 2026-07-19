import re

from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

from pages.basepage import BasePage


class CheckoutPage(BasePage):
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
    SHIPPING_METHOD = "input[name*='select_shipping'][name*='[method]']"
    CASH_PAY_BTN = "[value='cash_on_delivery']"
    NEXT_CASH_BTN = "[type='submit']"

    ERROR_INFO = ".invalid-feedback.d-block"
    SUCCESS_INFO = "[name='sylius_shop_checkout_select_shipping'] h5"
    SUCCESS_DHL = "[name='sylius_shop_checkout_select_payment']"
    SUCCESS_CASH = "[name='sylius_checkout_complete']"

    # Known site defect: the shipping-methods step intermittently comes back empty
    # for the same product/address. Matched by text (case-insensitive) rather than
    # a specific CSS class, since the exact markup for this banner wasn't confirmed
    # against the live DOM - adjust the pattern if it doesn't match in practice.
    NO_SHIPPING_METHODS_TEXT = re.compile("no shipping method", re.IGNORECASE)


    def __init__(self, page):
        super().__init__(page)

    def fill_info_checkout(self, email, first_name, last_name, company, street, country, city, postcode, phone):
        email_field = self.page.locator(self.EMAIL_FIELD)

        try:
            email_field.wait_for(state="visible", timeout=3000)
            email_field.fill(email)
        except PlaywrightTimeoutError:
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
        self.page.locator(self.SHIPPING_METHOD).first.check()
        self.click(self.NEXT_BTN)

    def has_shipping_methods(self, timeout: int = 8000) -> bool:
        """True once at least one shipping-method radio button is visible."""
        try:
            self.page.locator(self.SHIPPING_METHOD).first.wait_for(state="visible", timeout=timeout)
            return True
        except PlaywrightTimeoutError:
            return False

    def shipping_unavailable_message_visible(self) -> bool:
        """Detects the 'no shipping methods available' banner for the known site defect."""
        return self.page.get_by_text(self.NO_SHIPPING_METHODS_TEXT).count() > 0

    def reload_shipping_step(self):
        """Reload the current checkout step - used to retry past the intermittent
        'no shipping methods' defect without re-entering the whole address form."""
        self.page.reload()
        self.page.wait_for_load_state("networkidle")

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
    def success_load_checkout(self):
        return self.is_visible(self.EMAIL_FIELD)

    def is_shipping_step_active_successfully(self) -> bool:
        """
        Checks if the shipping step page is actively displaying the shipment setup,
        ensuring that the page didn't load the intermittent 'Warning' bug instead.
        """
        shipment_header = self.page.get_by_role("heading", name="Shipment #")
        return shipment_header.is_visible()

