import allure
import pytest
from tests.assertions import assert_equal, assert_true
from tests.base_test import BaseTest


@pytest.mark.usefixtures("setup_function")
class TestProduct(BaseTest):

    @pytest.mark.regression
    def test_change_size(self):
        """
        Steps to reproduce:
            1. Open the default product's page.
            2. Select size "L" from the size dropdown.

        Expected result:
            The size dropdown shows "L" as the selected value.
        """
        with allure.step("Open the product page and select size 'L'"):
            self.open_product()
            self.product_page.select_size("dress_l")

        self.product_page.assert_selected_size("dress_l")

    @pytest.mark.regression
    def test_add_quantity(self):
        """
        Steps to reproduce:
            1. Open the default product's page.
            2. Set the quantity field to 3.

        Expected result:
            The quantity field shows the value 3.
        """
        with allure.step("Open the product page and set quantity to 3"):
            self.open_product()
            self.product_page.add_quantity("3")

        self.product_page.assert_quantity_value("3")

    @pytest.mark.smoke
    def test_add_to_cart(self):
        """
        Steps to reproduce:
            1. Open the default product's page.
            2. Click "Add to Cart".

        Expected result:
            A cart success confirmation is displayed.
        """
        with allure.step("Add the default product to the cart"):
            self.add_product_to_cart()

        assert_true(
            self.cart_page.get_cart_page(),
            "Cart success confirmation should be visible after adding a product",
        )

    @pytest.mark.regression
    def test_add_review_no_start(self):
        """
        Steps to reproduce:
            1. Open the default product's page.
            2. Submit a review with a title, comment, and email, but no star rating.

        Expected result:
            A validation error is shown for the missing rating.
        """
        with allure.step("Open the product page and submit a review without a star rating"):
            self.open_product()
            self.product_page.add_review("test", "test", "test@walla.com")

        assert_true(
            self.product_page.error_message_review(),
            "A validation error should be shown when submitting a review with no rating selected",
        )

    @pytest.mark.regression
    def test_price_for_quantity(self):
        """
        Steps to reproduce:
            1. Open the default product's page.
            2. Set quantity to 1 and read the displayed unit price.
            3. Change quantity to 3 and wait for the price display to update.

        Expected result:
            The updated price equals the unit price multiplied by 3.
        """
        with allure.step("Open the product page and set quantity to 1"):
            self.open_product()
            self.product_page.add_quantity("1")
            current_price_text = self.product_page.get_price_text()
            current_price = self.product_page.get_price()

        with allure.step("Change quantity to 3 and wait for the price to update"):
            self.product_page.add_quantity("3")
            # The price re-render is async - wait for it to actually change instead
            # of reading it immediately (was returning the stale pre-change value).
            self.product_page.wait_for_price_change(current_price_text)
            updated_price = self.product_page.get_price()

        assert_equal(
            updated_price,
            current_price * 3,
            "Price for quantity 3 should equal the unit price x3",
        )
