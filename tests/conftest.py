import pytest

from pages.cart_page import Cart_Page
from pages.catalog_page import Catalog_Page
from pages.checkout_page import Checkout_Page
from pages.home_page import HomePage
from pages.product_page import ProductPage
from pages.login_page import LoginPage
from pages.register_page import RegisterPage

BASE_URL = "https://v2.demo.sylius.com/en_US/"

@pytest.fixture(scope="class")
def setup_class(request, browser):
    context = browser.new_context(
        viewport={'width': 1920, 'height': 1080},
        user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
    )
    page = context.new_page()
    page.goto(BASE_URL)

    request.cls.page = page
    request.cls.home_page = HomePage(page)
    request.cls.catalog_page = Catalog_Page(page)
    request.cls.cart_page = Cart_Page(page)
    request.cls.checkout_page = Checkout_Page(page)
    request.cls.product_page = ProductPage(page)
    request.cls.register_page = RegisterPage(page)
    request.cls.login_page = LoginPage(page)

    yield

    page.close()
    context.close()


@pytest.fixture(scope="function")
def setup_function(request, browser):
    context = browser.new_context(
        viewport={'width': 1920, 'height': 1080},
        user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
    )
    page = context.new_page()
    page.goto(BASE_URL)

    request.cls.page = page
    request.cls.home_page = HomePage(page)
    request.cls.catalog_page = Catalog_Page(page)
    request.cls.cart_page = Cart_Page(page)
    request.cls.checkout_page = Checkout_Page(page)
    request.cls.product_page = ProductPage(page)
    request.cls.register_page = RegisterPage(page)
    request.cls.login_page = LoginPage(page)

    yield

    page.close()
    context.close()