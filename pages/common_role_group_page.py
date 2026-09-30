from utils.logger import get_logger

logger = get_logger(__name__)


class RoleGroupPage:
    def __init__(self, page):
        logger.debug("Initializing RoleGroupPage with page object")
        self.page = page
        logger.info("RoleGroupPage initialized successfully")

    def go_to_role_group_page(self, url):
        logger.info("Navigating to Role Group page: %s", url)
        logger.debug("Calling page.goto() with URL")
        self.page.goto(url)
        logger.debug("Waiting for network to be idle")
        self.page.wait_for_load_state("networkidle")
        logger.info("Successfully navigated to and loaded Role Group page")

    def get_title(self):
        logger.info("Retrieving Role Group page title")
        locator = self.page.locator(".page-title")
        locator.wait_for(state="visible")
        title = locator.text_content()
        logger.info("Page title found: %s", title)
        return title

    def is_page_loaded(self):
        logger.debug("Checking if Role Group page is loaded")
        return (
            self.page.url.endswith("/role-group")
            and self.page.locator(".page-title").is_visible()
        )

    def is_add_group_button_visible(self):
        logger.debug("Checking visibility of Add Group button")
        add_group = self.page.locator("button[class='primary-button ng-star-inserted']")
        return add_group.is_visible()

    def is_role_group_table_visible(self):
        logger.debug("Checking visibility of Role Group table")
        table = self.page.locator("//div[@class='component-body']")
        return table.is_visible()

    def is_search_box_visible(self):
        logger.debug("Checking visibility of Search box")
        search_box = self.page.get_by_placeholder("Search and Press Enter")
        return search_box.is_visible()

    def click_add_group(self):
        logger.info("Clicking Add New Group button")
        try:
            backdrop = self.page.locator(".cdk-overlay-backdrop")
            if backdrop.is_visible():
                self.page.keyboard.press("Escape")
                self.page.wait_for_timeout(200)
        except Exception:
            pass
        btn = self.page.locator("button.primary-button, button:has-text('Add Group'), button:has-text('Group')").first
        try:
            btn.click(timeout=5000)
        except Exception:
            btn.click(force=True)


    def click_save(self):
        logger.info("Clicking Save button")
        btn = self.page.get_by_role("button", name="Save")
        try:
            btn.click(timeout=5000)
        except Exception:
            btn.click(force=True)


    def get_success_message(self):
        logger.info("Waiting for success snackbar message")
        logger.debug("Locating snackbar container")
        snackbar = self.page.locator(".mat-mdc-snack-bar-container")
        logger.debug("Waiting for snackbar to be visible")
        snackbar.wait_for(state="visible")
        logger.debug("Extracting snackbar message text")
        message = snackbar.inner_text().strip()
        logger.info("Snackbar message: %s", message)
        return message

    def enter_role_group_name(self, role_name):
        logger.info("Entering role group name: %s", role_name)
        logger.debug("Locating Group Name textbox")
        textbox = self.page.get_by_role("textbox", name="Group Name")
        logger.debug("Filling Group Name field with: %s", role_name)
        textbox.fill(role_name)
        logger.debug("Role group name entered successfully")

    def get_component_title(self):
        logger.info("Retrieving component title")
        locator = self.page.locator(".component-title")
        locator.wait_for(state="visible")
        title = locator.text_content()
        logger.info("Component title found: %s", title)
        return title

    def get_input_box_error_message(self):
        logger.info("Retrieving input box error message")
        logger.debug("Locating mat-error element")
        error_locator = self.page.locator("mat-error")
        if error_locator.is_visible():
            logger.debug("Error locator is visible, extracting message")
            error_message = error_locator.text_content().strip()
            logger.info("Error message found: %s", error_message)
            return error_message
        logger.debug("No error locator visible")
        logger.info("No error message visible")
        return None

    def get_created_at_values(self):
        logger.debug("Retrieving created_at values from table")
        rows = self.page.locator("div.component-body table tbody tr")
        logger.debug("Found %s rows in table", rows.count())
        created_at_values = [
            rows.nth(i).locator("td").nth(1).inner_text().strip()
            for i in range(rows.count())
        ]
        logger.info("Created_at values retrieved: %s", created_at_values)
        return created_at_values
