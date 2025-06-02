import random

import pyperclip
from playwright.sync_api import Page

from tgl.streak.box import Box
from tgl.streak.streak import Streak


def send_messages(
    page: Page,
    streak: Streak,
    message: str,
):
    print("Message:", message)

    streak_boxes: list = streak.get_boxes_by_stage(
        streak.pipeline_key, streak.stage_key
    )
    assert isinstance(streak_boxes, list), f"streak_boxes is a {type(streak_boxes)}"
    print("# of boxes from Streak", len(streak_boxes))

    for streak_box in streak_boxes:
        assert isinstance(streak_box, dict), f"streak_box is a {type(streak_box)}"
        try:
            send_message(page, streak_box, message)
        except TimeoutError as e:
            print("Timeout reached. Skipping", e)
        page.wait_for_timeout(random.randint(10, 15) * 1000)


def send_message(page: Page, streak_box: dict, message: str):
    box: Box = Box(streak_box["name"])
    box.box_key = streak_box["boxKey"]
    box.stage_key = streak_box["stageKey"]

    page.goto("/messaging/thread/new/")

    # Get Message into clipboard
    pyperclip.copy(message.format(name=box.first_name()))

    # Logged in
    page.get_by_placeholder("Type a name or multiple names").fill(box.name)
    page.wait_for_timeout(random.randint(5, 7) * 1000)
    page.locator(
        "div.msg-connections-typeahead__search-results ul > li button"
    ).locator("nth=0").click()
    page.wait_for_timeout(random.randint(5, 7) * 1000)
    page.keyboard.press("Enter")
    page.wait_for_timeout(random.randint(5, 7) * 1000)
    page.keyboard.press("Control+V")
    page.wait_for_timeout(random.randint(5, 7) * 1000)
    page.get_by_role("button", name="Send", exact=True).click()
