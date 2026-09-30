import os
import sys
import importlib
from pathlib import Path
import pytest
from playwright.sync_api import sync_playwright

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

import config.config as config_module
from config.global_var import (
    get_project_logs_path,
    get_project_screenshot_path,
    prepare_project_artifact_dirs,
)
from utils.logger import enable_file_logging, get_logger

logger = get_logger(__name__)

ZOOM_SCRIPT = """
() => {
    const applyZoom = () => {
        const zoomLevel = '1';

        if (document.documentElement) {
            document.documentElement.style.zoom = zoomLevel;
        }

        if (document.body) {
            document.body.style.zoom = zoomLevel;
        }
    };

    applyZoom();

    new MutationObserver(applyZoom).observe(document.documentElement, {
        childList: true,
        subtree: true
    });
}
"""

@pytest.fixture(scope="session")
def playwright_instance():
    logger.info("Starting Playwright session for Trio")
    with sync_playwright() as p:
        yield p
    logger.info("Playwright session ended")

@pytest.fixture(scope="session")
def browser(playwright_instance, request):
    browser_type = getattr(playwright_instance, config_module.BROWSER)

    cli_headless = request.config.getoption("--headless", default=False)
    effective_headless = True if cli_headless else config_module.HEADLESS

    launch_args = []
    if effective_headless:
        launch_args = [
            "--disable-gpu",
            "--disable-dev-shm-usage",
            "--no-sandbox",
            "--disable-setuid-sandbox",
            "--window-size=1920,1080",
        ]
    else:
        launch_args = ["--start-maximized"]

    browser = browser_type.launch(
        headless=effective_headless,
        args=launch_args,
    )
    logger.info("Launched Trio browser instance (%s) headless=%s", config_module.BROWSER, effective_headless)
    yield browser
    logger.info("Trio browser instance closed")

def _new_context_with_zoom(browser, **kwargs):
    context = browser.new_context(viewport=None, **kwargs)
    context.add_init_script(ZOOM_SCRIPT)
    return context

def pytest_addoption(parser):
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Run browser in headless mode",
    )

def pytest_configure(config):
    if config.getoption("collectonly", default=False):
        return
    prepare_project_artifact_dirs(project="trio")
    enable_file_logging("trio")

@pytest.fixture(scope="session")
def project_config():
    return {
        "project": "trio",
        "base_url": config_module.BASE_URL,
        "username": config_module.USERNAME,
        "password": config_module.PASSWORD,
        "invalid_username": config_module.INVALID_USERNAME,
        "invalid_password": config_module.INVALID_PASSWORD,
        "dashboard_url": config_module.DASHBOARD_URL,
        "sim_data_details_url": config_module.SIM_DATA_DETAILS_URL,
        "role_management_url": config_module.ROLE_MANAGEMENT_URL,
        "role_group_url": config_module.ROLE_GROUP_URL,
        "device_details_url": config_module.DEVICE_DETAILS_URL,
        "ota_url": config_module.OTA_URL,
        "production_page_url": config_module.PRODUCTION_PAGE_URL,
        "create_production_url": config_module.CREATE_PRODUCTION_URL,
        "add_production_url": config_module.ADD_PRODUCTION_URL,
        "user_management_url": config_module.USER_MANAGEMENT_URL,
        "government_servers_url": config_module.GOVERNMENT_SERVERS_URL,
        "dispatched_device_url": config_module.DISPATCHED_DEVICE_URL,
        "profile_url": config_module.PROFILE_URL,
        "customer_master_url": config_module.CUSTOMER_MASTER_URL,
        "model_url": config_module.MODEL_URL,
        "create_new_model": config_module.CREATE_NEW_MODEL,
        "update_model": config_module.UPDATE_MODEL,
        "api_base_url": config_module.API_BASE_URL,
        "page_title": config_module.PAGE_TITLE,
        "imei": config_module.IMEI,
        "browser": config_module.BROWSER,
        "headless": config_module.HEADLESS,
        "video_recording": config_module.VIDEO_RECORDING,
        "screenshot_on_failure": config_module.SCREENSHOT_ON_FAILURE,
        "log_level": config_module.LOG_LEVEL,
        "api_username": config_module.API_USERNAME,
        "api_password": config_module.API_PASSWORD,
        "customer": config_module.CUSTOMER,
        "login_user": config_module.LOGIN_USER,
        "valid_uid": config_module.VALID_UID,
        "valid_uin": config_module.VALID_UIN,
        "command_to_search": config_module.COMMAND_TO_SEARCH,
        "vin": config_module.VIN,
        "iccid": config_module.ICCID,
    }

