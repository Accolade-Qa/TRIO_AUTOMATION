import os
import sys
from pathlib import Path
import yaml
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent
PROJECT_NAME = "trio"

# Load environment credentials
load_dotenv(dotenv_path=ROOT.parent / ".env")
load_dotenv(dotenv_path=ROOT / f"{PROJECT_NAME}.env", override=True)

# Load YAML configuration
PROJECT_CONFIG_PATH = ROOT / f"{PROJECT_NAME}.yaml"
_PROJECT_CONFIG = {}
if PROJECT_CONFIG_PATH.exists():
    with PROJECT_CONFIG_PATH.open("r", encoding="utf-8") as f:
        _PROJECT_CONFIG = yaml.safe_load(f) or {}

def _get(key, default=None):
    env_val = os.getenv(key)
    if env_val is not None and str(env_val).strip() != "":
        return env_val
    project_val = _PROJECT_CONFIG.get(key.lower())
    if project_val is not None:
        return project_val
    return default

BASE_URL = _get("BASE_URL")
USERNAME = _get("USERNAME", _get("APP_USERNAME"))
PASSWORD = _get("PASSWORD", _get("APP_PASSWORD"))
LOGIN_USER = _get("LOGIN_USER", USERNAME)
BROWSER = _get("BROWSER", "chromium")
HEADLESS = str(_get("HEADLESS", "True")).lower() == "true"
LOG_LEVEL = _get("LOG_LEVEL", "INFO")
PAGE_TITLE = _get("PAGE_TITLE", _PROJECT_CONFIG.get("page_title", "AEPL Trio QA Diagnostic Cloud"))
DASHBOARD_URL = _get("DASHBOARD_URL", _PROJECT_CONFIG.get("dashboard_url"))
SIM_DATA_DETAILS_URL = _get("SIM_DATA_DETAILS_URL", _PROJECT_CONFIG.get("sim_data_details_url"))
ROLE_MANAGEMENT_URL = _get("ROLE_MANAGEMENT_URL", _PROJECT_CONFIG.get("role_management_url"))
ROLE_GROUP_URL = _get("ROLE_GROUP_URL", _PROJECT_CONFIG.get("role_group_url"))
DEVICE_DETAILS_URL = _get("DEVICE_DETAILS_URL", _PROJECT_CONFIG.get("device_details_url"))
OTA_URL = _get("OTA_URL", _PROJECT_CONFIG.get("ota_url"))
PRODUCTION_PAGE_URL = _get("PRODUCTION_PAGE_URL", _PROJECT_CONFIG.get("production_page_url"))
CREATE_PRODUCTION_URL = _get("CREATE_PRODUCTION_URL", _PROJECT_CONFIG.get("create_production_url"))
ADD_PRODUCTION_URL = _get("ADD_PRODUCTION_URL", _PROJECT_CONFIG.get("add_production_url"))
USER_MANAGEMENT_URL = _get("USER_MANAGEMENT_URL", _PROJECT_CONFIG.get("user_management_url"))
GOVERNMENT_SERVERS_URL = _get("GOVERNMENT_SERVERS_URL", _PROJECT_CONFIG.get("government_servers_url"))
DISPATCHED_DEVICE_URL = _get("DISPATCHED_DEVICE_URL", _PROJECT_CONFIG.get("dispatched_device_url"))
PROFILE_URL = _get("PROFILE_URL", _PROJECT_CONFIG.get("profile_url"))
CUSTOMER_MASTER_URL = _get("CUSTOMER_MASTER_URL", _PROJECT_CONFIG.get("customer_master_url"))
MODEL_URL = _get("MODEL_URL", _PROJECT_CONFIG.get("model_url"))
CREATE_NEW_MODEL = _get("CREATE_NEW_MODEL", _PROJECT_CONFIG.get("create_new_model"))
UPDATE_MODEL = _get("UPDATE_MODEL", _PROJECT_CONFIG.get("update_model"))
API_BASE_URL = _get("API_BASE_URL", _PROJECT_CONFIG.get("api_base_url"))
INVALID_USERNAME = _get("INVALID_USERNAME", "ABCD")
INVALID_PASSWORD = _get("INVALID_PASSWORD", "12345")
IMEI = _get("IMEI", _PROJECT_CONFIG.get("imei"))
VALID_UID = _get("VALID_UID", _PROJECT_CONFIG.get("valid_uid"))
VALID_UIN = _get("VALID_UIN", _PROJECT_CONFIG.get("valid_uin"))
COMMAND_TO_SEARCH = _get("COMMAND_TO_SEARCH", _PROJECT_CONFIG.get("command_to_search"))
VIN = _get("VIN", _PROJECT_CONFIG.get("vin"))
ICCID = _get("ICCID", _PROJECT_CONFIG.get("iccid"))
VIDEO_RECORDING = str(_get("VIDEO_RECORDING", "False")).lower() == "true"
SCREENSHOT_ON_FAILURE = str(_get("SCREENSHOT_ON_FAILURE", "True")).lower() == "true"
API_USERNAME = _get("API_USERNAME", USERNAME)
API_PASSWORD = _get("API_PASSWORD", PASSWORD)
TICKET_BASE_URL = _get("TICKET_BASE_URL", API_BASE_URL)
TICKET_USERNAME = _get("TICKET_USERNAME", API_USERNAME)
TICKET_PASSWORD = _get("TICKET_PASSWORD", API_PASSWORD)
CUSTOMER = _get("CUSTOMER", _PROJECT_CONFIG.get("customer"))
