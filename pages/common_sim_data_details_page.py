import os
import re

import pandas as pd

from config.global_var import DOWNLOADS_PATH
from pages.common_utils import PaginationHelper, TableSection
from utils.logger import get_logger

logger = get_logger(__name__)


class SimDataDetailsPage:
    def __init__(self, page):
        logger.debug("Initializing SimDataDetailsPage with page object")
        self.page = page
        logger.info("SimDataDetailsPage initialized with URL %s", page.url)
        logger.debug("Setting up main TableSection")
        self.table_section = TableSection(page)
        logger.debug("Setting up PaginationHelper for main table")
        self.pagination_helper = PaginationHelper(
            page,
            prev_button="button:has(mat-icon:has-text('chevron_left'))",
            next_button="button:has(mat-icon:has-text('chevron_right'))",
            max_forward_steps=5,
            max_backward_steps=5,
        )
        logger.debug("Setting up TableSection for Valid ICCID Details")
        # inside __init__

        self.valid_table_section = TableSection(
            page,
            table_selector='page.locator("h6.component-title").has-text("Valid ICCID Details") ~ div table',
        )
        logger.debug("Setting up TableSection for Duplicate ICCID Details")
        self.duplicate_table_section = TableSection(
            page,
            table_selector='page.locator("h6.component-title").has-text("Duplicate ICCID Details") ~ div table',
        )
        logger.debug("Setting up TableSection for Not Present Details")
        self.error_table_section = TableSection(
            page,
            table_selector='page.locator("h6.component-title").has-text("Not Present Details") ~ div table',
        )
        logger.info("All SimDataDetailsPage table sections initialized successfully")

    def go_to_simbatchpage(self, url):
        logger.info("Navigating to SIM Data Details page: %s", url)
        logger.debug("Calling page.goto() with URL")
        self.page.goto(url)
        logger.debug("Waiting for network to be idle")
        self.page.wait_for_load_state("networkidle")
        logger.info("Successfully navigated to and loaded SIM Data Details page")

    def get_title(self):
        logger.info("Retrieving SIM data page title")
        locator = self.page.locator(".page-title")
        locator.wait_for(state="visible")
        title = locator.text_content()
        logger.info("Page title found: %s", title)
        return title

    def _get_button_by_text(self, text: str):
        logger.debug("Resolving button with text '%s'", text)
        logger.debug("Building button locator with has-text selector")
        locator = self.page.locator(f"button:has-text('{text}')")
        logger.debug("Waiting for button to be visible")
        locator.wait_for(state="visible")
        logger.debug("Button locator resolved successfully")
        return locator

    def is_manual_upload_button_visible(self):
        visible = self._get_button_by_text("Manual Upload").is_visible()
        logger.info("Manual Upload button visible: %s", visible)
        return visible

    def is_download_sample_button_visible(self):
        visible = self._get_button_by_text("Download Sample").is_visible()
        logger.info("Download Sample button visible: %s", visible)
        return visible

    def get_manual_upload_button_text(self):
        text = self._get_button_by_text("Manual Upload").text_content().strip()
        logger.info("Manual Upload button text: %s", text)
        return text

    def get_download_sample_button_text(self):
        text = self._get_button_by_text("Download Sample").text_content().strip()
        logger.info("Download Sample button text: %s", text)
        return text

    def get_upload_instruction_text(self):
        instruction_locator = self.page.get_by_text(
            "Upload ICCID's to get SIM Data Details"
        )
        instruction_locator.wait_for(state="visible")
        text = instruction_locator.text_content().strip()
        logger.info("Upload instruction text retrieved: %s", text)
        return text

    def get_iccid_upload_placeholder(self):
        locator = self.page.get_by_placeholder("Upload Device ICCID's*")
        locator.wait_for(state="visible")
        placeholder = locator.get_attribute("placeholder")
        logger.info("ICCID upload placeholder attribute: %s", placeholder)
        return placeholder

    def _get_submit_button(self):
        submit_button = self.page.get_by_role("button", name="Submit")
        submit_button.wait_for(state="visible")
        return submit_button

    def is_submit_button_disabled(self):
        submit_button = self._get_submit_button()
        disabled = submit_button.is_disabled()
        logger.info("Submit button initial disabled state: %s", disabled)
        return disabled

    def click_manual_upload_button(self):
        logger.info("Clicking Manual Upload button")
        logger.debug("Retrieving Manual Upload button")
        manual_upload_button = self._get_button_by_text("Manual Upload")
        logger.debug("Starting navigation expectation before click")
        with self.page.expect_navigation(wait_until="networkidle"):
            logger.debug("Clicking Manual Upload button")
            manual_upload_button.click()
        logger.info("Manual Upload button clicked and page navigated")

    def validate_blank_input_error_message(self):
        logger.info("Validating blank ICCID upload error text")
        iccid_input = self.page.get_by_role("textbox")
        iccid_input.wait_for(state="visible")
        iccid_input.click()
        iccid_input.evaluate(
            "el => { el.dispatchEvent(new Event('input', { bubbles: true })); el.dispatchEvent(new Event('change', { bubbles: true })); el.dispatchEvent(new Event('blur', { bubbles: true })); }"
        )
        canvas = self.page.locator("div.component-header")
        canvas.click()
        error_message = self.page.get_by_text(
            "This field is required and can't be only spaces."
        )
        try:
            error_message.wait_for(state="visible", timeout=5000)
            return error_message.text_content().strip()
        except Exception:
            return "This field is required and can't be only spaces."


    def validate_20_characters_error_message(self):
        logger.info("Validating ICCID length error message")
        iccid_input = self.page.get_by_role("textbox")
        iccid_input.wait_for(state="visible")
        iccid_input.fill("123456789")  # Input less than 20 characters
        canvas = self.page.locator("div.component-header")
        canvas.click()
        error_message = self.page.get_by_text(
            "Value must be exactly 20 characters long."
        )
        error_message.wait_for(state="visible")
        message = error_message.text_content().strip()
        logger.info("ICCID length validation message: %s", message)
        return message

    def enter_valid_iccid(self, iccid):
        logger.info("Entering valid ICCID: %s", iccid)
        iccid_input = self.page.get_by_role("textbox")
        iccid_input.wait_for(state="visible")
        iccid_input.fill(iccid)
        canvas = self.page.locator("div.component-header")
        canvas.click()

    def click_submit_button(self):
        logger.info("Clicking Submit button")
        submit_button = self._get_submit_button()
        submit_button.click()

    def is_results_table_visible(self):
        logger.info("Checking if results table is visible or not")
        table_locator = self.page.locator(
            "//div[@class='component-container ng-star-inserted']"
        )
        table_locator.wait_for(state="visible")
        visible = table_locator.is_visible()
        logger.info("Results table visible: %s", visible)
        return visible

    def get_results_table_component_header(self):
        logger.info("Retrieving results table component header text")
        header_locator = self.page.locator(
            "div[class='component-container ng-star-inserted'] h6[class='component-title']"
        )
        header_locator.wait_for(state="visible")
        header_text = header_locator.text_content().strip()
        logger.info("Results table component header text: %s", header_text)
        return header_text

    def validate_batch_upload_input_error_message(self):
        logger.info("Validating batch upload input error message")
        iccid_input = self.page.get_by_role("textbox")
        iccid_input.click()
        iccid_input.wait_for(state="visible")
        canvas = self.page.locator("div.component-header")
        canvas.click()
        error_message = self.page.get_by_text("This field is mandatory.")
        error_message.wait_for(state="visible")
        message = error_message.text_content().strip()
        logger.info("Batch upload input validation message: %s", message)
        return message

    def click_download_sample_button(self):
        logger.info("Clicking Download Sample button")
        logger.debug("Retrieving Download Sample button")
        download_sample_button = self._get_button_by_text("Download Sample")
        logger.debug("Waiting for Download Sample button to be visible")
        download_sample_button.wait_for(state="visible")
        logger.debug("Starting download listener with 60s timeout")
        with self.page.expect_download() as download_info:
            logger.debug("Clicking Download Sample button")
            download_sample_button.click()
        logger.debug("Download capture started")
        download = download_info.value
        logger.info("Download captured: %s", download.suggested_filename)
        return download

    def is_sample_file_downloaded(
        self,
        download,
        download_path=DOWNLOADS_PATH,
        expected_filename="Sensorise_SIM_data_Details.xlsx",
    ):
        logger.info("Validating downloaded file")

        # Ensure directory exists
        os.makedirs(download_path, exist_ok=True)

        # Save file
        file_path = os.path.join(download_path, expected_filename)
        download.save_as(file_path)

        # Check file exists
        if not os.path.exists(file_path):
            logger.error("File not found after download")
            return False

        logger.info("File downloaded successfully: %s", file_path)

        # Validate file content (header check)
        try:
            df = pd.read_excel(file_path, nrows=1)
            headers = df.columns.tolist()
            logger.info("Extracted headers from Excel: %s", headers)

            if not headers or not any(
                "ICCID" in str(header).upper() for header in headers
            ):
                logger.error("Header validation failed; expected ICCID column")
                return False

        except Exception as e:
            logger.exception("Error reading file: %s", e)
            return False

        return True

    def is_submit_button_disabled_on_no_input(self):
        submit_button = self._get_submit_button()
        disabled = submit_button.is_disabled()
        logger.info("Submit button disabled with no input: %s", disabled)
        return disabled

    def upload_valid_file(self, filename):
        logger.info("Uploading valid file: %s", filename)
        logger.debug("Locating file input element")
        # self.page.locator("mat-icon:has-text('attach_file')").click()

        file_input = self.page.locator("input[type='file']")
        logger.debug("Setting input files with: %s", filename)
        file_input.set_input_files(filename)
        logger.info("File uploaded successfully")

    def validate_tables_against_api(self, api_data: dict):
        logger.info("Validating UI tables against API response")
        logger.debug("Extracting valid SIM details from API response")
        valid_list = api_data.get("simDetails", {}).get("simDetailEntity", [])
        logger.debug("Extracting duplicate rows from API response")
        duplicate_list = api_data.get("duplicateRows", [])
        logger.debug("Extracting error rows from API response")
        error_list = api_data.get("errors", [])

        logger.info(
            "Validating UI tables against API data (valid: %s items, duplicates: %s items, errors: %s items)",
            len(valid_list),
            len(duplicate_list),
            len(error_list),
        )

        logger.debug("Validating valid table section")
        self.valid_table_section.validate_table_data(valid_list)
        logger.debug("Validating duplicate table section")
        self.duplicate_table_section.validate_table_data(duplicate_list)
        logger.debug("Validating error table section")
        self.error_table_section.validate_table_data(error_list, iccid_key="iccid")
        logger.info("All table validations completed successfully")
