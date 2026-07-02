import pytest
from data.base_data import first_name, last_name, email,password
from tests.base_test import BaseTest
import time

@pytest.mark.usefixtures("setup_function")

class Test_All(BaseTest):
    def test_e2e_no_login(self):
        self.home_page.goto_dresses()
        self.catalog_page.click_on_product("Sunshine Strappy Delight")
        self.product_page.next_page()
        self.cart_page.checkout()
        self.checkout_page.fill_info_checkout("shalev6005@gmail.com","shalev","shapiro","shapiro","mishoal","AU","new york","1234567","123456789")
        self.checkout_page.choose_dhl()
        self.checkout_page.choose_cash()
        time.sleep(4)
        assert self.checkout_page.success_cash() is True

    def test_e2e_login(self):
        self.home_page.goto_login()
        self.login_page.login("shop@example.com","sylius")
        self.home_page.goto_home()
        self.home_page.goto_dresses()
        self.catalog_page.click_on_product("Sunshine Strappy Delight")
        self.product_page.next_page()
        self.cart_page.checkout()
        self.checkout_page.fill_info_checkout("shalev6005@gmail.com","shalev","shapiro","shapiro","mishoal","AU","new york","1234567","123456789")
        self.checkout_page.choose_dhl()
        self.checkout_page.choose_cash()
        time.sleep(4)
        assert self.checkout_page.success_cash() is True

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

    def test_new_register(self):
        self.home_page.goto_register()
        self.register_page.register("shalev","Shapiro","shale64v@gmail.com","123456789","123456789","123456789")
        assert "Thank you for your registration" in self.register_page.is_register_success_visible()

    def test_same_email(self):
        self.home_page.goto_register()
        self.register_page.register(email,first_name,last_name,email,password,password)
        assert self.register_page.is_non_success_msg() is True




