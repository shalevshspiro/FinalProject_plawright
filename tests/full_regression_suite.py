"""
Aggregates every test class in the project into a single suite class, so the
entire regression pack can be run and reported as one unit without touching
any of the individual test files:

    pytest tests/full_regression_suite.py

Deliberately named without a test_*/​*_test filename pattern, so pytest's
normal directory-wide discovery (plain `pytest` with no args) does NOT pick
this file up on its own - otherwise every test would run twice: once under
its original file, and again here. Point pytest at this file explicitly
(by path, as above) when you want the combined run/report.
"""

import time

import pytest

# Import the *modules*, not the classes directly. Binding a class name (e.g.
# `from tests.home_test import TestHome`) at this module's top level makes
# pytest re-collect it here as its own standalone test class - doubling every
# test. Keeping the classes behind a module attribute (module.TestHome)
# avoids that: only TestFullSuite itself gets collected from this file.
from tests import (
    home_test,
    catalog_test,
    product_test,
    cart_test,
    checkout_test,
    e_to_e_test,
    login_register_test,
    pro_test,
    api_test,
)


# Tracks which module the previously-run test came from, across the whole
# session, so we can detect when execution crosses from one original test
# class into the next (e.g. TestHome -> TestCatalog).
_last_test_module = {"name": None}


@pytest.fixture(autouse=True)
def _pause_between_test_groups(request):
    """
    5s pause whenever this run moves from one original test class to another.
    Detected via the test function's defining module - inherited methods keep
    their original __module__ (e.g. "tests.home_test"), even though they're
    collected here under TestFullSuite. Gives the demo site a breather between
    groups instead of hammering it continuously across ~37 back-to-back tests,
    only applies to this aggregated run - the individual test files are
    unaffected when run on their own.
    """
    current_module = request.function.__module__
    previous_module = _last_test_module["name"]

    if previous_module is not None and previous_module != current_module:
        print(f"\n⏸  Pausing 5s between test groups ({previous_module} -> {current_module})...")
        time.sleep(5)

    yield

    _last_test_module["name"] = current_module


@pytest.mark.usefixtures("setup_function")
class TestFullSuite(
    home_test.TestHome,
    catalog_test.TestCatalog,
    product_test.TestProduct,
    cart_test.TestCart,
    checkout_test.TestCheckout,
    e_to_e_test.TestE2E,
    login_register_test.TestRegister,
    pro_test.TestSecurityPro,
    # api_test.TestApiPro,
):
    """
    Every test method from every class above, collected under one class via
    multiple inheritance. No new test logic lives here - it's purely an
    aggregation point.
    """
    pass
