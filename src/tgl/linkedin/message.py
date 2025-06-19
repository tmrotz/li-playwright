import errno
import random

import pyperclip
from playwright.sync_api import Page
from playwright.sync_api import TimeoutError as PWTimeoutError

from tgl.streak.box import Box
from tgl.streak.streak import Streak


class Message:
    def run(
        self,
        page: Page,
        streak: Streak,
        message_template: str,
        message_stage_key: str,
        messaged_stage_key: str,
    ):
        print("Message Template:", message_template)

        streak_boxes: list = streak.get_boxes_by_stage(message_stage_key)
        assert isinstance(streak_boxes, list), f"streak_boxes is a {type(streak_boxes)}"
        print("# of boxes from Streak", len(streak_boxes))

        self._send_messages(
            page, streak, message_template, messaged_stage_key, streak_boxes
        )

    def _send_messages(
        self,
        page: Page,
        streak: Streak,
        message_template: str,
        messaged_stage_key: str,
        boxes: list,
    ):
        for box in boxes:
            assert isinstance(box, dict), f"streak_box is a {type(box)}"
            try:
                self._send_message(page, box, message_template)
            except TimeoutError as e:
                print("Timeout reached. Skipping", e)
            else:
                streak.update_box(box["boxKey"], stage_key=messaged_stage_key)

            page.wait_for_timeout(random.randint(15, 22) * 1_000)

    def _send_message(self, page: Page, streak_box: dict, message: str):
        box: Box = Box(streak_box["name"])

        page.goto("/messaging/thread/new/")

        # Get Message into clipboard
        pyperclip.copy(message.format(name=box.first_name()))

        page.get_by_placeholder("Type a name or multiple names").fill(box.name)
        page.wait_for_timeout(random.randint(5, 10) * 1_000)

        button = page.locator(
            "button",
            has=page.locator("dt", has_text="• 1st"),
        ).first
        try:
            button.wait_for(timeout=5000)
        except PWTimeoutError:
            raise TimeoutError(
                errno.ETIMEDOUT, "Didn't find 1st connection with name: " + box.name
            )
        else:
            button.click()

        page.wait_for_timeout(random.randint(5, 10) * 1_000)
        page.keyboard.press("Enter")
        page.wait_for_timeout(random.randint(5, 10) * 1_000)
        page.keyboard.press("Control+V")
        page.wait_for_timeout(random.randint(5, 12) * 1_000)
        page.get_by_role("button", name="Send", exact=True).click()
