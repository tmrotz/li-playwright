import random

from playwright.sync_api import Locator, Page
from playwright.sync_api import TimeoutError as PWTimeoutError
from requests import Response

from tgl.linkedin import scrape
from tgl.streak.box import Box
from tgl.streak.streak import Streak

headline_selector = (
    "div:nth-of-type(2) > div:nth-of-type(2) > div:nth-of-type(1) > div:nth-of-type(2)"
)
location_selector = "div > div.relative > div > span.break-words"


# Go to network page
# Scroll down a bit
# Get links
# Get all Streak boxes
# Scrape until same box in Streak
class ScrapeNetwork:
    def run(
        self,
        page: Page,
        streak: Streak,
    ):
        boxes: list = streak.get_all_boxes()
        linkedin_key = streak.get_linkedin_key()
        urls = list(map(lambda b: b["fields"][linkedin_key], boxes))
        print(urls)

        self._network_scrape(page, streak, urls)

        print("Done scraping")

    def _network_scrape(self, page: Page, streak: Streak, streak_urls: list[str]):
        page.goto("mynetwork/invite-connect/connections")

        section: Locator = page.locator("section", has_text="Connections")
        section.wait_for()

        lisT: Locator = section.get_by_role("list")
        items: Locator = lisT.get_by_role("listitem")

        users = []
        for item in items.all():
            item.scroll_into_view_if_needed()
            link: Locator = item.get_by_role("link").first
            href = link.get_attribute("href")
            if href:
                user = href.split("/")[-2]
                if f"linkedin.com/in/{user}" not in streak_urls:
                    users.append(user)

        for user in users:
            try:
                box: Box = scrape.scrape_page(page, user)
            except PWTimeoutError as e:
                print("Something went wrong, skipping", e)
                continue
            else:
                response: Response = streak.create_box_with_data(box)

            page.wait_for_timeout(random.randint(10, 15) * 1_000)

        print("Done network scraping")
