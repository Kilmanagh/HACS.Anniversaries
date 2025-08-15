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
    # Create anniversary data from config entry
    from .data import AnniversaryData
    
    # Convert config entry to AnniversaryData
    config = entry.options or entry.data
    anniversary_data = AnniversaryData.from_config(config)
    anniversaries = {entry.entry_id: anniversary_data}
    
    # Initialize coordinator
    coordinator = AnniversaryDataUpdateCoordinator(hass, anniversaries)
    
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
    
    # Setup custom cards
    await _setup_cards(hass)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok


async def update_listener(hass: HomeAssistant, entry: ConfigEntry):
    """Handle options update."""
    await hass.config_entries.async_reload(entry.entry_id)


async def _setup_cards(hass: HomeAssistant) -> None:
    """Set up custom cards for the integration."""
    try:
        # Import and setup cards module
        from . import cards
        await cards.async_setup(hass, {})
        _LOGGER.info("Anniversary cards setup completed")
    except Exception as e:
        _LOGGER.error(f"Failed to setup anniversary cards: {e}")
