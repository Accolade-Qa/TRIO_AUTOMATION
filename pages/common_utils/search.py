from __future__ import annotations

from typing import Sequence

from playwright.sync_api import Locator, Page, expect

from utils.logger import get_logger

logger = get_logger(__name__)


class SearchHelper:
    def __init__(
        self,
        page: Page,
        input_selector: str = "input[placeholder='Search and Press Enter']",
        row_selector: str = "tr.ng-star-inserted",
    ):
        self.page = page
        self.input_selector = input_selector
        self.row_selector = row_selector

    def _search_input_candidates(self) -> list[Locator]:
        return [
            self.page.locator(self.input_selector),
            self.page.get_by_placeholder("Search and Press Enter"),
            self.page.locator("input[placeholder*='Search']"),
            self.page.locator("//input[contains(@placeholder,'Search')]"),
        ]

    def _visible_search_input(self) -> Locator:
        errors = []

        for search_input in self._search_input_candidates():
            try:
                candidate = search_input.first

                # Assertion: Search input should be visible
                expect(candidate).to_be_visible(timeout=5000)

                return candidate

            except Exception as exc:
                errors.append(str(exc))

        logger.debug("Search input locator attempts failed: %s", errors)
        raise AssertionError("No visible search input found on the current page")

    def run_search(self, query: str) -> dict[str, Sequence[str] | int | bool | None]:
        result = {
            "success": True,
            "results_found": 0,
            "results": [],
            "error": None,
        }

        try:
            search_input = self._visible_search_input()

            logger.info("Executing search for query '%s'", query)

            search_input.scroll_into_view_if_needed()

            # Assertion: Input should be enabled before interaction
            expect(search_input).to_be_enabled()

            search_input.fill(query)

            # Assertion: Verify entered value
            expect(search_input).to_have_value(query)

            # Dispatch Angular input/change events to trigger client-side filtering
            search_input.evaluate(
                "el => { el.dispatchEvent(new Event('input', { bubbles: true })); el.dispatchEvent(new Event('change', { bubbles: true })); }"
            )

            # waiting for whole page content to load
            self.page.wait_for_load_state("load")

            search_input.press("Enter")
            self.page.wait_for_timeout(500)

            # Wait for either result rows to appear or the 'No Data Found' indicator.
            try:
                # Wait briefly for rows to be attached to DOM
                self.page.wait_for_selector(self.row_selector, timeout=5000)
            except Exception:
                # If rows didn't appear or search filtered all rows out, record zero results
                no_data_img = self.page.locator("img[alt='No Data Found']")
                no_data_text = self.page.locator("text=No Data Found")
                no_data_container = self.page.locator(".no-data-found, .no-data, div:has-text('No Data Found')")

                if (
                    (no_data_img.count() > 0 and no_data_img.first.is_visible())
                    or (no_data_text.count() > 0 and no_data_text.first.is_visible())
                    or (no_data_container.count() > 0 and no_data_container.first.is_visible())
                    or self.page.locator("tbody tr").count() == 0
                ):
                    result["results_found"] = 0
                    logger.info("No data found for query '%s'", query)
                    return result

                result["results_found"] = 0
                logger.info("Search query '%s' yielded 0 matching rows", query)
                return result


            # Try to scope rows to the table nearest the search input to avoid capturing rows
            # from unrelated tables on the page.
            scoped_rows = search_input.locator(
                "xpath=ancestor::div[contains(@class,'component-container')]//table//tbody/tr"
            )

            if scoped_rows.count() == 0:
                scoped_rows = search_input.locator(
                    "xpath=ancestor::div[contains(@class,'component-body')]//table//tbody/tr"
                )

            if scoped_rows.count() == 0:
                scoped_rows = search_input.locator(
                    "xpath=following::table[1]//tbody/tr"
                )

            rows = (
                scoped_rows
                if scoped_rows.count() > 0
                else self.page.locator(self.row_selector)
            )

            # Get stable count once rows are present
            row_count = rows.count()

            # Read all visible row texts in a single DOM evaluation to avoid hidden rows
            try:
                row_texts = rows.evaluate_all(
                    "nodes => nodes.filter(n => n.offsetHeight > 0 && window.getComputedStyle(n).display !== 'none').map(n => n.innerText)"
                )
            except Exception:
                # Fallback to per-row reading if evaluate_all is not supported
                row_texts = []
                for i in range(row_count):
                    try:
                        row_loc = rows.nth(i)
                        if row_loc.is_visible():
                            row_texts.append(row_loc.inner_text())
                    except Exception:
                        logger.warning("Failed to read row %s text via fallback", i)

            for idx, row_text in enumerate(row_texts):
                # Skip empty rows instead of failing—some tables have placeholder/hidden rows
                row_text_str = str(row_text).strip()
                if not row_text_str:
                    logger.debug("Skipping empty row at index %s", idx)
                    continue
                result["results"].append(row_text_str)

            result["results_found"] = len(result["results"])
            logger.info("%s rows found for query '%s'", result["results_found"], query)


        except Exception as exc:
            logger.exception(
                "Search helper failed for query '%s': %s",
                query,
                exc,
            )

            result["success"] = False
            result["error"] = str(exc)

            # Assertion: Fail test immediately if search helper fails
            assert False, f"Search operation failed: {exc}"

        return result
