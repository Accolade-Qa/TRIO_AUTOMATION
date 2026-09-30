from utils.logger import get_logger

logger = get_logger(__name__)


class BasePage:

    def __init__(self, page):
        self.page = page

        logger.debug("Initializing BasePage")

        self.footer = page.locator("div.footer-col.footer-left")

        self.version = page.locator("body app-root app-footer span:nth-child(1)")

        logger.debug("BasePage initialized successfully for URL: %s", page.url)

    def get_page_title(self):
        logger.debug("Retrieving browser page title")

        title = self.page.title()

        logger.debug("Page title retrieved: %s", title)

        return title

    def highlight(self, locator):
        logger.debug("Highlighting locator")

        locator.wait_for(state="visible")

        locator.evaluate("el => el.style.border = '3px solid purple'")

        logger.debug("Locator highlighted successfully")

        return locator

    def get_title(self):
        logger.info("Fetching page title")

        locator = self.page.locator(".page-title")

        locator.wait_for(state="visible")

        title_text = locator.text_content()

        logger.info("Page title: %s", title_text)

        return title_text

    def get_component_title(self):
        logger.info("Fetching component title")

        locator = self.page.locator(".component-title")

        locator.wait_for(state="visible")

        title_text = locator.text_content()

        logger.info("Component title: %s", title_text)

        return title_text

    def navigate_to(self, url: str):
        logger.info("Navigating to URL: %s", url)

        self.page.goto(url)

        self.page.wait_for_load_state("networkidle")

        logger.info("Navigation completed: %s", url)

    def wait_for_text(self, text: str):
        logger.info("Waiting for text: %s", text)

        locator = self.page.get_by_text(text, exact=True)

        locator.wait_for(state="visible")

        logger.info("Text became visible: %s", text)

        return locator
