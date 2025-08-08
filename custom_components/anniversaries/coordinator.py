from datetime import timedelta, date
import logging
import random
import aiohttp
from collections import OrderedDict

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .const import DOMAIN, CONF_ON_THIS_DAY
from .data import AnniversaryData

_LOGGER = logging.getLogger(__name__)

WIKIPEDIA_API_URL = "https://en.wikipedia.org/api/rest_v1/feed/onthisday/events/{month}/{day}"


class AnniversaryDataUpdateCoordinator(DataUpdateCoordinator[dict[str, AnniversaryData]]):
    """A coordinator to manage anniversary data and API calls."""

    def __init__(self, hass: HomeAssistant, anniversaries: dict[str, AnniversaryData], websession: aiohttp.ClientSession) -> None:
        """Initialize the coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(days=1),  # Update once per day
        )
        self.anniversaries = anniversaries
        self.websession = websession
        self._on_this_day_cache = OrderedDict()
        self.upcoming = []

    @property
    def upcoming_anniversaries(self) -> list[AnniversaryData]:
        """Return a sorted list of the next 5 upcoming anniversaries."""
        return self.upcoming

    async def _async_update_data(self) -> dict[str, AnniversaryData]:
        """Fetch the latest data from Wikipedia."""
        today = date.today()

        # Clean up old cache entries
        if len(self._on_this_day_cache) > 7:
            self._on_this_day_cache.popitem(last=False)

        # Check if we need to fetch new "On This Day" data
        if today not in self._on_this_day_cache:
            try:
                async with self.websession.get(
                    WIKIPEDIA_API_URL.format(month=today.month, day=today.day)
                ) as response:
                    response.raise_for_status()
                    data = await response.json()
                    if data.get("events"):
                        # Cache the list of events for the day
                        self._on_this_day_cache[today] = [event["text"] for event in data["events"]]
            except aiohttp.ClientError as err:
                _LOGGER.warning("Error fetching 'On This Day' data: %s", err)
                self._on_this_day_cache[today] = [] # Avoid retrying for a while

        # Assign a random event to each anniversary that has the feature enabled
        for anniversary in self.anniversaries.values():
            if anniversary.config.get(CONF_ON_THIS_DAY):
                if self._on_this_day_cache.get(today):
                    anniversary.on_this_day_event = random.choice(self._on_this_day_cache[today])
                else:
                    anniversary.on_this_day_event = None
            else:
                anniversary.on_this_day_event = None

        self.upcoming = sorted(
            self.anniversaries.values(),
            key=lambda x: x.next_anniversary_date,
        )[:5]

        return self.anniversaries
