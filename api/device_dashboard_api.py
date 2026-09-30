from utils.logger import get_logger
from .api_client import APIClient
from .endpoints import (
    GET_DISCARDED_DEVICE_COUNT,
    GET_DISPATCHED_DEVICE_COUNT,
    GET_INSTALLED_DEVICE_COUNT,
    GET_PRODUCTION_DEVICE_COUNT,
)
from config.config import API_USERNAME, API_PASSWORD, API_BASE_URL

logger = get_logger(__name__)


class DeviceDashboardAPI(APIClient):
    """API client for device dashboard operations."""

    @staticmethod
    def get_device_counts(
        page,
        api_base_url=API_BASE_URL,
        api_username=API_USERNAME,
        api_password=API_PASSWORD,
    ):
        """Fetch device counts by status from API.

        Args:
            page: Playwright page object with request context.
            api_base_url: Base URL for API.
            api_username: API username.
            api_password: API password.

        Returns:
            dict: Device status titles mapped to their counts.
        """
        device_count_endpoints = [
            ("TOTAL PRODUCTION DEVICES", GET_PRODUCTION_DEVICE_COUNT),
            ("TOTAL DISPATCHED DEVICES", GET_DISPATCHED_DEVICE_COUNT),
            ("TOTAL INSTALLED DEVICES", GET_INSTALLED_DEVICE_COUNT),
            ("TOTAL DISCARDED DEVICES", GET_DISCARDED_DEVICE_COUNT),
        ]

        result = {}

        for title, endpoint in device_count_endpoints:
            full_endpoint = APIClient.build_endpoint(api_base_url, endpoint)
            try:
                logger.info("Fetching %s from %s", title, full_endpoint)
                data = APIClient.send_request(
                    page, api_base_url, api_username, api_password, "GET", full_endpoint
                )
                count = data.get("data")
                logger.debug("API response for '%s': %s", title, data)
                if count is None:
                    count = data.get("count")
                    logger.debug(
                        "Using alternate count field for '%s': %s", title, count
                    )
                result[title] = int(count)
                logger.info("Device count for '%s': %s", title, result[title])
            except Exception as e:
                logger.warning("Failed to fetch %s: %s", title, str(e))
                result[title] = 0

        logger.info("Fetched all device counts: %s", result)
        return result
