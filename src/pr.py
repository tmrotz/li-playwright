import os
from configparser import ConfigParser

from playwright.sync_api import (
    Browser,
    BrowserContext,
    BrowserType,
    Page,
    sync_playwright,
)

import linkedin.messaging
import linkedin.scraping
from streak.Streak import Streak


def run(config: ConfigParser, command: str):
    streak = Streak(config["streak.keys"]["api"])
    streak.pipeline_key = config["streak.keys"]["pipeline"]
    streak.stage_key = config["streak.keys"]["stage"]

    username = config["linkedin"]["username"]
    password = config["linkedin"]["password"]
    message = config["linkedin"]["message"]

    with sync_playwright() as p:

        file = f"states/{username}.json"

        chrome: BrowserType = p.chromium
        browser: Browser = chrome.launch(headless=False)

        context: BrowserContext = browser.new_context(
            base_url="https://www.linkedin.com",
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

        if command == "message":
            linkedin.messaging.run(page, streak, message)
        if command == "scrape":
            linkedin.scraping.run(page, streak)

        browser.close()
