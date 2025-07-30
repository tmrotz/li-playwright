from playwright.sync_api import Locator, Page
from playwright.sync_api import TimeoutError as PWTimeoutError

from tgl.streak.box import Box

headline_selector = (
    "div:nth-of-type(2) > div:nth-of-type(2) > div:nth-of-type(1) > div:nth-of-type(2)"
)
location_selector = "div > div.relative > div > span.break-words"


def scrape_page(page: Page, user: str) -> Box:
    page.goto("/in/" + user)
    section: Locator = page.locator("section", has_text="Contact info")

    name = section.locator("h1").text_content()
    if name is None:
        print("name not available")
        raise Exception("name not available")

    box: Box = Box(name.strip())

    box.linkedin = f"linkedin.com/in/{user}"

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

    # experience: Locator = page.get_by_text("Experience", exact=True).first
    # section: Locator = page.locator("section").filter(has=experience)
    # div = section.get_by_role("list").first.locator(":scope > li:first-child > div")
    #
    # lines: list[str] = div.inner_text().splitlines()
    # box.position = lines[0]
    # box.company = lines[2]
    # if "·" in box.company:
    #     box.company = box.company.split(" · ")[0]

    # Contact Info Section!
    page.locator("a", has_text="Contact info").first.click()

    section: Locator = page.locator("section").filter(
        has=page.locator("h2", has_text="Contact Info")
    )
    section.wait_for()

    # connected = section.locator("section", has_text="Connected").locator("span")
    # try:
    #     connected.wait_for(timeout=1_000)
    # except PWTimeoutError:
    #     print("Not connected, skipping")
    # else:
    #     box.connected = datetime.strptime(
    #         connected.inner_text().strip(), "%b %d, %Y"
    #     )

    email = section.locator("section", has_text="Email").locator("a")
    try:
        email.wait_for(timeout=1_000)
    except PWTimeoutError:
        print("No email, skipping")
    else:
        box.email = email.inner_text().strip()

    phone = section.locator("section", has_text="Phone").locator("span").first
    try:
        phone.wait_for(timeout=1_000)
    except PWTimeoutError:
        print("No phone, skipping")
    else:
        box.phone = phone.inner_text().strip()

    return box
