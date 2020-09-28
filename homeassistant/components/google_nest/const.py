"""Constants for the Google Nest Device Access integration."""

DOMAIN = "google_nest"

OAUTH2_AUTHORIZE = (
    "https://nestservices.google.com/partnerconnections/{project_id}/auth"
)
OAUTH2_TOKEN = "https://www.googleapis.com/oauth2/v4/token"

SDM_SCOPES = ["https://www.googleapis.com/auth/sdm.service"]

API_URL = "https://smartdevicemanagement.googleapis.com/v1/enterprises/{project_id}"

DEVICES = "devices"
