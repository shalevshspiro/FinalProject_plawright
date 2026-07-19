# Sylius Shop - Test Automation

End-to-end, API, security, and performance test suite for [Sylius](https://sylius.com)'s public demo shop (`v2.demo.sylius.com`), built with Python, Playwright, and pytest. Reports are generated with Allure.

Sylius is an open-source e-commerce platform. The demo instance is public and shared - anyone can run traffic against it at any time. That constraint shaped a few of the decisions below, and it's called out explicitly where it matters instead of being papered over.

## Stack

- Python 3.9
- pytest + pytest-playwright
- Playwright (sync API)
- allure-pytest for reporting

## Project structure

```
pages/            Page Object Model - one class per page, all inheriting from BasePage
  basepage.py      shared element helpers (click, fill, wait, highlight-on-action)
  home_page.py, login_page.py, register_page.py, catalog_page.py,
  product_page.py, cart_page.py, checkout_page.py

tests/
  base_test.py            shared fixtures/helpers for UI test classes (add_product_to_cart,
                           choose_shipping_with_retry, etc.)
  assertions.py            assert_true / assert_equal / assert_contains / assert_url_equals -
                           wrap a check in an Allure step and attach Expected vs Actual
  conftest.py              browser/page fixtures, screenshot-on-failure hook, Allure auto-open
  full_regression_suite.py  aggregates every test class into one, for a single combined run/report

  home_test.py, catalog_test.py, product_test.py, cart_test.py,
  checkout_test.py, e_to_e_test.py, login_register_test.py    functional UI coverage
  pro_test.py                                                  security + performance checks
  api_test.py                                                  API-level tests (no browser)

data/base_data.py   centralized test data (URLs, credentials, default address, payloads)
pytest.ini          markers, addopts (headed + slowmo by default, Allure results dir)
```

## Running it

```
pip install -r requirements.txt
playwright install chromium
pytest
```

By default this runs headed with slowmo (see `pytest.ini`) so you can watch it work. For a headless/CI run, drop `--headed --slowmo 500` from `addopts` or override on the command line.

To run everything as a single aggregated suite/report:

```
pytest tests/full_regression_suite.py
```

(This file is deliberately named so plain `pytest` doesn't also pick it up - otherwise every test would run twice, once under its own file and once again here.)

### Reports

Every run writes to `allure-results/`. If the Allure commandline tool is installed (`brew install allure` on macOS), a report opens automatically once the run finishes - see `pytest_sessionfinish` in `conftest.py`. Failed tests get a full-page screenshot attached automatically, and the last element the test interacted with or checked is highlighted in it, so you can usually tell what broke without re-running anything.

Test markers (`pytest -m smoke`, `-m security`, etc.):

- `smoke` - fast critical-path checks
- `regression` - broader functional coverage
- `e2e` - full purchase journeys, guest and logged-in
- `api` - hits the Sylius API directly, no browser
- `security` - XSS, broken access control, brute-force login, negative-quantity injection
- `performance` - navigation stress/response-time test

## Known issues in the environment (not bugs in this suite)

A few things surfaced while building this that are worth flagging up front, because a green or red run doesn't always mean what it looks like on a shared public demo:

- **Intermittent "no shipping methods available" at checkout.** Reproduces with the exact same product/address, sometimes. `choose_shipping_with_retry()` in `base_test.py` retries a few times with a fresh cart and a backoff, and raises a clear message if it doesn't clear up - it doesn't hide the underlying defect, it just stops it from being reported as a random `TimeoutError`.
- **Shared demo account cart state.** `shop@example.com` is a public login used by anyone testing against this instance, so its cart can already contain items from a previous run. `catalog_page.click_on_product()` explicitly excludes the mini-cart drawer from its locator for this reason.
- **Catalog counts can drift.** `test_item_num` expects 18 products in a category; if someone else's script adds/disables a product in the meantime, that number moves with zero code change on this end. Documented in the test itself rather than loosened, since a tolerant assertion would hide a real regression too.
- **API tests use quantity=1, not a higher number.** Same root cause - shared inventory can run low enough that a request for e.g. quantity=2 silently gets clamped to what's left. Documented inline in `api_test.py`.

## A couple of specific design choices

- `BasePage` highlights the target element (Playwright's built-in `.highlight()`) before every click, fill, and visibility check - not just for headed debugging, but so failure screenshots show exactly what the test was looking at.
- `TestApiPro` takes the `playwright` fixture instead of opening its own `sync_playwright()` context. Doing the latter works fine in isolation but breaks with "Sync API inside the asyncio loop" once API tests run in the same process as UI tests (e.g. via the full suite) - this only became visible after wiring the aggregator together.
