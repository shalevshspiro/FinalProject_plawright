import re

import allure
import pytest
from playwright.sync_api import expect

from data.base_data import CHECKOUT_ADDRESS
from tests.assertions import assert_true
from tests.base_test import BaseTest


@pytest.mark.usefixtures("setup_function")
class TestCheckout(BaseTest):
    import re
    from playwright.sync_api import expect

    @pytest.mark.regression
    def test_personal_info(self):
        """
        Steps to reproduce:
            1. Add the default product to the cart and proceed to checkout.
            2. Fill in a valid address (CHECKOUT_ADDRESS).

        Expected result:
            Checkout advances to the shipping-method selection step
            (URL contains "/checkout/select-shipping").
        """
        with allure.step("Add a product to cart, checkout, and fill in valid address details"):
            self.add_product_to_cart()
            self.cart_page.checkout()
            self.checkout_page.fill_info_checkout(**CHECKOUT_ADDRESS)

        with allure.step("Verify checkout advanced to the shipping-method step"):
            expect(self.page).to_have_url(re.compile(r".*/checkout/select-shipping"), timeout=10000)

        assert_true(
            self.checkout_page.is_shipping_step_active_successfully(),
            "Checkout should reach the active shipping step after valid address details",
        )

    @pytest.mark.regression
    def test_error_email(self):
        """
        Steps to reproduce:
            1. Add the default product to the cart and proceed to checkout.
            2. Fill in the address form with an invalid email ("shalev6005!!gmail.com").

        Expected result:
            A validation error is shown for the invalid email format.
        """
        with allure.step("Add a product to cart, checkout, and fill in an invalid email"):
            self.add_product_to_cart()
            self.cart_page.checkout()
            invalid_address = {**CHECKOUT_ADDRESS, "email": "shalev6005!!gmail.com"}
            self.checkout_page.fill_info_checkout(**invalid_address)
            self.checkout_page.wait_for_visible(self.checkout_page.ERROR_INFO)

        assert_true(
            self.checkout_page.error_info(),
            "A validation error should be shown for an invalid email format",
        )
