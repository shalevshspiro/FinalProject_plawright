import time

import pytest
from tests.base_test import BaseTest

@pytest.mark.usefixtures("setup_function")
class Test_e2e(BaseTest):

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


