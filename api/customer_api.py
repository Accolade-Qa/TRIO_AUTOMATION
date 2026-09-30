from utils.logger import get_logger
from .api_client import APIClient
from .endpoints import GET_CUSTOMERS, SAVE_CUSTOMER
from config.config import API_BASE_URL, API_USERNAME, API_PASSWORD
from utils.helpers import Helpers
import json

logger = get_logger(__name__)


class CustomerAPI(APIClient):
    """API client for customer data operations."""

    @staticmethod
    def get_customer_list(
        page,
        api_base_url=API_BASE_URL,
        api_username=API_USERNAME,
        api_password=API_PASSWORD,
    ):
        """Fetch all customer names from API.

        Args:
            page: Playwright page object with request context.
            api_base_url: Base URL for API.
            api_username: API username.
            api_password: API password.

        Returns:
            list: Customer names fetched from API.
        """

        # Some projects expose user API under /api prefix (sampark).
        # if "sampark-qa" in api_base_url or api_base_url.rstrip("/").endswith(
        #     "sampark-qa.accoladeelectronics.com"
        # ):
        #     login_endpoint = f"/api/users/getUserdetails?id={id}"
        # else:
        #     login_endpoint = f"/users/getUserdetails?id={id}"

        customer_endpoint = APIClient.build_endpoint(
            api_base_url,
            GET_CUSTOMERS,
        )

        logger.info("Fetching customer list from %s", customer_endpoint)

        try:
            response_data = APIClient.send_request(
                page, api_base_url, api_username, api_password, "GET", customer_endpoint
            )

            customers = response_data.get("data", [])

            customer_names = [
                customer.get("customerName", "").strip()
                for customer in customers
                if customer.get("customerName")
            ]

            logger.info("Retrieved %d customer names from API", len(customer_names))
            logger.debug("Customer names: %s", customer_names)

            return customer_names
        except Exception as e:
            logger.error("Failed to fetch customer list: %s", str(e))
            raise

    @staticmethod
    def save_customer(
        page,
        api_base_url=API_BASE_URL,
        api_username=API_USERNAME,
        api_password=API_PASSWORD,
    ):
        """Save a new customer via API."""
        customer_name = "API cust " + Helpers.generate_random_string(5)
        payload = {
            "id": 0,
            "customerName": customer_name,
        }
        customer_endpoint = APIClient.build_endpoint(
            api_base_url,
            SAVE_CUSTOMER,
        )

        logger.info("Saving customer using %s", customer_endpoint)

        try:
            response_data = APIClient.send_request(
                page,
                api_base_url,
                api_username,
                api_password,
                "POST",
                customer_endpoint,
                data=json.dumps(payload),
            )
            logger.info("Successfully saved new customer: %s", customer_name)
            return response_data, customer_name

        except Exception as e:
            logger.error("Failed to save customer: %s", str(e))
            raise
