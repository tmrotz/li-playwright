import random

from playwright.sync_api import Page
from requests import Response

from tgl.linkedin import scrape
from tgl.streak.box import Box
from tgl.streak.streak import Streak


class ScrapeStage:
    def run(
        self,
        page: Page,
        streak: Streak,
        scrape_stage_key: str,
        scraped_stage_key: str,
    ):
        streak_boxes: list = streak.get_boxes_by_stage(scrape_stage_key)
        print("# of boxes to scrape", len(streak_boxes))

        linkedin_key = streak.get_linkedin_key()

        for streak_box in streak_boxes:
            url = streak_box["fields"][linkedin_key]

            # URL may have ending slash: https://www.linkedin.com/in/brad-rachal/
            splits: list[str] = url.split("/")
            user = splits[-1]
            if not user:
                user = splits[-2]
            if not user:
                print("Bad Linkedin URL: " + url)
                continue

            try:
                box: Box = scrape.scrape_page(page, user)
            except Exception as e:
                print("Something went wrong. Skipping", e)
            else:
                print("Scraped data", box)
                response: Response = streak.update_box(
                    streak_box["key"],
                    streak.create_fields_data(box),
                    stage_key=scraped_stage_key,
                )

            page.wait_for_timeout(random.randint(10, 15) * 1_000)

        print("Done stage scraping")
