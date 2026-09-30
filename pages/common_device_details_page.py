import os
import re

from playwright.sync_api import expect

from pages.common_utils import PaginationHelper, SearchHelper, TableSection
from config.global_var import DOWNLOADS_PATH
from utils.logger import get_logger

logger = get_logger(__name__)


class DeviceDetailsPage:
    def __init__(self, page):
        logger.debug("Initializing DeviceDetailsPage with page object")
        self.page = page
        logger.debug("Setting up SearchHelper")
        self.search_helper = SearchHelper(page)
        logger.debug("Setting up TableSection")
        self.table_section = TableSection(page)
        logger.debug("Setting up PaginationHelper")
        self.pagination_helper = PaginationHelper(page)
        logger.info("DeviceDetailsPage initialized successfully")

    # ------------------ INTERNAL HELPERS ------------------

    def _login_packet_base(self):
        return "//h6[text()='Last 50 Login Packets']/ancestor::div[contains(@class,'component-container')]"

    # ------------------ PAGINATION ------------------

    def set_pagination_for_login_packets(self):
        logger.debug("Setting pagination for login packets")
        self.pagination_helper = PaginationHelper(self.page)
        logger.debug("Pagination for login packets set successfully")

    def get_login_packet_pagination(self):
        logger.debug("Retrieving login packet pagination configuration")
        base = self._login_packet_base()
        logger.debug("Building PaginationHelper with scoped selectors")

        pagination = PaginationHelper(
            self.page,
            content_selector=f"{base}//table",
            page_input=f"{base}//input[contains(@class,'page-input')]",
            next_button=f"{base}//button[.//mat-icon[text()='chevron_right']]",
            prev_button=f"{base}//button[.//mat-icon[text()='chevron_left']]",
            total_pages_selector=f"{base}//span[contains(text(),'of')]",
        )
        logger.debug("Login packet pagination helper created successfully")
        return pagination

    # ------------------ NAVIGATION ------------------

    def go_to_device_details_page(self, url):
        logger.info("Navigating to Device Details page: %s", url)
        logger.debug("Calling page.goto() with URL")
        self.page.goto(url)
        logger.debug("Waiting for network to be idle")
        self.page.wait_for_load_state("networkidle")
        logger.info("Successfully navigated to Device Details page")

    def get_title(self):
        logger.debug("Retrieving Device Details page heading")
        heading = self.page.get_by_role("heading", name="Device Details")
        logger.debug("Waiting for heading to be visible")
        heading.wait_for(state="visible")
        title_text = heading.inner_text()
        logger.info("Device Details page title: %s", title_text)
        return title_text

    def is_page_loaded(self):
        logger.debug("Checking if Device Details page is loaded")
        url_valid = self.page.url.endswith("/device-details")
        heading_visible = self.page.get_by_role(
            "heading", name="Device Details"
        ).is_visible()
        is_loaded = url_valid and heading_visible
        logger.info(
            "Device Details page loaded: %s (URL valid: %s, Heading visible: %s)",
            is_loaded,
            url_valid,
            heading_visible,
        )
        return is_loaded

    # ------------------ PAGE ELEMENTS ------------------

    def is_device_details_page_buttons_are_visible(self):
        logger.debug("Checking visibility of Device Details page buttons")
        buttons = self.page.get_by_role("button")
        logger.debug("Waiting for first button to be visible")
        buttons.first.wait_for(state="visible")
        logger.debug("Checking all buttons visibility")
        all_visible = all(buttons.nth(i).is_visible() for i in range(buttons.count()))
        logger.info("All Device Details page buttons visible: %s", all_visible)
        return all_visible

    def is_device_kpi_cards_visible(self):
        logger.debug("Checking visibility of Device KPI cards")
        kpi_cards = self.page.locator(".kpi-card")
        logger.debug("Waiting for first KPI card to be visible")
        kpi_cards.first.wait_for(state="visible")
        logger.debug("Checking all KPI cards visibility")
        all_visible = all(
            kpi_cards.nth(i).is_visible() for i in range(kpi_cards.count())
        )
        logger.info("All Device KPI cards visible: %s", all_visible)
        return all_visible

    # ------------------ KPI CARDS ------------------

    def _is_cards_visible(self):
        logger.info("Checking KPI card visibility")
        cards_locator = self.page.locator(".kpi-details")
        cards_locator.wait_for(state="visible")
        visible = cards_locator.is_visible()
        logger.info("KPI cards visibility check result: %s", visible)
        return visible

    def _cards_parent(self):
        logger.debug("Retrieving KPI cards parent container")
        cards_parent = self.page.locator("div.kpi-section")
        logger.debug("Waiting for cards parent to be visible")
        cards_parent.wait_for(state="visible")
        logger.debug("KPI cards parent container is ready")
        return cards_parent

    def _card_elements(self):
        logger.debug("Retrieving all card element locators")
        card_elements = self._cards_parent().locator(":scope > div")
        logger.debug("Card elements locator retrieved successfully")
        return card_elements

    def get_cards_count(self):
        count = self._card_elements().count()
        logger.info("Found %s dashboard cards", count)
        return count

    def get_card_element(self, index):
        logger.debug("Retrieving card element at index %s", index)
        card_element = self._card_elements().nth(index)
        logger.debug("Card element at index %s retrieved", index)
        return card_element

    def get_cards_title_text(self, index):
        logger.debug("Getting title for card index %s", index)
        card = self.get_card_element(index)
        card_title_locator = card.locator("div.kpi-details span").nth(0)
        card_title_locator.wait_for(state="visible")
        title = card_title_locator.inner_text()
        logger.info("Card index %s title text: %s", index, title)
        return title

    def get_cards_inner_count(self, index):
        logger.debug("Getting count for card index %s", index)
        card = self.get_card_element(index)
        card_count_locator = card.locator("div.kpi-details span").nth(1)
        card_count_locator.wait_for(state="visible")
        count_text = card_count_locator.inner_text()
        logger.info("Card index %s displayed count: %s", index, count_text)
        return count_text

    # ------------------ SEARCH ------------------

    def search_for_device(self, device):
        logger.info("Searching for device: %s", device)
        logger.debug("Delegating search to SearchHelper")
        search_result = self.search_helper.run_search(str(device))
        logger.info("Device search completed for: %s", device)
        return search_result

    # ------------------ TABLE ACTIONS ------------------

    def click_on_view_device_in_table(self, device):
        logger.info("Clicking view icon for device: %s", device)
        logger.debug("Building row locator for device: %s", device)
        row = self.page.locator(f"//tr[td[contains(text(), '{device}')]]")
        logger.debug("Waiting for device row to be visible")
        row.wait_for(state="visible")
        logger.debug("Device row is visible, retrieving view button locator")
        view_button = row.locator("button:has(mat-icon:has-text('visibility'))")
        logger.debug("Checking if view button exists for device: %s", device)
        if view_button.count() == 0:
            logger.error("View button not found for device: %s", device)
            raise Exception(f"View button not found for device {device}")
        logger.debug("View button found, clicking it")
        view_button.click()
        logger.info("Successfully clicked view button for device: %s", device)

    # ------------------ COMPONENT TITLES ------------------

    def get_table_component_title_text(self, index):
        logger.debug("Getting title for table component index %s", index)
        title_locator = self.page.locator(".component-title").nth(index)
        title_locator.wait_for(state="visible")
        title = title_locator.inner_text()
        logger.info("Table component index %s title text: %s", index, title)
        return title

    # ------------------ HEADERS ------------------

    def get_inside_table_headers_count(self):
        logger.debug("Counting table headers")
        count = self.page.locator(".component-body .header").count()
        logger.info("Found %s table headers", count)
        return count

    def get_table_component_headers(self):
        logger.info("Getting headers for table component")

        headers_locator = self.page.locator(".component-body .header")
        headers_locator.first.wait_for(state="visible")

        headers = [
            headers_locator.nth(i).inner_text().strip()
            for i in range(headers_locator.count())
        ]

        logger.info("Table component headers: %s", headers)
        return headers

    # ------------------ LOGIN PACKET TABLE (FIXED) ------------------

    def get_login_packet_table_headers(self):
        """
        Scoped headers for Login Packet table
        """
        logger.debug("Retrieving login packet table headers")
        base = self._login_packet_base()
        logger.debug("Building header locator with base selector")
        headers = self.page.locator(f"{base}//thead//th")
        logger.debug("Waiting for headers to be visible")
        headers.first.wait_for(state="visible")
        header_list = [
            headers.nth(i).inner_text().strip().upper() for i in range(headers.count())
        ]
        logger.info("Login packet table headers retrieved: %s", header_list)
        return header_list

    def get_device_details_table_data(self):
        """
        Scoped table data for Login Packet table
        """
        logger.info("Extracting login packet table data (row-wise)")

        # base = self._login_packet_base()
        # rows = self.page.locator(f"{base}//tbody//tr")

        rows = self.page.locator("tr.ng-star-inserted")
        rows.first.wait_for(state="visible", timeout=5000)

        table_data = []

        for i in range(rows.count()):
            row = rows.nth(i)
            cols = row.locator("td")

            row_data = [cols.nth(j).inner_text().strip() for j in range(cols.count())]

            # if i is zero or not gets anything then check the no data image is present
            if i == 0 and not row_data:
                self.table_section.has_no_data()
                logger.warning("No data found in login packet table")

            table_data.append(row_data)

        logger.info("Extracted table data: %s", table_data)
        return table_data

    # ------------------ EXPORT (FIXED) ------------------

    def check_export_button(self):
        """
        Scoped export button validation
        """
        logger.info("Verifying export button functionality")
        base = self._login_packet_base()
        logger.debug("Building export button locator with scoped selector")
        export_btn = self.page.locator(
            f"{base}//button[.//text()[contains(.,'Export')]]"
        )

        result = {"success": True, "error": None}

        try:
            logger.debug("Waiting for export button to be visible")
            export_btn.wait_for(state="visible", timeout=10000)
            logger.debug("Export button visible, scrolling into view if needed")
            export_btn.scroll_into_view_if_needed()
            logger.debug("Verifying export button is enabled")
            expect(export_btn).to_be_enabled(timeout=10000)
            logger.debug("Export button is enabled, clicking it")
            export_btn.click()
            logger.debug("Export button clicked, waiting for processing")
            self.page.wait_for_load_state("networkidle", timeout=10000)
            logger.info("Export button verification completed successfully")

        except Exception as e:
            result["success"] = False
            result["error"] = str(e)
            logger.exception("Export button verification failed: %s", e)

        return result

    def click_export_button(self):
        """
        Clicks the export button and handles the download.
        Note: The button triggers an async download via backend API.
        """
        # Search for Export button directly on the page
        logger.info("Preparing to click Export button and handle download")
        logger.debug("Building export button locator")
        export_btn = self.page.locator("//button[contains(.,'Export')]")
        logger.debug("Waiting for export button to be visible")
        export_btn.wait_for(state="visible", timeout=10000)
        logger.debug("Scrolling export button into view if needed")
        export_btn.scroll_into_view_if_needed()

        logger.info("Export button found and scrolled into view")

        # Start listening for the download before clicking
        # The backend may generate the file and trigger download
        logger.debug("Starting download listener with 60s timeout")
        with self.page.expect_download(timeout=60000) as download_info:
            # Also wait for any network activity to complete
            logger.info("Clicking export button")
            export_btn.click()
            # Wait a moment for the backend to process
            logger.debug("Waiting for network to be idle after export button click")
            self.page.wait_for_load_state("networkidle", timeout=10000)
            logger.info("Export button clicked, waiting for download to complete")

        download = download_info.value
        logger.info("Download captured: %s", download.suggested_filename)
        return download
