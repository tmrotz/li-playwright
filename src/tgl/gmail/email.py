import random
from configparser import SectionProxy

from playwright.sync_api import Page

from tgl.streak.streak import Streak

TEST = False


class Email:
    def run(
        self,
        page: Page,
        config: SectionProxy,
        streak: Streak,
        email_stage_key: str,
        emailed_stage_key: str,
    ):
        print("Sending emails")

        boxes: list = streak.get_boxes_by_stage(email_stage_key)
        if not boxes:
            print("Didn't get any boxes from Streak")
            return

        subject = config.get("subject") or "???"
        message = config.get("message") or "???"

        first_name_key = streak.get_first_name_key()
        email_key = streak.get_email_key()

        for box in boxes:
            self._email(
                page,
                box["fields"][email_key],
                subject,
                message.format(name=box["fields"][first_name_key]),
            )
            streak.update_box(box["boxKey"], stage_key=emailed_stage_key)
            page.wait_for_timeout(random.randint(5, 11) * 1_000)

        print("Done emailing")

    def _email(self, page: Page, to: str, subject: str, message: str):
        page.get_by_text("Compose", exact=True).click()
        page.wait_for_timeout(3_000)
        page.locator('input[aria-label="To recipients"]').fill(to)
        page.wait_for_timeout(3_000)
        page.get_by_placeholder("Subject", exact=True).fill(subject)
        page.wait_for_timeout(3_000)
        page.locator('div[aria-label="Message Body"]').fill(message)
        page.wait_for_timeout(3_000)
        page.get_by_role("button").filter(has_text="Send").click()
