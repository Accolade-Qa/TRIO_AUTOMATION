from pages.common_login_page import LoginPage
from utils.logger import get_logger
import time
from config.global_var import SCREENSHOT_PATH

import re
import pytest

logger = get_logger(__name__)


@pytest.mark.auth
@pytest.mark.critical
@pytest.mark.regression
class TestLoginPage:
    @pytest.fixture(autouse=True)
    def log_test_case(self, request):
        test_name = request.node.name
        logger.info("Starting Login Page test: %s", test_name)
        logger.debug("Executing test node: %s", request.node.nodeid)
        yield
        report = getattr(request.node, "rep_call", None)
        if report is None:
            logger.debug("Login Page test finished without call report: %s", test_name)
        elif report.passed:
            logger.info("Login Page test passed: %s", test_name)
        elif report.failed:
            logger.error("Login Page test failed: %s", test_name)
            logger.debug(
                "Login Page failure details for %s: %s",
                test_name,
                report.longrepr,
            )
        elif report.skipped:
            logger.warning("Login Page test skipped: %s", test_name)

    @pytest.mark.smoke
    @pytest.mark.regression
    def test_login_page_valid_credentials_authentication(
        self,
        login_page,
        project_config,
        test_data,
        report_case,
    ):
        logger.info("Starting validation of login with valid credentials")
        login_page.load(project_config["base_url"])

        expected_url = project_config["dashboard_url"]
        login_page.login(
            project_config["username"],
            project_config["password"],
        )

        login_page.page.wait_for_url("**/device-dashboard-page", timeout=60000)
        actual_url = login_page.page.url

        assert project_config["username"] in [
            test_data.get("login_user"),
            test_data.get("username"),
        ], "Configured username should match project login user"
        assert (
            project_config["dashboard_url"] in actual_url
        ), f"Expected dashboard URL to contain {project_config['dashboard_url']}, got {actual_url}"

        report_case(
            expected=expected_url,
            actual=actual_url,
            message="Validate successful navigation to dashboard after login",
        )

        assert actual_url == expected_url, (
            f"Expected to navigate to '{expected_url}' after login, "
            f"but got '{actual_url}'"
        )

    @pytest.mark.smoke
    @pytest.mark.regression
    def test_login_page_invalid_credentials_error(
        self,
        login_page,
        project_config,
        report_case,
    ):
        logger.info("Starting validation of login with invalid credentials")
        login_page.load(project_config["base_url"])

        expected_error_message = "Minimum 6 characters required"
        actual_error_message = (
            login_page.login_with_invalid_credentials(
                project_config["invalid_username"],
                project_config["invalid_password"],
            )
            .strip()
            .lower()
            .rstrip(".")
        )

        expected_error_normalized = expected_error_message.strip().lower().rstrip(".")
        report_case(
            expected=expected_error_normalized,
            actual=actual_error_message,
            message="Validate error message for invalid credentials",
        )

        assert actual_error_message == expected_error_normalized, (
            f"Expected error message '{expected_error_normalized}', "
            f"but got '{actual_error_message}'"
        )

    @pytest.mark.smoke
    @pytest.mark.regression
    def test_login_page_username_only_validation_error(
        self,
        login_page,
        project_config,
        report_case,
    ):
        logger.info("Starting validation of login with username only")
        login_page.load(project_config["base_url"])

        expected_error_message = "minimum 6 characters required"
        error_message = login_page.login_with_usernameonly(project_config["username"])
        assert error_message != "", "Error message should not be empty"

        actual_error_normalized = error_message.strip().lower().rstrip(".")
        report_case(
            expected=expected_error_message,
            actual=actual_error_normalized,
            message="Validate error message for username only",
        )

        assert actual_error_normalized == expected_error_message, (
            f"Expected error message '{expected_error_message}', "
            f"but got '{actual_error_normalized}'"
        )

    @pytest.mark.smoke
    @pytest.mark.regression
    def test_login_page_password_only_validation_error(
        self,
        login_page,
        project_config,
        report_case,
    ):
        logger.info("Starting validation of login with password only")
        login_page.load(project_config["base_url"])

        expected_error_message = "This field is required and can't be only spaces."
        error_message = login_page.login_with_passwordonly(
            " ",
            project_config["password"],
        )
        assert error_message != "", "Error message should not be empty"

        actual_error = error_message.strip().lower().rstrip(".")
        expected_error = expected_error_message.strip().lower().rstrip(".")

        report_case(
            expected=expected_error,
            actual=actual_error,
            message="Validate error message for password only",
        )

        assert actual_error == expected_error, (
            f"Expected error message '{expected_error}', " f"but got '{actual_error}'"
        )

    @pytest.mark.ui
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_login_page_title_validation(
        self,
        login_page,
        project_config,
        report_case,
    ):
        logger.info("Starting validation of login page title")
        login_page.load(project_config["base_url"])

        expected_title = project_config["page_title"]
        actual_title = login_page.verify_page_title(expected_title)

        actual_title_normalized = actual_title.strip().lower()
        expected_title_normalized = expected_title.strip().lower()

        report_case(
            expected=expected_title_normalized,
            actual=actual_title_normalized,
            message="Validate login page title",
        )

        assert actual_title_normalized == expected_title_normalized, (
            f"Expected page title '{expected_title}', " f"but got '{actual_title}'"
        )

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_login_page_footer_links_presence(
        self,
        login_page,
        project_config,
        report_case,
    ):
        logger.info("Starting validation of footer links presence")
        login_page.load(project_config["base_url"])

        expected_links = ["Accolade Electronics Pvt. Ltd."]
        actual_links = login_page.verify_footer_links_present()

        expected_links_str = ", ".join(expected_links)
        actual_links_str = ", ".join(actual_links) if actual_links else "No links found"

        report_case(
            expected=expected_links_str,
            actual=actual_links_str,
            message="Validate footer links presence",
        )

        links_found = all(
            any(exp.lower() in link.lower() for link in actual_links)
            for exp in expected_links
        )

        assert (
            links_found
        ), f"Expected footer links {expected_links} not found in {actual_links}"

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_login_page_footer_links_clickability(
        self,
        login_page,
        project_config,
        report_case,
    ):
        logger.info("Starting validation of footer links clickability")
        login_page.load(project_config["base_url"])
        results = login_page.verify_footer_links_clickable()

        all_clickable = all(link["clickable"] for link in results)
        expected_result = "All footer links should be clickable"
        actual_result = ", ".join(
            [f"{link['text']}: {link['clickable']}" for link in results]
        )

        report_case(
            expected=expected_result,
            actual=actual_result,
            message="Validate footer links are clickable",
        )

        assert all_clickable, (
            f"Expected all footer links to be clickable, " f"but got: {actual_result}"
        )

    @pytest.mark.smoke
    @pytest.mark.regression
    def test_login_page_footer_current_year_validation(
        self,
        login_page,
        project_config,
        report_case,
    ):
        logger.info("Starting validation of footer year")
        login_page.load(project_config["base_url"])
        footer_text, current_year = login_page.verify_footer_year()

        expected_year_presence = f"Footer should contain year {current_year}"
        year_found = current_year in footer_text

        report_case(
            expected=expected_year_presence,
            actual=footer_text,
            message="Validate footer contains current year",
        )

        assert year_found, (
            f"Expected year {current_year} to be found in footer text, "
            f"but got: {footer_text}"
        )

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_login_page_build_version_format_validation(
        self,
        login_page,
        project_config,
        report_case,
    ):
        logger.info("Starting validation of build version format")
        login_page.load(project_config["base_url"])
        version = login_page.get_build_version()

        expected_format = "Build version should be in format X.Y.Z"
        not_empty = version is not None and version != ""
        valid_format = bool(re.search(r"\d+\.\d+\.\d+", version))

        report_case(
            expected=expected_format,
            actual=version,
            message="Validate build version format",
        )

        assert not_empty, "Build version should not be empty"
        assert valid_format, (
            f"Expected build version in format X.Y.Z, " f"but got: {version}"
        )
