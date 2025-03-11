import os
from typing import List

import pyperclip

from playwright.sync_api import (
    Browser,
    BrowserContext,
    BrowserType,
    Page,
    Playwright,
    sync_playwright,
)


class Box:
    name: str

    def __init__(self, name: str):
        self.name = name


base_url = "https://www.linkedin.com"
message = "It worked! again again"
boxes: List[Box] = [Box("Rachal")]


def run(playwright: Playwright, file="states/default.json"):
    chrome: BrowserType = playwright.chromium
    browser: Browser = chrome.launch(headless=False)

    context: BrowserContext = browser.new_context(
        base_url=base_url,
        storage_state=file if os.path.isfile(file) else None,
        permissions=["clipboard-read", "clipboard-write"],
    )

    page: Page = context.new_page()
    page.goto("/messaging/thread/new/")

    if not page.url.endswith("/messaging/thread/new/"):
        page.get_by_label("Email or phone").fill(username)
        page.get_by_label("Password").fill(password)
        page.get_by_label("Sign in", exact=True).click()
        context.storage_state(path=file)

    page.wait_for_url("/messaging/thread/new/")

    for box in boxes:
        # Get Message into clipboard
        pyperclip.copy(message)

        # Logged in
        page.get_by_placeholder("Type a name or multiple names").fill(box.name)
        page.wait_for_timeout(3000)
        page.locator(
            "div.msg-connections-typeahead__search-results ul > li button"
        ).locator("nth=0").click()
        page.wait_for_timeout(1000)
        page.keyboard.press("Enter")
        page.wait_for_timeout(1000)
        page.keyboard.press("Control+V")
        page.wait_for_timeout(1000)
        page.get_by_role("button", name="Send", exact=True).click()
        page.pause()


with sync_playwright() as p:
    user = "travis"
    run(p, f"states/{user}.json")
