from pages.basepage import BasePage


class CartPage(BasePage):
    ADD_COUPON_FIELD = "#sylius_shop_cart_promotionCoupon"
    ADD_COUPON_BTN = "[data-action='live#$render']"
    CHECKOUT_BTN = ".d-grid button"
    PAYPAL_BTN = "[data-funding-source='paypal']"
    CLEAR_CART_BTN = "[data-live-action-param='clearCart']"
    ADD_QUANTITY_FIELD_CART = "#sylius_shop_cart_items_0_quantity"
    CART_HOME_TITLE = ".offcanvas-header h1:has-text('Cart')"



    #assert
    SUCCESS_CART_PAGE= ".alert-success.my-2"
    EMPTY_CART = ".alert-info div"
    COUPON_ERROR = ".invalid-feedback.d-block"


    def __init__(self, page):
        super().__init__(page)

    def clear_cart(self):
        self.click(self.CLEAR_CART_BTN)

    def coupon(self,coupon_code):
        self.fill_text(self.ADD_COUPON_FIELD,coupon_code)
        self.click(self.ADD_COUPON_BTN)

    def checkout(self):
        self.click(self.CHECKOUT_BTN)

    def open_paypal_window(self):
        with self.page.expect_popup(timeout=45000) as popup_info:
            paypal_frame = self.page.frame_locator("iframe[allowtransparency='true']").nth(0)
            paypal_frame.locator("[data-funding-source='paypal']").click(timeout=30000)

        return popup_info.value

    #assert
    def get_cart_page(self):
        return self.is_visible(self.SUCCESS_CART_PAGE)

    def get_empty_cart(self):
        return self.is_visible(self.EMPTY_CART)

    def get_coupon_error(self):
        return self.is_visible(self.COUPON_ERROR)
    def get_cart_home_title(self):
        return self.is_visible(self.CART_HOME_TITLE)



