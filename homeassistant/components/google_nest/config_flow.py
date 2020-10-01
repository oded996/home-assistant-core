"""Config flow for Google Nest Device Access."""
import logging
from typing import Dict

from homeassistant import config_entries
from homeassistant.helpers import config_entry_oauth2_flow

from .const import DOMAIN, SDM_SCOPES

_LOGGER = logging.getLogger(__name__)


class OAuth2FlowHandler(
    config_entry_oauth2_flow.AbstractOAuth2FlowHandler, domain=DOMAIN
):
    """Config flow to handle Google Nest Device Access OAuth2 authentication."""

    DOMAIN = DOMAIN
    VERSION = 1
    # TODO: Investigate options for using cloud pubsub to get events pushed
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    @property
    def logger(self) -> logging.Logger:
        """Return logger."""
        return logging.getLogger(__name__)

    @property
    def extra_authorize_data(self) -> Dict[str, str]:
        """Extra data that needs to be appended to the authorize url."""
        return {
            "scope": ",".join(SDM_SCOPES),
            # Add params to ensure we get back a refresh token
            "access_type": "offline",
            "prompt": "consent",
        }
