import time
import pytest
from tests.base_test import BaseTest


@pytest.mark.usefixtures("setup_function")
class Test_e2e(BaseTest):

    def test_e2e_load_loop(self):
        """ריצת עומס מקומית באמצעות לולאת פייתון קלאסית"""

        for i in range(100):
            print(f"\n--- מתחיל הרצה מספר {i + 1} מתוך 100 ---")

            # 1. ביצוע תהליך ה-E2E המלא
            self.home_page.goto_dresses()
            self.catalog_page.click_on_product("Sunshine Strappy Delight")
            self.product_page.next_page()
            self.cart_page.checkout()
            self.checkout_page.fill_info_checkout("shalev6005@gmail.com", "shalev", "shapiro", "shapiro", "mishoal",
                                                  "AU", "new york", "1234567", "123456789")
            self.checkout_page.choose_dhl()
            self.checkout_page.choose_cash()
            time.sleep(4)

            # 2. אימות הצלחה בכל סיבוב של הלולאה
            assert self.checkout_page.success_cash() is True, f"האתר הפסיק להגיב או קרס בהרצה מספר {i + 1}!"