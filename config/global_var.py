import os
import platform
import sys
from datetime import datetime

if platform.system() == "Windows":
    path_divider = "\\"
else:
    path_divider = "/"

ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
CONFIG_PATH = os.path.join(ROOT_DIR, "config")
DATA_FILES_PATH = os.path.join(ROOT_DIR, "test_data")
SCREENSHOT_PATH = os.path.join(ROOT_DIR, f"Artifacts{path_divider}Screenshots")
LOGS_PATH = os.path.join(ROOT_DIR, f"Artifacts{path_divider}Logs")
VIDEO_DIR = os.path.join(ROOT_DIR, f"Artifacts{path_divider}Videos")
DOWNLOADS_PATH = os.path.join(ROOT_DIR, f"Artifacts{path_divider}Downloads")
PROD_DOWNLOAD_PATH = os.path.join(ROOT_DIR, f"Artifacts{path_divider}Downloads")

def get_current_project(default="trio"):
    return "trio"

_ARTIFACT_RUN_ID = os.getenv("ARTIFACT_RUN_ID")

def get_artifact_run_id():
    global _ARTIFACT_RUN_ID
    if _ARTIFACT_RUN_ID:
        return _ARTIFACT_RUN_ID

    _ARTIFACT_RUN_ID = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    _ARTIFACT_RUN_ID = f"{_ARTIFACT_RUN_ID}_pid-{os.getpid()}"
    return _ARTIFACT_RUN_ID

def get_project_logs_path(project=None, run_id=None):
    return os.path.join(
        LOGS_PATH,
        project or get_current_project(),
        run_id or get_artifact_run_id(),
    )

def get_project_screenshot_path(project=None, run_id=None):
    return os.path.join(
        SCREENSHOT_PATH,
        project or get_current_project(),
        run_id or get_artifact_run_id(),
    )

def prepare_project_artifact_dirs(project=None, run_id=None):
    project_name = (project or get_current_project() or "trio").lower()
    resolved_run_id = run_id or get_artifact_run_id()

    logs_dir = os.path.join(LOGS_PATH, project_name, resolved_run_id)
    screenshot_dir = os.path.join(SCREENSHOT_PATH, project_name, resolved_run_id)

    os.makedirs(logs_dir, exist_ok=True)
    os.makedirs(screenshot_dir, exist_ok=True)

    return {
        "project": project_name,
        "run_id": resolved_run_id,
        "logs_dir": logs_dir,
        "screenshots_dir": screenshot_dir,
    }
