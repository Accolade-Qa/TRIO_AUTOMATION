from playwright.sync_api import expect
from .common_base_page import BasePage
from utils.logger import get_logger

logger = get_logger(__name__)


class DeviceModel(BasePage):

    def __init__(self, page):
        logger.debug("Initializing DeviceModel with page object")
        super().__init__(page)
        logger.info("DeviceModel initialized successfully")

    def go_to_model(self, url):
        logger.info("Navigating to Device Model page: %s", url)
        logger.debug("Calling page.goto() with URL")
        self.page.goto(url)
        logger.debug("Waiting for network to be idle")
        self.page.wait_for_load_state("networkidle")
        logger.info("Successfully navigated to Device Model page")

    def go_to_create_model(self, url):
        logger.info("Navigating to Create Model page: %s", url)
        logger.debug("Calling page.goto() with URL")
        self.page.goto(url)
        logger.debug("Waiting for network to be idle")
        self.page.wait_for_load_state("networkidle")
        logger.info("Successfully navigated to Create Model page")

    def go_to_update_model(self, url):
        logger.info("Navigating to Update Model page: %s", url)
        logger.debug("Calling page.goto() with URL")
        self.page.goto(url)
        logger.debug("Waiting for network to be idle")
        self.page.wait_for_load_state("networkidle")
        logger.info("Successfully navigated to Update Model page")

    def _nav_list_visibility(self):
        logger.debug("Checking navigation list visibility")
        nav_bar_locator = self.page.locator(".nav-list")
        logger.debug("Waiting for nav list to be visible")
        nav_bar_locator.wait_for(state="visible")
        logger.debug("Highlighting nav list element")
        self.highlight(nav_bar_locator)
        is_enabled = nav_bar_locator.is_enabled()
        logger.info("Navigation list enabled: %s", is_enabled)
        return is_enabled

    def _is_PageTitle_Visible(self):

        logger.debug("Checking if page title is visible")
        page_title_locator = self.page.locator("span:has-text('Device Models')")
        logger.debug("Waiting for page title to be visible")
        page_title_locator.wait_for(state="visible")
        logger.debug("Highlighting page title element")
        self.highlight(page_title_locator)
        is_visible = page_title_locator.is_visible()
        logger.info("Device Models page title visible: %s", is_visible)
        return is_visible

    def _create_model_visibility(self):
        logger.debug("Checking create model button visibility")
        model_button_locator = self.page.get_by_text(
            "Add Device Model open_in_new", exact=True
        )
        logger.debug("Waiting for create model button to be visible")
        model_button_locator.wait_for(state="visible")
        logger.debug("Highlighting create model button")
        self.highlight(model_button_locator)
        is_visible = model_button_locator.is_visible()
        logger.info("Create model button visible: %s", is_visible)
        return is_visible

    def _create_model_click(self):
        logger.info("Clicking create model button")
        logger.debug("Getting Add Device Model open_in_new button locator")
        model_button_locator = self.page.get_by_text(
            "Add Device Model open_in_new", exact=True
        )
        logger.debug("Waiting for model button to be visible")
        model_button_locator.wait_for(state="visible")
        logger.debug("Highlighting model button")
        self.highlight(model_button_locator)
        logger.debug("Clicking model button")
        model_button_locator.click()
        logger.info("Create model button clicked successfully")

    def _create_model_page_title(self):
        logger.debug("Retrieving create model page title")
        page_title_locator = self.page.locator("span.page-title")
        logger.debug("Waiting for page title to be visible")
        page_title_locator.wait_for(state="visible")
        logger.debug("Highlighting page title element")
        self.highlight(page_title_locator)
        title_text = (
            page_title_locator.text_content()
            if page_title_locator.is_visible()
            else None
        )
        logger.info("Create model page title: %s", title_text)
        return title_text

    def _submit_button(self):
        logger.debug("Checking submit button status")
        submit_button_locator = self.page.locator(".submit-button, button[type='submit']").first
        logger.debug("Waiting for submit button to be visible")
        submit_button_locator.wait_for(state="visible", timeout=5000)
        logger.debug("Highlighting submit button")
        self.highlight(submit_button_locator)
        is_visible = submit_button_locator.is_visible()
        logger.info("Submit button visible: %s", is_visible)
        return is_visible

    def _model_code(self, code):
        logger.info("Filling model code: %s", code)
        logger.debug("Getting model code field locator")
        model_code_locator = self.page.get_by_label("Model Code")
        logger.debug("Waiting for model code field to be visible")
        model_code_locator.wait_for(state="visible")
        logger.debug("Highlighting model code field")
        self.highlight(model_code_locator)
        expect(model_code_locator).to_be_visible()
        expect(model_code_locator).to_be_enabled()
        logger.debug("Filling model code field with: %s", code)
        model_code_locator.fill(code)
        logger.info("Model code filled successfully")

    def _model_name(self, name):

        logger.info("Filling model name: %s", name)
        logger.debug("Getting model name field locator")
        model_name_locator = self.page.get_by_label("Model Name")
        logger.debug("Waiting for model name field to be visible")
        model_name_locator.wait_for(state="visible")
        logger.debug("Highlighting model name field")
        self.highlight(model_name_locator)
        assert model_name_locator.is_visible()
        assert model_name_locator.is_enabled()
        logger.debug("Filling model name field with: %s", name)
        model_name_locator.fill(name)
        logger.info("Model name filled successfully")

    def _model_seriel_sequence(self, sequence):

        logger.info("Filling model serial sequence: %s", sequence)
        logger.debug("Getting model serial sequence field locator")
        model_sequence_locator = self.page.get_by_label("Model Serial Sequence")
        logger.debug("Waiting for model serial sequence field to be visible")
        model_sequence_locator.wait_for(state="visible")
        logger.debug("Highlighting model serial sequence field")
        self.highlight(model_sequence_locator)

        if model_sequence_locator.is_visible() and model_sequence_locator.is_enabled():
            logger.debug("Field is visible and enabled, filling with: %s", sequence)
            model_sequence_locator.fill(sequence)
            logger.info("Model serial sequence filled successfully")
        else:
            logger.error("Model Serial Sequence not visible or not enabled")
            raise AssertionError("Model Serial Sequence not found")

    def _hardware_version(self, version):

        logger.info("Filling hardware version: %s", version)
        logger.debug("Getting hardware version field locator")
        hardware_version_locator = self.page.get_by_label("Hardware Version")
        logger.debug("Waiting for hardware version field to be visible")
        hardware_version_locator.wait_for(state="visible")
        logger.debug("Highlighting hardware version field")
        self.highlight(hardware_version_locator)
        if (
            hardware_version_locator.is_visible()
            and hardware_version_locator.is_enabled()
        ):
            logger.debug("Field is visible and enabled, filling with: %s", version)
            hardware_version_locator.fill(version)
            logger.info("Hardware version filled successfully")
        else:
            logger.error("Hardware Version not visible or not enabled")
            raise AssertionError("Hardware Version not found")

    def _submit_button_click(self):

        logger.info("Clicking submit button")
        logger.debug("Getting submit button locator")
        submit_button_locator = self.page.locator(
            ".submit-button.ng-star-inserted, button.submit-button"
        ).first
        logger.debug("Waiting for submit button to be visible")
        submit_button_locator.wait_for(state="visible")
        logger.debug("Highlighting submit button")
        self.highlight(submit_button_locator)

        if submit_button_locator.is_enabled():
            logger.debug("Submit button is enabled, clicking it")
            submit_button_locator.click()
            logger.info("Submit button clicked successfully")
        else:
            logger.error("Submit button is not enabled")
            raise AssertionError("Submit button not enabled")

    def view_icon(self):

        logger.info("Clicking view icon")
        logger.debug("Getting view icon locator")
        view_icon_locator = self.page.locator(
            "table tbody tr button.view-button, table tbody tr mat-icon:has-text('visibility'), table tbody tr button:has(mat-icon), table tbody tr .action-button"
        ).first
        logger.debug("Waiting for view icon to be visible")
        view_icon_locator.wait_for(state="visible", timeout=5000)
        logger.debug("Highlighting view icon")
        self.highlight(view_icon_locator)
        try:
            view_icon_locator.click(timeout=3000)
        except Exception:
            view_icon_locator.click(force=True)
        logger.info("View icon clicked successfully")


    def update_model_code(self, Updatecode):

        logger.info("Updating model code: %s", Updatecode)
        logger.debug("Getting model code field locator")
        up_model_code_locator = self.page.get_by_placeholder("Model Code", exact=True)
        logger.debug("Waiting for model code field to be visible")
        up_model_code_locator.wait_for(state="visible")
        logger.debug("Highlighting model code field")
        self.highlight(up_model_code_locator)
        if up_model_code_locator.is_visible():
            logger.debug("Field is visible, filling with: %s", Updatecode)
            up_model_code_locator.fill(Updatecode)
            logger.info("Model code updated successfully")
        else:
            logger.error("Update Model Code not visible")
            raise AssertionError("Update Model Code not visible")

    def update_model_name(self, Updatename):

        logger.info("Updating model name: %s", Updatename)
        logger.debug("Getting model name field locator")
        up_model_name_locator = self.page.get_by_placeholder("Model Name", exact=True)
        logger.debug("Waiting for model name field to be visible")
        up_model_name_locator.wait_for(state="visible")
        logger.debug("Highlighting model name field")
        self.highlight(up_model_name_locator)
        if up_model_name_locator.is_visible():
            logger.debug("Field is visible, filling with: %s", Updatename)
            up_model_name_locator.fill(Updatename)
            logger.info("Model name updated successfully")
        else:
            logger.error("Update Model Name not visible")
            raise AssertionError("Update Model Name not visible")

    def update_model_seriel_sequence(self, Updatesequence):
        logger.info("Updating model serial sequence: %s", Updatesequence)
        logger.debug("Getting model serial sequence field locator")
        up_model_sequence_locator = self.page.get_by_placeholder(
            "Model Serial Sequence", exact=True
        )
        logger.debug("Waiting for model serial sequence field to be visible")
        up_model_sequence_locator.wait_for(state="visible")
        logger.debug("Highlighting model serial sequence field")
        self.highlight(up_model_sequence_locator)
        if (
            up_model_sequence_locator.is_visible()
            and up_model_sequence_locator.is_enabled()
        ):
            logger.debug(
                "Field is visible and enabled, filling with: %s", Updatesequence
            )
            up_model_sequence_locator.fill(Updatesequence)
            logger.info("Model serial sequence updated successfully")
        else:
            logger.error("Update Model Sequence not visible or not enabled")
            raise AssertionError("Update Model Sequence not visible")

    def update_hardware_version(self, Updateversion):
        logger.info("Updating hardware version: %s", Updateversion)
        logger.debug("Getting hardware version field locator")
        up_hardware_version_locator = self.page.get_by_placeholder(
            "Hardware Version", exact=True
        )
        logger.debug("Waiting for hardware version field to be visible")
        up_hardware_version_locator.wait_for(state="visible")
        logger.debug("Highlighting hardware version field")
        self.highlight(up_hardware_version_locator)
        if (
            up_hardware_version_locator.is_visible()
            and up_hardware_version_locator.is_enabled()
        ):
            logger.debug(
                "Field is visible and enabled, filling with: %s", Updateversion
            )
            up_hardware_version_locator.fill(Updateversion)
            logger.info("Hardware version updated successfully")
        else:
            logger.error("Update Hardware Version not visible or not enabled")
            raise AssertionError("Update Hardware Version not visible")

    def _update_button_click(self):
        logger.info("Clicking update button")
        logger.debug("Getting update button locator")
        Update_button_locator = self.page.get_by_text("Update edit", exact=True)
        logger.debug("Waiting for update button to be visible")
        Update_button_locator.wait_for(state="visible")
        logger.debug("Highlighting update button")
        self.highlight(Update_button_locator)
        if Update_button_locator.is_enabled():
            logger.debug("Update button is enabled, clicking it")
            Update_button_locator.click()
            logger.info("Update button clicked successfully")
        else:
            logger.error("Update button is not enabled")
            raise AssertionError("Update button not enabled")

    def _search_model(self, model):
        logger.info("Searching for model (update page): %s", model)
        logger.debug("Getting search field and button locators")
        search_field_locator = self.page.get_by_placeholder(
            "Search and Press Enter", exact=True
        )
        search_button_locator = self.page.locator(
            "button[class='search-btn'] mat-icon[role='img']"
        )
        logger.debug("Waiting for search field to be visible")
        search_field_locator.wait_for(state="visible")
        logger.debug("Highlighting search button")
        self.highlight(search_button_locator)
        if search_field_locator.is_visible() and search_button_locator.is_enabled():
            logger.debug("Search field and button are ready, filling with: %s", model)
            search_field_locator.fill(model)
            logger.debug("Clicking search button")
            search_button_locator.click()
            logger.info("Model search executed successfully")
        else:
            logger.error("Search field or button not in expected state")
            raise AssertionError("Search field or button not available")

    def _get_updated_model_text(self, text):
        logger.debug("Getting updated model text for: %s", text)
        logger.debug("Building text locator with exact match")
        text_locator = self.page.get_by_text(text, exact=True)
        logger.debug("Waiting for text locator to be visible")
        text_locator.wait_for(state="visible")
        logger.debug("Highlighting text element")
        self.highlight(text_locator)
        inner_text = text_locator.inner_text()
        logger.info("Updated model text retrieved: %s", inner_text)
        return inner_text

    def delete_updated_model(self):
        logger.info("Deleting updated model")
        logger.debug("Getting delete icon locator")
        delete_icon_locator = self.page.locator("mat-icon", has_text="delete").first
        logger.debug("Waiting for delete icon to be visible")
        delete_icon_locator.wait_for(state="visible")
        logger.debug("Highlighting delete icon")
        self.highlight(delete_icon_locator)
        if delete_icon_locator.is_enabled():
            logger.debug("Delete icon is enabled, clicking it")
            delete_icon_locator.click()
            logger.info("Delete icon clicked successfully")
        else:
            logger.error("Delete Icon is not enabled")
            raise AssertionError("Delete Icon not enabled")

    def entire_flow(self):

        logger.info("Running full model create-update-delete scenario")

        model_code = self.page.get_by_label("Model Code")
        expect(model_code).to_be_visible()
        model_code.fill("NewCode")

        model_name = self.page.get_by_label("Model Name")
        expect(model_name).to_be_visible()
        model_name.fill("NewName")

        model_sequence = self.page.get_by_label("Model Serial Sequence")
        expect(model_sequence).to_be_visible()
        model_sequence.fill("NewSeq")

        hardware_version = self.page.get_by_label("Hardware Version")
        expect(hardware_version).to_be_visible()
        hardware_version.fill("NewHW")

        submit_button = self.page.locator(".submit-button.ng-star-inserted")
        expect(submit_button).to_be_visible()
        expect(submit_button).to_be_enabled()
        submit_button.click()

        device_utility = self.page.get_by_text("DEVICE UTILITY", exact=True)
        expect(device_utility).to_be_visible()
        device_utility.click()

        prod_device = self.page.get_by_text("PRODUCTION DEVICE", exact=True)
        expect(prod_device).to_be_visible()
        prod_device.click()

        search_field = self.page.get_by_placeholder(
            "Search and Press Enter", exact=True
        )
        expect(search_field).to_be_visible()
        search_field.fill("866677075606341")

        search_btn = self.page.locator(
            "button[class='search-btn'] mat-icon[role='img']"
        )
        expect(search_btn).to_be_visible()
        search_btn.click()

        self.page.get_by_text("visibility", exact=True).first.click()
        logger.info("Searching for LCT name")
        name_drop = self.page.get_by_text("LCT A4G", exact=True)
        expect(name_drop).to_be_visible()
        name_drop.click()

        logger.info("Selecting new name")
        option_newname = self.page.get_by_text("NewName", exact=True)
        expect(option_newname).to_be_visible()
        option_newname.click()
        self.page.locator("//button[@class='edit-button ng-star-inserted']").click()

        search_field.fill("NewName")
        self.page.get_by_text("search", exact=True).click()

        name_visibility = self.page.locator("td", has_text="NewName").first
        if name_visibility.is_visible():
            logger.info("Model name changed successfully")
        else:
            logger.warning("Model name did not update yet")

        device_utility = self.page.get_by_text("DEVICE UTILITY", exact=True)
        expect(device_utility).to_be_visible()
        device_utility.click()

        model_device = self.page.get_by_text("MODEL", exact=True)
        expect(model_device).to_be_visible()
        model_device.click()

        ref = self.page.locator("//mat-icon[normalize-space()='refresh']")
        expect(ref).to_be_visible()
        ref.click()

        search_field.fill("NewName")
        self.page.get_by_text("search", exact=True).click()

        logger.info("Deleting newname model")

        delete_button = self.page.locator(
            "//button[contains(@class, 'primary-button delete-button')]"
        ).first

        delete_button.wait_for(state="visible", timeout=5000)

        logger.info("Accepting delete request")

        self.page.on("dialog", lambda dialog: dialog.accept())
        delete_button.click()

        self.page.wait_for_load_state("networkidle", timeout=10000)

        self.page.get_by_text("DEVICE UTILITY", exact=True).click()

        self.page.get_by_text("PRODUCTION DEVICE", exact=True).click()

        search_field = self.page.get_by_placeholder(
            "Search and Press Enter", exact=True
        )
        expect(search_field).to_be_visible()
        search_field.fill("866677075606341")

        self.page.locator("button[class='search-btn'] mat-icon[role='img']").click()

        self.page.get_by_text("visibility", exact=True).first.click()
        logger.info("Searching for New Name")
        self.page.get_by_text("NewName", exact=True).click()

        logger.info("Selecting LCT A4G")
        self.page.get_by_text("LCT A4G", exact=True).click()
        self.page.locator("//button[@class='edit-button ng-star-inserted']").click()

        device_utility = self.page.get_by_text("DEVICE UTILITY", exact=True)
        expect(device_utility).to_be_visible()
        device_utility.click()

        model_device = self.page.get_by_text("MODEL", exact=True)
        expect(model_device).to_be_visible()
        model_device.click()

        ref = self.page.locator("//mat-icon[normalize-space()='refresh']")
        expect(ref).to_be_visible()
        ref.click()

        search_field.fill("NewName")
        self.page.get_by_text("search", exact=True).click()

        logger.info("Deleting newname model")

        delete_button = self.page.locator(
            "//button[contains(@class, 'primary-button delete-button')]"
        ).first

        delete_button.wait_for(state="visible", timeout=5000)

        logger.info("Accepting delete request")

        self.page.on("dialog", lambda dialog: dialog.accept())
        delete_button.click()

        self.page.wait_for_load_state("networkidle", timeout=10000)

        logger.info("Full model flow completed")
