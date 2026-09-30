from __future__ import annotations

from playwright.sync_api import Locator, Page

from utils.logger import get_logger

logger = get_logger(__name__)


class TableSection:
    def __init__(
        self,
        page: Page,
        table_selector: str | Locator = "div.component-body table",
        header_selector: str | None = None,
    ):
        self.page = page
        self.table_selector = table_selector
        self.header_selector = header_selector or f"{table_selector} thead th"
        self.button_selector = f"{table_selector} tbody tr td button"

    def wait_for_table(self) -> Locator:
        table_locator = self.page.locator(self.table_selector)
        table_locator.wait_for(state="visible")
        return table_locator

    def get_headers(self) -> list[str]:
        headers_locator = self.page.locator(self.header_selector)
        headers_locator.first.wait_for(state="visible")

        headers = [
            headers_locator.nth(i).inner_text().strip()
            for i in range(headers_locator.count())
        ]

        logger.info("Table headers retrieved: %s", headers)
        return headers

    def get_rows(self, row_selector: str = "tbody tr") -> list[str]:
        table = self.wait_for_table()
        rows = table.locator(row_selector)

        values = [rows.nth(i).inner_text().strip() for i in range(rows.count())]

        logger.info("Collected %s rows for selector %s", len(values), row_selector)
        return values

    def has_no_data(self) -> bool:
        table_loc = (
            self.table_selector
            if isinstance(self.table_selector, Locator)
            else self.page.locator(self.table_selector)
        )

        # Common text selector for no data
        text_selector = "text=No Data Found, text=nodatafound, text=No Data, text=No records found"
        
        # Common image selector for no data (checking class, alt, src)
        img_selector = (
            "img.no-data-img, "
            "img[alt='nodatafound'], "
            "img[alt='No Data Found'], "
            "img[alt*='nodata' i], "
            "img[alt*='no data' i], "
            "img[class*='no-data'], "
            "img[src*='dataNotFound'], "
            "img[src*='nodata'], "
            "img[src*='no-data']"
        )

        # 1. Check text inside table
        try:
            no_data_text = table_loc.locator(text_selector)
            if no_data_text.count() > 0:
                for i in range(no_data_text.count()):
                    if no_data_text.nth(i).is_visible():
                        return True
        except Exception as e:
            logger.debug("Error checking no_data_text inside table: %s", e)

        # 2. Check image inside table
        try:
            no_data_img = table_loc.locator(img_selector)
            if no_data_img.count() > 0:
                for i in range(no_data_img.count()):
                    if no_data_img.nth(i).is_visible():
                        return True
        except Exception as e:
            logger.debug("Error checking no_data_img inside table: %s", e)

        return False

    def get_row_count(self) -> int:
        rows = self.page.locator(f"{self.table_selector} tbody tr")
        return rows.count()

    def validate_table_data(
        self,
        expected_list: list,
        iccid_key: str = "iccid",
    ):
        """
        Generic reusable validator
        """

        if expected_list:
            row_count = self.get_row_count()

            assert row_count > 0, "Expected data but table is empty"

            ui_text = self.page.locator(self.table_selector).inner_text()

            expected_iccids = [item.get(iccid_key) for item in expected_list]

            for iccid in expected_iccids:
                assert iccid in ui_text, f"{iccid} not found in UI table"

        else:
            assert self.has_no_data(), "Expected 'No Data Found' but table has data"

    def get_table_data(self) -> list[dict[str, str]]:
        """
        Returns complete table data in row-wise dictionary format

        Example:
        [
            {
                "ICCID": "12345",
                "Status": "Active"
            },
            {
                "ICCID": "67890",
                "Status": "Inactive"
            }
        ]
        """

        table = self.wait_for_table()
        headers = self.get_headers()

        rows = table.locator("tbody tr")

        table_data = []

        for i in range(rows.count()):
            cells = rows.nth(i).locator("td")

            row_dict = {
                headers[j]: cells.nth(j).inner_text().strip()
                for j in range(cells.count())
            }

            table_data.append(row_dict)

        logger.info("Extracted table data: %s", table_data)

        return table_data

    def get_row_data(self, row_index: int) -> dict[str, str]:
        table = self.wait_for_table()
        headers = self.get_headers()

        rows = table.locator("tbody tr")

        total_rows = rows.count()

        if row_index >= total_rows:
            raise IndexError(
                f"Row index {row_index} out of range. Total rows: {total_rows}"
            )

        cells = rows.nth(row_index).locator("td")

        row_data = {
            headers[j]: cells.nth(j).inner_text().strip() for j in range(cells.count())
        }

        logger.info("Extracted row data at index %s: %s", row_index, row_data)

        return row_data

    def _get_button_text(self, button: Locator) -> str:
        """Extract a readable label for a button."""
        text = button.get_attribute("aria-label")

        if not text:
            text = button.get_attribute("title")

        if not text:
            try:
                text = button.locator("mat-icon").inner_text().strip()
            except Exception:
                text = ""

        if not text:
            text = button.inner_text().strip()

        return text.strip() if text else ""

    def get_action_buttons(self, row_index: int) -> list[str]:
        """
        Returns a list of action button names for a specific row index
        """

        table = self.wait_for_table()
        rows = table.locator("tbody tr")

        total_rows = rows.count()

        assert total_rows > 0, "No rows found in table"

        if row_index >= total_rows:
            raise IndexError(
                f"Row index {row_index} out of range. Total rows: {total_rows}"
            )

        buttons = rows.nth(row_index).locator("td button")

        button_count = buttons.count()

        assert button_count > 0, f"No action buttons found for row index {row_index}"

        buttons_text = []

        for i in range(button_count):
            button = buttons.nth(i)
            text = self._get_button_text(button)
            if text:
                buttons_text.append(text)

        logger.info(
            "Found action buttons at row index %s: %s",
            row_index,
            buttons_text,
        )

        return buttons_text

    def get_action_button(
        self, row_index: int, action_name: str | None = None
    ) -> Locator | list[Locator]:
        """Return a matching button for a row, or all buttons in the row when no name is passed."""
        table = self.wait_for_table()
        rows = table.locator("tbody tr")

        if row_index >= rows.count():
            raise IndexError(
                f"Row index {row_index} out of range. Total rows: {rows.count()}"
            )

        row_buttons = rows.nth(row_index).locator("td button")

        if action_name is None:
            return [row_buttons.nth(i) for i in range(row_buttons.count())]

        for i in range(row_buttons.count()):
            button = row_buttons.nth(i)
            if self._get_button_text(button).lower() == action_name.lower():
                return button

        raise ValueError(
            f"Action button '{action_name}' not found for row index {row_index}"
        )

    def get_disabled_action_buttons(self) -> list[dict[str, int | str | bool]]:
        """Iterate every row and return any action buttons that are not enabled."""
        table = self.wait_for_table()
        rows = table.locator("tbody tr")
        total_rows = rows.count()

        disabled_buttons = []

        for row_index in range(total_rows):
            row_buttons = rows.nth(row_index).locator("td button")
            for button_index in range(row_buttons.count()):
                button = row_buttons.nth(button_index)
                button_text = self._get_button_text(button)
                if not button_text:
                    continue

                is_enabled = button.is_enabled() and not button.is_disabled()
                if not is_enabled:
                    disabled_buttons.append(
                        {
                            "row_index": row_index,
                            "button_name": button_text,
                            "enabled": is_enabled,
                        }
                    )

        logger.info("Disabled action buttons found: %s", disabled_buttons)
        return disabled_buttons

    def is_action_button_enabled(
        self, row_index: int | None = None, action_name: str | None = None
    ) -> bool:
        """Check whether a specific button is enabled, or whether all row buttons are enabled."""
        if row_index is None:
            return len(self.get_disabled_action_buttons()) == 0

        if action_name is not None:
            button = self.get_action_button(row_index, action_name)
            return button.is_enabled() and not button.is_disabled()

        buttons = self.get_action_button(row_index)
        return all(
            button.is_enabled() and not button.is_disabled()
            for button in buttons
        )

    def is_action_button_disabled(
        self, row_index: int | None = None, action_name: str | None = None
    ) -> bool:
        """Check whether a specific button is disabled, or whether any row button is disabled."""
        if row_index is None:
            return len(self.get_disabled_action_buttons()) > 0

        if action_name is not None:
            button = self.get_action_button(row_index, action_name)
            return button.is_disabled() or not button.is_enabled()

        buttons = self.get_action_button(row_index)
        return any(
            button.is_disabled() or not button.is_enabled() for button in buttons
        )
