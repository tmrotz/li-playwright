from urllib.parse import quote

from playwright.sync_api import Locator, Page

TEST = True


class Connect:
    def run(self, page: Page, keywords: str, limit: int):
        page.goto("/search/results/people/?keywords=" + quote(keywords))

        page.wait_for_timeout(3_000)

        # Sometime divs, and sometimes ul/li's
        lisT: Locator = page.locator(
            "main > div:first-of-type > div:first-of-type > div:first-of-type > div:first-of-type > div:first-of-type > div:first-of-type > div:first-of-type > div:first-of-type"
        )

        if lisT.count() == 0:
            lisT = page.locator(
                "main > div > div > div > div > ul",
                has_not_text="Are these results helpful?",
            )
            lisT.highlight()
            page.pause()

        page.pause()
        people = lisT.locator(":scope > div", has_text="Connect")
        moo = 0
        # TODO: Add paging
        for person in people.all():
            try:
                self._connect(page, person)
            except:
                print("Problem connecting with that person")
                return

            moo = moo + 1
            if moo >= limit:
                return

        print("Done connecting")

    def _connect(self, page: Page, person: Locator):
        person.scroll_into_view_if_needed()
        page.wait_for_timeout(1_000)
        person.locator("a", has_text="Connect").last.click()
        page.wait_for_timeout(1_000)
        if TEST:
            page.get_by_role("button", name="Dismiss").last.click()
        else:
            page.locator("button", has_text="Send without a note").click()

        page.wait_for_timeout(3_000)


#
# function checkForOops() {
#   const div = document.querySelector('div.search-no-results');
#   if (div) {
#     const button: HTMLButtonElement | null = document.querySelector('button.artdeco-button.artdeco-button--3');
#     if (button) {
#       button.click();
#     }
#   }
# }
#
# function clickConnectButton(index: number) {
#   const peep_els = document.querySelectorAll('div.search-results-container > div > div > ul > li');
#   const peep_el = peep_els[index];
#   const button = peep_el.querySelector('button');
#   if (!button) {
#     throw 'button not found';
#   }
#   button.click();
# }
#
# /**
#  * Check if connect popup is different
#  * Sometimes it asks you to enter their email
#  * Just skip these
#  */
# function checkForEmail(): boolean {
#   const input: HTMLInputElement | null = document.querySelector('input[name=email]');
#   return input !== null;
# }
#
# /**
#  * Click the x in the top right
#  */
# function clickCancel() {
#   const button: HTMLButtonElement | null = document.querySelector('button.artdeco-modal__dismiss');
#   if (!button) {
#     console.log('button not found');
#     throw 'button not found';
#   }
#   button.click();
# }
#
# function clickSendInvintation() {
#   const xpath: XPathResult = document.evaluate('//button/span[contains(., "Send without a note")]', document);
#   const span: Node | null = xpath.iterateNext();
#   if (span && span.parentElement) {
#     const button = <HTMLButtonElement>span.parentElement;
#     button.click()
#   }
# }
#
# function clickNextButton() {
#   const xpath: XPathResult = document.evaluate('//button/span[contains(., "Next")]', document);
#   const span: Node | null = xpath.iterateNext();
#   if (span && span.parentElement) {
#     const button = <HTMLButtonElement>span.parentElement;
#     if (!button) {
#       return true;
#     }
#     button.click();
#   }
#   return false;
# }
