from playwright.sync_api import expect

from pages.basepage import BasePage


class ProductPage(BasePage):
    TITLE_TXT = ".mb-3.text-break"
    SEARCH_FIELD = "#criteria_search_value"
    ADD_TO_CART_BUTTON = "#add-to-cart-button"
    SELECT_DRESS_SIZE = "[data-option='dress_size']"
    ADD_QUANTITY_FIELD = "#sylius_shop_add_to_cart_cartItem_quantity"
    ADD_REVIEW_BUTTON = ".row.mb-2 a"
    TITLE_FIELD = "#sylius_shop_product_review_title"
    COMMENT_FIELD = "#sylius_shop_product_review_comment"
    EMAIL_FIELD = "#sylius_shop_product_review_author_email"
    ADD_NEW_REVIEW_BUTTON = ".mt-5 button"
    PRICE_TXT = ".fs-3"





    #assert
    ERROR_MESSAGE = ".invalid-feedback.d-block"


    def __init__(self, page):
        super().__init__(page)


    def select_size(self,value):
        self.select_by_value(self.SELECT_DRESS_SIZE,value)

    def add_quantity(self,quantity):
        self.fill_text(self.ADD_QUANTITY_FIELD,quantity)

    def add_to_cart(self):
        self.click(self.ADD_TO_CART_BUTTON)

    def add_review(self,title_review,comment_review,email_review):
        self.click(self.ADD_REVIEW_BUTTON)
        self.fill_text(self.TITLE_FIELD,title_review)
        self.fill_text(self.COMMENT_FIELD,comment_review)
        self.fill_text(self.EMAIL_FIELD,email_review)
        self.click(self.ADD_NEW_REVIEW_BUTTON)

    def get_price_text(self) -> str:
        return self.get_text(self.PRICE_TXT)

    def get_price(self):
        price_str = self.get_price_text()
        clean_price = price_str.replace("$", "").replace("€", "").strip()
        return float(clean_price)

    def wait_for_price_change(self, previous_price_text: str, timeout: int = 8000):
        """
        Wait for the live price display to actually update after a quantity
        change, instead of reading it immediately - the price re-render is
        async, so reading right away can return the stale pre-change value.
        """
        expect(self.page.locator(self.PRICE_TXT)).not_to_have_text(
            previous_price_text, timeout=timeout
        )

    #assert
    def success_product(self):
        return self.is_visible(self.ADD_TO_CART_BUTTON)

    def assert_quantity_value(self, expected_quantity):
        self.verify_input_value(self.ADD_QUANTITY_FIELD,str(expected_quantity))

    def assert_selected_size(self, expected_size_value):
        self.verify_input_value(self.SELECT_DRESS_SIZE, expected_size_value)

    def error_message_review(self):
        return self.is_visible(self.ERROR_MESSAGE)