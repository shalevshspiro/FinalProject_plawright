import time

from data.base_data import BASE_URL, CHECKOUT_ADDRESS, DEFAULT_PRODUCT_NAME
from pages.cart_page import CartPage
from pages.catalog_page import CatalogPage
from pages.checkout_page import CheckoutPage
from pages.home_page import HomePage
from pages.product_page import ProductPage
from pages.login_page import LoginPage
from pages.register_page import RegisterPage


class BaseTest:
    catalog_page: CatalogPage
    home_page: HomePage
    cart_page: CartPage
    checkout_page: CheckoutPage
    product_page: ProductPage
    register_page: RegisterPage
    login_page: LoginPage

    def open_product(self, product_name: str = DEFAULT_PRODUCT_NAME):
        """Navigate to the dresses catalog and open a given product's page."""
        self.home_page.goto_dresses()
        self.catalog_page.click_on_product(product_name)

    def add_product_to_cart(self, product_name: str = DEFAULT_PRODUCT_NAME):
        """Open a product and add it to the cart, waiting for the cart
        confirmation instead of a fixed sleep."""
        self.open_product(product_name)
        self.product_page.add_to_cart()
        self.cart_page.wait_for_visible(self.cart_page.SUCCESS_CART_PAGE)

    def choose_shipping_with_retry(
        self,
        product_name: str = DEFAULT_PRODUCT_NAME,
        address: dict = None,
        max_attempts: int = 3,
        backoff_seconds: float = 3.0,
    ):
        """Retry the confirmed unavailable state without changing the cart."""
        if max_attempts < 1:
            raise ValueError("max_attempts must be at least 1")
        for attempt in range(1, max_attempts + 1):
            if self.checkout_page.has_shipping_methods(timeout=8000):
                self.checkout_page.choose_dhl()
                return
            assert self.checkout_page.shipping_unavailable_message_visible(), (
                "Shipping controls missing without the expected unavailable message"
            )
            if attempt < max_attempts:
                time.sleep(backoff_seconds)
                self.checkout_page.reload_shipping_step()
        raise AssertionError(
            f"No shipping methods available after {max_attempts} attempts on the same cart"
        )
