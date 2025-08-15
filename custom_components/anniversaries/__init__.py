"""Anniversary integration for Home Assistant."""
from __future__ import annotations

import asyncio
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN, PLATFORMS
from .coordinator import AnniversaryDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Anniversary from a config entry."""
    # Initialize coordinator with single anniversary from this entry
    coordinator = AnniversaryDataUpdateCoordinator(hass, entry)
    
    # Initial data fetch
    await coordinator.async_config_entry_first_refresh()

    # Store coordinator
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = coordinator
    hass.data[DOMAIN]["coordinator"] = coordinator  # For backward compatibility
    hass.data[DOMAIN]["coordinator_lock"] = hass.data[DOMAIN].get("coordinator_lock", asyncio.Lock())

    # Setup platforms
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    # Register update listener
    entry.async_on_unload(entry.add_update_listener(update_listener))
    
    # Register static path for cards (simple approach)
    hass.http.register_static_path(
        "/local/anniversaries",
        hass.config.path("custom_components/anniversaries/www"),
        cache_headers=False
    )

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok


async def update_listener(hass: HomeAssistant, entry: ConfigEntry):
    """Handle options update."""
    await hass.config_entries.async_reload(entry.entry_id)
