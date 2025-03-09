import os

import pyperclip

from playwright.sync_api import (
    Browser,
    BrowserContext,
    BrowserType,
    Page,
    Playwright,
    sync_playwright,
)

username = ""
password = "SofaRahuSahe0="
base_url = "https://www.linkedin.com"
name = "Rachal"
message = "It worked!"


def run(playwright: Playwright, file="state.json"):
    chrome: BrowserType = playwright.chromium
    browser: Browser = chrome.launch(headless=False)

    if not os.path.isfile(file):
        file = None
    context: BrowserContext = browser.new_context(
        base_url=base_url,
        storage_state=file,
        permissions=["clipboard-read", "clipboard-write"],
    )

    page: Page = context.new_page()
    page.goto("/feed/", wait_until="domcontentloaded")

    if page.url != base_url + "/feed/":
        page.goto("/checkpoint/rm/sign-in-another-account")
        page.get_by_label("Email or phone").fill(username)
        page.get_by_label("Password").fill(password)
        page.get_by_label("Sign in", exact=True).click()
        page.wait_for_url("/feed/")
        page.context.storage_state(path=file)

    # Get Message into clipboard
    pyperclip.copy(message)

    # Logged in
    page.goto("/messaging/thread/new/")
    page.get_by_placeholder("Type a name or multiple names").fill(name)
    page.wait_for_timeout(3000)
    page.locator(
        "div.msg-connections-typeahead__search-results ul > li button"
    ).locator("nth=0").click()
    page.keyboard.press("Enter")
    page.keyboard.press("Control+V")
    page.get_by_role("button", name="Send", exact=True).click()
    page.pause()


with sync_playwright() as p:
    run(p)
