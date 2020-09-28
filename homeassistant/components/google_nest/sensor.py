"""Support for Google Nest SDM sensors."""

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import TEMP_CELSIUS
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.typing import HomeAssistantType

from .const import DEVICES, DOMAIN


async def async_setup_entry(
    hass: HomeAssistantType, entry: ConfigEntry, async_add_entities
) -> None:
    """Set up the sensors."""

    entities = []
    for device in hass.data[DOMAIN][DEVICES]:
        entities.append(ExampleSensor(device.type))
    async_add_entities(entities)


class ExampleSensor(Entity):
    """Representation of a Sensor."""

    def __init__(self, name):
        """Initialize the sensor."""
        self._state = None
        self._name = name

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return TEMP_CELSIUS

    def update(self):
        """Fetch new state data for the sensor.

        This is the only method that should fetch new data for Home Assistant.
        """
        self._state = 23
