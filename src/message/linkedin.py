from typing import List

import pyperclip
from playwright.sync_api import Locator, Page

from message.streak.Box import Box
from message.streak.Streak import Streak

headline_selector = (
    "div:nth-of-type(2) > div:nth-of-type(2) > div:nth-of-type(1) > div:nth-of-type(2)"
)
location_selector = "div > div.relative > div > span.break-words"


def message(
    page: Page,
    streak: Streak,
    message: str,
):
    # print(streak.get_pipeline(config["streak.keys"]["pipeline"]))

    box: Box = Box("Brad Rachal")
    box.box_key = "boxKey"
    box.stage_key = "stageKey"
    boxes: List[Box] = [box]

    json = streak.get_boxes_by_stage(streak.pipeline_key, streak.stage_key)
    for _ in json:
        box: Box = Box(_["name"])
        box.box_key = _["boxKey"]
        box.stage_key = _["stageKey"]
        boxes.append(box)

    for box in boxes:
        page.goto("/messaging/thread/new/")

        # Get Message into clipboard

        pyperclip.copy(message.format(name=box.first_name()))

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


def scrape(page: Page, streak: Streak):
    page.get_by_placeholder("Search").fill("Programmer")
    page.keyboard.press("Enter")
    page.get_by_role("button", name="People").click()
    page.wait_for_timeout(2500)

    links = []
    for _ in page.locator("div.search-results-container li", has_text="Connect").all():
        href = _.locator("a").first.get_attribute("href")
        links.append(href)

    for _ in links:
        page.goto(_)
        section: Locator = page.locator("section", has_text="Contact info")

        name = section.get_by_role("heading").text_content()
        if name is None:
            print("name not available")
            break

        box: Box = Box(name.strip())

        headline = section.locator(headline_selector).text_content()
        if headline is None:
            print("headline not available", headline_selector)
            break
        box.headline = headline.strip()

        location = section.locator(location_selector).text_content()
        if location is None:
            print("location not available", location_selector)
            break
        box.location = location.strip()

        print(box)
