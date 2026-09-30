from utils.logger import get_logger
from .api_client import APIClient
from .endpoints import DELETE_ROLE_GROUP, GET_ROLE_GROUPS
from config.config import API_BASE_URL, API_USERNAME, API_PASSWORD

logger = get_logger(__name__)


class RoleGroupAPI(APIClient):
    """API client for role group operations."""

    @staticmethod
    def get_role_groups(
        page,
        api_base_url=API_BASE_URL,
        api_username=API_USERNAME,
        api_password=API_PASSWORD,
    ):
        """Fetch all role groups from API.

        Args:
            page: Playwright page object with request context.
            api_base_url: Base URL for API.
            api_username: API username.
            api_password: API password.

        Returns:
            dict: API response payload containing role groups data and totalItems count.
        """
        endpoint = APIClient.build_endpoint(
            api_base_url,
            GET_ROLE_GROUPS,
        )

        logger.info("Fetching role groups list from %s", endpoint)
        return APIClient.send_request(
            page,
            api_base_url,
            api_username,
            api_password,
            "GET",
            endpoint,
        )

    @staticmethod
    def delete_role_group(
        page,
        group_id,
        api_base_url=API_BASE_URL,
        api_username=API_USERNAME,
        api_password=API_PASSWORD,
    ):
        """Delete a role group by ID via API.

        Args:
            page: Playwright page object with request context.
            group_id: ID of the role group to delete.
            api_base_url: Base URL for API.
            api_username: API username.
            api_password: API password.

        Returns:
            dict: API response payload.
        """
        endpoint = APIClient.build_endpoint(
            api_base_url,
            DELETE_ROLE_GROUP.format(group_id=group_id),
        )

        logger.info("Sending DELETE request for role group ID %s to %s", group_id, endpoint)
        return APIClient.send_request(
            page,
            api_base_url,
            api_username,
            api_password,
            "DELETE",
            endpoint,
        )

    @staticmethod
    def delete_role_groups(
        page,
        api_base_url=API_BASE_URL,
        api_username=API_USERNAME,
        api_password=API_PASSWORD,
    ):
        """Fetch all role groups count and attempt to delete role group permissions using GET and DELETE methods.

        Args:
            page: Playwright page object with request context.
            api_base_url: Base URL for API.
            api_username: API username.
            api_password: API password.

        Returns:
            dict: Summary of deletion execution.
        """
        logger.info("Testing delete role group functionality via API")

        # Step 1: GET all role groups count
        response = RoleGroupAPI.get_role_groups(
            page, api_base_url, api_username, api_password
        )
        total_roles = response.get("totalItems", 0)

        # Step 2: Iterate and DELETE role group by ID
        for i in range(1, total_roles + 1):
            try:
                del_response = RoleGroupAPI.delete_role_group(
                    page, i, api_base_url, api_username, api_password
                )

                assert (
                    del_response.get("message") == "User Deleted Successfully!!"
                ), f"Failed to delete permission for role group {i}"

                logger.info("Deleted role group %s successfully", i)

            except Exception as e:
                error_message = str(e)

                if (
                    "Cannot delete group: Group is assigned to one or more roles."
                    in error_message
                ):
                    logger.warning(
                        "Cannot delete role group %s: Role is assigned to users",
                        i,
                    )
                    continue

                logger.error(
                    "Unexpected error while deleting role group %s: %s",
                    i,
                    error_message,
                )
                raise

        logger.info("Delete role group API operation completed")
        return {"success": True, "total_groups_processed": total_roles}
