from pages.basepage import BasePage


class Catalog_Page(BasePage):

    SEARCH_FIELD = "#criteria_search_value"
    SEARCH_BUTTON = ".input-group button"
    SHOW_DROPDOWN = ".gap-2 > div:nth-child(1) > button"
    SORT_DROPDOWN = ".gap-2 > div:nth-child(2) > button"
    LIMIT_18  = "[href$='limit=18']"
    FROM_A_TO_Z = "[data-text='from a to z']"
    NEXT_BUTTON = "[rel='next']"
    PREVIOUS_BUTTON = "[rel='prev']"


    #assert
    SEARCH_SUCCESS = "[alt$='value']"
    SEARCH_ERROR = ".alert.alert-info"
    CARD = ".object-fit-cover"
    PRODUCT_NAME = ".h6.text-break"







    def __init__(self, page):
        super().__init__(page)

    def search_by_button(self,search_value):
        self.fill_text(self.SEARCH_FIELD, search_value)
        self.click(self.SEARCH_BUTTON)

    def search_by_enter(self,search_value):
        self.fill_text(self.SEARCH_FIELD, search_value)
        self.page.locator(self.SEARCH_FIELD).press("Enter")

    def show_results(self):
        self.click(self.SHOW_DROPDOWN)
        self.click(self.LIMIT_18)

    def sort_results(self):
        self.click(self.SORT_DROPDOWN)
        self.click(self.FROM_A_TO_Z)

    def go_next(self):
        self.click(self.NEXT_BUTTON)

    def go_previous(self):
        self.click(self.PREVIOUS_BUTTON)

    def click_on_product(self, product_name):
        dynamic_product_locator = f"[product='{product_name}']"
        self.click(dynamic_product_locator)


    #assers
    def search_success(self, search_term):
        dynamic_locator = f"[alt$='{search_term}]"
        return self.is_visible(dynamic_locator)

    def search_error(self):
        return self.is_visible(self.SEARCH_ERROR)

    def count_cards(self):
        return self.page.locator(self.CARD).count()

    def get_title_text(self):
        return self.page.locator(self.PRODUCT_NAME).all_text_contents()

    def get_current_url(self) -> str:
        return self.page.url

