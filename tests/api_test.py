import allure
import pytest
from playwright.sync_api import Playwright

from tests.assertions import assert_equal


class TestApiPro:
    """
    API test suite against the Sylius Shop API (v2).
    Self-contained: builds its own APIRequestContext, so it needs no browser,
    no conftest fixture and no Page Object Model - it talks straight to the API.

    Covers:
      1. A full API E2E checkout flow (login -> variant -> cart -> add item).
      2. A security check: the cart must reject a negative quantity.
    """

    BASE_URL = "https://v2.demo.sylius.com"
    API = "/api/v2/shop"

    VALID_EMAIL = "shop@example.com"
    VALID_PASSWORD = "sylius"

    LD_JSON = "application/ld+json"
    MERGE_PATCH = "application/merge-patch+json"

    # ------------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------------
    @staticmethod
    def _login(api):
        """Authenticates and returns a Bearer token string."""
        with allure.step("Authenticate and obtain a Bearer token"):
            res = api.post(
                f"{TestApiPro.API}/customers/token",
                headers={"Content-Type": "application/json", "Accept": "application/json"},
                data={"email": TestApiPro.VALID_EMAIL, "password": TestApiPro.VALID_PASSWORD},
            )
            assert res.ok, f"Login failed: {res.status} {res.text()}"
            token = res.json()["token"]
            print("  ✅ Authenticated - JWT received")
            return token

    @staticmethod
    def _first_variant(api, auth_headers):
        """Returns (variant_iri, price) for the first available product variant."""
        with allure.step("Fetch the first available product variant"):
            res = api.get(
                f"{TestApiPro.API}/product-variants?page=1&itemsPerPage=5",
                headers=auth_headers,
            )
            assert res.ok, f"Fetching variants failed: {res.status} {res.text()}"
            members = res.json()["hydra:member"]
            assert members, "No product variants returned by the API"
            variant = members[0]
            print(f"  ✅ Variant: {variant['@id']} (price={variant['price']})")
            return variant["@id"], variant["price"]

    @staticmethod
    def _create_cart(api, auth_headers):
        """Creates an empty order (cart) and returns its tokenValue."""
        with allure.step("Create a new empty cart (order)"):
            res = api.post(
                f"{TestApiPro.API}/orders",
                headers={**auth_headers, "Content-Type": TestApiPro.LD_JSON},
                data={},
            )
            assert res.ok, f"Cart creation failed: {res.status} {res.text()}"
            token_value = res.json()["tokenValue"]
            print(f"  ✅ Cart created - tokenValue={token_value}")
            return token_value

    # ------------------------------------------------------------------------
    # 1. API E2E - happy path
    # ------------------------------------------------------------------------
    @pytest.mark.api
    def test_api_e2e_add_item_to_cart(self, playwright: Playwright):
        """
        Full API E2E: authenticate, pick a real variant, open a cart,
        add the item, and verify the item is present with the correct quantity.

        Uses the `playwright` fixture provided by pytest-playwright (already
        running for the session) instead of opening a second, nested
        `sync_playwright()` context - doing the latter raises "Playwright Sync
        API inside the asyncio loop" once this test runs alongside UI tests
        that already have the plugin's event loop active (e.g. via the full
        regression suite).

        Steps to reproduce:
            1. Authenticate via POST /customers/token.
            2. Fetch the first available product variant.
            3. Create a new empty cart (order).
            4. POST 1 unit of that variant to the cart's items.

        Expected result:
            The cart contains exactly 1 item, with quantity == 1.
        """
        print("\n🌐 API E2E - login -> variant -> cart -> add item")

        api = playwright.request.new_context(base_url=TestApiPro.BASE_URL)
        try:
            token = self._login(api)
            auth = {"Authorization": f"Bearer {token}", "Accept": self.LD_JSON}

            variant_iri, _ = self._first_variant(api, auth)
            cart_token = self._create_cart(api, auth)

            with allure.step("Add 1 unit of the variant to the cart"):
                # Note: We use quantity=1 because Sylius is a public demo environment.
                # Other test scripts frequently deplete the virtual inventory, causing
                # requests for quantity > 1 to silently default back to 1.
                # Testing for quantity=1 ensures test stability (no Test Data Pollution).
                res = api.post(
                    f"{self.API}/orders/{cart_token}/items",
                    headers={**auth, "Content-Type": self.LD_JSON},
                    data={"productVariant": variant_iri, "quantity": 1},
                )
                assert res.ok, f"Add-to-cart failed: {res.status} {res.text()}"

                body = res.json()
                items = body.get("items", [])
                assert items, "Cart is empty after adding an item"

            assert_equal(
                items[0]["quantity"],
                1,
                "Cart item quantity should equal the quantity requested (1)",
            )

            print("  ✅ Item present in cart with correct quantity")
            print("✅ API E2E passed")
        finally:
            api.dispose()

    # ------------------------------------------------------------------------
    # 2. SECURITY - negative quantity must be rejected
    # ------------------------------------------------------------------------
    @pytest.mark.api
    @pytest.mark.security
    def test_api_negative_quantity_rejected(self, playwright: Playwright):
        """
        OWASP API - improper input validation.
        The cart must never accept a negative quantity. A negative quantity that
        is accepted can drive a negative line total (store owes the customer).

        Invariant asserted: the API rejects the request (4xx) OR does not persist
        a negative quantity. If a negative quantity is accepted, the test fails
        and the failure message documents the vulnerability.

        Uses the shared `playwright` fixture - see test_api_e2e_add_item_to_cart
        for why a nested `sync_playwright()` context is avoided here.

        Steps to reproduce:
            1. Authenticate, fetch a variant, and create a new cart (as above).
            2. POST a quantity of -5 for that variant to the cart's items.

        Expected result:
            The API either rejects the request (4xx) or, if it responds 2xx,
            does not persist a negative quantity (stored quantity is None or >= 0).
        """
        print("\n🔒 API security - negative quantity injection into cart")

        api = playwright.request.new_context(base_url=TestApiPro.BASE_URL)
        try:
            token = self._login(api)
            auth = {"Authorization": f"Bearer {token}", "Accept": self.LD_JSON}

            variant_iri, _ = self._first_variant(api, auth)
            cart_token = self._create_cart(api, auth)

            with allure.step("Attack: try to add a negative quantity (-5) to the cart"):
                res = api.post(
                    f"{self.API}/orders/{cart_token}/items",
                    headers={**auth, "Content-Type": self.LD_JSON},
                    data={"productVariant": variant_iri, "quantity": -5},
                )
                print(f"  Response status for quantity=-5: {res.status}")

            with allure.step("Guard: confirm the request actually reached validation"):
                # A 405/404 would mean the request never reached validation - that
                # must not be mistaken for a security control. Flag it explicitly.
                assert res.status not in (404, 405), (
                    f"Request did not reach validation (status {res.status}) - "
                    "fix the endpoint/method before trusting this result"
                )

            # Case A - API rejected it with a validation error (secure behaviour)
            if res.status in (400, 422):
                print("  ✅ API rejected the negative quantity (validation works)")
                return
            if not res.ok:
                print(f"  ✅ API rejected the request (status {res.status})")
                return

            # Case B - API returned 2xx: inspect whether it actually persisted
            with allure.step("Inspect whether the negative quantity was actually persisted"):
                body = res.json()
                items = body.get("items", [])
                stored_qty = items[0]["quantity"] if items else None
                print(f"  Stored quantity: {stored_qty}")

            allure.attach("None, or >= 0", name="Expected result", attachment_type=allure.attachment_type.TEXT)
            allure.attach(str(stored_qty), name="Actual result", attachment_type=allure.attachment_type.TEXT)
            assert stored_qty is None or stored_qty >= 0, (
                "🚨 VULNERABILITY: cart accepted and stored a negative quantity "
                f"({stored_qty}) - can produce a negative order total"
            )

            print("  ✅ Negative quantity not persisted")
        finally:
            api.dispose()
