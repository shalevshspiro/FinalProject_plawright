import allure
import pytest
from tests.assertions import assert_contains, assert_true, assert_url_equals
from tests.base_test import BaseTest


@pytest.mark.usefixtures("setup_function")
class TestHome(BaseTest):

    @pytest.mark.smoke
    def test_navigate_to_dresses_category(self):
        """
        Steps to reproduce:
            1. Open the home page.
            2. Click the "Dresses" category link.

        Expected result:
            The URL contains "taxons/category/dresses".
        """
        with allure.step("Navigate to the Dresses category from the home page"):
            self.home_page.goto_dresses()

        current_url = self.catalog_page.get_current_url()
        assert_contains(
            current_url,
            "taxons/category/dresses",
            "URL should contain the Dresses category path",
        )

    @pytest.mark.smoke
    def test_navigate_to_home_page(self):
        """
        Steps to reproduce:
            1. Open the home page.
            2. Navigate to the login page.
            3. Click the site logo / home link to return to the home page.

        Expected result:
            The URL is back to "https://v2.demo.sylius.com/en_US/".
        """
        with allure.step("Go to the login page, then back to the home page"):
            self.home_page.goto_login()
            self.home_page.goto_home()

        current_url = self.catalog_page.get_current_url()
        assert_url_equals(
            current_url,
            "https://v2.demo.sylius.com/en_US/",
            "Should return to the Home Page",
        )

    @pytest.mark.smoke
    def test_navigate_to_cart_page(self):
        """
        Steps to reproduce:
            1. Open the home page.
            2. Click the cart icon.

        Expected result:
            The cart panel opens and its title is visible.
        """
        with allure.step("Open the cart from the home page"):
            self.home_page.goto_cart()

        assert_true(
            self.cart_page.get_cart_home_title(),
            "Cart panel title should be visible after opening the cart",
        )
