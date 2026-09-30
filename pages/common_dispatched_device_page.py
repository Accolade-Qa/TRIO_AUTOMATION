import os

from click import Path

from config.global_var import DOWNLOADS_PATH
from utils.logger import get_logger
from pages.common_utils.table_section import TableSection
from pages.common_base_page import BasePage

logger = get_logger(__name__)


class DispatchedDevicePage:
    def __init__(self, page):
        logger.debug("Initializing Dispatched Devices Page with page object")
        self.page = page
        logger.info("DispatchedDevicePage initialized successfully")

    def go_to_dispatcheddevicepage(self, url):
        logger.info("Navigating to Dispatched Device page: %s", url)
        self.page.goto(url)
        self.page.wait_for_load_state("networkidle")
        logger.info("Navigation to Dispatched Device page completed: %s", url)

    def is_page_loaded(self):
        logger.debug("Checking if Dispatched Device page is loaded")
        return self.page.url.endswith("/dispatched-devices")

    def is_manual_upload_button_visible(self):
        logger.debug("Checking visibility of Manual Upload button")
        manual_upload = self.page.locator("//div[@class='page-header']//button[1]")
        return manual_upload.is_visible()

    def is_bulk_upload_button_visible(self):
        logger.debug("Checking visibility of Bulk Upload button")
        bulk_upload = self.page.locator("//div[@class='page-header']//button[2]")
        return bulk_upload.is_visible()

    def is_checkbox_visible(self):
        logger.debug("Checking visibility of checkbox in Dispatched Device page")
        checkbox = self.page.locator("span:has-text('Select Customer')")
        return checkbox.is_visible()

    def is_view_actions_button_visible(self):
        logger.debug("Checking visibility of View Actions button")
        view_actions = (
            self.page.locator("mat-icon").filter(has_text="visibility").last()
        )
        return view_actions.is_visible()

    def is_delete_action_button_visible(self):
        logger.debug("Checking visibility of Delete Action button")
        delete_action = self.page.locator("mat-icon").filter(has_text="delete").last()
        return delete_action.is_visible()

    def is_dispatched_device_table_visible(self):
        logger.debug("Checking visibility of Dispatched Device table")
        table = self.page.locator("//div[@class='component-body']")
        return table.is_visible()

    def is_search_box_visible(self):
        logger.debug("Checking visibility of Search box")
        search_box = self.page.get_by_placeholder("Search and Press Enter")
        return search_box.is_visible()

    def get_table_headers(self):
        logger.debug("Retrieving table headers from Dispatched Device page")
        table = TableSection(self.page)
        headers = table.get_headers()
        logger.info("Table headers retrieved: %s", headers)
        return headers

    def get_customer_list(self):
        logger.debug("Retrieving customer list from Select Customer dropdown")
        dropdown = self.page.locator("div.dropdown-placeholder-wrapper")
        dropdown.click()
        options = self.page.locator("div.list-items ul li").all_inner_texts()
        dropdown.press("Escape")
        logger.info("Customer list retrieved: %s", options)
        return options

    def get_customer_list_from_manual_upload(self):
        logger.debug(
            "Retrieving customer list from Select Customer dropdown in Manual Upload form"
        )
        dropdown = self.page.locator("mat-select[role='combobox']")
        dropdown.click()
        options = self.page.locator("mat-option span").all_inner_texts()
        dropdown.press("Escape")
        logger.info("Customer list retrieved from Manual Upload form: %s", options)
        return options

    def select_customer(self, customer_name):
        logger.debug("Selecting customer '%s' from dropdown", customer_name)
        dropdown = self.page.locator("mat-select[role='combobox']")
        dropdown.click()

        self.page.wait_for_selector("mat-option span", state="visible")

        option = self.page.locator(f"div mat-option span:has-text('{customer_name}')")
        option.click()
        logger.info("Customer '%s' selected from dropdown", customer_name)

    def select_customer_dispatched_device_page(self, customer_name):
        logger.debug(
            "Selecting customer '%s' from dropdown on dispatched device page",
            customer_name,
        )
        dropdown = self.page.locator("div.dropdown-placeholder-wrapper")
        dropdown.click()
        option = self.page.locator(f"div.list-items ul li:has-text('{customer_name}')")
        option.click()
        logger.info(
            "Customer '%s' selected from dropdown on dispatched device page",
            customer_name,
        )

    def is_select_customer_dropdown_visible(self):
        logger.debug("Checking visibility of Select Customer dropdown")
        dropdown = self.page.locator("mat-select[role='combobox']")
        return dropdown.is_visible()

    def click_manual_upload_button(self):
        logger.debug("Clicking Manual Upload button")
        manual_upload = self.page.locator("//div[@class='page-header']//button[1]")
        manual_upload.click()
        logger.info("Manual Upload button clicked")

    def get_manual_upload_page_title(self):
        base = BasePage(self.page)
        logger.debug("Retrieving Manual Upload page title")
        title = base.get_title()
        logger.info("Manual Upload page title retrieved: %s", title)
        return title

    def fill_uid_input(self, value):
        logger.debug("Filling UID input field with value: %s", value)
        uid_input = self.page.locator("input[id='uid']")
        uid_input.clear()
        uid_input.fill(value)
        logger.info("UID input field filled with value: %s", value)

    def clear_uid_input_and_click(self):
        logger.debug("Clearing UID input field")
        uid_input = self.page.locator("input[id='uid']")
        uid_input.click()
        uid_input.fill("")
        uid_input.press("Backspace")
        uid_input.blur()
        logger.info("UID input field cleared and blurred")

    def click_on_outside(self):
        logger.debug("Clicking on outside to trigger validation")
        out = self.page.locator("div.button-group")
        out.click()
        logger.info("Outside clicked to trigger validation")

    def get_uid_error_message(self):
        logger.debug("Retrieving UID field error message")
        error_message_element = self.page.locator(
            "//mat-form-field[.//input[@id='uid']]//mat-error"
        )
        try:
            error_message_element.first.wait_for(state="visible", timeout=3000)
        except Exception:
            pass
        error_message = (
            error_message_element.first.text_content().strip()
            if error_message_element.first.is_visible()
            else ""
        )
        logger.info("UID error message retrieved: %s", error_message)
        return error_message

    def fill_customer_part_number_input(self, value):
        logger.debug("Filling Customer Part Number input field with value: %s", value)
        cpn_input = self.page.locator("input[formcontrolname='customerPartNumber']")
        cpn_input.clear()
        cpn_input.fill(value)
        logger.info("Customer Part Number input field filled with value: %s", value)

    def clear_customer_part_number_input(self):
        logger.debug("Clearing Customer Part Number input field")
        cpn_input = self.page.locator("input[formcontrolname='customerPartNumber']")
        cpn_input.clear()
        logger.info("Customer Part Number input field cleared")

    def get_customer_part_number_error_message(self):
        logger.debug("Retrieving Customer Part Number field error message")
        error_message_element = self.page.locator(
            "//mat-error[contains(text(), '') or contains(text(), 'Remove')]"
        )
        error_message = (
            error_message_element.text_content().strip()
            if error_message_element.is_visible()
            else ""
        )
        logger.info("Customer Part Number error message retrieved: %s", error_message)
        return error_message

    def click_save_button_on_manual_upload_form(self):
        logger.debug("Clicking Save button on Manual Upload form")
        save_button = self.page.locator("//button[contains(text(), 'Submit')]")
        save_button.click()
        logger.info("Save button clicked on Manual Upload form")

    def is_save_button_disabled(self):
        logger.debug("Checking if Save button on Manual Upload form is disabled")
        save_button = self.page.locator("//button[contains(text(), 'Submit')]")
        is_disabled = save_button.is_disabled()
        logger.info("Save button disabled state: %s", is_disabled)
        return is_disabled

    def get_manual_upload_success_message(self):
        logger.debug("Retrieving success message after manual upload")
        success_message_element = self.page.locator("//simple-snack-bar").first
        success_message = (
            success_message_element.text_content().strip()
            if success_message_element.is_visible()
            else ""
        )
        logger.info("Manual upload success message retrieved: %s", success_message)
        return success_message

    def click_bulk_upload_button(self):
        logger.debug("Clicking Bulk Upload button for the first device in the table")
        bulk = self.page.locator("//div[@class='page-header']//button[2]")
        bulk.click()
        logger.info("Bulk Upload button clicked for the first device in the table")

    def get_bulk_upload_page_title(self):
        base = BasePage(self.page)
        logger.debug("Retrieving Bulk Upload page title")
        title = base.get_title()
        logger.info("Bulk Upload page title retrieved: %s", title)
        return title

    def click_on_file_upload_input_box(self):
        logger.debug("Clicking on file upload input box")
        file_input = self.page.locator("input[formcontrolname='file']")
        file_input.click()
        logger.info("File upload input box clicked")

    def get_file_upload_error_message(self):
        logger.debug("Retrieving file upload error message")
        error_message_element = self.page.locator(
            "//mat-error[contains(@id, 'mat-mdc-error-0')]"
        )
        error_message = (
            error_message_element.text_content().strip()
            if error_message_element.is_visible()
            else ""
        )
        logger.info("File upload error message retrieved: %s", error_message)
        return error_message

    def is_bulk_upload_submit_button_disabled(self):
        logger.debug("Checking if Submit button on Bulk Upload form is disabled")
        submit_button = self.page.locator("//button[contains(text(), 'Submit')]")
        is_disabled = submit_button.is_disabled()
        logger.info("Submit button disabled state: %s", is_disabled)
        return is_disabled

    def simulate_file_selection(self, file_path):
        logger.debug(
            "Simulating file selection for bulk upload with file: %s",
            file_path,
        )

        file_input = self.page.locator("input[type='file']")

        file_input.set_input_files(file_path)

        logger.info(
            "File selection simulated for bulk upload with file: %s",
            file_path,
        )

    def click_bulk_upload_submit_button(self):
        logger.debug("Clicking Submit button on Bulk Upload form")
        submit_button = self.page.locator("//button[contains(text(), 'Submit')]")
        submit_button.click()
        logger.info("Submit button clicked on Bulk Upload form")

    def get_bulk_upload_result_message(self):
        logger.debug("Retrieving result message after bulk upload")

        snackbar_message = self.page.locator(
            "simple-snack-bar .mat-mdc-snack-bar-label"
        ).first

        snackbar_message.wait_for(state="visible")

        result_message = snackbar_message.text_content().strip()

        logger.info(
            "Bulk upload result message retrieved: %s",
            result_message,
        )

        return result_message

    def is_uploaded_dispatch_device_list_displayed(self):
        logger.debug("Checking if uploaded dispatched device list is displayed")

        table = self.page.locator("h6:has-text('Uploaded Dispatch Device List')")

        table.wait_for(state="visible", timeout=30000)

        is_visible = table.is_visible()

        logger.info(
            "Uploaded Dispatch Device List component visibility: %s",
            is_visible,
        )

        return is_visible

    def is_invalid_dispatch_device_list_displayed(self):
        logger.debug("Checking if invalid dispatched device list is displayed")

        table = self.page.locator("h6:has-text('Invalid Dispatch Device List')")

        table.wait_for(state="visible", timeout=30000)

        is_visible = table.is_visible()

        logger.info(
            "Invalid Dispatch Device List component visibility: %s",
            is_visible,
        )

        return is_visible

    def get_uploaded_dispatch_device_list_headers(self):
        logger.debug("Retrieving headers from Uploaded Dispatch Device List table")

        headers_locator = self.page.locator(
            "div.component-container:has(h6.component-title:text-is('Uploaded Dispatch Device List')) "
            "table thead th"
        )

        headers_locator.first.wait_for(state="visible")

        headers = [header.strip() for header in headers_locator.all_inner_texts()]

        logger.info(
            "Uploaded Dispatch Device List table headers retrieved: %s",
            headers,
        )

        return headers

    def get_invalid_dispatch_device_list_headers(self):
        logger.debug("Retrieving headers from Invalid Dispatch Device List table")

        headers_locator = self.page.locator(
            "div.component-container:has(h6.component-title:text-is('Invalid Dispatch Device List')) "
            "table thead th"
        )

        headers_locator.first.wait_for(state="visible")

        headers = [header.strip() for header in headers_locator.all_inner_texts()]

        logger.info(
            "Invalid Dispatch Device List table headers retrieved: %s",
            headers,
        )

        return headers

    def is_uploaded_dispatch_device_list_no_data(self):
        logger.debug(
            "Checking if No Data Found image is displayed in Uploaded Dispatch Device List table"
        )

        no_data_image = self.page.locator(
            "div.component-container:has(h6.component-title:text-is('Uploaded Dispatch Device List')) "
            "img[alt='No Data Found']"
        )

        is_visible = no_data_image.count() > 0

        logger.info(
            "No Data Found image visibility in Uploaded Dispatch Device List table: %s",
            is_visible,
        )

        return is_visible

    def is_invalid_dispatch_device_list_no_data(self):
        logger.debug(
            "Checking if No Data Found image is displayed in Invalid Dispatch Device List table"
        )

        no_data_image = self.page.locator(
            "div.component-container:has(h6.component-title:text-is('Invalid Dispatch Device List')) "
            "img[alt='No Data Found']"
        )

        is_visible = no_data_image.count() > 0

        logger.info(
            "No Data Found image visibility in Invalid Dispatch Device List table: %s",
            is_visible,
        )

        return is_visible

    def get_invalid_dispatch_device_list_rows(self):
        logger.debug("Retrieving rows from Invalid Dispatch Device List table")

        rows_locator = self.page.locator(
            "div.component-container:has(h6.component-title:text-is('Invalid Dispatch Device List')) "
            "table tbody tr"
        )

        rows_locator.first.wait_for(state="visible")

        rows = [row.strip() for row in rows_locator.all_inner_texts()]

        logger.info(
            "Invalid Dispatch Device List table rows retrieved: %s",
            rows,
        )

        return rows

    def get_uploaded_dispatch_device_list_rows(self):
        logger.debug("Retrieving rows from Uploaded Dispatch Device List table")

        rows_locator = self.page.locator(
            "div.component-container:has(h6.component-title:text-is('Uploaded Dispatch Device List')) "
            "table tbody tr"
        )

        rows_locator.first.wait_for(state="visible")

        rows = [row.strip() for row in rows_locator.all_inner_texts()]

        logger.info(
            "Uploaded Dispatch Device List table rows retrieved: %s",
            rows,
        )

        return rows

    def is_export_button_enabled_in_uploaded_list(self):
        logger.debug(
            "Checking Export button enabled state in Uploaded Dispatch Device List section"
        )

        export_button = self.page.locator(
            "div.component-container:has(h6.component-title:text-is('Uploaded Dispatch Device List')) "
            "button:has-text('Export')"
        )

        export_button.first.wait_for(state="visible")

        is_enabled = export_button.is_enabled()

        logger.info(
            "Export button enabled state in Uploaded Dispatch Device List section: %s",
            is_enabled,
        )

        return is_enabled

    def is_export_button_enabled_in_invalid_list(self):
        logger.debug(
            "Checking Export button enabled state in Invalid Dispatch Device List section"
        )

        export_button = self.page.locator(
            "div.component-container:has(h6.component-title:text-is('Invalid Dispatch Device List')) "
            "button:has-text('Export')"
        )

        export_button.first.wait_for(state="visible")

        is_enabled = export_button.is_enabled()

        logger.info(
            "Export button enabled state in Invalid Dispatch Device List section: %s",
            is_enabled,
        )

        return is_enabled
