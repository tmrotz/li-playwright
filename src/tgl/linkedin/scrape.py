from playwright.sync_api import Locator, Page

from tgl.streak.box import Box
from tgl.streak.streak import Streak

headline_selector = (
    "div:nth-of-type(2) > div:nth-of-type(2) > div:nth-of-type(1) > div:nth-of-type(2)"
)
location_selector = "div > div.relative > div > span.break-words"


class Scrape:
    def run(self, page: Page, streak: Streak):
        page.get_by_placeholder("Search").fill("Programmer")
        page.keyboard.press("Enter")
        page.get_by_role("button", name="People").click()
        page.wait_for_timeout(2500)

        links = []
        for _ in page.locator(
            "div.search-results-container li", has_text="Connect"
        ).all():
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
