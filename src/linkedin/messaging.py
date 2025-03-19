from typing import List

import pyperclip
from playwright.sync_api import Page

from streak.Box import Box
from streak.Streak import Streak


def run(
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
