"""API Client for authentication and common request handling."""

import json
from utils.logger import get_logger

logger = get_logger(__name__)


class APIClient:
    """Client for authenticated API requests with centralized token management."""

    @staticmethod
    def is_sampark_api(api_base_url):
        """Return True when the configured API host is the sampark QA deployment."""
        if not api_base_url:
            return False

        normalized_base_url = api_base_url.rstrip("/")
        return "sampark-qa" in normalized_base_url or normalized_base_url.endswith(
            "sampark-qa.accoladeelectronics.com"
        )

    @staticmethod
    def is_atcu_api(api_base_url):
        """Return True when the configured API host is the ATCU deployment."""
        if not api_base_url:
            return False

        normalized_base_url = api_base_url.rstrip("/").lower()
        return "aepl-tcu4g-qa" in normalized_base_url or "6101" in normalized_base_url


    @staticmethod
    def build_endpoint(api_base_url, endpoint):
        """Normalize an API endpoint for the active project.

        Sampark APIs expose a common ``/api`` prefix while the remaining
        projects use the unprefixed route name directly. This helper keeps the
        prefixing decision in one place and allows the individual API modules to
        stay focused on their business logic.
        """
        if not endpoint:
            return endpoint

        normalized_endpoint = endpoint if endpoint.startswith("/") else f"/{endpoint}"

        requires_api_prefix = APIClient.is_sampark_api(api_base_url)
        if requires_api_prefix and not normalized_endpoint.startswith("/api/"):
            return f"/api{normalized_endpoint}"

        return normalized_endpoint


    @staticmethod
    def resolve_api_credentials(page, api_base_url=None, api_username=None, api_password=None):
        """Resolve API settings from the active project's config and env file."""
        from config import config

        resolved_url = (api_base_url or config.API_BASE_URL).rstrip("/")
        resolved_username = api_username or config.API_USERNAME
        resolved_password = api_password or config.API_PASSWORD

        return resolved_url, resolved_username, resolved_password



    @staticmethod
    def get_bearer_token(page, api_base_url=None, api_username=None, api_password=None):
        """Authenticate with API and retrieve bearer token.

        Args:
            page: Playwright page object with request context.
            api_base_url: Base URL for API.
            api_username: API username.
            api_password: API password.

        Returns:
            str: Bearer token for subsequent API requests.
        """
        api_base_url, api_username, api_password = APIClient.resolve_api_credentials(
            page, api_base_url, api_username, api_password
        )


        from config import config

        login_endpoint = getattr(config, "API_LOGIN_ENDPOINT", "/users/login")
        login_url = f"{api_base_url}{APIClient.build_endpoint(api_base_url, login_endpoint)}"

        login_payload = {
            "userEmail": api_username,
            "password": api_password,
        }

        logger.info("Logging in to API user %s at %s", api_username, login_url)
        try:
            login_response = page.request.post(
                login_url,
                data=json.dumps(login_payload),
                headers={"Content-Type": "application/json"},
            )

            if not login_response.ok:
                response_text = login_response.text()
                logger.error(
                    "API login failed with status %s: %s",
                    login_response.status,
                    response_text,
                )
                raise Exception(
                    f"API login failed: {login_response.status} {response_text}"
                )

            login_data = login_response.json()
            token = login_data.get("data", {}).get("token") or login_data.get("token")
            if token:
                logger.info("API login succeeded, acquired bearer token")
                return token

            raise Exception(f"API login response did not contain a bearer token: {login_data}")
        except Exception as e:
            logger.error("API login request failed: %s", str(e))
            raise Exception(
                f"Failed to retrieve API bearer token from {login_url}: {e}"
            ) from e


    @staticmethod
    def get_request_headers(
        page,
        api_base_url,
        api_username,
        api_password,
        extra_headers=None,
        include_json_content_type=True,
        token=None,
    ):
        if token is None:
            token = APIClient.get_bearer_token(
                page,
                api_base_url,
                api_username,
                api_password,
            )

        headers = {
            "Authorization": f"Bearer {token}",
            "token": token
        }

        if include_json_content_type:
            headers["Content-Type"] = "application/json"


        if extra_headers:
            headers.update(extra_headers)

        return headers

    @staticmethod
    def send_request(
        page, api_base_url, api_username, api_password, method, endpoint, **kwargs
    ):
        """Send an authenticated API request."""

        api_base_url, api_username, api_password = APIClient.resolve_api_credentials(
            page, api_base_url, api_username, api_password
        )
        endpoint = APIClient.build_endpoint(api_base_url, endpoint)

        headers = kwargs.pop("headers", None)

        files = kwargs.pop("files", None)
        if files is not None:
            kwargs["multipart"] = files

        include_json_content_type = files is None

        # Use supplied token if available
        token = kwargs.pop("token", None)

        headers = APIClient.get_request_headers(
            page,
            api_base_url,
            api_username,
            api_password,
            extra_headers=headers,
            include_json_content_type=include_json_content_type,
            token=token,
        )

        url = f"{api_base_url}{endpoint}"

        logger.info("Sending %s request to %s", method, endpoint)

        method_upper = method.upper()

        if method_upper == "GET":
            response = page.request.get(url, headers=headers, **kwargs)
        elif method_upper == "POST":
            response = page.request.post(url, headers=headers, **kwargs)
        elif method_upper == "PUT":
            response = page.request.put(url, headers=headers, **kwargs)
        elif method_upper == "PATCH":
            response = page.request.patch(url, headers=headers, **kwargs)
        elif method_upper == "DELETE":
            response = page.request.delete(url, headers=headers, **kwargs)
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")

        if response.ok:
            logger.info("API request succeeded with status %s", response.status)

            if response.status == 204:
                return {}

            try:
                return response.json()
            except json.JSONDecodeError as decode_err:
                response_text = response.text()

                if not response_text or response_text.isspace():
                    return {}

                logger.error(
                    "Failed to parse JSON response from %s: %s",
                    endpoint,
                    response_text,
                )

                raise Exception(
                    f"API request to {endpoint} returned invalid JSON: "
                    f"{decode_err}. Response body: {response_text}"
                ) from decode_err

        response_text = response.text()

        logger.warning(
            "API request to %s failed with status %s: %s",
            endpoint,
            response.status,
            response_text,
        )

        raise Exception(
            f"API request to {endpoint} failed: {response.status} {response_text}"
        )
