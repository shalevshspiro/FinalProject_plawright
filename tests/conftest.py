from __future__ import annotations

import os
import shutil
import subprocess

import allure
import pytest

from data.base_data import BASE_URL
from pages.cart_page import CartPage
from pages.catalog_page import CatalogPage
from pages.checkout_page import CheckoutPage
from pages.home_page import HomePage
from pages.product_page import ProductPage
from pages.login_page import LoginPage
from pages.register_page import RegisterPage


@pytest.fixture(scope="function")
def setup_function(request, browser):
    context = browser.new_context(
        viewport={'width': 1920, 'height': 1080},
        user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
    )
    page = context.new_page()

    page.set_default_timeout(15000)

    page.goto(BASE_URL)

    request.cls.page = page
    request.cls.home_page = HomePage(page)
    request.cls.catalog_page = CatalogPage(page)
    request.cls.cart_page = CartPage(page)
    request.cls.checkout_page = CheckoutPage(page)
    request.cls.product_page = ProductPage(page)
    request.cls.register_page = RegisterPage(page)
    request.cls.login_page = LoginPage(page)

    yield

    page.close()
    context.close()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    On a failed test, attach a full-page screenshot to the Allure report.
    Runs for every test (UI or API), but only actually captures anything for
    UI tests that have a `page` (API tests like TestApiPro have none, so this
    is skipped for them). The screenshot naturally shows the last element
    BasePage highlighted (click/fill/is_visible/etc. all highlight their
    target before acting), so the bug and the element involved are visible in
    the same image.
    """
    outcome = yield
    report = outcome.get_result()

    if report.when != "call" or not report.failed:
        return

    page = getattr(item.instance, "page", None)
    if page is None:
        return

    try:
        screenshot_bytes = page.screenshot(full_page=True)
        allure.attach(
            screenshot_bytes,
            name=f"failure-{item.name}",
            attachment_type=allure.attachment_type.PNG,
        )
    except Exception as error:
        print(f"⚠️  Could not capture failure screenshot: {error}")


def _find_allure_binary() -> str | None:
    """
    Resolve the `allure` executable path. shutil.which() alone isn't enough
    when pytest is launched from an IDE (PyCharm's Run button, for example) -
    GUI-launched processes often don't inherit the PATH additions your shell
    profile (.zshrc/.bash_profile) sets up for Homebrew, so `allure` can be
    installed and working fine in a terminal yet still be invisible here.
    Fall back to the common Homebrew install locations before giving up.
    """
    found = shutil.which("allure")
    if found:
        return found

    for candidate in ("/opt/homebrew/bin/allure", "/usr/local/bin/allure"):
        if os.path.exists(candidate):
            return candidate

    return None


def pytest_sessionfinish(session, exitstatus):
    """
    Automatically open the Allure report once the whole run finishes.
    Requires the Allure commandline tool installed locally (macOS:
    `brew install allure`) - this only renders/serves the results already
    written to allure-results/ (see pytest.ini's --alluredir); it does not
    install Allure itself.
    """
    allure_bin = _find_allure_binary()

    if allure_bin is None:
        print(
            "\n⚠️  Allure CLI not found (checked PATH, /opt/homebrew/bin, "
            "/usr/local/bin) - skipping auto-open report. If you already ran "
            "`brew install allure` but still see this, you're probably running "
            "pytest from an IDE run configuration that doesn't inherit your "
            "shell's PATH - try running `pytest` from an actual terminal "
            "instead, or add allure's install directory to the IDE's run "
            "configuration environment."
        )
        return

    print(f"\n📊 Opening Allure report (using {allure_bin})...")
    try:
        subprocess.Popen(
            [allure_bin, "serve", "allure-results"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            # Detach from pytest's process group. Without this, an IDE that
            # tears down the whole process tree when the test run "finishes"
            # can kill the report server before it even gets to open the
            # browser - it would look like nothing happened.
            start_new_session=True,
        )
    except Exception as error:
        print(f"⚠️  Failed to launch Allure report: {error}")
