"""
Home Assistant custom cards for Anniversaries integration.

This module registers and loads custom Lovelace cards for the Anniversaries integration.
These cards provide enhanced UI components for displaying anniversary data.
"""

import logging
from homeassistant.core import HomeAssistant
from homeassistant.components.http import HomeAssistantView
from homeassistant.helpers.typing import ConfigType
from aiohttp import web

_LOGGER = logging.getLogger(__name__)

DOMAIN = "anniversaries"
CARDS_PATH = "www/cards"


class AnniversaryCardsView(HomeAssistantView):
    """View to serve anniversary cards."""
    
    url = "/api/anniversaries/cards/{card_name}"
    name = "api:anniversaries:cards"
    requires_auth = False

    def __init__(self, hass: HomeAssistant):
        """Initialize the view."""
        self.hass = hass

    async def get(self, request, card_name):
        """Serve card files."""
        try:
            card_file = self.hass.config.path(f"custom_components/{DOMAIN}/www/{card_name}")
            with open(card_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Determine content type
            if card_name.endswith('.js'):
                content_type = 'application/javascript'
            elif card_name.endswith('.css'):
                content_type = 'text/css'
            else:
                content_type = 'text/plain'
                
            return web.Response(
                text=content,
                content_type=content_type,
                headers={'Cache-Control': 'no-cache'}
            )
        except FileNotFoundError:
            return web.Response(status=404, text="Card not found")
        except Exception as e:
            _LOGGER.error(f"Error serving card {card_name}: {e}")
            return web.Response(status=500, text="Internal server error")


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the anniversaries cards component."""
    # Register the view to serve cards
    hass.http.register_view(AnniversaryCardsView(hass))
    
    # Register cards with frontend
    await _register_cards(hass)
    
    return True


async def _register_cards(hass: HomeAssistant) -> None:
    """Register anniversary cards with the frontend."""
    try:
        # List of our custom cards
        cards = [
            "anniversary-timeline-card.js",
            "anniversary-details-card.js", 
            "anniversary-calendar-card.js",
            "anniversary-stats-card.js"
        ]
        
        # Register each card as a frontend module
        for card in cards:
            card_url = f"/api/anniversaries/cards/{card}"
            
            # Add to frontend extra modules
            if "frontend_extra_module_url" not in hass.data:
                hass.data["frontend_extra_module_url"] = set()
            
            hass.data["frontend_extra_module_url"].add(card_url)
            _LOGGER.info(f"Registered anniversary card: {card}")
        
        # Trigger frontend to reload resources
        hass.bus.async_fire("lovelace_reload_resources")
        
    except Exception as e:
        _LOGGER.error(f"Failed to register anniversary cards: {e}")
