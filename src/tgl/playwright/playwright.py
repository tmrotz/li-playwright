import os
from configparser import ConfigParser, SectionProxy
from pathlib import Path

from playwright.sync_api import (
    Browser,
    BrowserContext,
    BrowserType,
    Page,
    sync_playwright,
)


def runGMail(config: ConfigParser, klass, *args, **kwargs):
    gmail: SectionProxy = config["gmail"]

    with sync_playwright() as p:
        chrome: BrowserType = p.chromium
        options = {
            "args": ["--disable-blink-features=AutomationControlled"],
            "headless": False,
        }
        browser: Browser = chrome.launch(**options)

        file: Path = Path.home().joinpath(f"{gmail.get("username")}-gmail.json")

        context: BrowserContext = browser.new_context(
            base_url="https://mail.google.com",
            storage_state=file if os.path.isfile(file) else None,
            permissions=["clipboard-read", "clipboard-write"],
        )

        page: Page = context.new_page()
        page.goto("/")
        page.wait_for_url("/mail/u/0/#inbox")

        if not page.url.endswith("/mail/u/0/#inbox"):
            page.locator("input[type='email']").fill(gmail.get("username") or "")
            page.get_by_text("Next", exact=True).click()
            page.locator("input[type='password']").fill(gmail.get("password") or "")
            page.get_by_text("Next", exact=True).click()
            page.wait_for_url("/mail/u/0/#inbox")
            context.storage_state(path=file)

        klass.run(page, gmail, *args, **kwargs)

        browser.close()


def runLI(config: ConfigParser, klass, *args, **kwargs):
    linkedin = config["linkedin"]

    with sync_playwright() as p:

        chrome: BrowserType = p.chromium
        browser: Browser = chrome.launch(headless=False)

        file: Path = Path.home().joinpath(f"{linkedin.get("username")}.json")

        context: BrowserContext = browser.new_context(
            base_url="https://www.linkedin.com",
            storage_state=file if os.path.isfile(file) else None,
            permissions=["clipboard-read", "clipboard-write"],
        )

        page: Page = context.new_page()
        page.goto("/feed/")

        if not page.url.endswith("/feed/"):
            page.get_by_label("Email or phone").fill(linkedin.get("username") or "")
            page.get_by_label("Password").fill(linkedin.get("password") or "")
            page.get_by_label("Sign in", exact=True).click()
            page.wait_for_url("/feed/")
            context.storage_state(path=file)

        klass.run(page, *args, **kwargs)

        browser.close()
