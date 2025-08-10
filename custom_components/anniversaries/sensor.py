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
        self._attr_unique_id = f"{entry.entry_id}_sensor"
        self._entry = entry

        self.config = entry.options or entry.data
        self._icon_normal = self.config.get(CONF_ICON_NORMAL, DEFAULT_ICON_NORMAL)
        self._icon_today = self.config.get(CONF_ICON_TODAY, DEFAULT_ICON_TODAY)
        self._icon_soon = self.config.get(CONF_ICON_SOON, DEFAULT_ICON_SOON)
        self._soon_days = self.config.get(CONF_SOON, DEFAULT_SOON)
        self._attr_native_unit_of_measurement = self.config.get(CONF_UNIT_OF_MEASUREMENT, DEFAULT_UNIT_OF_MEASUREMENT)

    @property
    def anniversary(self) -> AnniversaryData | None:
        """Return the anniversary data."""
        if not hasattr(self.coordinator, 'anniversaries') or self.coordinator.anniversaries is None:
            return None
        return self.coordinator.anniversaries.get(self._entity_id)

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return self.anniversary is not None

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        anniversary = self.anniversary
        if anniversary is None:
            return "Unknown Anniversary"
        return anniversary.name

    @property
    def native_value(self) -> int | None:
        """Return the state of the sensor."""
        anniversary = self.anniversary
        if anniversary is None:
            return None
        return anniversary.days_remaining

    @property
    def icon(self) -> str:
        """Return the icon of the sensor."""
        anniversary = self.anniversary
        if anniversary is None:
            return self.config.get(CONF_ICON_NORMAL, DEFAULT_ICON_NORMAL)
        
        days_remaining = anniversary.days_remaining
        if days_remaining == 0:
            return self.config.get(CONF_ICON_TODAY, DEFAULT_ICON_TODAY)
        if days_remaining <= self.config.get(CONF_SOON, DEFAULT_SOON):
            return self.config.get(CONF_ICON_SOON, DEFAULT_ICON_SOON)
        return self.config.get(CONF_ICON_NORMAL, DEFAULT_ICON_NORMAL)

    @property
    def extra_state_attributes(self) -> dict[str, any]:
        """Return the state attributes."""
        anniversary = self.anniversary
        if anniversary is None:
            return {}
            
        attrs = {
            ATTR_NEXT_DATE: anniversary.next_anniversary_date,
            ATTR_WEEKS: anniversary.weeks_remaining,
            ATTR_ZODIAC_SIGN: anniversary.zodiac_sign,
            ATTR_IS_MILESTONE: anniversary.is_milestone,
            ATTR_GENERATION: anniversary.generation,
            ATTR_BIRTHSTONE: anniversary.birthstone,
            ATTR_BIRTH_FLOWER: anniversary.birth_flower,
        }
        if anniversary.named_anniversary:
            attrs[ATTR_NAMED_ANNIVERSARY] = anniversary.named_anniversary
        if anniversary.current_years is not None:
            attrs[ATTR_YEARS_CURRENT] = anniversary.current_years
        if anniversary.next_years is not None:
            attrs[ATTR_YEARS_NEXT] = anniversary.next_years
        if anniversary.half_anniversary_date is not None:
            attrs[ATTR_HALF_DATE] = anniversary.half_anniversary_date
            attrs[ATTR_HALF_DAYS] = anniversary.days_until_half_anniversary
        if not anniversary.unknown_year:
            attrs[ATTR_DATE] = anniversary.date
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
