from faker.generator import random

from pages.common_utils.table_section import TableSection
from pages.common_utils.search import SearchHelper
from utils.logger import get_logger
import re
from pages.common_base_page import BasePage
from utils.helpers import Helpers

logger = get_logger(__name__)


class GovtServerPage(BasePage):
    def __init__(self, page):
        self.page = page

    def get_page_title(self):
        """Get the title of the Government Server page"""
        title = super().get_title()
        logger.debug("Retrieved Government Server page title: %s", title)
        return title

    def get_component_title(self):
        """Get the title of the Government Server component"""
        component_title = super().get_component_title()
        logger.debug("Retrieved Government Server component title: %s", component_title)
        return component_title

    def get_table_headers(self):
        """Get the headers of the table on the Government Server page"""
        table = TableSection(self.page)
        if table.has_no_data():
            logger.warning(
                "Government Server table has no data, cannot retrieve headers"
            )
            return []

        headers = table.get_headers()
        logger.debug("Retrieved Government Server table headers: %s", headers)
        return headers

    def is_add_govt_server_button_visible_and_enabled(self):
        """Check if the 'Add Government Server' button is visible and enabled"""
        button_locator = self.page.get_by_text("Add Government Server")
        is_visible = button_locator.is_visible()
        is_enabled = button_locator.is_enabled()
        logger.debug(
            "'Add Government Server' button visibility: %s, enabled state: %s",
            is_visible,
            is_enabled,
        )
        return is_visible, is_enabled

    def click_add_govt_server_button(self):
        """Click the 'Add Government Server' button"""
        button_locator = self.page.get_by_text("Add Government Server")
        if button_locator.is_visible() and button_locator.is_enabled():
            button_locator.click()
            self.page.wait_for_url("**/govt-servers-add")
            self.page.wait_for_load_state("networkidle")
            logger.info("Clicked 'Add Government Server' button")
        else:
            logger.error(
                "'Add Government Server' button is not clickable. Visible: %s, Enabled: %s",
                button_locator.is_visible(),
                button_locator.is_enabled(),
            )
            raise Exception("'Add Government Server' button is not clickable")

    def get_input_fields_locators(self):
        return {
            "state": self.page.locator("input[formcontrolname='state']"),
            "stateCode": self.page.locator("input[formcontrolname='stateCode']"),
            "govtIp1": self.page.locator("input[formcontrolname='govtIp1']"),
            "port1": self.page.locator("input[formcontrolname='port1']"),
            "govtIp2": self.page.locator("input[formcontrolname='govtIp2']"),
            "port2": self.page.locator("input[formcontrolname='port2']"),
            "stateEnable": self.page.locator("input[formcontrolname='stateEnable']"),
        }

    def get_valid_invalid_inputs_for_field(self):
        """
        Return dictionary containing invalid inputs and expected error messages
        for each field.

        Format:
        {
            "field_name": [
                ("invalid_input", "expected_error_message"),
            ]
        }
        """

        return {
            "state": [
                (
                    " ",
                    "This field is required and can't be only spaces.",
                ),
                (
                    f"invalid_{Helpers.generate_random_state_name()}",
                    "Only alphabets and spaces are allowed.",
                ),
                (
                    Helpers.generate_random_number(5),
                    "Only alphabets and spaces are allowed.",
                ),
                (
                    "@#$%",
                    "Only alphabets and spaces are allowed.",
                ),
                (
                    f" {Helpers.generate_random_string(5)}",
                    "Remove leading or trailing spaces.",
                ),
                (
                    f"{Helpers.generate_random_string(5)} ",
                    "Remove leading or trailing spaces.",
                ),
            ],
            "stateCode": [
                (
                    " ",
                    "This field is required and can't be only spaces.",
                ),
                (
                    f"invalid_{Helpers.generate_random_state_abbreviation()}",
                    "Only alphabets and spaces are allowed.",
                ),
                (
                    Helpers.generate_random_number(5),
                    "Only alphabets and spaces are allowed.",
                ),
                (
                    "@#$%",
                    "Only alphabets and spaces are allowed.",
                ),
                (
                    f" {Helpers.generate_random_string(3)}",
                    "Remove leading or trailing spaces.",
                ),
                (
                    f"{Helpers.generate_random_string(3)} ",
                    "Remove leading or trailing spaces.",
                ),
            ],
            "govtIp1": [
                # (
                #     f"invalid_{Helpers.generate_random_ip()}",
                #     "Please enter a valid IP Address.",
                # ),
                # (
                #     f" {Helpers.generate_random_ip()}QW@#@#$",
                #     "Please enter a valid IP Address.",
                # ),
                (
                    f"{Helpers.generate_random_ip() + Helpers.generate_random_ip()}",
                    "Maximum 20 characters allowed.",
                ),
            ],
            "port1": [
                (
                    " ",
                    "Enter a valid port number (1-65535).",
                ),
                (
                    f"invalid_{Helpers.generate_random_number(5)}",
                    "Enter a valid port number (1-65535).",
                ),
                (
                    "#@!$!@#",
                    "Enter a valid port number (1-65535).",
                ),
                (
                    Helpers.generate_random_number(10),
                    "Enter a valid port number (1-65535).",
                ),
                (
                    "0",
                    "Enter a valid port number (1-65535).",
                ),
                (
                    "65536",
                    "Enter a valid port number (1-65535).",
                ),
            ],
            "govtIp2": [
                # (
                #     f"invalid_{Helpers.generate_random_ip()}",
                #     "Please enter a valid IP Address.",
                # ),
                # (
                #     f" {Helpers.generate_random_ip()}QW@#@#$",
                #     "Please enter a valid IP Address.",
                # ),
                (
                    f"{Helpers.generate_random_ip() + Helpers.generate_random_ip()}",
                    "Maximum 20 characters allowed.",
                ),
            ],
            "port2": [
                (
                    " ",
                    "Enter a valid port number (1-65535).",
                ),
                (
                    f"invalid_{Helpers.generate_random_number(5)}",
                    "Enter a valid port number (1-65535).",
                ),
                (
                    "#@!$!@#",
                    "Enter a valid port number (1-65535).",
                ),
                (
                    Helpers.generate_random_number(10),
                    "Enter a valid port number (1-65535).",
                ),
                (
                    "0",
                    "Enter a valid port number (1-65535).",
                ),
                (
                    "65536",
                    "Enter a valid port number (1-65535).",
                ),
            ],
            "stateEnable": [
                (
                    " ",
                    "Please enter a valid State Enable.",
                ),
                (
                    "invalid_input",
                    "Please enter a valid State Enable.",
                ),
                (
                    "#@!$!@#",
                    "Please enter a valid State Enable.",
                ),
            ],
        }

    def enter_valid_input_for_field(self):
        return {
            "state": Helpers.generate_random_state_name(),
            "stateCode": Helpers.generate_random_state_abbreviation(),
            "govtIp1": Helpers.generate_random_ip(),
            "port1": random.randint(1, 65535),
            "govtIp2": Helpers.generate_random_ip(),
            "port2": random.randint(1, 65535),
            "stateEnable": "true",
        }

    def get_error_message_from_field(self, field_name):
        """Get error message displayed for specific field"""

        field_locator = self.get_input_fields_locators()[field_name]

        error_locator = field_locator.locator(
            "xpath=ancestor::mat-form-field//mat-error"
        )

        try:
            error_locator.first.wait_for(state="visible", timeout=3000)

            error_message = error_locator.first.inner_text().strip()

            logger.debug(
                "Retrieved error message for field '%s': %s",
                field_name,
                error_message,
            )

            return error_message

        except Exception:
            logger.debug(
                "No visible error message found for field '%s'",
                field_name,
            )

            return None

    def click_submit_button(self):
        """Click Submit button"""

        submit_button = self.page.get_by_role("button", name="Submit")

        submit_button.wait_for(state="visible")

        submit_button.click(force=True)
        self.page.wait_for_load_state("networkidle")

        logger.info("Clicked Submit button and waited for page activity to settle")

    def click_outside_to_get_error_msg(self):
        component_title = self.page.locator("h6.component-title")
        component_title.click()

    def is_submit_button_enabled(self):
        """Check whether Submit button is enabled"""

        submit_button = self.page.get_by_role("button", name="Submit")

        submit_button.wait_for(state="visible")

        is_enabled = submit_button.is_enabled()

        logger.debug(
            "Submit button enabled state: %s",
            is_enabled,
        )

        return is_enabled

    def get_success_message(self):
        """Get success message displayed after form submission"""

        success_message_locator = self.page.locator("simple-snack-bar").filter(
            has_text="Data Fetched Successfully"
        )

        success_message_locator.wait_for(state="visible")

        success_message = success_message_locator.first.inner_text().strip()

        logger.info(
            "Retrieved success message: %s",
            success_message,
        )

        return success_message

    def search_server(self, server_name):
        """Search for a specific server"""

        search_helper = SearchHelper(self.page)

        response = search_helper.run_search(server_name)

        logger.info(
            "Result of searched row is -> %s",
            response["results"],
        )

        return response

    def get_view_button(self):
        """Get view button locator"""

        return self.page.get_by_text("visibility").first

    def click_view_button(self):
        """Click on view button"""

        logger.info("Clicking on view button")

        view_button = self.get_view_button()

        view_button.click()

        self.page.wait_for_load_state("networkidle")

    def click_refresh_button(self):
        """Click on refresh button in the header"""
        logger.info("Clicking on refresh button in the header")
        refresh_btn = self.page.locator("//mat-icon[normalize-space()='refresh']").first
        refresh_btn.click()
        self.page.wait_for_load_state("networkidle")

    def get_page_title_on_view_page(self):
        """Get page title on view page"""

        page_title = self.page.locator("span.page-title")
        page_title.wait_for(state="visible", timeout=5000)

        return page_title.inner_text().strip()

    def is_firmware_master_button_visible_and_enabled(self):
        """Check if the 'Firmware Master' button is visible and enabled"""
        button_locator = self.page.get_by_text("Firmware Master")
        is_visible = button_locator.is_visible()
        is_enabled = button_locator.is_enabled()
        logger.debug(
            "'Firmware Master' button visibility: %s, enabled state: %s",
            is_visible,
            is_enabled,
        )
        return is_visible, is_enabled

    def click_firmware_master_button(self):
        """Click the 'Firmware Master' button"""
        button_locator = self.page.get_by_text("Firmware Master")

        try:
            # Wait briefly for the button to appear
            button_locator.first.wait_for(state="visible", timeout=10000)

            # Prefer a normal click when enabled, otherwise attempt a forced click
            if button_locator.first.is_enabled():
                button_locator.first.click()
            else:
                logger.warning(
                    "Firmware Master button visible but not enabled, attempting forced click"
                )
                button_locator.first.click(force=True)

            # Wait for navigation/load to settle
            try:
                self.page.wait_for_url("**/firmware-master", timeout=10000)
            except Exception:
                logger.debug(
                    "No navigation to firmware-master URL after click; continuing to wait for networkidle"
                )

            self.page.wait_for_load_state("networkidle")
            logger.info("Clicked 'Firmware Master' button")

        except Exception as exc:
            # Log diagnostics to help debugging locator timeouts
            try:
                count = button_locator.count()
                texts = button_locator.all_inner_texts()
            except Exception:
                count = "<failed-to-evaluate>"
                texts = "<failed-to-evaluate>"

            logger.error(
                "Failed to click 'Firmware Master' button: %s; locator count=%s; texts=%s",
                exc,
                count,
                texts,
            )

            # Fallback: if locator not present, attempt direct navigation to firmware-master route
            if count == 0:
                try:
                    target = self.page.url.rstrip("/") + "/firmware-master"
                    logger.info("Attempting direct navigation to %s", target)
                    self.page.goto(target, wait_until="networkidle", timeout=15000)
                    self.page.wait_for_load_state("networkidle")
                    logger.info("Direct navigation to firmware-master succeeded")
                    return
                except Exception as nav_exc:
                    logger.error(
                        "Direct navigation to firmware-master failed: %s", nav_exc
                    )

            raise

    def get_oc_firmware_list_from_ui(self):
        """Get available OC firmware list from Firmware Master List table"""

        logger.info("Clicking Add Open CPU Firmware button")

        self.page.get_by_text("Add Open CPU Firmware").click()

        self.page.wait_for_load_state("networkidle")
        self.page.locator("//h6[normalize-space()='Firmware Master List']").wait_for(
            state="visible", timeout=10000
        )

        firmware_cells = self.page.locator(
            "//h6[normalize-space()='Firmware Master List']"
            "/ancestor::div[contains(@class,'component-container')]"
            "//table/tbody/tr/td[3]"
        )

        firmware_list = [
            firmware.strip()
            for firmware in firmware_cells.all_inner_texts()
            if firmware.strip()
        ]

        logger.info(
            "Total firmwares found in UI: %s",
            len(firmware_list),
        )

        logger.info(
            "Firmware list extracted from UI: %s",
            firmware_list,
        )

        return sorted(firmware_list)

    def click_on_add_open_cpu_firmware_button(self):
        logger.info("Clicking on the add open cpu firmware button")
        self.page.get_by_text("Add Open CPU Firmware").click()
        self.page.wait_for_load_state("networkidle")
        self.page.locator("//h6[normalize-space()='Firmware Master List']").wait_for(
            state="visible", timeout=10000
        )

    def search_respective_server(self):
        """Search for a specific server"""
        # if "sampark-qa" in self.page.url:
        state_name = "SURAJ"
        # else:
        #     state_name = "Shital"

        # Search server
        logger.info("Searching server with state name: %s", state_name)

        searched_response = self.search_server(state_name)

        # Open View Page
        self.click_view_button()
        self.page.wait_for_load_state("networkidle")

        logger.debug("Search response: %s", searched_response)

    def get_oc_firmware_master_list_from_ui(self):
        """Get OC firmware master list from UI"""

        logger.info("Clicking Add Open CPU Firmware button")

        self.page.get_by_text("Add Open CPU Firmware").click()

        self.page.wait_for_load_state("networkidle")
        self.page.locator("//h6[normalize-space()='Firmware Master List']").wait_for(
            state="visible", timeout=10000
        )

        firmware_master_list = []

        rows = self.page.locator(
            "//h6[normalize-space()='Firmware Master List']"
            "/ancestor::div[contains(@class,'component-container')]"
            "//table/tbody/tr"
        )

        row_count = rows.count()

        logger.info(
            "Total rows found in Firmware Master List table: %s",
            row_count,
        )

        for i in range(row_count):
            firmware_name = rows.nth(i).locator("td").nth(1).inner_text().strip()

            if firmware_name:
                firmware_master_list.append(firmware_name)

        logger.info(
            "Firmware Master List extracted from UI: %s",
            firmware_master_list,
        )

        return sorted(firmware_master_list)

    def validate_open_cpu_firmware_checkboxes_default_state(self):
        """
        Validate all firmware checkboxes are present and unchecked by default.

        Returns:
            dict: Validation result details
        """

        logger.info("Opening Open CPU Firmware Master List")

        # wait for button to be visible and enabled before clicking
        self.page.get_by_text("Add Open CPU Firmware").wait_for(
            state="visible", timeout=10000
        )
        self.page.get_by_text("Add Open CPU Firmware").click()

        self.page.wait_for_load_state("networkidle")
        self.page.locator("//h6[normalize-space()='Firmware Master List']").wait_for(
            state="visible", timeout=10000
        )

        firmware_rows = self.page.locator(
            "//h6[normalize-space()='Firmware Master List']"
            "/ancestor::div[contains(@class,'component-container')]"
            "//table/tbody/tr"
        )

        firmware_rows.first.wait_for(state="visible")

        total_rows = firmware_rows.count()

        logger.info(
            "Total firmware rows found: %s",
            total_rows,
        )

        checked_checkbox_indexes = []

        for index in range(total_rows):
            checkbox = firmware_rows.nth(index).locator("input[type='checkbox']")

            if checkbox.is_checked():
                checked_checkbox_indexes.append(index + 1)

        logger.info(
            "Checked checkbox indexes: %s",
            checked_checkbox_indexes,
        )

        result = {
            "total_checkboxes": total_rows,
            "checked_checkbox_indexes": checked_checkbox_indexes,
            "all_unchecked": len(checked_checkbox_indexes) == 0,
        }

        logger.info(
            "Checkbox validation result: %s",
            result,
        )

        return result

    def select_open_cpu_firmware_checkbox_by_index(self, index):
        """
        Select Open CPU firmware checkbox by index (1-based index)

        Args:
            index (int): 1-based index of the checkbox to select

        Returns:
            bool: True if checkbox is selected successfully, False otherwise
        """

        logger.info(
            "Selecting Open CPU firmware checkbox at index: %s",
            index,
        )

        firmware_rows = self.page.locator(
            "//h6[normalize-space()='Firmware Master List']"
            "/ancestor::div[contains(@class,'component-container')]"
            "//table/tbody/tr"
        )

        firmware_rows.first.wait_for(state="visible")

        total_rows = firmware_rows.count()

        if index < 1 or index > total_rows:
            logger.error(
                "Invalid checkbox index: %s. Total firmware rows available: %s",
                index,
                total_rows,
            )
            return False

        checkbox_to_select = firmware_rows.nth(index - 1).locator(
            "input[type='checkbox']"
        )
        checkbox_to_select.wait_for(state="visible")

        if not checkbox_to_select.is_checked():
            try:
                checkbox_to_select.check(force=True)
            except Exception as exc:
                logger.warning(
                    "checkbox_to_select.check() failed at index %s: %s. Falling back to JS click/set.",
                    index,
                    exc,
                )

                # Fallback: use element handle to set checked property and dispatch events
                try:
                    handle = checkbox_to_select.element_handle()
                    if handle:
                        self.page.evaluate(
                            "(el) => { el.click(); el.checked = true; el.dispatchEvent(new Event('change', { bubbles: true })); }",
                            handle,
                        )
                except Exception as exc2:
                    logger.exception(
                        "Fallback JS check failed for checkbox at index %s: %s",
                        index,
                        exc2,
                    )

            # Verify checkbox state
            try:
                if not checkbox_to_select.is_checked():
                    logger.error("Checkbox at index %s did not become checked", index)
                    return False
            except Exception:
                logger.error("Unable to verify checkbox state at index %s", index)
                return False

            logger.info(
                "Checkbox at index %s selected successfully",
                index,
            )
            return True

        logger.info(
            "Checkbox at index %s is already selected",
            index,
        )
        return True

    def get_open_cpu_firmware_name_by_index(self, index):
        rows = self.page.locator(
            "//h6[normalize-space()='Firmware Master List']"
            "/ancestor::div[contains(@class,'component-container')]"
            "//table/tbody/tr"
        )

        if index < 1 or index > rows.count():
            logger.error(
                "Invalid firmware row index: %s. Total rows available: %s",
                index,
                rows.count(),
            )
            return ""

        row_text = rows.nth(index - 1).inner_text().strip()

        logger.info(
            "Row %s text: %s",
            index,
            row_text,
        )

        cols = row_text.split("\t")

        logger.info(
            "Columns extracted: %s",
            cols,
        )

        firmware_name = cols[1].strip() if len(cols) > 1 else ""

        logger.info(
            "Firmware name extracted: %s",
            firmware_name,
        )

        return firmware_name

    def is_firmware_present_in_open_cpu_list(self, firmware_name):
        """
        Check if a specific firmware is present in the Open CPU Firmware Master List.

        Args:
            firmware_name (str): Name of the firmware to check

        Returns:
            bool: True if firmware is present, False otherwise
        """

        logger.info(
            "Checking presence of firmware '%s' in Open CPU Firmware Master List",
            firmware_name,
        )

        candidate_locators = [
            # Open CPU Firmware List table (Column 2 and 3)
            self.page.locator(".component-container")
            .filter(has=self.page.get_by_text("Open CPU Firmware List"))
            .locator("table tbody tr td:nth-child(2)"),
            self.page.locator(".component-container")
            .filter(has=self.page.get_by_text("Open CPU Firmware List"))
            .locator("table tbody tr td:nth-child(3)"),
            # Firmware Master List table (Column 2 and 3)
            self.page.locator(".component-container")
            .filter(has=self.page.get_by_text("Firmware Master List"))
            .locator("table tbody tr td:nth-child(2)"),
            self.page.locator(".component-container")
            .filter(has=self.page.get_by_text("Firmware Master List"))
            .locator("table tbody tr td:nth-child(3)"),
        ]

        seen_firmware_names = []
        for index_loc, loc in enumerate(candidate_locators):
            try:
                # Read all texts in one go to avoid per-locator timeouts
                texts = loc.all_inner_texts()
            except Exception as exc:
                logger.warning(
                    "Failed to read candidate locator at index %s: %s", index_loc, exc
                )
                texts = []

            logger.debug(
                "Checking locator index %s with %s candidate firmware names",
                index_loc,
                len(texts),
            )

            for index, raw_text in enumerate(texts):
                current_firmware_name = raw_text.strip()
                seen_firmware_names.append(current_firmware_name)

                # Skip common header-like labels
                if current_firmware_name.lower() in (
                    "firmware type",
                    "open cpu",
                    "firmware",
                ):
                    continue

                # Use case-insensitive substring match to be robust to formatting
                if firmware_name.lower() in current_firmware_name.lower():
                    logger.info(
                        "Firmware '%s' found in the list at locator index %s row %s",
                        firmware_name,
                        index_loc,
                        index + 1,
                    )
                    return True

        logger.info(
            "Firmware '%s' not found in any candidate list. Seen firmware names: %s",
            firmware_name,
            seen_firmware_names,
        )
        return False

    def get_open_cpu_firmware_version_by_index(self, index):
        rows = self.page.locator(
            "//h6[normalize-space()='Firmware Master List']"
            "/ancestor::div[contains(@class,'component-container')]"
            "//table/tbody/tr"
        )

        row_text = rows.nth(index).inner_text().strip()

        logger.info(
            "Row %s text: %s",
            index,
            row_text,
        )

        cols = row_text.split("\t")

        logger.info(
            "Columns extracted: %s",
            cols,
        )

        firmware_version = cols[2].strip()

        logger.info(
            "Firmware version extracted: %s",
            firmware_version,
        )

        return firmware_version

    def get_device_firmware_master_list_from_ui(self):
        """Get Device firmware master list from UI"""

        logger.info("Opening Device Firmware Master List")

        add_device_firmware_button = self.page.get_by_role(
            "button", name="Add Device Firmware"
        )
        add_device_firmware_button.wait_for(state="visible", timeout=15000)
        add_device_firmware_button.click()

        self.page.wait_for_load_state("networkidle")

        device_firmware_container = self.page.locator(
            "//button[normalize-space()='Add Device Firmware']"
            "/ancestor::div[contains(@class,'component-container')]"
        )

        rows = device_firmware_container.locator(".//table/tbody/tr")

        try:
            rows.first.wait_for(state="visible", timeout=20000)
        except Exception:
            logger.warning(
                "Device Firmware Master List rows did not appear within 20s; trying a broader fallback."
            )
            rows = self.page.locator(
                "//table[contains(., 'Device Firmware Master List')]/tbody/tr"
            )
            try:
                rows.first.wait_for(state="visible", timeout=10000)
            except Exception:
                logger.warning(
                    "Fallback row selector did not become visible; checking for checkboxes in the same component."
                )
                checkbox_rows = self.page.locator(
                    "//button[normalize-space()='Add Device Firmware']"
                    "/ancestor::div[contains(@class,'component-container')]"
                    "//input[@type='checkbox']"
                )
                try:
                    checkbox_rows.first.wait_for(state="visible", timeout=10000)
                    logger.info(
                        "Found %s checkboxes in Device Firmware Master List fallback.",
                        checkbox_rows.count(),
                    )
                except Exception:
                    logger.error(
                        "Device Firmware Master List content did not appear after fallback waits."
                    )
                return []

        firmware_master_list = []

        row_count = rows.count()

        logger.info(
            "Total rows found in Device Firmware Master List table: %s",
            row_count,
        )

        for i in range(row_count):
            firmware_name = rows.nth(i).locator("td").nth(1).inner_text().strip()

            if firmware_name:
                firmware_master_list.append(firmware_name)

        logger.info(
            "Device Firmware Master List extracted from UI: %s",
            firmware_master_list,
        )

        return sorted(firmware_master_list)

    def validate_device_firmware_checkboxes_default_state(self):
        """
        Validate all firmware checkboxes are present and unchecked by default in Device Firmware Master List.

        Returns:
            dict: Validation result details
        """

        logger.info("Opening Device Firmware Master List")

        self.page.get_by_text("Add Device Firmware").click()

        self.page.wait_for_load_state("networkidle")
        self.page.locator("input[type='checkbox']").first.wait_for(
            state="visible", timeout=10000
        )

        checkboxes = self.page.locator("input[type='checkbox']")

        checkboxes.first.wait_for(state="visible")

        total_checkboxes = checkboxes.count()

        logger.info(
            "Total firmware checkboxes found: %s",
            total_checkboxes,
        )

        checked_checkbox_indexes = []

        for index in range(total_checkboxes):
            checkbox = checkboxes.nth(index)

            if checkbox.is_checked():
                checked_checkbox_indexes.append(index + 1)

        logger.info(
            "Checked checkbox indexes: %s",
            checked_checkbox_indexes,
        )

        result = {
            "total_checkboxes": total_checkboxes,
            "checked_checkbox_indexes": checked_checkbox_indexes,
            "all_unchecked": len(checked_checkbox_indexes) == 0,
        }

        logger.info(
            "Checkbox validation result: %s",
            result,
        )

        return result

    def select_device_firmware_checkbox_by_index(self, index):
        """
        Select Device firmware checkbox by index (1-based index)

        Args:
            index (int): 1-based index of the checkbox to select

        Returns:
            bool: True if checkbox is selected successfully, False otherwise
        """

        logger.info(
            "Selecting Device firmware checkbox at index: %s",
            index,
        )

        checkboxes = self.page.locator("input[type='checkbox']")

        total_checkboxes = checkboxes.count()

        if index < 1 or index > total_checkboxes:
            logger.error(
                "Invalid checkbox index: %s. Total checkboxes available: %s",
                index,
                total_checkboxes,
            )
            return False

        checkbox_to_select = checkboxes.nth(index - 1)

        if not checkbox_to_select.is_checked():
            try:
                checkbox_to_select.check()
            except Exception as exc:
                logger.warning(
                    "checkbox_to_select.check() failed at index %s: %s. Falling back to JS click/set.",
                    index,
                    exc,
                )
                try:
                    handle = checkbox_to_select.element_handle()
                    if handle:
                        self.page.evaluate(
                            "(el) => { el.click(); el.checked = true; el.dispatchEvent(new Event('change', { bubbles: true })); }",
                            handle,
                        )
                except Exception:
                    logger.exception(
                        "Fallback JS check failed for device firmware checkbox at index %s",
                        index,
                    )

            # Verify checkbox state
            if not checkbox_to_select.is_checked():
                logger.error("Checkbox at index %s did not become checked", index)
                return False

            logger.info(
                "Checkbox at index %s selected successfully",
                index,
            )
            return True
        else:
            logger.info(
                "Checkbox at index %s is already selected",
                index,
            )
            return True

    def validate_add_firmware_master_title(self):
        """Validate title on Add Firmware Master page"""

        title_locator = self.page.locator("span.page-title")

        title_locator.wait_for(state="visible")

        title_text = title_locator.inner_text().strip()

        logger.info(
            "Retrieved title on Add Firmware Master page: %s",
            title_text,
        )

        return title_text

    def get_firmware_master_table_headers(self):
        """Get headers of the table on Firmware Master page"""

        try:
            self.page.locator("table thead th, th").first.wait_for(state="attached", timeout=5000)
        except Exception:
            pass

        table = TableSection(self.page)
        headers = table.get_headers()

        if not headers:
            # Fallback direct locator
            header_locs = self.page.locator("table thead th, th").all()
            headers = [loc.inner_text() for loc in header_locs if loc.inner_text().strip()]

        # Normalize headers: uppercase, collapse whitespace and replace newlines
        normalized = []
        for h in headers:
            txt = h.replace("\n", " ")
            txt = re.sub(r"\s+", " ", txt).strip().upper()
            normalized.append(txt)

        logger.debug(
            "Retrieved Firmware Master table headers (normalized): %s",
            normalized,
        )

        return normalized


    def is_add_firmware_button_visible_and_enabled(self):
        """Check if the 'Add Firmware' button is visible and enabled on Firmware Master page"""

        button_locator = self.page.get_by_text("Add Firmware")

        is_visible = button_locator.is_visible()
        is_enabled = button_locator.is_enabled()
        logger.debug(
            "'Add Firmware' button visibility: %s, enabled state: %s",
            is_visible,
            is_enabled,
        )

        return is_visible, is_enabled

    def get_add_firmware_form_title(self):
        """Get title of the form displayed after clicking 'Add Firmware' button"""

        title_locator = self.page.locator("span.page-title")

        title_locator.wait_for(state="visible")

        title_text = title_locator.inner_text().strip()

        logger.info(
            "Retrieved title on Add Firmware form: %s",
            title_text,
        )

        return title_text

    def click_add_firmware_button(self):
        """Click the 'Add Firmware' button and wait for the form to appear."""
        button_locator = self.page.get_by_text("Add Firmware")

        if button_locator.is_visible() and button_locator.is_enabled():
            button_locator.click()
            title_locator = self.page.locator("span.page-title")
            title_locator.wait_for(state="visible")
            self.page.wait_for_load_state("networkidle")
            logger.info("Clicked 'Add Firmware' button and opened Add Firmware form")
        else:
            logger.error(
                "'Add Firmware' button is not clickable. Visible: %s, Enabled: %s",
                button_locator.is_visible(),
                button_locator.is_enabled(),
            )
            raise Exception("'Add Firmware' button is not clickable")

    def get_input_fields_on_add_firmware_details(self):
        """Get the input fields displayed on the Add Firmware form."""

        form_title_locator = self.page.locator("span.page-title")
        form_title_locator.wait_for(state="visible")
        logger.info(
            "Locating Add Firmware input fields on form with title: %s",
            form_title_locator.inner_text().strip(),
        )

        return {
            "firmware_name": self.page.locator("input[id='firmwareName']"),
            "description": self.page.locator("input[id='description']"),
            "file": self.page.locator("input[formcontrolname='fileName']"),
            "release_date": self.page.locator("input[formcontrolname='releaseDate']"),
            "device_type": self.page.locator(
                "mat-select[formcontrolname='firmwareType']"
            ),
        }
