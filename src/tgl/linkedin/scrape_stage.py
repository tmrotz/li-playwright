import random

from playwright.sync_api import Locator, Page
from playwright.sync_api import TimeoutError as PWTimeoutError
from requests import Response

from tgl.streak.box import Box
from tgl.streak.streak import Streak

headline_selector = (
    "div:nth-of-type(2) > div:nth-of-type(2) > div:nth-of-type(1) > div:nth-of-type(2)"
)
location_selector = "div > div.relative > div > span.break-words"


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
            try:
                box: Box = self._scrape(page, streak_box["fields"][linkedin_key])
            except Exception as e:
                print("Something went wrong. Skipping", e)
            else:
                print("Scraped data", box)
                response: Response = streak.update_box(
                    streak_box["key"],
                    streak.create_fields_data(box),
                    stage_key=scraped_stage_key,
                )

            page.wait_for_timeout(random.randint(10, 15) * 1000)

        print("Done scraping")

    def _scrape(self, page: Page, url: str) -> Box:
        # URL may have ending slash: https://www.linkedin.com/in/brad-rachal/
        splits: list[str] = url.split("/")
        user = splits[-1]
        if not user:
            user = splits[-2]
        if not user:
            raise Exception("Bad Linkedin URL: " + url)

        page.goto("/in/" + user)
        section: Locator = page.locator("section", has_text="Contact info")

        name = section.locator("h1").text_content()
        if name is None:
            print("name not available")
            raise Exception("name not available")

        box: Box = Box(name.strip())

        headline = section.locator(headline_selector).text_content()
        if headline is None:
            print("headline not available", headline_selector)
            raise Exception("headline not available")
        box.headline = headline.strip()

        location = section.locator(location_selector).text_content()
        if location is None:
            print("location not available", location_selector)
            raise Exception("location not available")
        box.location = location.strip()

        experience: Locator = page.get_by_text("Experience", exact=True).first
        section: Locator = page.locator("section").filter(has=experience)
        experiences: list[str] = (
            section.get_by_role("list").first.inner_text().splitlines()
        )

        uniques = []
        for e in experiences[:10]:
            if e not in uniques:
                uniques.append(e)

        box.position = uniques[0]
        box.company = uniques[1].split(" · ")[0]

        # Contact Info Section!
        page.locator("a", has_text="Contact info").first.click()

        section: Locator = page.locator("section").filter(
            has=page.locator("h2", has_text="Contact Info")
        )
        section.wait_for()

        # connected = section.locator("section", has_text="Connected").locator("span")
        # try:
        #     connected.wait_for(timeout=1000)
        # except PWTimeoutError:
        #     print("Not connected, skipping")
        # else:
        #     box.connected = datetime.strptime(
        #         connected.inner_text().strip(), "%b %d, %Y"
        #     )

        email = section.locator("section", has_text="Email").locator("a")
        try:
            email.wait_for(timeout=1000)
        except PWTimeoutError:
            print("No email, skipping")
        else:
            box.email = email.inner_text().strip()

        phone = section.locator("section", has_text="Phone").locator("span").first
        try:
            phone.wait_for(timeout=1000)
        except PWTimeoutError:
            print("No phone, skipping")
        else:
            box.phone = phone.inner_text().strip()

        return box
