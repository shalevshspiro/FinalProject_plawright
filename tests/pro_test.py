import time
import statistics
import pytest
import random
import string

import allure

from data.base_data import (
    CHECKOUT_ADDRESS,
    DEFAULT_PRODUCT_NAME,
    VALID_USER_EMAIL,
    VALID_USER_PASSWORD,
    XSS_PAYLOAD,
)
from tests.assertions import assert_equal, assert_true
from tests.base_test import BaseTest


@pytest.mark.usefixtures("setup_function")
class TestSecurityPro(BaseTest):
    """
    Advanced QA suite: security & performance checks against the Sylius demo shop.
    Each test is self-contained, deterministic, and asserts on a concrete condition.
    """

    # --- Shared test data ---------------------------------------------------
    BASE_URL = "https://v2.demo.sylius.com/en_US/"
    PRODUCT_NAME = DEFAULT_PRODUCT_NAME
    VALID_USER = VALID_USER_EMAIL
    VALID_PASSWORD = VALID_USER_PASSWORD

    REVIEW_EMAIL = "tester@example.com"

    STRESS_ITERATIONS = 25
    MAX_RESPONSE_TIME = 10        # seconds - hard ceiling per request
    NETWORK_IDLE_TIMEOUT = 5000   # ms

    # ------------------------------------------------------------------------
    # 1. SECURITY - Cross-Site Scripting (XSS)
    # ------------------------------------------------------------------------
    @pytest.mark.security
    def test_xss_injection_checkout_address(self):
        """
        OWASP A03:2021 - Injection (XSS).
        Injects a <script> payload into checkout address fields (first name, city),
        drives the flow to the order-summary page where those values are reflected,
        and verifies the payload is escaped instead of rendered as live HTML.

        Note: the address fields are the reflection point - the summary page renders
        the entered name/city back as text, which is exactly where stored XSS surfaces.

        Steps to reproduce:
            1. Add a product to the cart and proceed to checkout.
            2. Fill in the address form with a <script>alert('XSS')</script>
               payload in the first_name and city fields.
            3. Choose a shipping method and pay by cash on delivery.
            4. Reach the order-summary page.

        Expected result:
            The raw <script> tag does NOT appear unescaped anywhere in the
            summary page's HTML (the payload is rendered as harmless text).
        """
        print("\n🔒 XSS - injecting script payload into checkout address")
        xss_payload = XSS_PAYLOAD

        with allure.step("Add a product to cart and open checkout"):
            self.add_product_to_cart(self.PRODUCT_NAME)
            self.cart_page.checkout()

        with allure.step("Inject a <script> XSS payload into first_name/city fields"):
            xss_address = {**CHECKOUT_ADDRESS, "first_name": xss_payload, "city": xss_payload}
            self.checkout_page.fill_info_checkout(**xss_address)
            # Pass the payload-injected address explicitly so a retry (fresh cart/session)
            # re-submits the same XSS payload instead of falling back to the plain default.
            self.choose_shipping_with_retry(product_name=self.PRODUCT_NAME, address=xss_address)
            self.checkout_page.choose_cash()
            self.checkout_page.wait_for_visible(self.checkout_page.SUCCESS_CASH)

        with allure.step("Guard: confirm the flow actually reached the order summary"):
            assert self.checkout_page.success_cash(), (
                "Did not reach checkout summary - XSS reflection could not be evaluated\n"
                "  Expected: checkout summary page reached\n"
                "  Actual:   flow did not complete"
            )

        with allure.step("Verify the raw <script> tag is NOT present unescaped in the page"):
            page_content = self.page.content()
            allure.attach(
                "Payload should be HTML-escaped, not present as a raw <script> tag",
                name="Expected result", attachment_type=allure.attachment_type.TEXT,
            )
            allure.attach(
                "present" if xss_payload in page_content else "not present (escaped)",
                name="Actual result", attachment_type=allure.attachment_type.TEXT,
            )
            assert xss_payload not in page_content, (
                "🚨 XSS VULNERABILITY: unescaped <script> payload reflected on checkout summary"
            )

        print("✅ XSS blocked - payload was escaped on the summary page")

    @pytest.mark.performance
    def test_sequential_stress_navigation_response_times(self):
        """
        Performance / stress test.
        Repeatedly navigates product page <-> home page, measures each round-trip,
        and asserts the slowest round-trip stays within an acceptable ceiling.
        Uses direct page.goto() so the loop is stable and independent of menu state.

        Steps to reproduce:
            1. Open the default product's page and capture its URL.
            2. Loop 25x: navigate home -> product, timing each full round-trip.

        Expected result:
            All 25 round-trips complete with no failures, and the slowest
            round-trip stays under 10 seconds.
        """
        print(f"\n⚡ Stress - {self.STRESS_ITERATIONS} navigation round-trips")

        with allure.step("Reach the product page once and capture both URLs"):
            self.open_product(self.PRODUCT_NAME)
            product_url = self.page.url
            home_url = self.BASE_URL
            print(f"  Product URL: {product_url}")

        response_times = []
        failed_requests = 0

        with allure.step(f"Loop {self.STRESS_ITERATIONS}x: home -> product, timing each round-trip"):
            for i in range(self.STRESS_ITERATIONS):
                try:
                    start = time.time()

                    self.page.goto(home_url)
                    self.page.wait_for_load_state("networkidle", timeout=self.NETWORK_IDLE_TIMEOUT)

                    self.page.goto(product_url)
                    self.page.wait_for_load_state("networkidle", timeout=self.NETWORK_IDLE_TIMEOUT)

                    elapsed = time.time() - start
                    response_times.append(elapsed)
                    print(f"  {i + 1:>2}/{self.STRESS_ITERATIONS} - {elapsed:.2f}s ✅")

                except Exception as error:
                    failed_requests += 1
                    print(f"  {i + 1:>2}/{self.STRESS_ITERATIONS} - ❌ {error}")

        self._print_stress_report(response_times, failed_requests)
        self._attach_stress_report(response_times, failed_requests)

        with allure.step("Verify no round-trips failed and the slowest stayed within budget"):
            assert_equal(failed_requests, 0, "No round-trip should fail under sequential load")
            assert max(response_times) < self.MAX_RESPONSE_TIME, (
                f"Slowest round-trip should stay under {self.MAX_RESPONSE_TIME}s\n"
                f"  Expected: < {self.MAX_RESPONSE_TIME}s\n"
                f"  Actual:   {max(response_times):.2f}s"
            )

        print("✅ Stress passed - all round-trips within budget")

    @staticmethod
    def _print_stress_report(response_times, failed_requests):
        """Prints a compact performance summary for the stress run."""
        if not response_times:
            print("\n📊 No successful requests to report")
            return

        stdev = statistics.stdev(response_times) if len(response_times) > 1 else 0.0
        print("\n📊 Stress report")
        print(f"  ✅ Successful : {len(response_times)}")
        print(f"  ❌ Failed     : {failed_requests}")
        print(f"  ⏱️  Avg        : {statistics.mean(response_times):.2f}s")
        print(f"  ⏱️  Min        : {min(response_times):.2f}s")
        print(f"  ⏱️  Max        : {max(response_times):.2f}s")
        print(f"  📈 Std dev    : {stdev:.2f}s")

    @staticmethod
    def _attach_stress_report(response_times, failed_requests):
        """Attaches the same performance summary to the Allure report."""
        if not response_times:
            allure.attach("No successful requests to report", name="Stress report",
                           attachment_type=allure.attachment_type.TEXT)
            return

        stdev = statistics.stdev(response_times) if len(response_times) > 1 else 0.0
        report = (
            f"Successful : {len(response_times)}\n"
            f"Failed     : {failed_requests}\n"
            f"Avg        : {statistics.mean(response_times):.2f}s\n"
            f"Min        : {min(response_times):.2f}s\n"
            f"Max        : {max(response_times):.2f}s\n"
            f"Std dev    : {stdev:.2f}s"
        )
        allure.attach(report, name="Stress report", attachment_type=allure.attachment_type.TEXT)

    # ------------------------------------------------------------------------
    # 3. SECURITY - Broken Access Control
    # ------------------------------------------------------------------------
    @pytest.mark.security
    def test_broken_access_control_exposed_identifiers(self):
        """
        OWASP A01:2021 - Broken Access Control.
        Logs in as a valid user and verifies the account page does not leak
        raw user/customer identifiers that could enable horizontal access.

        Steps to reproduce:
            1. Log in with valid demo-shop credentials.
            2. Inspect the rendered page HTML for identifier-leak patterns
               (user_id=, account_id=, customer_id=, /user/, /customer/).

        Expected result:
            None of the leak indicators are present in the page source.
        """
        print("\n🔒 Access control - scanning account page for exposed identifiers")

        with allure.step("Authenticate as a valid user"):
            self.home_page.goto_login()
            self.login_page.login(self.VALID_USER, self.VALID_PASSWORD)
            print(f"  URL after login: {self.page.url}")
            assert self.login_page.login_success(), "Login failed - cannot evaluate access control"

        with allure.step("Scan the rendered page for identifier leakage"):
            page_source = self.page.content().lower()
            leak_indicators = [
                "user_id=",
                "account_id=",
                "customer_id=",
                "/user/",
                "/customer/",
            ]
            exposed = [token for token in leak_indicators if token in page_source]

        allure.attach("No raw identifiers exposed", name="Expected result",
                       attachment_type=allure.attachment_type.TEXT)
        allure.attach(str(exposed) if exposed else "none found", name="Actual result",
                       attachment_type=allure.attachment_type.TEXT)
        assert not exposed, (
            f"🚨 BROKEN ACCESS CONTROL: exposed identifier(s) found -> {exposed}"
        )

        print("✅ Access control OK - no raw identifiers exposed")

    @pytest.mark.security
    def test_brute_force_login_probe(self):
        """
        OWASP A07:2021 - Identification and Authentication Failures.
        Simulates an attacker brute-forcing a known account: same real email,
        N different random passwords.

        This is a documented security PROBE, not a pass/fail gate:
          - It ASSERTS the invariant that must always hold: wrong credentials never
            grant access. A random password succeeding would be a critical auth flaw.
          - It OBSERVES and reports whether any mitigation (lockout / rate-limit /
            CAPTCHA) engaged. Absence of lockout is reported as a deployment finding,
            not asserted - such protection normally lives in the infrastructure layer
            (WAF / reverse proxy), outside this application instance.

        Steps to reproduce:
            1. Open the login page.
            2. Attempt to log in 20 times with the same real email and a
               different random 12-character password each time.

        Expected result:
            None of the 20 random passwords grant access. (Whether the site
            engages a lockout/throttle after N attempts is observed and
            reported, but not asserted - see note above.)
        """
        print("\n🛡️  Brute-force probe - attacker simulation on a known account")

        email = self.VALID_USER  # real, valid account
        attempts = 20  # attacker tries N random passwords

        with allure.step("Open the login page"):
            self.home_page.goto_login()

        breaches = 0
        rejected = 0
        behaviour_changed_at = None  # first attempt where the site stopped behaving normally

        with allure.step(f"Attempt {attempts} logins with random passwords for a known account"):
            for i in range(attempts):
                random_password = "".join(
                    random.choice(string.ascii_letters + string.digits) for _ in range(12)
                )

                self.login_page.login(email, random_password)
                self.page.wait_for_load_state("load")

                # Did a random password get us in? That would be broken authentication.
                if self.login_page.login_success():
                    breaches += 1
                    print(f"  {i + 1:>2}/{attempts} - 🚨 ACCESS GRANTED with a random password!")
                    break

                rejected += 1

                # Observe: still a normal login error, or did behaviour change (lockout/throttle)?
                if self.login_page.error_login():
                    print(f"  {i + 1:>2}/{attempts} - rejected (standard login error)")
                else:
                    if behaviour_changed_at is None:
                        behaviour_changed_at = i + 1
                    print(f"  {i + 1:>2}/{attempts} - rejected (no standard error - possible mitigation)")

        # --- Finding report ---
        finding = (
            f"Attempts        : {attempts}\n"
            f"Rejected        : {rejected}\n"
        )
        if behaviour_changed_at:
            finding += f"Behaviour change: attempt #{behaviour_changed_at} (possible lockout / throttle)\n"
        else:
            finding += (
                "Account lockout : NOT observed\n"
                "Note: brute-force mitigation (lockout / rate-limit / CAPTCHA) is normally\n"
                "      enforced at the infrastructure layer (WAF / reverse proxy), outside\n"
                "      this application instance - a deployment finding, not an app bug.\n"
            )
        print("\n📋 Brute-force finding")
        print(finding)
        allure.attach(finding, name="Brute-force finding", attachment_type=allure.attachment_type.TEXT)

        # Deterministic invariant: brute force must NEVER grant access.
        assert_equal(breaches, 0, "No random password should ever grant access (broken authentication)")

        print("✅ Probe complete - no random password granted access")
