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
    ADD_NEW_REVIEW_BUTTON = "[fdprocessedid='58cqcp']"





    #assert
    ERROR_MESSAGE = ".invalid-feedback.d-block"


    def __init__(self, page):
        super().__init__(page)


    def select_size(self,value):
        self.select_by_value(self.SELECT_DRESS_SIZE,value)

    def add_quantity(self,quantity):
        self.fill_text(self.ADD_QUANTITY_FIELD,quantity)

    def next_page(self):
        self.click(self.ADD_TO_CART_BUTTON)

    def add_review(self,title_review,comment_review,email_review):
        self.click(self.ADD_REVIEW_BUTTON)
        self.fill_text(self.TITLE_FIELD,title_review)
        self.fill_text(self.COMMENT_FIELD,comment_review)
        self.fill_text(self.EMAIL_FIELD,email_review)
        self.click(self.ADD_NEW_REVIEW_BUTTON)









    #assert
    def success_product(self):
        return self.is_visible(self.ADD_TO_CART_BUTTON)

    def assert_quantity_value(self, expected_quantity):
        self.verify_input_value(self.ADD_QUANTITY_FIELD,str(expected_quantity))

    def assert_selected_size(self, expected_size_value):
        self.verify_input_value(self.SELECT_DRESS_SIZE, expected_size_value)

    def error_message_review(self):
        return self.is_visible(self.ERROR_MESSAGE)