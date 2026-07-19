from __future__ import annotations

from playwright.sync_api import Page, Locator, expect


class BasePage:

    def __init__(self, page: Page):
        self.page = page

    def _get_element(self, locator: str | Locator) -> Locator:
        if isinstance(locator, str):
            return self.page.locator(locator)
        return locator

    def _highlight(self, el: Locator):
        """
        Draws Playwright's built-in highlight box around the element right
        before we act on it - purely a visual aid for headed/slowmo runs, so
        you can actually see which element the script is about to touch.
        No-ops harmlessly in headless mode (nothing to see, but it doesn't
        error or slow anything down meaningfully).
        """
        try:
            el.highlight()
        except Exception:
            # Never let a debug visual break the actual test action.
            pass

    def wait_for_visible(self, locator: str | Locator, timeout: int = 10000):
        el = self._get_element(locator)
        el.wait_for(state="visible", timeout=timeout)

    def wait_for_attached(self, locator: str | Locator, timeout: int = 10000):
        """המתן שהאלמנט יהיה ב-DOM (גם אם מוסתר)"""
        el = self._get_element(locator)
        el.wait_for(state="attached", timeout=timeout)

    def click(self, locator: str | Locator, timeout: int = 10000, force: bool = False):
        el = self._get_element(locator)
        if not force:
            el.wait_for(state="visible", timeout=timeout)
        self._highlight(el)
        el.click(force=force)

    def fill_text(self, locator: str | Locator, text: str, timeout: int = 10000):
        el = self._get_element(locator)
        el.wait_for(state="visible", timeout=timeout)
        self._highlight(el)
        el.fill(text)

    def get_text(self, locator: str | Locator, timeout: int = 10000) -> str:
        el = self._get_element(locator)
        el.wait_for(state="visible", timeout=timeout)
        self._highlight(el)
        return el.inner_text()

    def is_visible(self, locator: str | Locator) -> bool:
        el = self._get_element(locator)
        if el.is_visible():
            # Highlight it here (not after the check) so that on a failing
            # assertion right after this call, the failure screenshot shows
            # exactly which element was being verified.
            self._highlight(el)
            return True
        return False

    def select_by_value(self, locator: str | Locator, value: str, timeout: int = 10000):
        el = self._get_element(locator)
        el.wait_for(state="visible", timeout=timeout)
        self._highlight(el)
        el.select_option(value=value)

    def double_click(self, locator: str | Locator, timeout: int = 10000):
        el = self._get_element(locator)
        el.wait_for(state="visible", timeout=timeout)
        self._highlight(el)
        el.dblclick()

    def hover(self, locator: str | Locator, timeout: int = 10000):
        el = self._get_element(locator)
        el.wait_for(state="visible", timeout=timeout)
        self._highlight(el)
        el.hover()

    def left_click(self, locator: str | Locator, timeout: int = 10000):
        el = self._get_element(locator)
        el.wait_for(state="visible", timeout=timeout)
        self._highlight(el)
        el.click(button="left")

    def get_locator_by_text(self, selector: str, text: str) -> Locator:
        return self.page.locator(selector, has_text=text)

    def press_key(self, key: str):
        self.page.keyboard.press(key)

    def verify_input_value(self, locator, expected_value):
        el = self.page.locator(locator)
        self._highlight(el)
        expect(el).to_have_value(expected_value)