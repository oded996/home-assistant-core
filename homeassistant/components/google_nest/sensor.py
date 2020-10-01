"""Support for Google Nest SDM sensors."""

from datetime import timedelta
import logging
from typing import Optional

import async_timeout
from google_nest_sdm.device import Device, HumidityMixin, InfoMixin, TemperatureMixin
from google_nest_sdm.google_nest_api import GoogleNestAPI

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import PERCENTAGE, TEMP_CELSIUS
from homeassistant.helpers.typing import HomeAssistantType
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
    UpdateFailed,
)

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistantType, entry: ConfigEntry, async_add_entities
) -> None:
    """Set up the sensors."""

    auth = hass.data[DOMAIN][entry.entry_id]
    nest_api = GoogleNestAPI(auth)

    async def async_update_data():
        """Fetch data from API endpoint.

        This is the place to pre-process the data to lookup tables
        so entities can quickly look up their data.
        """
        try:
            # Note: asyncio.TimeoutError and aiohttp.ClientError are already
            # handled by the data update coordinator.
            async with async_timeout.timeout(10):
                return await nest_api.async_get_devices()
        # TODO: update to use api specific error messages
        except Exception as err:
            raise UpdateFailed(f"Error communicating with API: {err}")

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        # Name of the data. For logging purposes.
        name="google_nest",
        update_method=async_update_data,
        # Polling interval. Will only be polled if there are subscribers.
        # TODO: Make poll interval configurable?
        update_interval=timedelta(seconds=30),
    )

    # Fetch initial data so we have data when entities subscribe
    await coordinator.async_refresh()

    entities = []
    for idx, device in enumerate(coordinator.data):
        if device.has_trait(TemperatureMixin.NAME):
            entities.append(TemperatureSensor(coordinator, idx))
        if device.has_trait(HumidityMixin.NAME):
            entities.append(HumiditySensor(coordinator, idx))
    async_add_entities(entities)


class SensorBase(CoordinatorEntity):
    """Representation of a dynamically updated Sensor."""

    def __init__(self, coordinator: DataUpdateCoordinator, idx: int):
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._idx = idx

    @property
    def _device(self) -> Device:
        """Return the latest device state from the coordinator."""
        return self.coordinator.data[self._idx]

    @property
    def device_name(self):
        """Return the name of the physical device that includes the sensor."""
        if self._device.has_trait(InfoMixin.NAME) and self._device.custom_name:
            return self._device.custom_name
        # Build a name from the room/structure
        parent_relations = self._device.parent_relations
        if parent_relations:
            items = sorted(parent_relations.items())
            names = [name for id, name in items]
            return " ".join(names)
        # TODO: Include room here
        return self.unique_id

    @property
    def device_info(self):
        """Return device specific attributes."""
        return {
            "identifiers": {(DOMAIN, self._device.name)},
            "name": self.device_name,
        }


class TemperatureSensor(SensorBase):
    """Representation of a Temperature Sensor."""

    @property
    def unique_id(self) -> Optional[str]:
        """Return a unique ID."""
        # The API returns the identifier under the name field.
        return f"{self._device.name}-temperature"

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{self.device_name} Temperature"

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._device.ambient_temperature_celsius

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return TEMP_CELSIUS


class HumiditySensor(SensorBase):
    """Representation of a Humidity Sensor."""

    @property
    def unique_id(self) -> Optional[str]:
        """Return a unique ID."""
        # The API returns the identifier under the name field.
        return f"{self._device.name}-humidity"

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{self.device_name} Humidity"

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._device.ambient_humidity_percent

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return PERCENTAGE
