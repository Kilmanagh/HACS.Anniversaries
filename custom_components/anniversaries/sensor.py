"""Sensor platform for Anniversaries."""
from __future__ import annotations

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    ATTRIBUTION,
    ATTR_YEARS_NEXT,
    ATTR_YEARS_CURRENT,
    ATTR_DATE,
    ATTR_NEXT_DATE,
    ATTR_WEEKS,
    ATTR_HALF_DATE,
    ATTR_HALF_DAYS,
    ATTR_ZODIAC_SIGN,
    ATTR_NAMED_ANNIVERSARY,
    ATTR_IS_MILESTONE,
    ATTR_GENERATION,
    ATTR_BIRTHSTONE,
    ATTR_BIRTH_FLOWER,
    DOMAIN,
    DEFAULT_ICON_NORMAL,
    DEFAULT_ICON_TODAY,
    DEFAULT_ICON_SOON,
    DEFAULT_SOON,
    DEFAULT_UNIT_OF_MEASUREMENT,
    CONF_ICON_NORMAL,
    CONF_ICON_TODAY,
    CONF_ICON_SOON,
    CONF_SOON,
    CONF_UNIT_OF_MEASUREMENT,
    CONF_UPCOMING_ANNIVERSARIES_SENSOR,
    CONF_ENABLE_GENERATION_SENSOR,
    CONF_ENABLE_BIRTHSTONE_SENSOR,
    CONF_ENABLE_BIRTH_FLOWER_SENSOR,
)
from .coordinator import AnniversaryDataUpdateCoordinator
from .data import AnniversaryData


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the sensor platform."""
    coordinator: AnniversaryDataUpdateCoordinator = hass.data[DOMAIN]["coordinator"]

    # Add the individual anniversary sensor
    async_add_entities([AnniversarySensor(coordinator, entry.entry_id, entry)])

    # Add the summary sensor if it is enabled and doesn't exist yet
    if entry.options.get(CONF_UPCOMING_ANNIVERSARIES_SENSOR, False):
        lock = hass.data[DOMAIN]["coordinator_lock"]
        async with lock:
            if "summary_sensor_added" not in hass.data[DOMAIN]:
                async_add_entities([UpcomingAnniversariesSensor(coordinator)])
                hass.data[DOMAIN]["summary_sensor_added"] = True


class AnniversarySensor(CoordinatorEntity[AnniversaryDataUpdateCoordinator], SensorEntity):
    """anniversaries Sensor class."""

    _attr_attribution = ATTRIBUTION

    def __init__(
        self,
        coordinator: AnniversaryDataUpdateCoordinator,
        entity_id: str,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._entity_id = entity_id
        self._attr_name = self.anniversary.name
        self._attr_unique_id = f"{entry.entry_id}_sensor"

        self.config = entry.options or entry.data
        self._icon_normal = self.config.get(CONF_ICON_NORMAL, DEFAULT_ICON_NORMAL)
        self._icon_today = self.config.get(CONF_ICON_TODAY, DEFAULT_ICON_TODAY)
        self._icon_soon = self.config.get(CONF_ICON_SOON, DEFAULT_ICON_SOON)
        self._soon_days = self.config.get(CONF_SOON, DEFAULT_SOON)
        self._attr_native_unit_of_measurement = self.config.get(CONF_UNIT_OF_MEASUREMENT, DEFAULT_UNIT_OF_MEASUREMENT)

    @property
    def entity_id(self) -> str:
        """Return the entity ID with anniversary prefix."""
        name = self.anniversary.name.lower().replace(' ', '_').replace('-', '_')
        # Remove any non-alphanumeric characters except underscores
        import re
        clean_name = re.sub(r'[^a-z0-9_]', '', name)
        return f"sensor.anniversary_{clean_name}"


    @property
    def anniversary(self) -> AnniversaryData:
        """Return the anniversary data."""
        return self.coordinator.data[self._entity_id]

    @property
    def native_value(self) -> int:
        """Return the state of the sensor."""
        return self.anniversary.days_remaining

    @property
    def icon(self) -> str:
        """Return the icon of the sensor."""
        days_remaining = self.anniversary.days_remaining
        if days_remaining == 0:
            return self.config.get(CONF_ICON_TODAY, DEFAULT_ICON_TODAY)
        if days_remaining <= self.config.get(CONF_SOON, DEFAULT_SOON):
            return self.config.get(CONF_ICON_SOON, DEFAULT_ICON_SOON)
        return self.config.get(CONF_ICON_NORMAL, DEFAULT_ICON_NORMAL)

    @property
    def extra_state_attributes(self) -> dict[str, any]:
        """Return the state attributes."""
        attrs = {
            ATTR_NEXT_DATE: self.anniversary.next_anniversary_date,
            ATTR_WEEKS: self.anniversary.weeks_remaining,
            ATTR_ZODIAC_SIGN: self.anniversary.zodiac_sign,
            ATTR_IS_MILESTONE: self.anniversary.is_milestone,
        }
        if self.config.get(CONF_ENABLE_GENERATION_SENSOR, False):
            attrs[ATTR_GENERATION] = self.anniversary.generation
        if self.config.get(CONF_ENABLE_BIRTHSTONE_SENSOR, False):
            attrs[ATTR_BIRTHSTONE] = self.anniversary.birthstone
        if self.config.get(CONF_ENABLE_BIRTH_FLOWER_SENSOR, False):
            attrs[ATTR_BIRTH_FLOWER] = self.anniversary.birth_flower
        if self.anniversary.named_anniversary:
            attrs[ATTR_NAMED_ANNIVERSARY] = self.anniversary.named_anniversary
        if self.anniversary.current_years is not None:
            attrs[ATTR_YEARS_CURRENT] = self.anniversary.current_years
        if self.anniversary.next_years is not None:
            attrs[ATTR_YEARS_NEXT] = self.anniversary.next_years
        if self.anniversary.half_anniversary_date is not None:
            attrs[ATTR_HALF_DATE] = self.anniversary.half_anniversary_date
            attrs[ATTR_HALF_DAYS] = self.anniversary.days_until_half_anniversary
        if not self.anniversary.unknown_year:
            attrs[ATTR_DATE] = self.anniversary.date
        return attrs


class UpcomingAnniversariesSensor(CoordinatorEntity[AnniversaryDataUpdateCoordinator], SensorEntity):
    """Upcoming Anniversaries Sensor class."""

    _attr_attribution = ATTRIBUTION
    _attr_name = "Upcoming Anniversaries"
    _attr_icon = "mdi:calendar-multiple"

    def __init__(
        self,
        coordinator: AnniversaryDataUpdateCoordinator,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._attr_unique_id = f"{DOMAIN}_summary_sensor"

    @property
    def entity_id(self) -> str:
        """Return the entity ID."""
        return f"sensor.anniversary_upcoming_anniversaries"

    @property
    def native_value(self) -> str | None:
        """Return the state of the sensor."""
        upcoming = self.coordinator.upcoming_anniversaries
        if not upcoming:
            return "Nothing"
        return upcoming[0].name

    @property
    def extra_state_attributes(self) -> dict[str, any] | None:
        """Return the state attributes."""
        upcoming = self.coordinator.upcoming_anniversaries
        if not upcoming:
            return None

        attrs = {
            "upcoming": [
                {
                    "name": anniversary.name,
                    "date": anniversary.next_anniversary_date.isoformat(),
                    "days_remaining": anniversary.days_remaining,
                }
                for anniversary in upcoming
            ]
        }
        return attrs
