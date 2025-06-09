from playwright.sync_api import Locator, Page
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

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
        page.set_default_timeout(10000)
        streak_boxes: list = streak.get_boxes_by_stage(scrape_stage_key)
        print("# of boxes to scrape", len(streak_boxes))

        for streak_box in streak_boxes:
            url = streak_box["fields"][streak.get_linkedin_key()][12:]
            page.goto(url)
            section: Locator = page.locator("section", has_text="Contact info")

            name = section.get_by_role("heading").text_content()
            if name is None:
                print("name not available")
                continue

            box: Box = Box(name.strip())

            headline = section.locator(headline_selector).text_content()
            if headline is None:
                print("headline not available", headline_selector)
                continue
            box.headline = headline.strip()

            location = section.locator(location_selector).text_content()
            if location is None:
                print("location not available", location_selector)
                continue
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

            page.get_by_text("Contact info").click()

            section: Locator = page.locator("section", has_text="Contact Info")
            section.wait_for()

            email = section.locator("section", has_text="Email").locator("a")
            try:
                email.wait_for()
            except PlaywrightTimeoutError:
                print("No email, skipping")
            else:
                box.email = email.inner_text().strip()

            phone = page.locator("section", has_text="Phone").locator("span").first
            try:
                phone.wait_for()
            except PlaywrightTimeoutError:
                print("No phone, skipping")
            else:
                box.phone = phone.inner_text().strip()

            # connected = page.locator("section", has_text="Connected").locator("span")
            # connected.wait_for()
            # connected = connected.inner_text().strip()
            # connected[0:2], connected[
            # box.connected = ???

            print(box)

            streak.update_box(
                streak_box["key"],
                streak.create_fields_data(box),
                stage_key=scraped_stage_key,
            )
