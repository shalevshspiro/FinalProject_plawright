import time

import pytest
from data.base_data import first_name, last_name, email,password
from tests.base_test import BaseTest

@pytest.mark.usefixtures("setup_function")

class TestRegister(BaseTest):
    def test_new_register(self):
        self.home_page.goto_register()
        self.register_page.register("shalev","Shapiro","shasl2v@gmail.com","123456789","123456789","123456789")
        assert "Thank you for your registration" in self.register_page.is_register_success_visible()

    def test_same_email(self):
        self.home_page.goto_register()
        self.register_page.register(first_name,last_name,email,"1234556789",password,password)
        assert self.register_page.is_non_success_msg() is True

    def test_empty_field(self):
        self.home_page.goto_register()
        self.register_page.register(first_name,"shalev","sha05@gmail.com","123456789","123456789","")
        assert self.register_page.is_non_success_msg() is True

    def test_login(self):
        self.home_page.goto_login()
        self.login_page.login("shop@example.com","sylius")
        current_url = self.catalog_page.get_current_url()
        expected_url = "https://v2.demo.sylius.com/en_US/"
        assert current_url.rstrip('/') == expected_url.rstrip('/'), \
            f"Expected to return to Home Page ({expected_url}), but current URL is {current_url}"

    def test_error_login(self):
        self.home_page.goto_login()
        self.login_page.login("shalev","sylius")
        assert self.login_page.error_login() is True

    def test_success_logout(self):
        self.home_page.goto_login()
        self.login_page.login("shop@example.com","sylius")
        self.home_page.logout()
        assert self.home_page.logout_success() is True

    def test_forgot_password(self):
        self.home_page.goto_login()
        self.login_page.forgot_password("ido@gmail.com")
        assert self.login_page.rest_password_success() is True

