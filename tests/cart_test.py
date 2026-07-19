import allure
import pytest
from tests.assertions import assert_equal, assert_true
from tests.base_test import BaseTest


@pytest.mark.usefixtures("setup_function")
class TestCart(BaseTest):

    @pytest.mark.regression
    def test_clear_cart(self):
        """
        Steps to reproduce:
            1. Add the default product to the cart.
            2. Click "Clear cart".

        Expected result:
            The cart shows an "empty cart" message.
        """
        with allure.step("Add a product to the cart, then clear the cart"):
            self.add_product_to_cart()
            self.cart_page.clear_cart()
            # clear_cart() triggers a live-component (async) update - wait for the
            # empty-cart banner instead of asserting immediately on a stale DOM.
            self.cart_page.wait_for_visible(self.cart_page.EMPTY_CART)

        assert_true(
            self.cart_page.get_empty_cart(),
            "Cart should show the empty-cart message after clearing it",
        )

    @pytest.mark.regression
    def test_paypal(self):
        """
        Steps to reproduce:
            1. Add the default product to the cart.
            2. Click the PayPal button in the cart panel.

        Expected result:
            A PayPal popup opens with the header text "Pay with PayPal".
        """
        with allure.step("Add a product to the cart and open the PayPal popup"):
            self.add_product_to_cart()
            paypal_page = self.cart_page.open_paypal_window()
            paypal_page.wait_for_load_state("domcontentloaded")
            paypal_page.locator("#headerText").wait_for(state="visible", timeout=15000)

        assert_equal(
            paypal_page.locator("#headerText").inner_text(),
            "Pay with PayPal",
            "PayPal popup header text should read 'Pay with PayPal'",
        )

    @pytest.mark.smoke
    def test_checkout(self):
        """
        Steps to reproduce:
            1. Add the default product to the cart.
            2. Click "Checkout" in the cart panel.

        Expected result:
            The checkout page loads, with the email field visible.
        """
        with allure.step("Add a product to the cart and proceed to checkout"):
            self.add_product_to_cart()
            self.cart_page.checkout()
            # Wait for the checkout page to actually load before asserting on it -
            # checkout() only triggers navigation, it doesn't wait for it to land.
            self.checkout_page.wait_for_visible(self.checkout_page.EMAIL_FIELD)

        assert_true(
            self.checkout_page.success_load_checkout(),
            "Checkout page should load (email field visible) after clicking checkout",
        )

    @pytest.mark.regression
    def test_invalid_cupon(self):
        """
        Steps to reproduce:
            1. Add the default product to the cart.
            2. Enter an invalid coupon code ("123456") and apply it.

        Expected result:
            An invalid-coupon error message is displayed.
        """
        with allure.step("Add a product to the cart and apply an invalid coupon code"):
            self.add_product_to_cart()
            self.cart_page.wait_for_visible(self.cart_page.ADD_COUPON_FIELD)
            self.cart_page.coupon("123456")
            # coupon() submits via a live component (async) - wait for the error
            # message instead of asserting immediately on a stale DOM.
            self.cart_page.wait_for_visible(self.cart_page.COUPON_ERROR)

        assert_true(
            self.cart_page.get_coupon_error(),
            "An invalid-coupon error should be shown for coupon code '123456'",
        )
