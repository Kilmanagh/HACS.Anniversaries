"""Calendar platform for Anniversaries."""
from __future__ import annotations

from datetime import datetime, timedelta

from homeassistant.components.calendar import CalendarEntity, CalendarEvent
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .coordinator import AnniversaryDataUpdateCoordinator
from .data import AnniversaryData


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the calendar platform."""
    coordinator: AnniversaryDataUpdateCoordinator = hass.data[DOMAIN]["coordinator"]
    async_add_entities([AnniversaryCalendar(coordinator, entry.entry_id, entry)])


class AnniversaryCalendar(CalendarEntity):
    """Anniversary Calendar class."""

    def __init__(
        self,
        coordinator: AnniversaryDataUpdateCoordinator,
        entity_id: str,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the calendar."""
        self.coordinator = coordinator
        self._entity_id = entity_id
        self._attr_unique_id = f"{entry.entry_id}_calendar"

    @property
    def name(self) -> str:
        """Return the name of the calendar."""
        try:
            return self.anniversary.name
        except (KeyError, AttributeError):
            return "Unknown Anniversary"

    @property
    def entity_id(self) -> str:
        """Return the entity ID with anniversary prefix."""
        try:
            name = self.anniversary.name.lower().replace(' ', '_').replace('-', '_')
            # Remove any non-alphanumeric characters except underscores
            import re
            clean_name = re.sub(r'[^a-z0-9_]', '', name)
            return f"calendar.anniversary_{clean_name}"
        except (KeyError, AttributeError):
            return f"calendar.anniversary_unknown_{self._entity_id}"

    @property
    def anniversary(self) -> AnniversaryData:
        """Return the anniversary data."""
        return self.coordinator.data[self._entity_id]

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return (
            self.coordinator.last_update_success
            and self.coordinator.data is not None
            and self._entity_id in self.coordinator.data
        )

    @property
    def event(self) -> CalendarEvent | None:
        """Return the next upcoming event."""
        if not self.available:
            return None
        try:
            next_date = self.anniversary.next_anniversary_date
            description = (
                f"Happy {self.anniversary.next_years}th anniversary!"
                if self.anniversary.next_years is not None
                else self.anniversary.name
            )
            return CalendarEvent(
                summary=self.anniversary.name,
                start=next_date,
                end=next_date + timedelta(days=1),
                description=description,
            )
        except (KeyError, AttributeError):
            return None

    async def async_get_events(
        self, hass: HomeAssistant, start_date: datetime, end_date: datetime
    ) -> list[CalendarEvent]:
        """Get all events in a specific time frame."""
        if not self.available:
            return []
        
        try:
            events = []
            next_date = self.anniversary.next_anniversary_date
            if start_date.date() <= next_date <= end_date.date():
                description = (
                    f"Happy {self.anniversary.next_years}th anniversary!"
                    if self.anniversary.next_years is not None
                    else self.anniversary.name
                )
                events.append(
                    CalendarEvent(
                        summary=self.anniversary.name,
                        start=next_date,
                        end=next_date + timedelta(days=1),
                        description=description,
                    )
                )
            return events
        except (KeyError, AttributeError):
            return []
