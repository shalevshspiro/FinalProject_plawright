import time

import pytest
from tests.base_test import BaseTest

@pytest.mark.usefixtures("setup_function")
class TestHome(BaseTest):
    def test_navigate_to_dresses_category(self):
        self.home_page.goto_dresses()
        current_url = self.catalog_page.get_current_url()
        assert "taxons/category/dresses" in current_url, f"Expected to be in Dresses category, but URL is {current_url}"

    def test_navigate_to_home_page(self):
        self.home_page.goto_login()
        self.home_page.goto_home()
        current_url = self.catalog_page.get_current_url()
        expected_url = "https://v2.demo.sylius.com/en_US/"
        assert current_url.rstrip('/') == expected_url.rstrip('/'), \
            f"Expected to return to Home Page ({expected_url}), but current URL is {current_url}"

    def test_navigate_to_cart_page(self):
        self.home_page.goto_cart()
        assert self.cart_page.get_cart_home_title() is True
