"""The Anniversaries Integration"""
import logging
from datetime import datetime
import voluptuous as vol

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_NAME, CONF_SENSORS, Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_validation as cv, aiohttp_client
from homeassistant.helpers.template import Template

from .const import (
    CONF_DATE,
    CONF_DATE_TEMPLATE,
    CONF_ONE_TIME,
    CONF_COUNT_UP,
    CONF_HALF_ANNIVERSARY,
    DOMAIN,
)
from .coordinator import AnniversaryDataUpdateCoordinator
from .data import AnniversaryData

_LOGGER = logging.getLogger(__name__)

PLATFORMS = [Platform.SENSOR, Platform.CALENDAR]

def _validate_date(value):
    """Validate a date string."""
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError:
        pass
    try:
        return datetime.strptime(value, "%m-%d").date().replace(year=1900)
    except ValueError:
        raise vol.Invalid(f"Invalid date: {value}")

async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Set up the Anniversaries component from YAML."""
    if DOMAIN not in config:
        return True

    for sensor_config in config[DOMAIN].get(CONF_SENSORS, []):
        hass.async_create_task(
            hass.config_entries.flow.async_init(
                DOMAIN,
                context={"source": "import"},
                data=sensor_config,
            )
        )
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Anniversaries from a config entry."""
    hass.data.setdefault(DOMAIN, {"anniversaries": {}})

    config = entry.options or entry.data
    name = config[CONF_NAME]

    try:
        if CONF_DATE_TEMPLATE in config:
            date_str = await Template(config[CONF_DATE_TEMPLATE], hass).async_render()
            anniversary_date = _validate_date(date_str)
        else:
            anniversary_date = _validate_date(config[CONF_DATE])
    except Exception as ex:
        _LOGGER.error("Error parsing date for %s: %s", name, ex)
        return False

    unknown_year = anniversary_date.year == 1900

    anniversary = AnniversaryData(
        name=name,
        date=anniversary_date,
        is_one_time=config.get(CONF_ONE_TIME, False),
        is_count_up=config.get(CONF_COUNT_UP, False),
        show_half_anniversary=config.get(CONF_HALF_ANNIVERSARY, False),
        unknown_year=unknown_year,
        config=config,
    )

    if "coordinator" not in hass.data[DOMAIN]:
        websession = aiohttp_client.async_get_clientsession(hass)
        coordinator = AnniversaryDataUpdateCoordinator(hass, {}, websession)
        hass.data[DOMAIN]["coordinator"] = coordinator

    coordinator = hass.data[DOMAIN]["coordinator"]
    coordinator.anniversaries[entry.entry_id] = anniversary

    await coordinator.async_config_entry_first_refresh()

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    entry.async_on_unload(entry.add_update_listener(update_listener))

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        coordinator = hass.data[DOMAIN]["coordinator"]
        coordinator.anniversaries.pop(entry.entry_id)
        if not coordinator.anniversaries:
            hass.data.pop(DOMAIN)
    return unload_ok


async def update_listener(hass: HomeAssistant, entry: ConfigEntry):
    """Handle options update."""
    await hass.config_entries.async_reload(entry.entry_id)