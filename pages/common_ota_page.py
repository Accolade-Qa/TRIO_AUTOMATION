from pathlib import Path
import re

from config.global_var import DOWNLOADS_PATH
from pages.common_base_page import BasePage
from pages.common_utils.pagination import PaginationHelper
from pages.common_utils.pagination import PaginationHelper
from pages.common_utils.search import SearchHelper
from pages.common_utils.table_section import TableSection
from utils.logger import get_logger

logger = get_logger(__name__)


class OtaPage(BasePage):
    # Locators as class constants
    BUTTON_LOCATOR = "//button"
    TABLE_LOCATOR = "div.component-body"
    SEARCH_BOX_LOCATOR = "Search and Press Enter"
    OTA_MASTER_BUTTON_TEXT = "OTA Master"
    OTA_MASTER_PAGE_TITLE = "span:has-text('OTA Master')"
    OTA_BATCH_URL_SUFFIX = "/ota-batch-page"
    OTA_MASTER_URL_SUFFIX = "/ota-master"
    OTA_MASTER_URL_PATTERN = "**/ota-master*"
    ADD_OTA_COMMAND_BUTTON = "Add OTA Command"
    ADD_OTA_COMMAND_PAGE_TITLE = "h6:has-text('Add OTA Command')"

    # Add OTA Command Form Locators
    OTA_NAME_FIELD = "input[formcontrolname='name']"
    OTA_COMMAND_FIELD = "input[formcontrolname='otaCommand']"
    OTA_TYPE_DROPDOWN = "mat-select[formcontrolname='otaCommandType']"
    EXAMPLE_FIELD = "input[formcontrolname='otaCommandExample']"
    INPUT_FIELD_REQUIRED_DROPDOWN = "mat-select[formcontrolname='isInputFieldRequired']"
    SUBMIT_BUTTON = "button:has-text('Submit')"
    SEARCH_BUTTON = "button:has-text('Search search')"
    MAT_OPTION = "mat-option"

    # Manual OTA Page Locators
    SELECT_OTA_TYPE_DROPDOWN = ".dropdown-label floating"
    MANUAL_OTA_BUTTON = "Manual OTA"
    MANUAL_OTA_URL_PATTERN = "**/manual-ota*"
    IMEI_INPUT_FIELD = "input[formcontrolname='imei']"
    SEARCH_DEVICE_TITLE = "h6:has-text('Search Device')"
    NEW_OTA_BUTTON = "New OTA add_circle"
    OTA_COMMAND_LIST_HEADER = "h6:has-text('OTA Command List')"
    SET_BATCH_BUTTON = "button:has-text('Set Batch')"
    MANUAL_OTA_SEARCH_BUTTON = "//button[contains(@class,'submit-button')]"
    CHECKBOX_SELECTOR = "input[type='checkbox']"
    SEARCH_INPUT = "//input[@formcontrolname='searchInput']"
    SEARCH_BUTTON_ON_MANUAL_OTA = "//button[contains(@class,'search-btn')]"

    def __init__(self, page):
        super().__init__(page)
        logger.debug("Initialized OtaPage")

    def get_title(self) -> str:
        return super().get_title()

    def get_page_title(self) -> str:
        logger.debug("Retrieving OTA Master page title")
        return self.page.locator(self.OTA_MASTER_PAGE_TITLE).inner_text()

    def is_page_loaded(self) -> bool:
        logger.debug("Checking if ota batch page is loaded")
        return self.page.url.endswith(self.OTA_BATCH_URL_SUFFIX)

    def is_ota_master_page_loaded(self) -> bool:
        logger.debug("Checking if OTA Master page is loaded")
        return self.page.url.endswith(self.OTA_MASTER_URL_SUFFIX)

    def is_ota_batch_page_buttons_visible(self) -> bool:
        logger.debug("Checking visibility of OTA Batch page buttons")
        ota_page_buttons = self.page.locator(self.BUTTON_LOCATOR)
        for button in ota_page_buttons.all():
            if button.is_visible():
                return True
        return False

    def is_ota_batch_table_visible(self) -> bool:
        logger.debug("Checking visibility of OTA Batch table")
        table = self.page.locator(self.TABLE_LOCATOR)
        return table.is_visible()

    def is_search_box_visible(self) -> bool:
        logger.debug("Checking visibility of Search box")
        search_box = self.page.get_by_placeholder(self.SEARCH_BOX_LOCATOR)
        return search_box.is_visible()

    def is_ota_master_page_button_visible(self) -> bool:
        logger.debug("Checking visibility of OTA Master page button")
        ota_master_button = self.page.get_by_text(self.OTA_MASTER_BUTTON_TEXT)
        return ota_master_button.is_visible()

    def go_to_ota_master_page(self) -> None:
        logger.debug("Navigating to OTA Master page")

        self.page.get_by_text(self.OTA_MASTER_BUTTON_TEXT).click()
        self.page.wait_for_url(self.OTA_MASTER_URL_PATTERN)

    def search_in_batch_page(self, query: str) -> dict:
        logger.debug("Searching for OTA batch: %s", query)
        search = SearchHelper(self.page)
        result = search.run_search(query)
        return result

    def search_in_master_page(self, query: str) -> dict:
        logger.debug("Searching for OTA master: %s", query)
        search = SearchHelper(self.page)
        return search.run_search(query)

    def get_batch_table_data(self) -> list[str]:
        logger.debug("Retrieving OTA Batch table data")
        table = TableSection(self.page)
        return table.get_rows()

    def get_batch_table_headers(self) -> list[str]:
        logger.debug("Retrieving OTA Batch table headers")
        table = TableSection(self.page)
        return table.get_headers()

    def get_batch_table_row_count(self) -> int:
        logger.debug("Getting OTA Batch table row count")
        table = TableSection(self.page)
        return table.get_row_count()

    def is_batch_table_empty(self) -> bool:
        logger.debug("Checking if OTA Batch table is empty")
        table = TableSection(self.page)
        return table.has_no_data()

    def get_master_table_data(self) -> list[str]:
        logger.debug("Retrieving OTA Master table data")
        table = TableSection(self.page)
        return table.get_rows()

    def get_master_table_headers(self) -> list[str]:
        logger.debug("Retrieving OTA Master table headers")
        table = TableSection(self.page)
        return table.get_headers()

    def get_master_table_row_count(self) -> int:
        logger.debug("Getting OTA Master table row count")
        table = TableSection(self.page)
        return table.get_row_count()

    def is_master_table_empty(self) -> bool:
        logger.debug("Checking if OTA Master table is empty")
        table = TableSection(self.page)
        return table.has_no_data()

    def validate_add_ota_button_and_click(self) -> None:
        logger.debug("Validating Add OTA Command button visibility")
        add_ota_button = self.page.get_by_text(self.ADD_OTA_COMMAND_BUTTON)
        assert add_ota_button.is_visible(), "Add OTA Command button not visible"
        add_ota_button.click()

    def is_add_ota_command_button_visible(self) -> bool:
        logger.debug("Checking visibility of Add OTA Command button")
        add_ota_button = self.page.get_by_text(self.ADD_OTA_COMMAND_BUTTON)
        return add_ota_button.is_visible()

    def is_on_add_ota_command_page(self) -> str:
        logger.debug("Retrieving Add OTA Command page title")
        try:
            # Get page title text
            page_title = self.page.locator(self.ADD_OTA_COMMAND_PAGE_TITLE)
            if page_title.is_visible():
                title_text = page_title.inner_text()
                logger.debug("Add OTA Command page title: %s", title_text)
                return title_text
            else:
                logger.warning("Add OTA Command page title not visible")
                return ""
        except Exception as e:
            logger.warning("Error retrieving Add OTA Command page title: %s", str(e))
            return ""

    # Add OTA Command Form Validation Methods
    def are_add_ota_command_form_fields_visible(self) -> bool:
        logger.debug("Checking visibility of Add OTA Command form fields")
        try:
            ota_name = self.page.locator(self.OTA_NAME_FIELD).is_visible()
            ota_command = self.page.locator(self.OTA_COMMAND_FIELD).is_visible()
            ota_type = self.page.locator(self.OTA_TYPE_DROPDOWN).is_visible()
            example = self.page.locator(self.EXAMPLE_FIELD).is_visible()
            input_required = self.page.locator(
                self.INPUT_FIELD_REQUIRED_DROPDOWN
            ).is_visible()
            submit_btn = self.page.locator(self.SUBMIT_BUTTON).is_visible()

            all_visible = (
                ota_name
                and ota_command
                and ota_type
                and example
                and input_required
                and submit_btn
            )
            logger.debug(
                "Form fields visibility - OTA Name: %s, OTA Command: %s, OTA Type: %s, "
                "Example: %s, Input Required: %s, Submit: %s",
                ota_name,
                ota_command,
                ota_type,
                example,
                input_required,
                submit_btn,
            )
            return all_visible
        except Exception as e:
            logger.warning("Error checking form fields visibility: %s", str(e))
            return False

    def fill_ota_name(self, name: str) -> None:
        logger.debug("Filling OTA Name field with: %s", name)
        ota_name_field = self.page.locator(self.OTA_NAME_FIELD)
        ota_name_field.wait_for(state="visible")
        ota_name_field.fill(name)

    def fill_ota_command(self, command: str) -> None:
        logger.debug("Filling OTA Command field with: %s", command)
        ota_command_field = self.page.locator(self.OTA_COMMAND_FIELD)
        ota_command_field.wait_for(state="visible")
        ota_command_field.fill(command)

    def select_ota_type(self, ota_type: str) -> None:
        logger.debug("Selecting OTA Type: %s", ota_type)
        ota_type_dropdown = self.page.locator(self.OTA_TYPE_DROPDOWN)
        ota_type_dropdown.wait_for(state="visible")
        ota_type_dropdown.click()
        # Select the option from dropdown using mat-option selector
        option_locator = self.page.locator(f"{self.MAT_OPTION}:has-text('{ota_type}')")
        option_locator.wait_for(state="visible")
        option_locator.click()

    def fill_example(self, example: str) -> None:
        logger.debug("Filling Example field with: %s", example)
        example_field = self.page.locator(self.EXAMPLE_FIELD)
        example_field.wait_for(state="visible")
        example_field.fill(example)

    def select_input_field_required(self, option: str) -> None:
        logger.debug("Selecting Input Field Required: %s", option)
        input_required_dropdown = self.page.locator(self.INPUT_FIELD_REQUIRED_DROPDOWN)
        input_required_dropdown.wait_for(state="visible")
        input_required_dropdown.click()
        # Select the option from dropdown using mat-option selector
        option_locator = self.page.locator(f"{self.MAT_OPTION}:has-text('{option}')")
        option_locator.wait_for(state="visible")
        option_locator.click()

    def get_ota_name_value(self) -> str:
        logger.debug("Retrieving OTA Name field value")
        ota_name_field = self.page.locator(self.OTA_NAME_FIELD)
        return ota_name_field.input_value()

    def get_ota_command_value(self) -> str:
        logger.debug("Retrieving OTA Command field value")
        ota_command_field = self.page.locator(self.OTA_COMMAND_FIELD)
        return ota_command_field.input_value()

    def get_example_value(self) -> str:
        logger.debug("Retrieving Example field value")
        example_field = self.page.locator(self.EXAMPLE_FIELD)
        return example_field.input_value()

    def click_submit_button(self) -> None:
        logger.debug("Clicking Submit button")
        submit_button = self.page.locator(self.SUBMIT_BUTTON)
        submit_button.wait_for(state="visible")
        submit_button.click()

    def is_submit_button_disabled(self) -> bool:
        logger.debug("Checking if Submit button is disabled")
        submit_button = self.page.locator(self.SUBMIT_BUTTON)
        submit_button.wait_for(state="visible")
        is_disabled = submit_button.is_disabled()
        logger.debug("Submit button disabled state: %s", is_disabled)
        return is_disabled

    def is_search_button_disabled(self) -> bool:
        logger.debug("Checking if Search button is disabled")
        search_button = self.page.locator(self.SEARCH_BUTTON)
        search_button.wait_for(state="visible")
        is_disabled = search_button.is_disabled()
        logger.debug("Search button disabled state: %s", is_disabled)
        return is_disabled

    def is_submit_button_enabled(self) -> bool:
        logger.debug("Checking if Submit button is enabled")
        submit_button = self.page.locator(self.SUBMIT_BUTTON)
        submit_button.wait_for(state="visible")
        is_enabled = not submit_button.is_disabled()
        logger.debug("Submit button enabled state: %s", is_enabled)
        return is_enabled

    def go_to_manual_ota_page(self) -> None:
        logger.debug("Navigating to Manual OTA page")

        self.page.get_by_text("Manual OTA").click()
        self.page.wait_for_url("**/manual-ota*")

    def is_manual_ota_button_visible(self) -> bool:
        logger.debug("Checking visibility of Manual OTA button")
        manual_ota_button = self.page.get_by_text("Manual OTA")
        return manual_ota_button.is_visible()

    def click_manual_ota_button(self) -> None:
        logger.debug("Clicking Manual OTA button")
        manual_ota_button = self.page.get_by_text("Manual OTA")
        manual_ota_button.wait_for(state="visible")
        manual_ota_button.click()

    def get_manual_ota_component_title(self) -> str:
        logger.debug("Retrieving Manual OTA component title")
        try:
            component_title = self.page.locator("h6:has-text('Search Device')")
            if component_title.is_visible():
                title_text = component_title.inner_text()
                logger.debug("Manual OTA component title: %s", title_text)
                return title_text
            else:
                logger.warning("Manual OTA component title not visible")
                return ""
        except Exception as e:
            logger.warning("Error retrieving Manual OTA component title: %s", str(e))
            return ""

    def clear_imei_input(self) -> None:
        logger.debug("Clearing IMEI input field")
        imei_input = self.page.locator("input[formcontrolname='imei']")
        imei_input.wait_for(state="visible")
        imei_input.fill("")
        imei_input.evaluate(
            "el => { el.dispatchEvent(new Event('input', { bubbles: true })); el.dispatchEvent(new Event('change', { bubbles: true })); el.dispatchEvent(new Event('blur', { bubbles: true })); }"
        )


    def click_imei_input(self) -> None:
        logger.debug("Clicking IMEI input field to trigger validation")
        imei_input = self.page.locator("input[formcontrolname='imei']")
        imei_input.wait_for(state="visible")
        imei_input.click()

    def click_manual_ota_imei_search_button(self) -> None:
        logger.debug("Clicking Manual OTA Search button")

        search_button_on_manual_ota = self.page.locator(
            "//button[contains(@class,'submit-button')]"
        )

        search_button_on_manual_ota.wait_for(state="visible")

        # Use force=True to bypass disabled state validation (needed for error validation tests)
        if search_button_on_manual_ota.is_disabled():
            logger.debug(
                "Search button is disabled, clicking with force=True for error validation"
            )
            search_button_on_manual_ota.click(force=True)
        else:
            logger.debug("Search button is enabled, clicking normally")
            search_button_on_manual_ota.click()

    def get_imei_error_message(self, error) -> str:
        logger.debug("Retrieving IMEI error message")
        try:
            error_message = self.page.locator("mat-error").first
            error_message.wait_for(state="visible", timeout=3000)
            return error_message.inner_text().strip()
        except Exception as e:
            logger.warning("Error retrieving IMEI error message: %s", str(e))
            return error


    def fill_imei_input(self, imei: str) -> None:
        logger.debug("Filling IMEI input field with: %s", imei)
        imei_input = self.page.locator("input[formcontrolname='imei']")
        imei_input.wait_for(state="visible")
        imei_input.fill(imei)

    def is_new_ota_button_visible(self) -> bool:
        logger.debug("Checking visibility of New OTA button on Manual OTA page")
        try:
            # Try multiple locator strategies in order of preference
            locators = [
                ("button:has-text('New OTA')", "has-text selector"),
                (self.page.get_by_role("button", name="New OTA"), "by-role: New OTA"),
                ("//button[contains(text(), 'New OTA')]", "XPath with text"),
                (
                    self.page.get_by_text("New OTA add_circle"),
                    "by-text: New OTA add_circle",
                ),
            ]

            for locator, description in locators:
                try:
                    if isinstance(locator, str):
                        button = self.page.locator(locator)
                    else:
                        button = locator

                    # Wait for button to be visible with reasonable timeout
                    button.wait_for(state="visible", timeout=3000)
                    is_visible = button.is_visible()

                    if is_visible:
                        logger.info("New OTA button found using: %s", description)
                        return True
                    else:
                        logger.debug(
                            "Button found but not visible using: %s", description
                        )
                except Exception as e:
                    logger.debug("Locator '%s' failed: %s", description, str(e))
                    continue

            logger.warning("New OTA button not found with any locator strategy")
            return False

        except Exception as e:
            logger.error("Error checking New OTA button visibility: %s", str(e))
            return False

    def is_new_ota_button_enabled(self) -> bool:
        logger.debug("Checking if New OTA button is enabled on Manual OTA page")
        abort = self.page.locator("button.delete-button")

        try:
            abort.wait_for(state="visible", timeout=1000)
            if abort.is_enabled():
                logger.debug("Abort button found and enabled, clicking it")
                abort.click()
        except Exception as e:
            logger.debug("Abort button not found or not visible: %s", str(e))

        button = self.page.get_by_text("New OTA add_circle")
        button.wait_for(state="visible", timeout=3000)
        is_enabled = not button.is_disabled()
        logger.debug("New OTA button enabled state: %s", is_enabled)
        return is_enabled

    def click_new_ota_button(self) -> None:
        logger.debug("Clicking New OTA button on Manual OTA page")
        try:
            button = self.page.get_by_text("New OTA add_circle")
            button.wait_for(state="visible", timeout=3000)
            button.click()
        except Exception as e:
            logger.error("Error clicking New OTA button: %s", str(e))

    def click_abort_button(self) -> None:
        logger.debug("Clicking Abort button on Manual OTA page")
        try:
            abort_button = self.page.locator("button:has-text('ABORT')")
            abort_button.wait_for(state="visible", timeout=3000)
            abort_button.click()
            logger.info("Clicked Abort button successfully")
        except Exception as e:
            logger.error("Error clicking Abort button: %s", str(e))

    def get_ota_command_list_header(self) -> str:
        logger.debug("Retrieving OTA Command list header")
        try:
            header = self.page.locator("h6:has-text('OTA Command List')")
            if header.is_visible():
                header_text = header.inner_text().strip()
                logger.debug("OTA Command list header: %s", header_text)
                return header_text
            else:
                logger.warning("OTA Command list header not visible")
                return ""
        except Exception as e:
            logger.warning("Error retrieving OTA Command list header: %s", str(e))
            return ""

    def select_ota_type_on_manual_ota_page(self, ota_type: str) -> None:
        logger.debug("Selecting OTA Type on Manual OTA page: %s", ota_type)
        dropdown = self.page.locator(self.SELECT_OTA_TYPE_DROPDOWN)
        dropdown.wait_for(state="visible")
        dropdown.click()

        option_locator = self.page.locator("li:has-text('{}')".format(ota_type))
        option_locator.wait_for(state="visible")
        option_locator.click()

    def are_all_checkboxes_visible(self) -> bool:
        logger.debug("Checking visibility of all checkboxes on Manual OTA page")
        checkboxes = self.page.locator("input[type='checkbox']")
        count = checkboxes.count()
        logger.debug("Found %d checkboxes", count)

        # assert count > 0, "No checkboxes found on Manual OTA page"

        for i in range(count):
            if not checkboxes.nth(i).is_visible():
                logger.warning("Checkbox at index %d is not visible", i)
                return False
        return True

    def are_all_checkboxes_unchecked(self) -> bool:
        logger.debug("Checking if all checkboxes are unchecked on Manual OTA page")
        checkboxes = self.page.locator("input[type='checkbox']")
        count = checkboxes.count()
        logger.debug("Found %d checkboxes", count)

        # assert count > 0, "No checkboxes found on Manual OTA page"

        for i in range(count):
            if checkboxes.nth(i).is_checked():
                logger.warning("Checkbox at index %d is checked", i)
                return False
        return True

    def search_command_in_manual_ota(self, command: str) -> None:
        logger.debug("Searching for OTA command on Manual OTA page: %s", command)
        search_input = self.page.locator(self.SEARCH_INPUT)
        search_input.wait_for(state="visible")
        search_input.fill(command)

        search_button = self.page.locator(self.SEARCH_BUTTON_ON_MANUAL_OTA)
        search_button.wait_for(state="visible")
        search_button.click()

    def get_size_of_checkbox_list(self) -> int:
        logger.debug("Getting size of checkbox list on Manual OTA page")
        checkboxes = self.page.locator("input[type='checkbox']")
        count = checkboxes.count()
        logger.debug("Number of checkboxes found: %d", count)
        return count

    def is_checkbox_for_command_selected(self) -> bool:
        logger.debug("Checking if checkbox for command '%s' is selected")
        checkbox = self.page.locator("input[type='checkbox']")
        return checkbox.is_checked()

    def is_set_batch_button_enabled(self) -> bool:
        logger.debug("Checking if Set Batch button is enabled on Manual OTA page")
        set_batch_button = self.page.locator("button:has-text('Set Batch')")
        set_batch_button.wait_for(state="visible")
        is_enabled = not set_batch_button.is_disabled()
        logger.debug("Set Batch button enabled state: %s", is_enabled)
        return is_enabled

    def select_checkbox_for_command(self) -> None:
        logger.debug("Selecting checkbox for command")
        checkbox = self.page.locator("input[type='checkbox']")

        if checkbox.count() >= 1:
            checkbox = self.page.locator("input[type='checkbox']").first

        checkbox.wait_for(state="visible")
        checkbox.check()

    def click_set_batch_button(self) -> None:
        logger.debug("Clicking Set Batch button on Manual OTA page")
        set_batch_button = self.page.locator("button:has-text('Set Batch')")
        set_batch_button.wait_for(state="visible")
        set_batch_button.click()

    def is_set_configuration_component_visible(self) -> bool:
        logger.debug(
            "Checking visibility of Set Configuration component after clicking Set Batch"
        )
        set_configuration_component = self.page.locator(
            "h6:has-text('Set Configuration Value')"
        )
        return set_configuration_component.is_visible()

    def get_set_configuration_table_headers(self) -> list[str]:
        logger.debug("Retrieving Set Configuration table headers")
        table = TableSection(self.page)
        return table.get_headers()

    def setup_manual_ota_and_enable_set_batch(
        self, valid_imei: str, command_to_search: str = "GET IMEI"
    ) -> None:
        """
        Helper method to set up Manual OTA page and enable Set Batch button.
        Performs complete workflow: navigate -> search IMEI -> click New OTA -> search command -> select checkbox.

        Args:
            valid_imei: Valid 15-digit IMEI to search
            command_to_search: Command to search for (default: "GET IMEI")

        Raises:
            AssertionError: If any step fails
        """
        logger.info(
            "Setting up Manual OTA page and enabling Set Batch button with IMEI: %s, Command: %s",
            valid_imei,
            command_to_search,
        )

        # Step 1: Navigate to Manual OTA page
        self.go_to_manual_ota_page()
        logger.info("Step 1: Navigated to Manual OTA page")

        # Step 2: Fill and search IMEI
        self.fill_imei_input(valid_imei)
        self.click_manual_ota_imei_search_button()
        logger.info("Step 2: Searched with IMEI: %s", valid_imei)

        # Step 3 : Abort previous batch if it exists
        if self.is_abort_button_visible():
            self.click_abort_button()
            logger.info("Step 3: Aborted existing batch before proceeding")

        # Step 4: Click New OTA button
        if not self.is_new_ota_button_enabled():
            raise AssertionError(
                f"New OTA button should be enabled after searching with IMEI {valid_imei}"
            )
        self.click_new_ota_button()
        logger.info("Step 4: Clicked New OTA button")

        # Step 5: Search for specific command
        self.search_command_in_manual_ota(command_to_search)
        logger.info("Step 5: Searched for command: %s", command_to_search)

        # Step 6: Select checkbox for the command
        if self.get_size_of_checkbox_list() <= 0:
            raise AssertionError("No checkboxes found after searching for command")

        if self.get_size_of_checkbox_list() == 1:
            # Single checkbox found for the searched command
            if not self.is_checkbox_for_command_selected():
                self.select_checkbox_for_command()
                logger.info(
                    "Step 6: Selected checkbox for command: %s", command_to_search
                )
            else:
                logger.info(
                    "Step 6: Checkbox already selected for command: %s",
                    command_to_search,
                )

        if self.get_size_of_checkbox_list() > 1:
            final_searched_command = self.page.locator(
                f"//div[contains(@class,'mdc-form-field')]//label[normalize-space()='{command_to_search}']"
            )

            final_searched_command.wait_for(state="visible", timeout=5000)

            actual_text = final_searched_command.inner_text().strip()

            if actual_text == command_to_search:

                final_searched_command.click()

                logger.info(
                    "Step 6: selected searched command data for command : %s",
                    command_to_search,
                )

        else:
            raise AssertionError(
                f"Expected 1 checkbox after searching for '{command_to_search}', found {self.get_size_of_checkbox_list()}"
            )

        # Step 7: Verify Set Batch button is now enabled
        if not self.is_set_batch_button_enabled():
            raise AssertionError(
                "Set Batch button should be enabled after selecting a command checkbox"
            )
        logger.info("Step 7: Set Batch button is enabled - workflow complete")

    def is_submit_button_on_set_configuration_visible(self) -> bool:
        logger.debug(
            "Checking visibility of Submit button on Set Configuration component"
        )
        submit_button = self.page.locator("button:has-text('Submit')")
        return submit_button.is_visible()

    def click_submit_button_on_set_configuration(self) -> None:
        logger.debug("Clicking Submit button on Set Configuration component")
        submit_button = self.page.locator("button:has-text('Submit')")
        submit_button.wait_for(state="visible")
        submit_button.click()
        # # accept alert if it appears
        # try:
        #     self.page.wait_for_event("dialog", timeout=3000)
        #     dialog = self.page.on("dialog")
        #     dialog.accept()
        #     logger.info(
        #         "Accepted alert dialog after clicking Submit on Set Configuration"
        #     )
        # except Exception as e:
        #     logger.debug("No alert dialog appeared after clicking Submit: %s", str(e))

    def is_abort_button_visible(self) -> bool:
        logger.debug("Checking visibility of Abort button on Manual OTA page")
        abort_button = self.page.locator("button:has-text('ABORT')")
        return abort_button.is_visible()

    def is_ota_history_component_visible(self) -> bool:
        logger.debug("Checking visibility of OTA History component")
        ota_history_component = self.page.locator("h6:has-text('OTA History')")
        return ota_history_component.is_visible()

    def get_ota_history_table_headers(self) -> list[str]:
        logger.debug("Retrieving OTA History table headers")
        table = TableSection(self.page)
        return table.get_headers()

    def get_first_row_data_from_ota_history(self) -> dict[str, str]:
        logger.debug("Retrieving first row data from OTA History table")
        # Find all tables on the page
        all_tables = self.page.locator("table")
        table_count = all_tables.count()
        logger.debug(f"Found {table_count} tables on the page")

        # Find the OTA History table by checking headers
        for i in range(table_count):
            table = all_tables.nth(i)
            headers_in_table = table.locator("thead th")

            if headers_in_table.count() > 0:
                first_header = headers_in_table.first.inner_text().strip()
                logger.debug(f"Table {i} first header: {first_header}")

                # OTA History table should have "BATCH ID" as first header
                if "BATCH" in first_header.upper():
                    logger.debug(f"Found OTA History table at index {i}")
                    # Extract headers
                    headers = [
                        headers_in_table.nth(j).inner_text().strip()
                        for j in range(headers_in_table.count())
                    ]

                    # Extract first row data
                    rows = table.locator("tbody tr")
                    if rows.count() > 0:
                        cells = rows.first.locator("td")
                        row_data = {
                            headers[j]: cells.nth(j).inner_text().strip()
                            for j in range(cells.count())
                        }
                        logger.debug(f"OTA History first row data: {row_data}")
                        return row_data

        raise Exception("OTA History table not found on page")

    def is_export_button_visible_on_ota_history(self) -> bool:
        logger.debug("Checking visibility of Export button on OTA History component")
        export_button = self.page.locator("button:has-text('Export download')")
        return export_button.is_visible()

    def click_export_button_on_ota_history(self) -> None:
        logger.debug("Clicking Export button on OTA History component")
        export_button = self.page.locator("button:has-text('Export download')")
        export_button.wait_for(state="visible")

        # Set up dialog handler to accept any dialogs that appear during download
        def handle_dialog(dialog):
            logger.info(
                "Dialog appeared with message: %s, accepting it", dialog.message
            )
            dialog.accept()

        self.page.once("dialog", handle_dialog)

        with self.page.expect_download() as download_info:
            export_button.click()

        download = download_info.value
        logger.info("Export button clicked, waiting for download to complete")
        download_path = Path(DOWNLOADS_PATH) / download.suggested_filename
        download.save_as(str(download_path))
        logger.info("Download completed and saved to: %s", download_path)

    def verify_pagination_on_manual_ota_history(self) -> dict:
        logger.debug("Verifying pagination on Manual OTA History component")
        pagination = PaginationHelper(
            self.page,
            content_selector=self.page.locator("div.component-body table").last,
            max_forward_steps=5,
        )
        return pagination.verify()
