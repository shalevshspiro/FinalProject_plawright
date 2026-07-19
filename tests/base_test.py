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
        """
        Known application defect: the shipping-methods step intermittently returns
        'No shipping methods available'. It reproduces regardless of country/address,
        so this looks like real backend flakiness (e.g. a stuck cache or a bad node
        behind a load balancer) rather than a data/config problem. A same-page reload
        wasn't enough to dodge it in practice, so each retry:
          1. waits a few seconds to give the backend a chance to recover, then
          2. navigates back to the site's home page (the checkout page's header
             doesn't carry the full nav menu, so re-entering the flow directly
             from there breaks goto_dresses()), then
          3. re-enters checkout from scratch with a brand-new cart/session,
        instead of retrying the exact same stuck page/cart. If the defect still
        persists after all attempts, raise a clear diagnostic error instead of a
        bare Playwright TimeoutError.
        """
        address = address or CHECKOUT_ADDRESS

        for attempt in range(1, max_attempts + 1):
            if self.checkout_page.has_shipping_methods(timeout=8000):
                self.checkout_page.choose_dhl()
                return

            print(
                f"⚠️  KNOWN SITE BUG - no shipping methods available on attempt "
                f"{attempt}/{max_attempts}. Waiting {backoff_seconds}s and retrying "
                "with a fresh cart/session..."
            )
            time.sleep(backoff_seconds)

            if attempt < max_attempts:
                self.page.goto(BASE_URL)
                self.add_product_to_cart(product_name)
                self.cart_page.checkout()
                self.checkout_page.fill_info_checkout(**address)

        raise AssertionError(
            "🚨 Known site defect reproduced: 'No shipping methods available' persisted "
            f"after {max_attempts} attempts, each with a fresh cart/session and a "
            f"{backoff_seconds}s backoff. This is an application-side bug (intermittent "
            "shipping-method availability at checkout), not a broken locator or "
            "test-data issue - see bug report."
        )
