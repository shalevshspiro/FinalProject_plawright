"""
Shared Allure-aware assertion helpers.

Wrapping a check with these instead of a bare `assert` gives every failure a
consistent, readable shape in the Allure report: a named step (the
reproduction context), the Expected result, and the Actual result attached as
separate entries - instead of a raw AssertionError with no context. Combined
with the screenshot-on-failure hook in conftest.py, a red test in Allure shows
exactly what was expected, what actually happened, and what the page looked
like at that moment.
"""

import allure


def assert_equal(actual, expected, description: str):
    """Assert actual == expected, attaching both values to the Allure report."""
    with allure.step(f"Verify: {description}"):
        allure.attach(str(expected), name="Expected result", attachment_type=allure.attachment_type.TEXT)
        allure.attach(str(actual), name="Actual result", attachment_type=allure.attachment_type.TEXT)
        assert actual == expected, (
            f"{description}\n  Expected: {expected!r}\n  Actual:   {actual!r}"
        )


def assert_true(actual, description: str):
    """Assert actual is True, attaching both values to the Allure report."""
    with allure.step(f"Verify: {description}"):
        allure.attach("True", name="Expected result", attachment_type=allure.attachment_type.TEXT)
        allure.attach(str(actual), name="Actual result", attachment_type=allure.attachment_type.TEXT)
        assert actual is True, (
            f"{description}\n  Expected: True\n  Actual:   {actual!r}"
        )


def assert_url_equals(actual_url: str, expected_url: str, description: str = None):
    """Compares two URLs ignoring a trailing slash (a handful of tests land on
    a URL that may or may not have one)."""
    assert_equal(
        actual_url.rstrip("/"),
        expected_url.rstrip("/"),
        description or f"Should navigate to {expected_url}",
    )


def assert_contains(actual, expected_substring: str, description: str):
    """Assert expected_substring in actual, attaching both values to the Allure report."""
    with allure.step(f"Verify: {description}"):
        allure.attach(expected_substring, name="Expected to contain", attachment_type=allure.attachment_type.TEXT)
        allure.attach(str(actual), name="Actual result", attachment_type=allure.attachment_type.TEXT)
        assert expected_substring in actual, (
            f"{description}\n  Expected to contain: {expected_substring!r}\n  Actual:   {actual!r}"
        )
