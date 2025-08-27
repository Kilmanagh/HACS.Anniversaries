"""Anniversary integration for Home Assistant."""
from __future__ import annotations

import asyncio
import logging
import os

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN, PLATFORMS
from .coordinator import AnniversaryDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Anniversary from a config entry."""
    # Check if this entry has valid configuration - properly merge data and options
    config = {**entry.data}
    if entry.options:
        config.update(entry.options)
    
    if not config or (not config.get("name") and not config.get("date")):
        _LOGGER.warning(f"Removing empty/invalid config entry: {entry.entry_id}")
        hass.async_create_task(hass.config_entries.async_remove(entry.entry_id))
        return False
    
    # Initialize the shared coordinator if it doesn't exist
    hass.data.setdefault(DOMAIN, {})
    
    # Get or create the shared coordinator that manages ALL anniversaries
    if "coordinator" not in hass.data[DOMAIN]:
        from .data import AnniversaryData
        
        # Collect all anniversary config entries
        all_anniversaries = {}
        for config_entry in hass.config_entries.async_entries(DOMAIN):
            if config_entry.state == "loaded" or config_entry.entry_id == entry.entry_id:
                # Properly merge data and options (options override data)
                entry_config = {**config_entry.data}
                if config_entry.options:
                    entry_config.update(config_entry.options)
                
                if entry_config and (entry_config.get("name") or entry_config.get("date")):
                    try:
                        anniversary_data = AnniversaryData.from_config(entry_config)
                        all_anniversaries[config_entry.entry_id] = anniversary_data
                    except Exception as e:
                        _LOGGER.error(f"Failed to load anniversary {config_entry.entry_id}: {e}")
        
        # Create shared coordinator
        coordinator = AnniversaryDataUpdateCoordinator(hass, all_anniversaries)
        await coordinator.async_config_entry_first_refresh()
        
        hass.data[DOMAIN]["coordinator"] = coordinator
        hass.data[DOMAIN]["coordinator_lock"] = asyncio.Lock()
    else:
        # Add this entry's data to existing coordinator
        coordinator = hass.data[DOMAIN]["coordinator"]
        try:
            from .data import AnniversaryData
            # Properly merge data and options (options override data)
            config = {**entry.data}
            if entry.options:
                config.update(entry.options)
            anniversary_data = AnniversaryData.from_config(config)
            coordinator.anniversaries[entry.entry_id] = anniversary_data
            await coordinator.async_refresh()
        except Exception as e:
            _LOGGER.error(f"Failed to add anniversary {entry.entry_id}: {e}")
            return False
    
    # Store entry-specific coordinator reference
    hass.data[DOMAIN][entry.entry_id] = coordinator

    # Setup platforms
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    # Register update listener
    entry.async_on_unload(entry.add_update_listener(update_listener))
    
    # Register static path for cards (only once) - moved to end to ensure HTTP component is ready
    if "static_path_registered" not in hass.data[DOMAIN]:
        try:
            # Wait for HTTP component to be fully ready
            if hasattr(hass, 'http') and hass.http is not None:
                # Register the www directory to be accessible via /local/community/anniversaries/
                url_path = f"/local/community/{DOMAIN}"
                file_path = hass.config.path(f"custom_components/{DOMAIN}/www")
                
                _LOGGER.debug(f"Attempting to register static path: {url_path} -> {file_path}")
                _LOGGER.debug(f"Path exists: {os.path.exists(file_path)}")
                
                # Import StaticPathConfig from the HTTP component
                try:
                    from homeassistant.components.http import StaticPathConfig
                    
                    # Use StaticPathConfig object instead of dict
                    static_config = StaticPathConfig(url_path, file_path, True)
                    await hass.http.async_register_static_paths([static_config])
                    _LOGGER.info(f"Successfully registered static path: {url_path}")
                    
                except ImportError:
                    _LOGGER.error("Could not import StaticPathConfig")
                except AttributeError as e:
                    _LOGGER.error(f"StaticPathConfig missing attribute: {e}")
                    # Fallback to manual registration
                    try:
                        from aiohttp.web import StaticResource
                        resource = StaticResource(url_path, file_path)
                        hass.http.app.router.register_resource(resource)
                        _LOGGER.info(f"Successfully registered static path via fallback: {url_path}")
                    except Exception as fallback_error:
                        _LOGGER.error(f"Fallback registration failed: {fallback_error}")
                        
                except Exception as e:
                    _LOGGER.error(f"Unexpected error registering static path: {e}")
                
                hass.data[DOMAIN]["static_path_registered"] = True
            else:
                _LOGGER.warning("HTTP component not available or not initialized yet")
                
        except Exception as e:
            _LOGGER.error(f"Failed to register static path for cards: {e}")
            _LOGGER.error(f"Exception type: {type(e)}")
            import traceback
            _LOGGER.error(f"Traceback: {traceback.format_exc()}")
            # Don't fail the entire integration if static path registration fails
            _LOGGER.info("Continuing integration setup without static path registration")

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    # Unload platforms
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        # Remove this entry from the shared coordinator
        if "coordinator" in hass.data[DOMAIN]:
            coordinator = hass.data[DOMAIN]["coordinator"]
            if entry.entry_id in coordinator.anniversaries:
                del coordinator.anniversaries[entry.entry_id]
                await coordinator.async_refresh()
        
        # Remove entry-specific data
        hass.data[DOMAIN].pop(entry.entry_id, None)

    return unload_ok


async def update_listener(hass: HomeAssistant, entry: ConfigEntry):
    """Handle options update."""
    try:
        from .data import AnniversaryData
        
        # Get the shared coordinator
        if "coordinator" not in hass.data[DOMAIN]:
            _LOGGER.error("No coordinator found for update")
            return
            
        coordinator = hass.data[DOMAIN]["coordinator"]
        
        # Properly merge data and options (options override data)
        config = {**entry.data}
        if entry.options:
            config.update(entry.options)
            
        # Update the anniversary data in the coordinator
        anniversary_data = AnniversaryData.from_config(config)
        coordinator.anniversaries[entry.entry_id] = anniversary_data
        
        # Refresh the coordinator to update all entities
        await coordinator.async_refresh()
        _LOGGER.debug(f"Updated anniversary {entry.entry_id} with new configuration")
        
    except Exception as e:
        _LOGGER.error(f"Failed to update anniversary {entry.entry_id}: {e}")
        # Fall back to full reload if update fails
        await hass.config_entries.async_reload(entry.entry_id)
