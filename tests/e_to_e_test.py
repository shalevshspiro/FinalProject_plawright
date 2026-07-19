import allure
import pytest
from data.base_data import CHECKOUT_ADDRESS, VALID_USER_EMAIL, VALID_USER_PASSWORD
from tests.assertions import assert_true
from tests.base_test import BaseTest


@pytest.mark.usefixtures("setup_function")
class TestE2E(BaseTest):

    @pytest.mark.smoke
    @pytest.mark.e2e
    def test_e2e_no_login(self):
        """
        Steps to reproduce:
            1. Add the default product to the cart (as a guest).
            2. Proceed to checkout and fill in a valid address.
            3. Choose a shipping method.
            4. Choose cash on delivery as the payment method.

        Expected result:
            The order completes successfully (cash-on-delivery success screen shown).
        """
        with allure.step("Add product to cart and start checkout as a guest"):
            self.add_product_to_cart()
            self.cart_page.checkout()
            self.checkout_page.fill_info_checkout(**CHECKOUT_ADDRESS)

        with allure.step("Choose a shipping method and pay by cash on delivery"):
            self.choose_shipping_with_retry()
            self.checkout_page.choose_cash()
            self.checkout_page.wait_for_visible(self.checkout_page.SUCCESS_CASH)

        assert_true(
            self.checkout_page.success_cash(),
            "Guest checkout should complete successfully with cash on delivery",
        )

    @pytest.mark.smoke
    @pytest.mark.e2e
    def test_e2e_login(self):
        """
        Steps to reproduce:
            1. Log in with valid demo-shop credentials.
            2. Add the default product to the cart.
            3. Proceed to checkout and fill in a valid address.
            4. Choose a shipping method.
            5. Choose cash on delivery as the payment method.

        Expected result:
            The order completes successfully (cash-on-delivery success screen shown).
        """
        with allure.step("Log in, then add a product to cart and start checkout"):
            self.home_page.goto_login()
            self.login_page.login(VALID_USER_EMAIL, VALID_USER_PASSWORD)
            self.home_page.goto_home()
            self.add_product_to_cart()
            self.cart_page.checkout()
            self.checkout_page.fill_info_checkout(**CHECKOUT_ADDRESS)

        with allure.step("Choose a shipping method and pay by cash on delivery"):
            self.choose_shipping_with_retry()
            self.checkout_page.choose_cash()
            self.checkout_page.wait_for_visible(self.checkout_page.SUCCESS_CASH)

        assert_true(
            self.checkout_page.success_cash(),
            "Logged-in checkout should complete successfully with cash on delivery",
        )