@pytest.fixture(scope="session")
def test_data(project_config):
    return {
        "username": project_config.get("username"),
        "password": project_config.get("password"),
        "login_user": project_config.get("login_user"),
        "valid_uid": project_config.get("valid_uid"),
        "valid_uin": project_config.get("valid_uin"),
        "command_to_search": project_config.get("command_to_search"),
        "vin": project_config.get("vin"),
        "iccid": project_config.get("iccid"),
        "customer": project_config.get("customer"),
        "valid_imei": project_config.get("imei"),
    }

@pytest.fixture(scope="session")
def user_storage_state(browser, project_config):
    context = _new_context_with_zoom(browser, accept_downloads=True)
    auth_page = context.new_page()

    from pages.common_login_page import LoginPage

    login = LoginPage(auth_page)
    login.load(project_config["base_url"])
    login.login(project_config["username"], project_config["password"])
    auth_page.wait_for_load_state("networkidle")

    storage_state_data = context.storage_state()
    try:
        session_storage_json = auth_page.evaluate("() => JSON.stringify(sessionStorage)")
    except Exception:
        session_storage_json = "{}"

    auth_page.close()
    context.close()

    return {
        "storage_state": storage_state_data,
        "session_storage": session_storage_json,
    }

@pytest.fixture(scope="function")
def page(browser, project_config, user_storage_state):
    context = _new_context_with_zoom(
        browser,
        accept_downloads=True,
        storage_state=user_storage_state["storage_state"],
    )

    session_storage_json = user_storage_state.get("session_storage", "{}")
    if session_storage_json and session_storage_json != "{}":
        init_script = f"""
        (() => {{
            try {{
                const data = {session_storage_json};
                for (const key in data) {{
                    sessionStorage.setItem(key, data[key]);
                }}
            }} catch (e) {{
                console.error("Failed to seed sessionStorage:", e);
            }}
        }})();
        """
        context.add_init_script(init_script)

    page = context.new_page()

    if page.url == "about:blank":
        page.goto(project_config["base_url"], wait_until="domcontentloaded")
        try:
            page.wait_for_load_state("networkidle", timeout=5000)
        except Exception:
            pass

    yield page
    page.close()
    context.close()

def clean_error_message(err_str: str) -> str:
    if not err_str:
        return ""
    lines = err_str.strip().splitlines()
    if not lines:
        return ""
    for line in lines:
        line_strip = line.strip()
        if line_strip.startswith("E   assert ") or line_strip.startswith("E   AssertionError"):
            return line_strip[4:].strip()
        if line_strip.startswith("E "):
            return line_strip[2:].strip()
    return lines[-1].strip()

@pytest.fixture
def report_case(record_property):
    def _report_case(expected="", actual="", result="", message=""):
        clean_expected = clean_error_message(str(expected)) if expected != "" else ""
        clean_actual = clean_error_message(str(actual)) if actual != "" else ""
        record_property("expected", clean_expected)
        record_property("actual", clean_actual)

        if not result:
            if clean_expected == clean_actual:
                result = "PASS"
            elif clean_expected != "" and clean_actual != "":
                result = "PASS" if str(clean_expected).strip() == str(clean_actual).strip() else ""
            else:
                result = ""

        if result:
            record_property("result", result)
        if message:
            record_property("message", message)

    return _report_case

