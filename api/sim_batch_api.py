import json

from utils.logger import get_logger
from .api_client import APIClient
from .endpoints import GET_SIM_BATCH_DETAILS_BY_CSV, GET_SIM_BATCH_DETAILS_BY_ICCID
from LCT_AUTOMATION.test_data.device_data import DeviceData

logger = get_logger(__name__)


class SIMBatchAPI(APIClient):
    """API client for SIM batch data operations."""

    @staticmethod
    def get_sim_batch_details_by_csv(page, api_base_url, api_username, api_password):
        """Fetch SIM batch details from API by ICCID list.

        Args:
            page: Playwright page object with request context.
            api_base_url: Base URL for API.
            api_username: API username.
            api_password: API password.

        Returns:
            dict: SIM batch details from API response.
        """
        sim_details_endpoint = GET_SIM_BATCH_DETAILS_BY_CSV

        with open("./test_data/Sensorise_SIM_data_Details.xlsx", "rb") as f:
            file_content = f.read()
            multipart = {
                "file": {
                    "name": "Sensorise_SIM_data_Details.xlsx",
                    "mimeType": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    "buffer": file_content,
                }
            }

            logger.info("Fetching SIM batch details from %s", sim_details_endpoint)

            try:
                sim_details_data = APIClient.send_request(
                    page,
                    api_base_url,
                    api_username,
                    api_password,
                    "POST",
                    sim_details_endpoint,
                    files=multipart,
                )
                logger.info("Successfully fetched SIM batch details")
                duplicate_rows = sim_details_data.get("duplicateRows", [])
                sim_details = sim_details_data.get("simDetails", {})
                errors = sim_details_data.get("errors", [])

                return duplicate_rows, sim_details, errors
            except Exception as e:
                logger.error("Failed to fetch SIM batch details: %s", str(e))
                raise

    @staticmethod
    def get_sim_batch_by_manual_upload(page, api_base_url, api_username, api_password):
        """Fetch sim data details from a manual upload iccid

        Args:
            page: Playwright page object with request context.
            api_base_url: Base URL for API.
            api_username: API username.
            api_password: API password.

        Return:
            dict: Sim batch details from api response
        """
        devices = DeviceData().get_device_data()

        iccid = devices.get("device_3")[1]
        endpoint = GET_SIM_BATCH_DETAILS_BY_ICCID
        payload = [iccid]
        logger.info("Fetching sim data details from %s", endpoint)

        try:
            sim_data = APIClient.send_request(
                page,
                api_base_url,
                api_username,
                api_password,
                "POST",
                endpoint=endpoint,
                data=json.dumps(payload),
            )

            data = sim_data.get("data", {})

            return data

        except Exception as e:
            logger.error(
                "Failed to fetch sim data details via manual upload: %s", str(e)
            )
            raise
