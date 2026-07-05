from pages.cart_page import Cart_Page
from pages.catalog_page import Catalog_Page
from pages.checkout_page import Checkout_Page
from pages.home_page import HomePage
from pages.product_page import ProductPage
from pages.login_page import LoginPage
from pages.register_page import RegisterPage


class BaseTest:
    catalog_page: Catalog_Page
    home_page: HomePage
    cart_page: Cart_Page
    checkout_page: Checkout_Page
    product_page: ProductPage
    register_page: RegisterPage
    login_page: LoginPage
