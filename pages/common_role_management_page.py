from utils.logger import get_logger

from pages.common_utils.pagination import PaginationHelper

logger = get_logger(__name__)


class RoleManagementPage:
    def __init__(self, page):
        logger.debug("Initializing RoleManagementPage with page object")
        self.page = page
        logger.info("RoleManagementPage initialized successfully")

    def go_to_rolemanagementpage(self, url):
        logger.info("Navigating to Role Management page: %s", url)
        logger.debug("Calling page.goto() with URL")
        self.page.goto(url)
        logger.debug("Waiting for network to be idle")
        self.page.wait_for_load_state("networkidle")
        logger.info("Successfully navigated to and loaded Role Management page")

    def is_page_loaded(self):
        logger.debug("Checking if Role Management page is loaded")
        return self.page.url.endswith("/user-role")

    def is_add_role_button_visible(self):
        logger.debug("Checking visibility of Add Role open_in_new button")
        add_role = self.page.locator("button[class='primary-button ng-star-inserted']")
        return add_role.is_visible()

    def is_role_table_visible(self):
        logger.debug("Checking visibility of Role table")
        table = self.page.locator("//div[@class='component-body']")
        return table.is_visible()

    def is_search_box_visible(self):
        logger.debug("Checking visibility of Search box")
        search_box = self.page.get_by_placeholder("Search and Press Enter")
        return search_box.is_visible()

    def click_add_role(self):
        logger.info("Clicking Add New Role button")
        self.page.get_by_text("Add Role open_in_new", exact=True).click()

    def enter_role_name(self, role_name):
        logger.info("Entering role name: %s", role_name)
        logger.debug("Locating Role Name textbox")
        textbox = self.page.get_by_role("textbox", name="Role Name")
        logger.debug("Filling Role Name field with: %s", role_name)
        textbox.fill(role_name)
        logger.debug("Role name entered successfully")

    def select_role_type(self, role_type):
        logger.info("Selecting role type: %s", role_type)
        logger.debug("Clicking mat-select dropdown for role type")
        # Click mat-select dropdown
        self.page.locator("mat-select[formcontrolname='roleType']").click()
        logger.debug("Waiting for dropdown options panel to appear")
        # Wait for dropdown options panel
        self.page.locator("mat-option").first.wait_for()
        logger.debug("Clicking option with text: %s", role_type)
        # Click the option
        self.page.get_by_text(role_type, exact=True).click()
        logger.info("Role type '%s' selected successfully", role_type)

    def is_role_group_visible(self):
        logger.debug("Checking Role Group visibility")
        return self.page.locator("mat-select[formcontrolname='roleGroup']").is_visible()

    def select_role_group(self, group):
        logger.info("Selecting role group: %s", group)
        logger.debug("Clicking mat-select dropdown for role group")
        self.page.locator("mat-select[formcontrolname='roleGroup']").click()
        logger.debug("Waiting for dropdown options panel to appear")
        self.page.locator("mat-option").first.wait_for()
        logger.debug("Clicking option with text: %s", group)
        self.page.locator(f"mat-option:has-text('{group}')").click()
        logger.info("Role group '%s' selected successfully", group)

    def click_save(self):
        logger.info("Clicking Save button")
        self.page.locator(".submit-button.ng-star-inserted").click()

    def get_error_message(self):
        logger.debug("Fetching error message from snackbar")
        error_message = self.page.locator("simple-snack-bar").inner_text()
        logger.info("Error message retrieved: %s", error_message)
        return error_message

    def get_input_box_error_message(self):
        logger.debug("Fetching error message for input field")
        logger.debug("Locating mat-error element")
        error_locator = self.page.locator("mat-error")
        error_message = error_locator.inner_text()
        logger.info("Input error message retrieved: %s", error_message)
        return error_message

    def select_permission(self, page_name, permission_type):
        logger.info("Selecting %s permission for %s", permission_type, page_name)
        logger.debug("Building permission map for column index lookup")
        permission_map = {
            "select_all": 1,
            "view": 2,
            "create": 3,
            "update": 4,
            "delete": 5,
        }

        col_index = permission_map.get(permission_type.lower())

        if not col_index:
            logger.error("Invalid permission type: %s", permission_type)
            raise ValueError(f"Invalid permission type: {permission_type}")

        logger.debug(
            "Building checkbox locator for page '%s' and permission type '%s'",
            page_name,
            permission_type,
        )
        checkbox = self.page.locator(
            f"//tr[td//strong[text()='{page_name}']]/td[{col_index + 1}]//input[@type='checkbox']"
        )
        logger.debug("Checking checkbox for permission")
        checkbox.check()
        logger.info(
            "Permission '%s' for '%s' checked successfully", permission_type, page_name
        )

    def select_all_permissions(self):
        logger.info("Selecting all permissions via select_all checkbox")
        logger.debug("Clicking select_all checkbox with ID mat-mdc-checkbox-1-input")
        self.page.locator("#mat-mdc-checkbox-1-input").check()
        logger.info("All permissions checkbox checked successfully")

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

    def wait_for_snackbar_to_disappear(self):
        logger.debug("Waiting for snackbar to disappear")
        snackbar = self.page.locator("div.mat-mdc-snack-bar-label")

        try:
            logger.debug("Waiting for snackbar to be hidden with 5s timeout")
            snackbar.wait_for(state="hidden", timeout=5000)
            logger.debug("Snackbar disappeared successfully")
        except:
            logger.debug("Snackbar already gone or timeout occurred")
            pass  # ignore if already gone

    def is_sub_permission_disabled(self, sub_name, permission_type):
        logger.debug(
            "Checking if sub-permission is disabled for '%s' - '%s'",
            sub_name,
            permission_type,
        )
        permission_map = {
            "view": 2,
            "create": 3,
            "update": 4,
            "delete": 5,
        }

        col_index = permission_map[permission_type.lower()]
        logger.debug("Building checkbox locator for sub-permission check")
        checkbox = self.page.locator(
            f"//tr[td[contains(text(),'{sub_name}')]]/td[{col_index + 1}]//input"
        )
        is_disabled = checkbox.is_disabled()
        logger.debug(
            "Sub-permission '%s' for '%s' disabled status: %s",
            permission_type,
            sub_name,
            is_disabled,
        )
        return is_disabled

    def select_sub_permission(self, sub_name, permission_type):
        logger.info(f"Selecting {permission_type} for {sub_name}")

        permission_map = {
            "view": 2,
            "create": 3,
            "update": 4,
            "delete": 5,
        }

        col_index = permission_map[permission_type.lower()]

        row = self.page.locator(f"//tr[td[contains(text(),'{sub_name}')]]")

        checkbox = row.locator(f"td:nth-child({col_index + 1}) input")

        # Check if the permission is disabled before attempting to check it
        if checkbox.is_disabled():
            logger.warning(
                f"Permission '{permission_type}' for '{sub_name}' is disabled and cannot be selected"
            )
            return False

        # Wait for checkbox to be checked (may be auto-checked by parent group enable)
        try:
            checkbox.wait_for(state="checked", timeout=2000)
            logger.debug(
                f"Permission '{permission_type}' for '{sub_name}' is already checked (auto-enabled)"
            )
            return True
        except:
            # Checkbox is not checked, proceed to check it
            pass

        checkbox.scroll_into_view_if_needed()
        try:
            checkbox.check(force=True)
            logger.debug(f"Successfully checked {permission_type} for {sub_name}")
            return True
        except Exception as e:
            # If check fails (state can't change), checkbox is likely already checked
            logger.warning(
                f"Could not check {permission_type} for {sub_name}: {str(e)}"
            )
            return False

    def enable_permission_group(self, page_name):
        logger.info(f"Enabling permission group: {page_name}")

        row = self.page.locator(f"//tr[td//strong[text()='{page_name}']]")

        # Main checkbox = first checkbox column (Select All)
        checkbox = row.locator("td:nth-child(2) input")

        checkbox.scroll_into_view_if_needed()
        checkbox.check(force=True)

    def search_role(self, role_name):
        logger.info("Searching for role: %s", role_name)
        logger.debug("Locating search box")
        search_box = self.page.get_by_placeholder("Search and Press Enter")
        logger.debug("Filling search box with role name: %s", role_name)
        search_box.fill(role_name)
        search_box.evaluate(
            "el => { el.dispatchEvent(new Event('input', { bubbles: true })); el.dispatchEvent(new Event('change', { bubbles: true })); }"
        )
        logger.debug("Pressing Enter to execute search")
        search_box.press("Enter")
        self.page.wait_for_load_state("networkidle", timeout=5000)
        self.page.wait_for_timeout(500)
        logger.info("Search for role '%s' executed", role_name)


    def is_role_in_table(self, role_name):
        logger.info("Checking if role '%s' is present in the table", role_name)

        try:
            # Wait for table rows to appear
            self.page.wait_for_selector(
                "div.component-body table tbody tr", timeout=5000
            )

            # Find role cell
            # Use the table locator and get_by_text to reliably find the role
            table = self.page.locator("div.component-body table")
            try:
                table.wait_for(state="visible", timeout=5000)
            except Exception:
                # Table may be present but empty; continue to attempt text lookup
                pass

            role_locator = table.get_by_text(role_name)
            count = role_locator.count()

            logger.info("Role '%s' found %s time(s) in table", role_name, count)

            return count > 0

        except Exception as e:
            logger.error("Error while checking role '%s': %s", role_name, str(e))
            return False

    def get_table_row_data(self, index: int) -> str:
        logger.debug("Retrieving table row data for index %s", index)
        logger.debug("Locating row at index %s", index)
        row = self.page.locator("div.component-body table tbody tr").nth(index)
        logger.debug("Extracting and stripping row text content")
        row_data = row.inner_text().strip()
        logger.info("Row %s data retrieved: %s", index, row_data)
        return row_data

    def get_pagination_count(self):
        logger.debug("Getting pagination count from Role Management page")
        pagination_helper = PaginationHelper(self.page)
        count = pagination_helper.get_pagination_count()
        logger.info("Pagination count retrieved: %s", count)
        return count
