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
        """Return the name of the calendar."""
        anniversary = self.anniversary
        if anniversary is None:
            return "Unknown Anniversary"
        return anniversary.name

    @property
    def entity_id(self) -> str:
        """Return the entity ID with anniversary prefix."""
        anniversary = self.anniversary
        if anniversary is None:
            return f"calendar.anniversary_unknown_{self._entity_id}"
        
        name = anniversary.name.lower().replace(' ', '_').replace('-', '_')
        # Remove any non-alphanumeric characters except underscores
        import re
        clean_name = re.sub(r'[^a-z0-9_]', '', name)
        return f"calendar.anniversary_{clean_name}"

    @property
    def event(self) -> CalendarEvent | None:
        """Return the next upcoming event."""
        anniversary = self.anniversary
        if anniversary is None:
            return None
        
        next_date = anniversary.next_anniversary_date
        description = (
            f"Happy {anniversary.next_years}th anniversary!"
            if anniversary.next_years is not None
            else anniversary.name
        )
        return CalendarEvent(
            summary=anniversary.name,
            start=next_date,
            end=next_date + timedelta(days=1),
            description=description,
        )

    async def async_get_events(
        self, hass: HomeAssistant, start_date: datetime, end_date: datetime
    ) -> list[CalendarEvent]:
        """Get all events in a specific time frame."""
        anniversary = self.anniversary
        if anniversary is None:
            return []
        
        events = []
        next_date = anniversary.next_anniversary_date
        if start_date.date() <= next_date <= end_date.date():
            description = (
                f"Happy {anniversary.next_years}th anniversary!"
                if anniversary.next_years is not None
                else anniversary.name
            )
            events.append(
                CalendarEvent(
                    summary=anniversary.name,
                    start=next_date,
                    end=next_date + timedelta(days=1),
                    description=description,
                )
            )
        return events