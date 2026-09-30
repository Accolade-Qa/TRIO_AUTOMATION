import json

from utils.logger import get_logger
from .api_client import APIClient
from .endpoints import LOGIN

logger = get_logger(__name__)


class LoginAPI(APIClient):
    """API client for user authentication operations."""

    @staticmethod
    def login(page, username, password, api_base_url, api_username, api_password):
        """Authenticate user and obtain login data.

        Args:
            page: Playwright page object with request context.
            username: User's username for authentication (for logging).
            password: User's password for authentication (for logging).
            api_base_url: Base URL for API.
            api_username: API username for authentication.
            api_password: API password for authentication.

        Returns:
            dict: Login data from API response.
        """
        login_endpoint = APIClient.build_endpoint(api_base_url, LOGIN)

        logger.info("Attempting to log in user %s", username)

        login_payload = {
            "userEmail": api_username,
            "password": api_password,
        }

        try:
            # Perform login without using APIClient.send_request to avoid
            # invoking token lookup which would itself attempt a login
            # against the wrong endpoint (circular call). Use direct
            # request so the sampark `/api/users/login` path is honored.
            login_url = f"{api_base_url}{login_endpoint}"
            response = page.request.post(
                login_url,
                data=json.dumps(login_payload),
                headers={"Content-Type": "application/json"},
            )

            if not response.ok:
                raise Exception(
                    f"API login failed: {response.status} {response.text()}"
                )

            logger.info("Login successful for user %s", username)
            login_data = response.json().get("data")
            logger.debug("Received login data: %s", login_data)
            return login_data
        except Exception as e:
            logger.error("Login failed for user %s: %s", username, str(e))
            raise
