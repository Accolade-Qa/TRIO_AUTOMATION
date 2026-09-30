from utils.logger import get_logger
from config.config import TICKET_BASE_URL, TICKET_USERNAME, TICKET_PASSWORD
from utils.helpers import Helpers
from api.endpoints import (
    GENERATE_TICKET_TOKEN,
    GENERATE_TML_TICKET,
    GET_STATUS_UPDATE_LOGS,
    GET_DASHBOARD_COUNTS,
)


import json

logger = get_logger(__name__)


class TmlRequestAPI:

    @staticmethod
    def get_token(
        page=None,
        api_base_url=TICKET_BASE_URL,
    ):
        """
        Generate authentication token for the CRM APIs.
        """
        payload = {
            "username": TICKET_USERNAME,
            "password": TICKET_PASSWORD,
        }

        endpoint = GENERATE_TICKET_TOKEN

        logger.info("Fetching authentication token from %s", endpoint)

        try:
            import urllib.request
            import urllib.parse
            import ssl

            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE

            data = urllib.parse.urlencode(payload).encode("utf-8")
            req = urllib.request.Request(
                api_base_url + endpoint, data=data, method="POST"
            )

            with urllib.request.urlopen(req, context=ctx) as response:
                token_data = json.loads(response.read().decode("utf-8"))

            token = token_data.get("token")

            print("token :> ", token)

            if not token:
                raise Exception("Authentication token not found in response.")

            logger.info("Successfully fetched authentication token.")

            return token

        except Exception as e:
            logger.error("Failed to fetch authentication token: %s", str(e))
            raise

    @staticmethod
    def post_tml_request_log(
        page=None,
        api_base_url=TICKET_BASE_URL,
    ):
        state_name, state_code = Helpers.generate_random_indian_state_data()
        payload = [
            {
                "VIN_NO": f"ACCDEV07241580{Helpers.generate_random_number(3)}",
                "ICCID": "89916420534724851291",
                "UIN_NO": "ACON4NA082300092233",
                "DEVICE_IMEI": "861564061380138",
                "DEVICE_MAKE": "Accolade",
                "DEVICE_MODEL": "AEPL051401",
                "ENGINE_NO": "ENGINE_FIXED_00001",
                "REG_NUMBER": "AN01AB1000",
                "REGISTERED_MOBILE_NUMBER": Helpers.generate_random_phone(),
                "VEHICLE_OWNER_FIRST_NAME": Helpers.generate_random_string(5),
                "VEHICLE_OWNER_MIDDLE_NAME": "",
                "VEHICLE_OWNER_LAST_NAME": Helpers.generate_random_string(5),
                "ADDRESS_LINE_1": "SHIVANE",
                "ADDRESS_LINE_2": "SHIVANE",
                "VEHICLE_OWNER_CITY": "PUNE",
                "VEHICLE_OWNER_DISTRICT": "PUNE",
                "VEHICLE_OWNER_STATE": state_name,
                "VEHICLE_OWNER_COUNTRY": "India",
                "VEHICLE_OWNER_PINCODE": "411045",
                "VEHICLE_OWNER_REGISTERED_MOBILE": Helpers.generate_random_phone(),
                "POS_CODE": "AB123",
                "POA_DOC_NAME": "PANAB123",
                "POA_DOC_NO": "PAN1AB123",
                "POI_DOC_TYPE": "ADHARAB123",
                "POI_DOC_NO": "ADHARXYZ123",
                "RTO_OFFICE_CODE": f"{state_code}12",
                "RTO_STATE": state_code,
                "PRIMARY_OPERATOR": "BSNL",
                "SECONDARY_OPERATOR": "BHA",
                "PRIMARY_MOBILE_NUMBER": Helpers.generate_random_phone(),
                "SECONDARY_MOBILE_NUMBER": Helpers.generate_random_phone(),
                "VEHICLE_MODEL": "NANO",
                "DEALER_CODE": "1000",
                "COMMERCIAL_ACTIVATION_START_DATE": Helpers.get_timestamp(
                    fmt="%Y-%m-%d"
                ),
                "COMMERCIAL_ACTIVATION_EXPIRY_DATE": Helpers.get_future_date(
                    2, fmt="%Y-%m-%d"
                ),
                "MFG_YEAR": "2024",
                "ACCOLADE_POSTING_DATE_TIME": Helpers.get_timestamp(fmt="%Y-%m-%d"),
                "INVOICE_DATE": Helpers.get_timestamp(fmt="%Y-%m-%d"),
                "INVOICE_NUMBER": "AEPL100000000",
                "CERTIFICATE_VALIDITY_DURATION_IN_YEAR": "2",
            }
        ]

        endpoint = GENERATE_TML_TICKET

        logger.info("Creating TML request ticket.")

        try:
            token = TmlRequestAPI.get_token(api_base_url=api_base_url)

            import urllib.request
            import ssl

            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE

            body = json.dumps(payload).encode("utf-8")
            headers = {
                "token": token,
                "Content-Type": "application/json",
            }
            req = urllib.request.Request(
                api_base_url + endpoint, data=body, headers=headers, method="POST"
            )

            with urllib.request.urlopen(req, context=ctx) as response:
                tml_request_log_data = json.loads(response.read().decode("utf-8"))

            print("response :> OK")

            data_list = tml_request_log_data.get("data", [])
            if isinstance(data_list, list) and len(data_list) > 0:
                data = data_list[0]
            elif isinstance(data_list, dict):
                data = data_list
            else:
                data = {}

            ticket_number = (
                data.get("TICKET_NO")
                or data.get("ticketNo")
                or data.get("ticket_no")
                or data.get("TICKET_NUMBER")
                or tml_request_log_data.get("TICKET_NO")
                or tml_request_log_data.get("ticketNo")
                or tml_request_log_data.get("TICKET_NUMBER")
                or ""
            )
            VIN = data.get("VIN_NO") or data.get("vinNo") or (payload[0].get("VIN_NO") if payload else "")
            UIN = data.get("UIN_NO") or data.get("uinNo") or (payload[0].get("UIN_NO") if payload else "")
            ICCID = data.get("ICCID") or data.get("iccid") or (payload[0].get("ICCID") if payload else "")


            logger.info(
                "Successfully created TML request. Ticket Number: %s",
                ticket_number,
            )

            return (
                payload,
                VIN,
                UIN,
                ICCID,
                ticket_number,
                data
            )

        except Exception as e:
            logger.error("Failed to create TML request: %s", str(e))
            raise

    @staticmethod
    def get_status_update_logs(
        page=None,
        vin_no=None,
        api_base_url=TICKET_BASE_URL,
    ):
        """
        Fetch ticket status update logs from CRM API for validation against UI table.
        """
        endpoint = GET_STATUS_UPDATE_LOGS
        if vin_no:
            endpoint += f"?vinNo={vin_no}"

        logger.info("Fetching status update logs from %s", endpoint)

        try:
            token = TmlRequestAPI.get_token(api_base_url=api_base_url)

            import urllib.request
            import ssl

            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE

            headers = {
                "token": token,
                "Content-Type": "application/json",
            }
            req = urllib.request.Request(
                api_base_url + endpoint, headers=headers, method="GET"
            )

            with urllib.request.urlopen(req, context=ctx) as response:
                log_data = json.loads(response.read().decode("utf-8"))

            logger.info("Successfully fetched status update logs API data.")
            return log_data

        except Exception as e:
            logger.error("Failed to fetch status update logs API: %s", str(e))
            return {}

    @staticmethod
    def get_dash_counts(
        page=None,
        api_base_url=TICKET_BASE_URL,
        params=None,
    ):
        """
        Fetch ticket dashboard KPI counts from CRM API endpoint:
        /api/crm/getDashCounts?state=&dealer=&toDate=&fromDate=&assignTo=&initiatedBy=&ticketStatusFilter=&deviceType=&search=&id=&ticketCompletedAtFromDate=&ticketCompletedAtToDate=&tatType=
        """
        endpoint = GET_DASHBOARD_COUNTS
        if not params:
            params = "state=&dealer=&toDate=&fromDate=&assignTo=&initiatedBy=&ticketStatusFilter=&deviceType=&search=&id=&ticketCompletedAtFromDate=&ticketCompletedAtToDate=&tatType="

        full_url = f"{api_base_url}{endpoint}?{params}"
        logger.info("Fetching dashboard counts from %s", full_url)

        try:
            token = TmlRequestAPI.get_token(api_base_url=api_base_url)

            import urllib.request
            import ssl

            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE

            headers = {
                "token": token,
                "Content-Type": "application/json",
            }
            req = urllib.request.Request(full_url, headers=headers, method="GET")

            with urllib.request.urlopen(req, context=ctx) as response:
                counts_data = json.loads(response.read().decode("utf-8"))

            logger.info("Successfully fetched dashboard counts API data: %s", counts_data)
            return counts_data

        except Exception as e:
            logger.error("Failed to fetch dashboard counts API: %s", str(e))
            return {}


TmlRequestApi = TmlRequestAPI



