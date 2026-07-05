from __future__ import annotations

from playwright.async_api import expect
from playwright.sync_api import Page, Locator

class BasePage:

    def __init__(self, page: Page):
        self.page = page

    def _get_element(self, locator: str | Locator) -> Locator:
        if isinstance(locator, str):
            return self.page.locator(locator)
        return locator

    def wait_for_visible(self, locator: str | Locator, timeout: int = 10000):
        el = self._get_element(locator)
        el.wait_for(state="visible", timeout=timeout)

    def wait_for_attached(self, locator: str | Locator, timeout: int = 10000):
        """Wait for the element to be attached to the DOM (even if hidden)"""
        el = self._get_element(locator)
        el.wait_for(state="attached", timeout=timeout)

    def click(self, locator: str | Locator, timeout: int = 10000, force: bool = False):
        el = self._get_element(locator)
        if not force:
            el.wait_for(state="visible", timeout=timeout)
        el.click(force=force)

    def fill_text(self, locator: str | Locator, text: str, timeout: int = 10000):
        el = self._get_element(locator)
        el.wait_for(state="visible", timeout=timeout)
        el.fill(text)

    def get_text(self, locator: str | Locator, timeout: int = 10000) -> str:
        el = self._get_element(locator)
        el.wait_for(state="visible", timeout=timeout)
        return el.inner_text()

    def is_visible(self, locator: str | Locator) -> bool:
        el = self._get_element(locator)
        return el.is_visible()

    def select_by_value(self, locator: str | Locator, value: str, timeout: int = 10000):
        el = self._get_element(locator)
        el.wait_for(state="visible", timeout=timeout)
        el.select_option(value=value)

    def double_click(self, locator: str | Locator, timeout: int = 10000):
        el = self._get_element(locator)
        el.wait_for(state="visible", timeout=timeout)
        el.dblclick()

    def hover(self, locator: str | Locator, timeout: int = 10000):
        el = self._get_element(locator)
        el.wait_for(state="visible", timeout=timeout)
        el.hover()

    def left_click(self, locator: str | Locator, timeout: int = 10000):
        el = self._get_element(locator)
        el.wait_for(state="visible", timeout=timeout)
        el.click(button="left")

    def get_locator_by_text(self, selector: str, text: str) -> Locator:
        return self.page.locator(selector, has_text=text)

    def press_key(self, key: str):
        """Press a key - e.g. Enter, Escape"""
        self.page.keyboard.press(key)

    def verify_input_value(self, locator, expected_value):
        expect(self.page.locator(locator)).to_have_value(expected_value)