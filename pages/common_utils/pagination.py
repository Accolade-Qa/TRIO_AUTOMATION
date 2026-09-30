from __future__ import annotations

from typing import Optional

from playwright.sync_api import Page, Locator

from utils.logger import get_logger

logger = get_logger(__name__)


class PaginationHelper:

    def __init__(
        self,
        page: Page,
        page_input: str = "input.page-input",
        next_button: str = "button:has(mat-icon:has-text('chevron_right'))",
        prev_button: Optional[str] = None,
        content_selector: str | Locator = "div.component-body table",
        total_pages_selector: str = "text=/\\d+\\s*/\\s*\\d+/",
        max_forward_steps: Optional[int] = 8,
        max_backward_steps: Optional[int] = None,
    ):
        self.page = page
        self.page_input = page_input
        self.next_button = next_button
        self.prev_button = prev_button
        self.content_selector = content_selector
        self.total_pages_selector = total_pages_selector
        self.max_forward_steps = max_forward_steps
        self.max_backward_steps = max_backward_steps

    def _get_current_page(self, locator):
        raw_value = locator.input_value()
        try:
            return int(raw_value)
        except ValueError:
            digits = "".join(filter(str.isdigit, raw_value))
            if digits:
                return int(digits)
        return 1

    def get_pagination_count(self) -> int:
        input_locator = self.page.locator(self.page_input)
        input_locator.wait_for(state="visible")
        current_page = self._get_current_page(input_locator)
        total_pages = self._detect_total_pages(current_page)
        return total_pages

    def _wait_for_value_change(self, previous_value: str):
        script = (
            "({prev, selector}) => {"
            "  const el = document.querySelector(selector);"
            "  return el && el.value !== prev;"
            "}"
        )
        self.page.wait_for_function(
            script,
            arg={"prev": previous_value, "selector": self.page_input},
        )

    def _detect_total_pages(self, fallback: int) -> int:
        locator = self.page.locator(self.total_pages_selector)
        if locator.count() > 0:
            raw_text = locator.first.inner_text()
            if "/" in raw_text:
                candidate = raw_text.split("/")[-1].strip()
                if candidate.isdigit():
                    return int(candidate)
        return fallback

    def verify(self, include_backward: bool = False) -> dict:
        result = {
            "success": True,
            "pages_visited": [],
            "total_pages": 0,
            "error": None,
        }

        try:
            input_locator = self.page.locator(self.page_input)
            content_locator = (
                self.content_selector
                if not isinstance(self.content_selector, str)
                else self.page.locator(self.content_selector)
            )
            input_locator.wait_for(state="visible")
            content_locator.first.wait_for(state="visible")

            current_page = self._get_current_page(input_locator)
            total_pages = self._detect_total_pages(current_page)
            result["total_pages"] = total_pages
            logger.info(
                "Pagination verification started at page %s (total candidates %s)",
                current_page,
                total_pages,
            )

            visited = {current_page}
            result["pages_visited"].append(current_page)

            if total_pages <= 1:
                logger.info(
                    "Pagination has only one page (%s); skipping navigation",
                    current_page,
                )
                result["total_pages"] = 1
                return result

            steps = 0
            while True:
                if (
                    self.max_forward_steps is not None
                    and steps >= self.max_forward_steps
                ):
                    break

                next_button = self.page.locator(self.next_button)
                if next_button.count() == 0:
                    logger.warning("Next button not found during pagination")
                    result["success"] = False
                    result["error"] = "Next button not found"
                    break

                if next_button.is_disabled():
                    logger.info("Reached last page of pagination")
                    break

                prev_content = content_locator.inner_text()
                next_button.scroll_into_view_if_needed()
                next_button.click()

                self._wait_for_value_change(str(current_page))

                current_page = self._get_current_page(input_locator)
                if current_page in visited:
                    logger.warning(
                        "Pagination loop detected: current %s already visited",
                        current_page,
                    )
                    result["success"] = False
                    result["error"] = "Pagination loop detected"
                    break

                if current_page != result["pages_visited"][-1] + 1:
                    logger.warning(
                        "Page increment mismatch: expected %s got %s",
                        result["pages_visited"][-1] + 1,
                        current_page,
                    )
                    result["success"] = False
                    result["error"] = (
                        f"Page did not increment correctly: {result['pages_visited'][-1]} -> {current_page}"
                    )
                    break

                new_content = content_locator.inner_text()
                if prev_content == new_content:
                    logger.warning(
                        "Content did not change after pagination from page %s, but page index updated", current_page
                    )

                visited.add(current_page)
                result["pages_visited"].append(current_page)
                steps += 1

            if include_backward and self.prev_button:
                backward_steps = 0
                backward_limit = len(result["pages_visited"]) - 1
                if self.max_backward_steps is not None:
                    backward_limit = min(backward_limit, self.max_backward_steps)

                logger.info(
                    "Starting backward pagination verification (limit %s)",
                    backward_limit,
                )

                while backward_steps < backward_limit:
                    prev_button = self.page.locator(self.prev_button)
                    if prev_button.is_disabled():
                        logger.info("Reached first page during backward pagination")
                        break

                    prev_content = content_locator.inner_text()
                    prev_button.scroll_into_view_if_needed()
                    prev_button.click()

                    self._wait_for_value_change(str(current_page))
                    current_page = self._get_current_page(input_locator)

                    expected_previous = result["pages_visited"][-1] - 1
                    if current_page != expected_previous:
                        logger.warning(
                            "Backward pagination mismatch: expected %s got %s",
                            expected_previous,
                            current_page,
                        )
                        result["success"] = False
                        result["error"] = (
                            f"Backward pagination issue: {result['pages_visited'][-1]} -> {current_page}"
                        )
                        break

                    new_content = content_locator.inner_text()
                    if prev_content == new_content:
                        logger.warning(
                            "Backward pagination content did not change at page %s",
                            current_page,
                        )
                        result["success"] = False
                        result["error"] = "Content did not change on previous page"
                        break

                    result["pages_visited"].append(current_page)
                    backward_steps += 1

            result["total_pages"] = max(
                result["total_pages"], len(result["pages_visited"])
            )

        except Exception as exc:
            logger.exception("Pagination helper raised exception: %s", exc)
            result["success"] = False
            result["error"] = str(exc)

        return result
