from datetime import timedelta, date
import logging
import heapq

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.config_entries import ConfigEntry

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

class AnniversaryDataUpdateCoordinator(DataUpdateCoordinator[dict[str, "AnniversaryData"]]):
    """A coordinator to manage anniversary data."""

    def __init__(self, hass: HomeAssistant, entry: "ConfigEntry") -> None:
        """Initialize the coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(days=1),
        )
        self.entry = entry
        self.anniversaries = {}
        self.upcoming = []

    async def _async_update_data(self) -> dict[str, "AnniversaryData"]:
        """Fetch the latest data."""
        from .data import AnniversaryData
        
        try:
            # Create anniversary data from config entry
            config = self.entry.options or self.entry.data
            
            # Debug logging to see what's in the config
            _LOGGER.debug(f"Config data: {config}")
            
            # Check if this is a properly configured entry
            if not config:
                _LOGGER.error(f"No config data found for entry {self.entry.entry_id}")
                return {}
                
            anniversary_data = AnniversaryData.from_config(config)
            
            # Store in anniversaries dict using entry_id as key
            self.anniversaries = {self.entry.entry_id: anniversary_data}
            
            today = date.today()
            candidates = [
                a for a in self.anniversaries.values()
                if not (a.is_one_time and a.date < today)
            ]
            # Use days_remaining to ensure correct ordering for same-year rollover
            self.upcoming = heapq.nsmallest(
                5,
                candidates,
                key=lambda x: x.days_remaining,
            )
            # Return the anniversaries dict as the coordinator data
            return self.anniversaries
            
        except Exception as e:
            _LOGGER.error(f"Error processing anniversary data for entry {self.entry.entry_id}: {e}")
            _LOGGER.error(f"Config: {self.entry.data}")
            _LOGGER.error(f"Options: {self.entry.options}")
            return {}

    @property
    def upcoming_anniversaries(self) -> list["AnniversaryData"]:
        """Return a sorted list of the next 5 upcoming anniversaries."""
        return self.upcoming
