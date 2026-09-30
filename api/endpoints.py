"""Centralized endpoint templates for API routes used by the automation suite."""

# Authentication and user lookup endpoints
LOGIN = "/users/login"
GET_USER_DETAILS = "/users/getUserdetails?id={id}"

# Customer endpoints
GET_CUSTOMERS = "/customerMaster/getCustomers?page=1&size=100000&search="
SAVE_CUSTOMER = "/customerMaster/saveCustomer"

# Device dashboard endpoints
GET_PRODUCTION_DEVICE_COUNT = (
    "/device/getProductionDeviceCount?selectedDeviceModelId=&selectedCustomerId="
)
GET_DISPATCHED_DEVICE_COUNT = (
    "/device/getDispatchDeviceCount?selectedDeviceModelId=&selectedCustomerId="
)
GET_INSTALLED_DEVICE_COUNT = (
    "/device/getInstalledDeviceCount?selectedDeviceModelId=&selectedCustomerId="
)
GET_DISCARDED_DEVICE_COUNT = (
    "/device/getDiscardedDeviceCount?selectedDeviceModelId=&selectedCustomerId="
)

# Role group endpoints
GET_ROLE_GROUPS = "/roleGroup/getRolesGroup?page=0&size=1000&search="
DELETE_ROLE_GROUP = "/roleGroup/deleteRoleGroup?id={group_id}"

# Role management endpoints
GET_ROLES = "/roles/getRoles?page=0&size=1000&search=&userRole="
DELETE_ROLE = "/roles/deleteRole?roleId={role_id}"

# Government server endpoints
GET_ALL_STATE_SERVERS = (
    "/stateServers/getAllStateServerList?page=0&size=1000&search=&userId={user_id}"
)
GET_ALL_FIRMWARES = (
    "/firmwareMaster/getAllFirmwareList?page=0&size=1000&search=&firmwareType="
)
GET_STATE_FIRMWARES = (
    "/firmwareMaster/getStateFirmwares?page=0&size=1000&search="
    "&firmwareType={firmware_type}&userId={user_id}&stateServerId={state_server_id}"
)
GET_FIRMWARES_NOT_ADDED_IN_STATE = (
    "/firmwareMaster/getFirmwaresListNotAddedInState?page=0&size=1000&search="
    "&firmwareType={firmware_type}&stateServerId={state_server_id}"
)
GET_STATE_SERVER_DETAILS = "/stateServers/getStateServerDetails?id={server_id}"

# SIM batch endpoints
GET_SIM_BATCH_DETAILS_BY_CSV = "/sensoriseSimData/getSimDetailsByIccidUsingCsv"
GET_SIM_BATCH_DETAILS_BY_ICCID = "/sensoriseSimData/getSimDetailsByIccid"

# TML request endpoints
GENERATE_TICKET_TOKEN = "/api/crm/generateToken"
GENERATE_TML_TICKET = "/api/crm/generateTickets"
GET_STATUS_UPDATE_LOGS = "/api/crm/getStatusUpdateLogs"
GET_DASHBOARD_COUNTS = "/api/crm/getDashCounts"

# ATCU OTA batch endpoints
GET_ATCU_OTA_BATCH_LIST = (
    "/api/ota/fetchOtaBatchList?pageNo={page_no}&size={size}&search={search}"
)
GET_ATCU_OTA_BATCH_KPI = (
    "/api/ota/fetchOtaBatchKpi?pageNo={page_no}&size={size}&search={search}"
    "&batchRefId={batch_ref_id}&kpiSelected={kpi_selected}"
)

