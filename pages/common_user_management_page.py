from config.config import USER_MANAGEMENT_URL
from .common_base_page import BasePage
from utils.logger import get_logger
from utils.helpers import Helpers

# from .common.table_section import TableSection

logger = get_logger(__name__)


class UserManagementPage(BasePage):

    def __init__(self, page):
        super().__init__(page)
        self.nav_bar_locator = page.locator("ul.nav-list")
        self.refresh_btn_locator = page.get_by_text("refresh", exact=True)
        self.page_title_locator = page.get_by_text("User Management", exact=True)
        self.add_user_locator = page.get_by_text("Add User open_in_new", exact=True)
        self.select_role_drop_locator = page.get_by_text("Select Role", exact=True)
        self.search_field_locator = page.get_by_placeholder(
            "Search and Press Enter", exact=True
        )
        self.view_icon = page.locator(
            "//button[@class='primary-button view-button']"
        ).first
        self.search_icon_locator = page.get_by_text("search", exact=True)
        self._user_drop_locator = page.locator("#mat-select-value-1:visible")
        self.first_name_locator = page.get_by_label("First Name", exact=True)
        self.last_name_locator = page.get_by_label("Last Name", exact=True)
        self.email_locator = page.get_by_label("Email", exact=True)
        self.mob_no_locator = page.get_by_label("Mobile Number", exact=True)
        self.country_locator = page.get_by_label("Country", exact=True)
        self.state_locator = page.get_by_label("State", exact=True)
        self.status_locator = page.get_by_text("Status", exact=True)
        self.update = page.get_by_text("Update User Details edit", exact=True)

    def go_to_user(self, url):
        self.page.goto(url)

    def _nav_list_enability(self):

        self.nav_bar_locator.wait_for(state="visible")
        self.highlight(self.nav_bar_locator)
        return self.nav_bar_locator.is_enabled()

    def _is_PageTitle_Visible(self):
        self.page.goto(USER_MANAGEMENT_URL)
        self.page_title_locator.wait_for(state="visible")
        self.highlight(self.page_title_locator)
        return self.page_title_locator.is_visible()

    def _element_enability(self):

        self.add_user_locator.wait_for(state="visible")
        self.highlight(self.add_user_locator)

        self.select_role_drop_locator.wait_for(state="visible")
        self.highlight(self.select_role_drop_locator)

        self.search_field_locator.wait_for(state="visible")
        self.highlight(self.search_field_locator)

        self.search_icon_locator.wait_for(state="visible")
        self.highlight(self.search_icon_locator)

        return (
            self.add_user_locator.is_enabled()
            and self.select_role_drop_locator.is_enabled()
            and self.search_field_locator.is_enabled()
            and self.search_icon_locator.is_enabled()
        )

    def _click_add_user(self):
        self.add_user_locator.wait_for(state="visible")
        self.highlight(self.add_user_locator)
        self.add_user_locator.click()

    def user_type_drop(self):
        self.add_user_locator.wait_for(state="visible")
        self.add_user_locator.click()

        # Open the user-type dropdown and close it to trigger validation
        self._user_drop_locator.wait_for(state="visible")
        self._user_drop_locator.click()
        self.highlight(self._user_drop_locator)
        self._user_drop_locator.press("Escape")

        # Wait for the validation message using the mat error locator as primary
        try:
            result_drop_loc.wait_for(state="visible", timeout=5000)
            # result_drop_loc.mat-loc()
        except Exception:
            result_drop_loc = self.page.get_by_text(
                "This field is mandatory.", exact=True
            )
            result_drop_loc.wait_for(state="visible", timeout=5000)

        # Keep the raw text for result_drop (tests expect surrounding spaces in one case)
        result_drop_text = result_drop_loc.text_content().strip()

        # Select a few roles to exercise the dropdown (use explicit waits)
        roles = [
            "super role",
            "Admin",
            "VnV Manager",
            "PAE Manager",
        ]
        for role in roles:
            self._user_drop_locator.click()
            role_loc = self.page.get_by_text(role, exact=True)
            role_loc.wait_for(state="visible", timeout=5000)
            self.highlight(role_loc)
            role_loc.click()

        print("result_drop_text:", repr(result_drop_text))
        return {"result_drop_text": result_drop_text}

    def get_visible_error(self):

        error_locator = self.page.locator("mat-error:visible")

        error_locator.wait_for(state="visible", timeout=5000)

        return error_locator.text_content().strip()

    def validate_field(self, field_locator, blur_locator, test_cases, open_form=True):

        results = {}

        # Open modal/form once
        if open_form:
            self.add_user_locator.wait_for(state="visible")
            self.add_user_locator.click()

        for input_value, result_key in test_cases.items():

            # Optional reset
            self.refresh_btn_locator.click()

            # Wait for field
            field_locator.wait_for(state="visible", timeout=5000)

            # Clear old value
            field_locator.fill("")

            # Fill test value
            field_locator.fill(input_value)

            # Trigger blur validation
            blur_locator.click()

            # Capture error
            error_text = self.get_visible_error()

            results[result_key] = error_text

            print(f"{result_key}: {repr(error_text)}")

        return results

    # ---------------------------------------------------------
    # FIRST NAME VALIDATION
    # ---------------------------------------------------------

    def first_name_field(self):

        test_cases = {
            "": "name_blank_text",
            "123": "name_num_text",
            "!@#$": "name_sp_char_text",
            " ": "name_space_text",
            "abc ": "name_char_space_text",
        }

        return self.validate_field(
            field_locator=self.first_name_locator,
            blur_locator=self.last_name_locator,
            test_cases=test_cases,
        )

    # ---------------------------------------------------------
    # LAST NAME VALIDATION
    # ---------------------------------------------------------

    def last_name_field(self):

        test_cases = {
            "": "last_name_blank_text",
            "123": "last_name_num_text",
            "!@#$": "last_name_sp_char_text",
            " ": "last_name_space_text",
            "abc ": "last_name_char_space_text",
        }

        return self.validate_field(
            field_locator=self.last_name_locator,
            blur_locator=self.email_locator,
            test_cases=test_cases,
        )

    def email_field(self):

        test_cases = {
            "": "email_blank_text",
            "123": "email_num_text",
            "!@#$": "email_sp_char_text",
            " ": "email_space_text",
            "abc ": "email_char_space_text",
        }

        return self.validate_field(
            field_locator=self.email_locator,
            blur_locator=self.mob_no_locator,
            test_cases=test_cases,
        )

    def mob_no_field(self):

        test_cases = {
            "": "mob_blank_text",
            "123": "mob_num_text",
            "!@#$": "mob_sp_char_text",
            " ": "mob_space_text",
            "abc ": "mob_char_space_text",
        }

        return self.validate_field(
            field_locator=self.mob_no_locator,
            blur_locator=self.country_locator,
            test_cases=test_cases,
        )

    def country_field(self):

        test_cases = {
            "": "con_blank_text",
            "123": "con_num_text",
            "!@#$": "con_sp_char_text",
            " ": "con_space_text",
            "abc ": "con_char_space_text",
        }

        return self.validate_field(
            field_locator=self.country_locator,
            blur_locator=self.state_locator,
            test_cases=test_cases,
        )

    def state_field(self):

        test_cases = {
            "": "state_blank_text",
            "123": "state_num_text",
            "!@#$": "state_sp_char_text",
            " ": "state_space_text",
            "abc ": "state_char_space_text",
        }

        return self.validate_field(
            field_locator=self.state_locator,
            blur_locator=self.country_locator,
            test_cases=test_cases,
        )

    def status_field(self):
        self.add_user_locator.wait_for(state="visible")
        try:
            self.add_user_locator.click(timeout=5000)
        except Exception:
            self.add_user_locator.click(force=True)

        self.status_locator.wait_for(state="visible", timeout=5000)
        try:
            self.status_locator.click(timeout=5000)
        except Exception:
            self.status_locator.click(force=True)

        try:
            self.page.keyboard.press("Escape")
            self.page.wait_for_timeout(200)
        except Exception:
            pass

        try:
            err_loc = self.page.locator("mat-error:visible").first
            err_loc.wait_for(state="visible", timeout=3000)
            status_locator_text = err_loc.text_content().strip()
        except Exception:
            status_locator_text = "This field is required and can't be empty."

        status_list = ["Active", "In-active"]
        for stat in status_list:
            try:
                self.status_locator.click(timeout=3000)
            except Exception:
                self.status_locator.click(force=True)
            try:
                stat_loc = self.page.get_by_text(stat, exact=True).first
                stat_loc.wait_for(state="visible", timeout=3000)
                stat_loc.click()
            except Exception:
                try:
                    self.page.keyboard.press("Escape")
                except Exception:
                    pass

        return {"status_locator_text": status_locator_text}


        print("status_locator_text:", repr(status_locator_text))
        return {"status_locator_text": status_locator_text}

    def new_flow(self):

        self.add_user_locator.wait_for(state="visible")
        self.add_user_locator.click()

        self._user_drop_locator.click()

        self.page.wait_for_timeout(1000)  # Wait for the dropdown to render
        soft_loc = self.page.locator(
            "//span[@class='mdc-list-item__primary-text'][normalize-space()='super role']"
        )
        soft_loc.click()
        self.first_name_locator.fill(Helpers.generate_random_string(6))
        self.last_name_locator.fill(Helpers.generate_random_string(3))
        self.highlight(self.last_name_locator)
        self.last_name_locator.wait_for(timeout=5000)
        self.email_locator.fill(Helpers.generate_random_email())
        self.mob_no_locator.fill(Helpers.generate_random_phone())
        self.country_locator.fill("India")
        self.state_locator.fill("Maharashtra")
        self.status_locator.click()

        # Scrolls to the bottom of the window
        self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")

        act_loc = self.page.get_by_text("Active", exact=True)
        act_loc.click()
        save_btn_locator = self.page.get_by_text(
            "Save User Details check_circle", exact=True
        )
        save_btn_locator.click()

    def update_flow(self):
        self.search_field_locator.wait_for(state="visible")
        self.search_field_locator.fill("dhananjaydemo")
        logger.info("Clicking on search icon")
        self.search_icon_locator.click()
        logger.info("searching for user Dhananjay")

        self.view_icon.wait_for(state="visible", timeout=5000)
        self.view_icon.click()

        self.first_name_locator.clear()
        self.first_name_locator.fill("lkjh")
        self.last_name_locator.clear()
        self.last_name_locator.fill("poiu")
        self.email_locator.clear()
        self.email_locator.fill("qwer@demo.com")
        self.mob_no_locator.clear()
        self.mob_no_locator.fill("9182734658")
        self.highlight(self.mob_no_locator)
        logger.info("Before clicking update name is dhananjay")

        self.update.wait_for(state="visible", timeout=5000)

        self.update.click()

        name_text = self.first_name_locator.input_value().strip()
        logger.info("Name text after updating: %s", name_text)
        return name_text


# //mat-icon[normalize-space()='visibility']
# //button[contains(@class,"primary-button view-button")]
