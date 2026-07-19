import time

import allure
import pytest
from data.base_data import first_name, last_name, email, password, VALID_USER_EMAIL, VALID_USER_PASSWORD
from tests.assertions import assert_contains, assert_true, assert_url_equals
from tests.base_test import BaseTest


@pytest.mark.usefixtures("setup_function")
class TestRegister(BaseTest):

    @pytest.mark.regression
    def test_new_register(self):
        """
        Steps to reproduce:
            1. Open the registration page.
            2. Fill in the form with a brand-new, unique email address.
            3. Submit the registration.

        Expected result:
            A "Thank you for your registration" success message is shown.
        """
        with allure.step("Register a brand-new account with a unique email"):
            self.home_page.goto_register()
            unique_email = f"shalev_{int(time.time())}@example.com"
            self.register_page.register("shalev", "Shapiro", unique_email, "123456789", "123456789", "123456789")

        assert_contains(
            self.register_page.is_register_success_visible(),
            "Thank you for your registration",
            "A registration success message should be shown for a new, unique email",
        )

    @pytest.mark.regression
    def test_same_email(self):
        """
        Steps to reproduce:
            1. Open the registration page.
            2. Fill in the form using an email that's already registered.
            3. Submit the registration.

        Expected result:
            A validation error is shown (duplicate email).
        """
        with allure.step("Attempt to register with an email that's already in use"):
            self.home_page.goto_register()
            self.register_page.register(first_name, last_name, email, "1234556789", password, password)

        assert_true(
            self.register_page.is_non_success_msg(),
            "A validation error should be shown when registering with an already-used email",
        )

    @pytest.mark.regression
    def test_empty_field(self):
        """
        Steps to reproduce:
            1. Open the registration page.
            2. Fill in the form but leave the password-confirmation field empty.
            3. Submit the registration.

        Expected result:
            A validation error is shown for the missing confirmation.
        """
        with allure.step("Attempt to register with an empty password confirmation field"):
            self.home_page.goto_register()
            self.register_page.register(first_name, "shalev", "sha05@gmail.com", "123456789", "123456789", "")

        assert_true(
            self.register_page.is_non_success_msg(),
            "A validation error should be shown when the password confirmation field is empty",
        )

    @pytest.mark.smoke
    def test_login(self):
        """
        Steps to reproduce:
            1. Open the login page.
            2. Log in with valid demo-shop credentials.

        Expected result:
            The user is redirected back to the home page.
        """
        with allure.step("Log in with valid demo-shop credentials"):
            self.home_page.goto_login()
            self.login_page.login(VALID_USER_EMAIL, VALID_USER_PASSWORD)

        current_url = self.catalog_page.get_current_url()
        assert_url_equals(
            current_url,
            "https://v2.demo.sylius.com/en_US/",
            "Should return to the Home Page after a successful login",
        )

    @pytest.mark.regression
    def test_error_login(self):
        """
        Steps to reproduce:
            1. Open the login page.
            2. Attempt to log in with an unrecognized username.

        Expected result:
            A login error message is shown.
        """
        with allure.step("Attempt to log in with an invalid username"):
            self.home_page.goto_login()
            self.login_page.login("shalev", "sylius")

        assert_true(
            self.login_page.error_login(),
            "A login error should be shown for an unrecognized username",
        )

    @pytest.mark.smoke
    def test_success_logout(self):
        """
        Steps to reproduce:
            1. Log in with valid demo-shop credentials.
            2. Click "Logout".

        Expected result:
            The login button reappears in the header.
        """
        with allure.step("Log in, then log out"):
            self.home_page.goto_login()
            self.login_page.login(VALID_USER_EMAIL, VALID_USER_PASSWORD)
            self.home_page.logout()

        assert_true(
            self.home_page.logout_success(),
            "The login button should reappear after a successful logout",
        )

    @pytest.mark.regression
    def test_forgot_password(self):
        """
        Steps to reproduce:
            1. Open the login page.
            2. Click "Forgot password" and submit an email address.

        Expected result:
            A password-reset confirmation message is shown.
        """
        with allure.step("Request a password reset for a given email"):
            self.home_page.goto_login()
            self.login_page.forgot_password("ido@gmail.com")

        assert_true(
            self.login_page.rest_password_success(),
            "A password-reset confirmation message should be shown",
        )
