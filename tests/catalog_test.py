import allure
import pytest
from data.base_data import DEFAULT_PRODUCT_NAME
from tests.assertions import assert_contains, assert_equal, assert_true
from tests.base_test import BaseTest


@pytest.mark.usefixtures("setup_function")
class TestCatalog(BaseTest):

    @pytest.mark.regression
    def test_search_by_name(self):
        """
        Steps to reproduce:
            1. Go to the Dresses category.
            2. Type the product name in the search field and press Enter.

        Expected result:
            The product appears in the search results.
        """
        with allure.step(f"Go to Dresses, search for '{DEFAULT_PRODUCT_NAME}' via Enter"):
            self.home_page.goto_dresses()
            self.catalog_page.search_by_enter(DEFAULT_PRODUCT_NAME)

        assert_true(
            self.catalog_page.search_success(DEFAULT_PRODUCT_NAME),
            f"'{DEFAULT_PRODUCT_NAME}' should appear in the search results",
        )

    @pytest.mark.regression
    def test_search_by_enter(self):
        """
        Steps to reproduce:
            1. Go to the Dresses category.
            2. Type the product name in the search field and click the search button.

        Expected result:
            The product appears in the search results.
        """
        with allure.step(f"Go to Dresses, search for '{DEFAULT_PRODUCT_NAME}' via the search button"):
            self.home_page.goto_dresses()
            self.catalog_page.search_by_button(DEFAULT_PRODUCT_NAME)

        assert_true(
            self.catalog_page.search_success(DEFAULT_PRODUCT_NAME),
            f"'{DEFAULT_PRODUCT_NAME}' should appear in the search results",
        )

    @pytest.mark.regression
    def test_search_error(self):
        """
        Steps to reproduce:
            1. Go to the Dresses category.
            2. Search for a nonsense term that matches no product.

        Expected result:
            A "no results found" message is shown.
        """
        with allure.step("Go to Dresses, search for a nonsense term"):
            self.home_page.goto_dresses()
            self.catalog_page.search_by_button("assdfsx")

        assert_true(
            self.catalog_page.search_error(),
            "A 'no results found' message should be shown for a nonsense search term",
        )

    @pytest.mark.regression
    def test_search_03(self):
        """
        Steps to reproduce:
            1. Go to the Dresses category.
            2. Search using a partial, lowercase product name ("sunshine").

        Expected result:
            The full product name appears in the search results.
        """
        with allure.step("Go to Dresses, search using a partial/lowercase product name"):
            self.home_page.goto_dresses()
            self.catalog_page.search_by_button("sunshine")

        assert_true(
            self.catalog_page.search_success(DEFAULT_PRODUCT_NAME),
            f"'{DEFAULT_PRODUCT_NAME}' should appear when searching a partial term",
        )

    @pytest.mark.regression
    def test_item_num(self):
        """
        Steps to reproduce:
            1. Go to the Dresses category.
            2. Set the results-per-page limit to 18.

        Expected result:
            18 product cards are displayed.

        KNOWN ENVIRONMENT ISSUE (not fixed here, left for a product decision):
        this asserts an exact count (18) of the "Dresses" category on a public,
        shared demo shop. If another script/user enables, disables, or adds a
        product in that category, the count shifts (observed 17 vs 18) with
        zero code change on our side - this is catalog-level Test Data
        Pollution, not a locator/timing bug. Options if this proves unstable
        long-term: assert a tolerant range (e.g. >= 1) instead of an exact
        count, or seed/verify the catalog state before asserting.
        """
        with allure.step("Go to Dresses and set the results limit to 18 per page"):
            self.home_page.goto_dresses()
            self.catalog_page.show_results()

        assert_equal(
            self.catalog_page.count_cards(),
            18,
            "Dresses category should show 18 product cards at limit=18",
        )

    @pytest.mark.regression
    def test_next_page(self):
        """
        Steps to reproduce:
            1. Go to the Dresses category.
            2. Click the "next page" control.

        Expected result:
            The URL contains "page=2".
        """
        with allure.step("Go to Dresses and click 'next page'"):
            self.home_page.goto_dresses()
            self.catalog_page.go_next()

        current_url = self.catalog_page.get_current_url()
        assert_contains(
            current_url,
            "https://v2.demo.sylius.com/en_US/taxons/category/dresses?page=2",
            "URL should contain the page=2 query string after clicking next",
        )

    @pytest.mark.smoke
    def test_choose_product(self):
        """
        Steps to reproduce:
            1. Go to the Dresses category.
            2. Click on the product card for the target product.

        Expected result:
            The product page loads (Add to Cart button visible).
        """
        with allure.step(f"Go to Dresses and click on '{DEFAULT_PRODUCT_NAME}'"):
            self.home_page.goto_dresses()
            self.catalog_page.click_on_product(DEFAULT_PRODUCT_NAME)

        assert_true(
            self.product_page.success_product(),
            "Product page should load (Add to Cart button visible) after clicking the product",
        )

    @pytest.mark.regression
    def test_sort_by_abcd(self):
        """
        Steps to reproduce:
            1. Go to the Dresses category.
            2. Apply the "from A to Z" sort option.

        Expected result:
            The displayed product names are sorted alphabetically (A-Z).
        """
        with allure.step("Go to Dresses and sort products A to Z"):
            self.home_page.goto_dresses()
            self.catalog_page.sort_results()

        names_from_page = self.catalog_page.get_title_text()
        assert len(names_from_page) > 0, "The product list is empty, cannot verify sorting!"
        expected_names = sorted(names_from_page, key=str.lower)
        assert_equal(
            names_from_page,
            expected_names,
            "Product names should be sorted alphabetically (A to Z)",
        )
