import configparser
import json
import os
from configparser import SectionProxy
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
from streak import Box, Streak


def run(
    playwright: Playwright,
    username: str,
    password: str,
    message: str,
    boxes: List[Box],
):
    file = f"states/{username}.json"

    chrome: BrowserType = playwright.chromium
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

    for box in boxes:
        page.goto("/messaging/thread/new/")

        # Get Message into clipboard
        pyperclip.copy(message.format_map({"first": "Travis", "last": "Rotz"}))

        # Logged in
        page.get_by_placeholder("Type a name or multiple names").fill(box.name)
        page.wait_for_timeout(2000)
        page.locator(
            "div.msg-connections-typeahead__search-results ul > li button"
        ).locator("nth=0").click()
        page.wait_for_timeout(2000)
        page.keyboard.press("Enter")
        page.wait_for_timeout(2000)
        page.keyboard.press("Control+V")
        page.wait_for_timeout(2000)
        page.get_by_role("button", name="Send", exact=True).click()
        page.pause()

    browser.close()


if __name__ == "__main__":
    config: configparser.ConfigParser = configparser.ConfigParser()
    config.read("config.ini")

    with sync_playwright() as p:
        streak = Streak(config["Streak"]["api_key"])
        json = streak.get_boxes(
            config["Streak"]["pipeline_key"], config["Streak"]["stage_key"]
        )
        boxes: List[Box] = [Box("Rachal", "asdf", "asdf", {})]
        for box in json:
            boxes.append(
                Box(box["name"], box["boxKey"], box["stageKey"], box["fields"])
            )

        run(
            p,
            config["LinkedIn"]["username"],
            config["LinkedIn"]["password"],
            config["LinkedIn"]["message"],
            boxes,
        )
