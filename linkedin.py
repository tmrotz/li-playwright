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
from streak import Box, get_boxes

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
    page.goto("/feed/")

    if not page.url.endswith("/feed/"):
        page.get_by_label("Email or phone").fill(username)
        page.get_by_label("Password").fill(password)
        page.get_by_label("Sign in", exact=True).click()
        page.wait_for_url("/feed/")
        context.storage_state(path=file)

    for box in boxes:
        page.goto("/messaging/thread/new/")

        # Get Message into clipboard
        pyperclip.copy(message)

        # Logged in
        page.get_by_placeholder("Type a name or multiple names").fill(box.name)
        page.wait_for_timeout(2000)
        page.locator(
            "div.msg-connections-typeahead__search-results ul > li button"
        ).locator("nth=0").click()
        page.keyboard.press("Enter")
        page.keyboard.press("Control+V")
        page.get_by_role("button", name="Send", exact=True).click()
        page.pause()

    browser.close()


if __name__ == "__main__":
    # get_boxes()
    with sync_playwright() as p:
        user = "travis"
        run(p, f"states/{user}.json")
