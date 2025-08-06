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
    coordinator: AnniversaryDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(
        AnniversaryCalendar(coordinator, entity_id, entry)
        for entity_id in coordinator.data
    )


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
        self._attr_name = self.anniversary.name
        self._attr_unique_id = f"{entry.entry_id}_calendar"

    @property
    def anniversary(self) -> AnniversaryData:
        """Return the anniversary data."""
        return self.coordinator.data[self._entity_id]

    @property
    def event(self) -> CalendarEvent | None:
        """Return the next upcoming event."""
        next_date = self.anniversary.next_anniversary_date
        return CalendarEvent(
            summary=self.anniversary.name,
            start=next_date,
            end=next_date + timedelta(days=1),
            description=f"Happy {self.anniversary.next_years}th anniversary!",
        )

    async def async_get_events(
        self, hass: HomeAssistant, start_date: datetime, end_date: datetime
    ) -> list[CalendarEvent]:
        """Get all events in a specific time frame."""
        events = []
        next_date = self.anniversary.next_anniversary_date
        if start_date.date() <= next_date <= end_date.date():
            events.append(
                CalendarEvent(
                    summary=self.anniversary.name,
                    start=next_date,
                    end=next_date + timedelta(days=1),
                    description=f"Happy {self.anniversary.next_years}th anniversary!",
                )
            )
        return events
