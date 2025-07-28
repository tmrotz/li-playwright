import random

from playwright.sync_api import Locator, Page

TEST = False


class Withdraw:
    def run(
        self,
        page: Page,
    ):
        self._withdraw(page)

        print("Done withdrawing")

    def _withdraw(self, page: Page):
        page.goto("mynetwork/invitation-manager/sent")

        page.get_by_text(exact=True, text="Sent").click()

        for _ in range(0, 100):
            page.keyboard.press("PageDown")
            page.wait_for_timeout(2 * 1_000)

        people = []
        if TEST:
            people = page.get_by_role("listitem").filter(has_text="weeks ago").all()
        else:
            month: Locator = page.get_by_role("listitem").filter(has_text="month ago")
            months: Locator = page.get_by_role("listitem").filter(has_text="months ago")
            people = month.all() + months.all()

        for person in people:
            person.scroll_into_view_if_needed()
            person.get_by_role("button").click()
            page.wait_for_timeout(3 * 1_000)
            if TEST:
                page.locator("#root > dialog").get_by_role("button").filter(
                    has_text="Cancel"
                ).click()
            else:
                page.locator("#root > dialog").get_by_role("button").filter(
                    has_text="Withdraw"
                ).click()
            page.wait_for_timeout(random.randint(3, 7) * 1_000)
