from api.api_client import APIClient
from api.login_api import LoginAPI
from api.endpoints import (
    GET_ALL_FIRMWARES,
    GET_ALL_STATE_SERVERS,
    GET_FIRMWARES_NOT_ADDED_IN_STATE,
    GET_STATE_FIRMWARES,
    GET_STATE_SERVER_DETAILS,
)
from utils.logger import get_logger
from config.config import (
    API_BASE_URL,
    API_USERNAME,
    API_PASSWORD,
)

logger = get_logger(__name__)


class GovtServerAPI(APIClient):
    """API client for government server operations."""

    @staticmethod
    def _get_user_id(
        page,
        api_base_url=API_BASE_URL,
        api_username=API_USERNAME,
        api_password=API_PASSWORD,
    ):
        """
        Fetch logged-in user ID.
        """

        # Some projects expose user API under /api prefix (sampark).
        # if "sampark-qa" in api_base_url or api_base_url.rstrip("/").endswith(
        #     "sampark-qa.accoladeelectronics.com"
        # ):
        #     login_endpoint = f"/api/users/getUserdetails?id={id}"
        # else:
        #     login_endpoint = f"/users/getUserdetails?id={id}"
        """ add this above logic here in the future if needed, for now we are using the login API to get the user id"""

        login = LoginAPI.login(
            page, api_username, api_password, api_base_url, api_username, api_password
        )

        return login.get("id")

    @staticmethod
    def _send_get_request(
        page, api_base_url, api_username, api_password, endpoint, success_message
    ):
        """
        Common GET request handler.
        """

        logger.info("Request endpoint: %s", endpoint)

        try:
            response_data = APIClient.send_request(
                page,
                api_base_url,
                api_username,
                api_password,
                "GET",
                endpoint,
            )

            logger.info(success_message)

            return response_data.get("data", [])

        except Exception as e:

            error_message = str(e)

            # Handle API returning 500 with "Data not found !!"
            if "Data not found !!" in error_message:
                logger.warning(
                    "No data found for endpoint: %s",
                    endpoint,
                )
                return []

            logger.error("%s : %s", success_message, error_message)
            raise

    @staticmethod
    def _get_all_servers_list(
        page,
        api_base_url=API_BASE_URL,
        api_username=API_USERNAME,
        api_password=API_PASSWORD,
    ):
        """
        Fetch all servers from government server list.

        Returns:
            tuple: (servers_list, first_server_id, user_id)
        """

        user_id = GovtServerAPI._get_user_id(
            page, api_base_url, api_username, api_password
        )

        endpoint = APIClient.build_endpoint(
            api_base_url,
            GET_ALL_STATE_SERVERS.format(user_id=user_id),
        )

        servers = GovtServerAPI._send_get_request(
            page,
            api_base_url,
            api_username,
            api_password,
            endpoint,
            "Successfully fetched all servers",
        )

        if not servers:
            raise ValueError("No servers found in API response")

        server_id = servers[0].get("id")

        logger.info(
            "Retrieved %d servers from API",
            len(servers),
        )

        logger.debug("Servers: %s", servers)

        return servers, server_id, user_id

    @staticmethod
    def _get_server_id_by_state_name(
        page, api_base_url, api_username, api_password, state_name
    ):
        """
        Fetch server ID for a given state name.
        """

        servers, _, _ = GovtServerAPI._get_all_servers_list(
            page, api_base_url, api_username, api_password
        )

        matching_server = next(
            (server for server in servers if server.get("state") == state_name),
            None,
        )

        assert matching_server, f"No server found with state name: {state_name}"

        return matching_server.get("id")

    @staticmethod
    def get_all_firmware(
        page,
        api_base_url=API_BASE_URL,
        api_username=API_USERNAME,
        api_password=API_PASSWORD,
    ):
        """
        Fetch all firmware versions.
        """
        endpoint = APIClient.build_endpoint(
            api_base_url,
            GET_ALL_FIRMWARES,
        )

        firmware_versions = GovtServerAPI._send_get_request(
            page,
            api_base_url,
            api_username,
            api_password,
            endpoint,
            "Successfully fetched all firmware versions",
        )

        logger.info(
            "Retrieved %d firmware versions from API",
            len(firmware_versions),
        )

        logger.debug(
            "Firmware versions: %s",
            firmware_versions,
        )

        return firmware_versions

    @staticmethod
    def _get_firmwares_by_type(
        page,
        api_base_url=API_BASE_URL,
        api_username=API_USERNAME,
        api_password=API_PASSWORD,
        firmware_type=None,
        added_in_state=False,
        state_server_id=None,
    ):
        """
        Fetch firmware list by firmware type.

        Args:
            firmware_type: OC or D
            added_in_state: True if fetching firmwares added in state, False otherwise
            state_server_id: Optional state server ID to use for the request

        Returns:
            list: Firmware list
        """

        if state_server_id is None:
            _, state_server_id, user_id = GovtServerAPI._get_all_servers_list(
                page, api_base_url, api_username, api_password
            )
        else:
            user_id = GovtServerAPI._get_user_id(
                page, api_base_url, api_username, api_password
            )

        if added_in_state:
            endpoint = APIClient.build_endpoint(
                api_base_url,
                GET_STATE_FIRMWARES.format(
                    firmware_type=firmware_type,
                    user_id=user_id,
                    state_server_id=state_server_id,
                ),
            )
        else:
            endpoint = APIClient.build_endpoint(
                api_base_url,
                GET_FIRMWARES_NOT_ADDED_IN_STATE.format(
                    firmware_type=firmware_type,
                    state_server_id=state_server_id,
                ),
            )

        firmware_versions = GovtServerAPI._send_get_request(
            page,
            api_base_url,
            api_username,
            api_password,
            endpoint,
            f"Successfully fetched {firmware_type} firmware versions",
        )

        logger.debug(
            "%s firmware versions: %s",
            firmware_type,
            firmware_versions,
        )

        return firmware_versions

    @staticmethod
    def get_oc_firmwares_not_added(
        page,
        api_base_url=API_BASE_URL,
        api_username=API_USERNAME,
        api_password=API_PASSWORD,
    ):
        """
        Fetch OC firmware list.
        """

        return GovtServerAPI._get_firmwares_by_type(
            page, api_base_url, api_username, api_password, "OC", False
        )

    @staticmethod
    def get_oc_firmwares_added_in_state(
        page,
        api_base_url=API_BASE_URL,
        api_username=API_USERNAME,
        api_password=API_PASSWORD,
        state_name=None,
        state_server_id=None,
    ):
        """
        Fetch OC firmware list added in state.

        Args:
            page: Playwright page object
            api_base_url: Base URL for API.
            api_username: API username.
            api_password: API password.
            state_name: Optional state name to scope the request
            state_server_id: Optional server ID to scope the request
        """

        if state_name:
            state_server_id = GovtServerAPI._get_server_id_by_state_name(
                page,
                api_base_url,
                api_username,
                api_password,
                state_name,
            )

        return GovtServerAPI._get_firmwares_by_type(
            page,
            api_base_url,
            api_username,
            api_password,
            "OC",
            True,
            state_server_id,
        )

    @staticmethod
    def get_d_firmwares_not_added(
        page,
        api_base_url=API_BASE_URL,
        api_username=API_USERNAME,
        api_password=API_PASSWORD,
    ):
        """
        Fetch D firmware list.
        """

        return GovtServerAPI._get_firmwares_by_type(
            page, api_base_url, api_username, api_password, "D", False
        )

    @staticmethod
    def get_d_firmwares_added_in_state(
        page,
        api_base_url=API_BASE_URL,
        api_username=API_USERNAME,
        api_password=API_PASSWORD,
    ):
        """
        Fetch D firmware list.
        """

        return GovtServerAPI._get_firmwares_by_type(
            page, api_base_url, api_username, api_password, "D", True
        )

    @staticmethod
    def _get_state_server_details_response(
        page,
        api_base_url,
        api_username,
        api_password,
        server_id,
        success_message,
    ):
        """Fetch a single state server detail payload and return the response."""
        endpoint = APIClient.build_endpoint(
            api_base_url,
            GET_STATE_SERVER_DETAILS.format(server_id=server_id),
        )

        return GovtServerAPI._send_get_request(
            page,
            api_base_url,
            api_username,
            api_password,
            endpoint,
            success_message,
        )

    @staticmethod
    def get_state_server_details_by_id(
        page,
        api_base_url=API_BASE_URL,
        api_username=API_USERNAME,
        api_password=API_PASSWORD,
    ):
        """
        Fetch state server details by ID.
        """

        _, server_id, _ = GovtServerAPI._get_all_servers_list(
            page, api_base_url, api_username, api_password
        )

        response = GovtServerAPI._get_state_server_details_response(
            page,
            api_base_url,
            api_username,
            api_password,
            server_id,
            "Successfully fetched state server details",
        )

        oc_firmwares = GovtServerAPI.get_oc_firmwares_not_added(
            page, api_base_url, api_username, api_password
        )

        d_firmwares = GovtServerAPI.get_d_firmwares_not_added(
            page, api_base_url, api_username, api_password
        )

        logger.debug(
            "State server response: %s",
            response,
        )

        return response, oc_firmwares, d_firmwares

    @staticmethod
    def get_state_server_details_by_name(
        page,
        state_name,
        api_base_url=API_BASE_URL,
        api_username=API_USERNAME,
        api_password=API_PASSWORD,
    ):
        """
        Fetch state server details by state name.
        """

        servers, _, _ = GovtServerAPI._get_all_servers_list(
            page, api_base_url, api_username, api_password
        )

        matched_server = next(
            (server for server in servers if server.get("state") == state_name),
            None,
        )

        assert matched_server, f"No server found with state name: {state_name}"

        server_id = matched_server.get("id")

        response = GovtServerAPI._get_state_server_details_response(
            page,
            api_base_url,
            api_username,
            api_password,
            server_id,
            f"Successfully fetched state server details for {state_name}",
        )

        oc_firmwares = GovtServerAPI.get_oc_firmwares_not_added(
            page, api_base_url, api_username, api_password
        )

        d_firmwares = GovtServerAPI.get_d_firmwares_not_added(
            page, api_base_url, api_username, api_password
        )

        logger.debug(
            "State server response for %s: %s",
            state_name,
            response,
        )

        return response, oc_firmwares, d_firmwares