# Common Page Fixtures
@pytest.fixture
def login_page(browser):
    context = _new_context_with_zoom(browser, accept_downloads=True)
    page = context.new_page()
    from pages.common_login_page import LoginPage
    login = LoginPage(page)
    yield login
    page.close()
    context.close()

@pytest.fixture
def dashboard_page(page, project_config):
    from pages.common_dashboard_page import DashboardPage
    dashboard = DashboardPage(page)
    dashboard.go_to_dashboard(project_config["dashboard_url"])
    return dashboard

@pytest.fixture
def sim_data_details_page(page, project_config):
    from pages.common_sim_data_details_page import SimDataDetailsPage
    sim_data = SimDataDetailsPage(page)
    sim_data.go_to_simbatchpage(project_config["sim_data_details_url"])
    return sim_data

@pytest.fixture
def role_management_page(page, project_config):
    from pages.common_role_management_page import RoleManagementPage
    role_mgt = RoleManagementPage(page)
    role_mgt.go_to_rolemanagementpage(project_config["role_management_url"])
    return role_mgt

@pytest.fixture
def role_group_page(page, project_config):
    from pages.common_role_group_page import RoleGroupPage
    role_grp = RoleGroupPage(page)
    role_grp.go_to_role_group_page(project_config["role_group_url"])
    return role_grp

@pytest.fixture
def device_details_page(page, project_config, test_data):
    device = test_data.get("valid_imei") or project_config.get("imei", "866677075606341")
    from pages.common_dashboard_page import DashboardPage
    from pages.common_device_details_page import DeviceDetailsPage
    from pages.common_base_page import BasePage

    base = BasePage(page)
    dashboard = DashboardPage(page)
    device_details = DeviceDetailsPage(page)

    base.navigate_to(project_config["dashboard_url"])
    result = dashboard.search_helper.run_search(device)
    assert result["success"], f"Search failed: {result['error']}"
    dashboard.click_on_view_device_in_table(device)
    page.wait_for_url("**/device-details")
    return device_details

@pytest.fixture
def ota_page(page, project_config):
    from pages.common_ota_page import OtaPage
    from pages.common_base_page import BasePage
    ota = OtaPage(page)
    base = BasePage(page)
    base.navigate_to(project_config["ota_url"])
    return ota

@pytest.fixture
def dispatched_device_page(page, project_config):
    from pages.common_dispatched_device_page import DispatchedDevicePage
    from pages.common_base_page import BasePage
    dispatched = DispatchedDevicePage(page)
    base = BasePage(page)
    base.navigate_to(project_config["dispatched_device_url"])
    return dispatched

@pytest.fixture
def govt_server_page(page, project_config):
    from pages.common_govt_server_page import GovtServerPage
    from pages.common_base_page import BasePage
    govt = GovtServerPage(page)
    base = BasePage(page)
    base.navigate_to(project_config["government_servers_url"])
    return govt

@pytest.fixture
def profile_page(page, project_config):
    from pages.common_profile_page import ProfilePage
    from pages.common_base_page import BasePage
    profile = ProfilePage(page)
    base = BasePage(page)
    base.navigate_to(project_config["profile_url"])
    return profile

@pytest.fixture
def customer_master(page, project_config):
    from pages.common_customer_master_page import CustomerMasterPage
    customermaster = CustomerMasterPage(page)
    customermaster.go_to_customer(project_config["customer_master_url"])
    return customermaster

@pytest.fixture
def user_management(page, project_config):
    from pages.common_user_management_page import UserManagementPage
    usermanagement = UserManagementPage(page)
    usermanagement.go_to_user(project_config["user_management_url"])
    return usermanagement

@pytest.fixture
def model_page(page, project_config):
    from pages.common_model_page import DeviceModel
    model = DeviceModel(page)
    model.go_to_model(project_config["model_url"])
    return model

@pytest.fixture
def production_devices_page(page, project_config):
    from pages.common_production_devices_page import ProductionDevices
    from pages.common_base_page import BasePage
    production = ProductionDevices(page)
    base = BasePage(page)
    base.navigate_to(project_config["production_page_url"])
    return production
