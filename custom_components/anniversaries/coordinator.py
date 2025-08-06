import asyncio
from datetime import timedelta
import logging

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.helpers.template import Template

from .const import DOMAIN
from .data import AnniversaryData

_LOGGER = logging.getLogger(__name__)


class AnniversaryDataUpdateCoordinator(DataUpdateCoordinator[dict[str, AnniversaryData]]):
    """A coordinator to manage anniversary data."""

    def __init__(self, hass: HomeAssistant, anniversaries: dict[str, AnniversaryData]) -> None:
        """Initialize the coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(minutes=1),
        )
        self.anniversaries = anniversaries

    async def _async_update_data(self) -> dict[str, AnniversaryData]:
        """Fetch the latest data."""
        # For now, we don't have anything to update, as the date calculations are
        # properties of the AnniversaryData class. In the future, we might have
        # template-based dates to render here.
        # This coordinator is mainly for providing a central point for entities
        # to subscribe to updates.
        return self.anniversaries
