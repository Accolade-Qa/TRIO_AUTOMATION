from playwright.sync_api import expect
from .common_base_page import BasePage
import os
from utils.logger import get_logger
from config.global_var import PROD_DOWNLOAD_PATH
from config.config import PRODUCTION_PAGE_URL

logger = get_logger(__name__)


class ProductionDevices(BasePage):

    def __init__(self, page):
        self.page = page

        self.uid_locator = page.get_by_label("UID", exact=True)
        self.imei_locator = page.get_by_placeholder("IMEI", exact=True)
        self.iccid_locator = page.get_by_placeholder("ICCID", exact=True)
        self.mobile_locator = page.get_by_placeholder("Mobile Number", exact=True)
        self.ser_pro_locator = page.get_by_label("Service Provider", exact=True)
        self.alt_mob_locator = page.get_by_label("Alt Mobile No", exact=True)
        self.alt_ser_pro_locator = page.get_by_label("Alt Service Provider", exact=True)
        self.firmware_locator = page.get_by_label("Firmware", exact=True)
        self.sim_vendor_locator = page.get_by_label("SIM Vendor", exact=True)
        self.boot_exp_locator = page.get_by_role("button", name="Open calendar")
        self.submit_button_locator = page.get_by_text("Submit check_circle")
        self.update_button_locator = page.get_by_text("Update edit", exact=True)
        self.bulk_btn_locator = page.get_by_text("Bulk Upload open_in_new", exact=True)
        self.sam_btn_locator = page.locator("button.primary-button")
        self.up_btn_locator = page.locator("input[type='text']")
        self.add_submit_btn_locator = page.get_by_text(
            "Submit check_circle", exact=True
        )
        self.Uploaded_title_locator = page.get_by_text(
            "Uploaded Production Device List", exact=True
        )
        self.export_uploaded_locator = page.locator(
            "body > app-root:nth-child(1) > app-production-device:nth-child(5) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > button:nth-child(1)"
        )
        self.duplicate_title_locator = page.get_by_text(
            "Duplicate Device List", exact=True
        )
        self.export_duplicate_locator = page.locator(
            "body > app-root:nth-child(1) > app-production-device:nth-child(5) > div:nth-child(1) > div:nth-child(3) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > button:nth-child(1)"
        )
        self.invalid_title_locator = page.get_by_text("Invalid Device List", exact=True)
        self.export_invalid_locator = page.locator(
            "body > app-root:nth-child(1) > app-production-device:nth-child(5) > div:nth-child(1) > div:nth-child(4) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > button:nth-child(1)"
        )
        self.add_production_locator = page.get_by_text(
            "Add Production Devices", exact=True
        )

    def go_to_prod(self, url):
        self.page.goto(url)

    def _nav_list_visibility(self):
        nav_bar_locator = self.page.locator("ul.nav-list")
        nav_bar_locator.wait_for(state="visible")
        self.highlight(nav_bar_locator)

        return nav_bar_locator.is_enabled()

    def _is_PageTitle_Visible(self):
        self.page.goto(PRODUCTION_PAGE_URL)
        page_title_locator = self.page.locator(":text-is('Production Device')")
        page_title_locator.wait_for(state="visible")
        self.highlight(page_title_locator)

        return page_title_locator.is_visible()

    def _manual_upload_btn_visibility(self):
        manual_btn_locator = self.page.get_by_text(
            "Manual Upload open_in_new", exact=True
        )
        manual_btn_locator.wait_for(state="visible")
        self.highlight(manual_btn_locator)

        return manual_btn_locator.is_visible()

    def _manual_upload_click(self):
        manual_btn_locator = self.page.get_by_text(
            "Manual Upload open_in_new", exact=True
        )
        manual_btn_locator.wait_for(state="visible")
        self.highlight(manual_btn_locator)

        manual_btn_locator.click()

    def _create_prod_PageTitle(self):
        create_title_locator = self.page.get_by_text(
            "Create Production Device", exact=True
        )
        create_title_locator.wait_for(state="visible")
        self.highlight(create_title_locator)

        return create_title_locator.is_visible()

    def _uid_visibility(self):

        self.uid_locator.wait_for(state="visible")
        self.highlight(self.uid_locator)

        return self.uid_locator.is_visible()

    def _new_uid(self):

        self.uid_locator.wait_for(state="visible")
        self.highlight(self.uid_locator)
        self.uid_locator.fill("ACONSBA102500012345")

    def _new_imei(self):

        self.imei_locator.wait_for(state="visible")
        self.highlight(self.imei_locator)
        self.imei_locator.fill("866677075612345")

    def _new_iccid(self):

        self.iccid_locator.wait_for(state="visible")
        self.highlight(self.iccid_locator)
        self.iccid_locator.fill("89916450244842412345")

    def _new_model_name(self, value):
        try:
            backdrop = self.page.locator(".cdk-overlay-backdrop")
            if backdrop.is_visible():
                self.page.keyboard.press("Escape")
                self.page.wait_for_timeout(200)
        except Exception:
            pass

        self.dropdown = self.page.get_by_role("combobox").first
        self.dropdown.wait_for(state="visible", timeout=5000)
        self.highlight(self.dropdown)
        logger.info(f"Selecting role type: {value}")

        # Click mat-select dropdown
        try:
            self.dropdown.click(timeout=5000)
        except Exception:
            self.dropdown.click(force=True)

        # Wait for dropdown options panel
        try:
            self.page.locator("mat-option").first.wait_for(state="visible", timeout=5000)
            opt = self.page.locator("mat-option").filter(has_text=value).first
            if opt.is_visible():
                opt.click()
            else:
                self.page.locator("mat-option").first.click()
        except Exception as e:
            logger.warning("Failed to select mat-option for %s: %s", value, e)


    def _new_mobile_no(self):

        self.mobile_locator.wait_for(state="visible")
        self.highlight(self.mobile_locator)
        self.mobile_locator.fill("918273645512345")

    def _new_service_provider(self):

        self.ser_pro_locator.wait_for(state="visible")
        self.highlight(self.ser_pro_locator)
        self.ser_pro_locator.fill("Airtel")

    def _new_alt_mob_no(self):

        self.alt_mob_locator.wait_for(state="visible")
        self.highlight(self.alt_mob_locator)
        self.alt_mob_locator.fill("9182736455")

    def _new_alt_ser_pro(self):

        self.alt_ser_pro_locator.wait_for(state="visible")
        self.highlight(self.alt_ser_pro_locator)
        self.alt_ser_pro_locator.fill("BSNL")

    def _new_firmware(self):

        self.firmware_locator.wait_for(state="visible")
        self.highlight(self.firmware_locator)
        self.firmware_locator.fill("1.0.0")

    def _new_sim_vendor(self):

        self.sim_vendor_locator.evaluate(
            "element => element.scrollIntoView({block: 'center'})"
        )

        self.sim_vendor_locator.wait_for(state="visible")
        self.highlight(self.sim_vendor_locator)
        self.sim_vendor_locator.fill("Sensorise")

    def _new_boot_exp_date(self):

        self.boot_exp_locator.click()

        next_month = self.page.get_by_role("button", name="Next month")

        next_month.wait_for(state="visible")
        next_month.click()

        date = self.page.get_by_role("gridcell", name="15")

        date.wait_for(state="visible")
        date.click()

    def _submit_button(self):

        self.submit_button_locator.wait_for(state="visible")
        self.highlight(self.submit_button_locator)

        if self.submit_button_locator.is_enabled():
            self.submit_button_locator.click()
        else:
            raise AssertionError("Submit button not enabled")

    def _new_device_flow(self):

        self.uid_locator.fill("ACON4IA123455432100")

        self.imei_locator.fill("123455432109876")

        self.iccid_locator.fill("54321098766789012345")

        self.dropdown = self.page.get_by_role("combobox").first
        self.dropdown.click()
        try:
            self.page.locator("mat-option").first.wait_for(timeout=3000)
            self.page.locator("mat-option").first.click()
        except Exception:
            pass

        self.mobile_locator.fill("918273645512345")

        self.ser_pro_locator.fill("Airtel")

        self.alt_mob_locator.fill("918273645512345")

        self.alt_ser_pro_locator.fill("BSNL")

        self.firmware_locator.fill("1.0.0")

        self.sim_vendor_locator.fill("Sensorise")

        # self.boot_exp_locator.fill("15/05/2026")
        self.boot_exp_locator.click()
        next_month = self.page.get_by_role("button", name="Next month")
        next_month.click()

        date = self.page.get_by_role("gridcell", name="15")

        date.wait_for(state="visible")
        date.click()
        self.highlight(self.boot_exp_locator)

        if self.submit_button_locator.is_visible() and self.submit_button_locator.is_enabled():
            self.submit_button_locator.click()

    def _search_device(self):

        self.search_locator = self.page.get_by_placeholder(
            "Search and Press Enter", exact=True
        )
        self.search_locator.wait_for(state="visible")
        self.highlight(self.search_locator)
        self.search_locator.fill("ACON4IA123455432100")
        self.search_locator.press("Enter")
        self.page.wait_for_timeout(500)
        
        view_icon = self.page.locator("//tbody/tr[1]/td[5]/div[1]/button[1]/mat-icon[1]").first
        if view_icon.is_visible():
            view_icon.click(force=True)

        dropdown = self.page.get_by_role("combobox").first
        if dropdown.is_visible():
            dropdown.click()
            try:
                self.page.locator("mat-option").first.wait_for(timeout=3000)
                self.page.locator("mat-option").first.click()
            except Exception:
                pass

        if self.mobile_locator.is_visible():
            self.mobile_locator.fill("918273645554321")

        if self.ser_pro_locator.is_visible():
            self.ser_pro_locator.fill("Jio")

        if self.alt_mob_locator.is_visible():
            self.alt_mob_locator.fill("918273645554321")

        if self.alt_ser_pro_locator.is_visible():
            self.alt_ser_pro_locator.fill("Jio")

        if self.firmware_locator.is_visible():
            self.firmware_locator.fill("1.1.1")

        if self.sim_vendor_locator.is_visible():
            self.sim_vendor_locator.fill("Sensorise123")

        if self.boot_exp_locator.is_visible():
            self.boot_exp_locator.click()
            next_month = self.page.get_by_role("button", name="Next month")
            if next_month.is_visible():
                next_month.click()

            date = self.page.get_by_role("gridcell", name="28")
            if date.is_visible():
                date.click()
            self.highlight(self.boot_exp_locator)

        if self.update_button_locator.is_visible() and self.update_button_locator.is_enabled():
            self.update_button_locator.click()

    def _search_device_2(self):

        self.search_locator = self.page.get_by_placeholder(
            "Search and Press Enter", exact=True
        )
        self.search_locator.wait_for(state="visible")
        self.highlight(self.search_locator)
        self.search_locator.fill("ACON4IA123455432100")
        self.search_locator.press("Enter")
        self.page.wait_for_timeout(500)

        dlt_icon = self.page.locator(
            "tbody tr:nth-child(1) td:nth-child(5) div:nth-child(1) button:nth-child(2) mat-icon:nth-child(1)"
        ).first

        self.page.on("dialog", lambda dialog: dialog.accept())

        if dlt_icon.is_visible():
            dlt_icon.click(force=True)

        dlt_btn = self.page.get_by_text("delete", exact=True).first
        if dlt_btn.is_visible():
            dlt_btn.click(force=True)


    def _bulk_upload_btn_enability(self):
        bulk_btn_locator = self.page.get_by_text("Bulk Upload open_in_new", exact=True)
        bulk_btn_locator.wait_for(state="visible")
        self.highlight(bulk_btn_locator)
        return bulk_btn_locator.is_enabled()

    def _click_bulk_btn(self):
        self.bulk_btn_locator.wait_for(state="visible")
        self.highlight(self.bulk_btn_locator)
        self.bulk_btn_locator.click()

    def _btn_enability(self):

        self.sam_btn_locator.wait_for(state="visible")
        self.highlight(self.sam_btn_locator)

        assert self.sam_btn_locator.is_enabled()
        assert self.up_btn_locator.is_enabled()
        assert not self.add_submit_btn_locator.is_enabled()

    def click_sample_btn(self):
        self.sam_btn_locator.wait_for(state="visible")
        self.highlight(self.sam_btn_locator)

        with self.page.expect_download() as download_info:
            self.sam_btn_locator.click()

        download = download_info.value
        logger.info("download value is %s", download)

        return download

    def is_sample_file_downloaded(
        self,
        download,
        download_path=PROD_DOWNLOAD_PATH,
        expected_filename="Sample_Production_Sheet.xlsx",
    ):

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

        return True

    def upload_invalid_file(self, file_path):
        self.highlight(self.up_btn_locator)
        logger.info("started")
        self.page.locator("input[type='file']").set_input_files(file_path)
        logger.info("finished")
        rows = self.page.locator("table tbody tr")

        row_count = rows.count()

        self.export_invalid_locator

        return (
            row_count > 0 and self.export_invalid_locator.is_enabled(),
            "Export button is disabled",
        )

    def _check_file(self):
        self.add_submit_btn_locator.wait_for(state="visible")
        self.add_submit_btn_locator.click()

        logger.info("started")

        self.duplicate_title_locator.evaluate(
            "element => element.scrollIntoView({block: 'center'})"
        )

        self.invalid_title_locator.evaluate(
            "element => element.scrollIntoView({block: 'center'})"
        )

        self.add_production_locator.evaluate(
            "element => element.scrollIntoView({block: 'center'})"
        )

        self.Uploaded_title_locator.wait_for(state="visible")
        self.export_uploaded_locator.wait_for(state="visible")
        self.duplicate_title_locator.wait_for(state="visible")
        self.export_duplicate_locator.wait_for(state="visible")
        self.invalid_title_locator.wait_for(state="visible")
        self.export_invalid_locator.wait_for(state="visible")

        self.highlight(self.Uploaded_title_locator)
        self.highlight(self.export_uploaded_locator)
        self.highlight(self.duplicate_title_locator)
        self.highlight(self.export_duplicate_locator)
        self.highlight(self.invalid_title_locator)
        self.highlight(self.export_invalid_locator)

        result = (
            self.Uploaded_title_locator.is_visible()
            and self.export_uploaded_locator.is_visible()
            and self.duplicate_title_locator.is_visible()
            and self.export_duplicate_locator.is_visible()
            and self.invalid_title_locator.is_visible()
            and self.export_invalid_locator.is_visible()
        )

        self.page.reload()
        self.page.wait_for_load_state("networkidle")

        return result

    def upload_valid_file(self, file_path):
        self.highlight(self.up_btn_locator)
        self.page.locator("input[type='file']").set_input_files(file_path)
        rows = self.page.locator("table tbody tr")

        row_count = rows.count()

        self.export_uploaded_locator

        return (
            row_count > 0 and self.export_uploaded_locator.is_enabled(),
            "Export button is disabled",
        )

    def upload_duplicate_file(self, file_path):

        self.page.locator("input[type='file']").set_input_files(file_path)

        rows = self.page.locator("table tbody tr")

        row_count = rows.count()

        self.export_duplicate_locator

        return (
            row_count > 0 and self.export_duplicate_locator.is_enabled(),
            "Export button is disabled",
        )
