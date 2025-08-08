""" Config flow """
from collections import OrderedDict
from homeassistant.core import callback
import voluptuous as vol
from homeassistant import config_entries
from datetime import datetime
import uuid

from .const import (
    DEFAULT_COUNT_UP,
    DOMAIN,
    DEFAULT_ICON_NORMAL,
    DEFAULT_ICON_SOON,
    DEFAULT_ICON_TODAY,
    DEFAULT_SOON,
    DEFAULT_HALF_ANNIVERSARY,
    DEFAULT_UNIT_OF_MEASUREMENT,
    DEFAULT_ONE_TIME,
    CONF_ICON_NORMAL,
    CONF_ICON_TODAY,
    CONF_ICON_SOON,
    CONF_DATE,
    CONF_SOON,
    CONF_HALF_ANNIVERSARY,
    CONF_UNIT_OF_MEASUREMENT,
    CONF_ONE_TIME,
    CONF_COUNT_UP,
    CONF_UPCOMING_ANNIVERSARIES_SENSOR,
    CONF_ENABLE_GENERATION_SENSOR,
    CONF_ENABLE_BIRTHSTONE_SENSOR,
    CONF_ENABLE_BIRTH_FLOWER_SENSOR,
)

from homeassistant.const import CONF_NAME


from homeassistant.helpers import selector

@config_entries.HANDLERS.register(DOMAIN)
class AnniversariesFlowHandler(config_entries.ConfigFlow):
    """Handle a config flow for Anniversaries."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}
        if user_input is not None:
            try:
                # Validate date
                if is_not_date(user_input[CONF_DATE], user_input.get(CONF_ONE_TIME, False)):
                    raise ValueError("Invalid date")

                # Set a unique ID for the entry
                await self.async_set_unique_id(str(uuid.uuid4()))
                self._abort_if_unique_id_configured()

                return self.async_create_entry(title=user_input[CONF_NAME], data=user_input)
            except Exception:
                errors["base"] = "invalid_date"

        data_schema = vol.Schema(
            {
                vol.Required(CONF_NAME): str,
                vol.Required(CONF_DATE): str,
                vol.Optional(CONF_ONE_TIME, default=DEFAULT_ONE_TIME): bool,
                vol.Optional(CONF_COUNT_UP, default=DEFAULT_COUNT_UP): bool,
                vol.Optional(CONF_HALF_ANNIVERSARY, default=DEFAULT_HALF_ANNIVERSARY): bool,
                vol.Optional(CONF_UNIT_OF_MEASUREMENT, default=DEFAULT_UNIT_OF_MEASUREMENT): str,
                vol.Optional(CONF_ICON_NORMAL, default=DEFAULT_ICON_NORMAL): selector.IconSelector(),
                vol.Optional(CONF_ICON_TODAY, default=DEFAULT_ICON_TODAY): selector.IconSelector(),
                vol.Optional(CONF_SOON, default=DEFAULT_SOON): int,
                vol.Optional(CONF_ICON_SOON, default=DEFAULT_ICON_SOON): selector.IconSelector(),
            }
        )
        return self.async_show_form(step_id="user", data_schema=data_schema, errors=errors)

    async def async_step_import(self, user_input):
        """Import a config entry from configuration.yaml."""
        name = user_input[CONF_NAME]
        unique_id = f"yaml_{name.lower().replace(' ', '_')}"

        await self.async_set_unique_id(unique_id)
        self._abort_if_unique_id_configured()

        return self.async_create_entry(
            title=f"{name} (YAML)",
            data=user_input,
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        if config_entry.options.get("unique_id", None) is not None:
            return OptionsFlowHandler(config_entry)
        else:
            return EmptyOptions(config_entry)

def is_not_date(date, one_time):
    try:
        datetime.strptime(date, "%Y-%m-%d")
        return False
    except ValueError:
        if not one_time:
            pass
        else:
            return True
    try:
        datetime.strptime(date, "%m-%d")
        return False
    except ValueError:
        return True


class OptionsFlowHandler(config_entries.OptionsFlow):
    """Handle an options flow for Anniversaries."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        data_schema = vol.Schema(
            {
                vol.Optional(
                    CONF_UPCOMING_ANNIVERSARIES_SENSOR,
                    default=self.config_entry.options.get(CONF_UPCOMING_ANNIVERSARIES_SENSOR, False),
                ): bool,
                vol.Optional(
                    CONF_ENABLE_GENERATION_SENSOR,
                    default=self.config_entry.options.get(CONF_ENABLE_GENERATION_SENSOR, False),
                ): bool,
                vol.Optional(
                    CONF_ENABLE_BIRTHSTONE_SENSOR,
                    default=self.config_entry.options.get(CONF_ENABLE_BIRTHSTONE_SENSOR, False),
                ): bool,
                vol.Optional(
                    CONF_ENABLE_BIRTH_FLOWER_SENSOR,
                    default=self.config_entry.options.get(CONF_ENABLE_BIRTH_FLOWER_SENSOR, False),
                ): bool,
                vol.Optional(
                    CONF_COUNT_UP,
                    default=self.config_entry.options.get(CONF_COUNT_UP, DEFAULT_COUNT_UP),
                ): bool,
                vol.Optional(
                    CONF_ONE_TIME,
                    default=self.config_entry.options.get(CONF_ONE_TIME, DEFAULT_ONE_TIME),
                ): bool,
                vol.Optional(
                    CONF_HALF_ANNIVERSARY,
                    default=self.config_entry.options.get(CONF_HALF_ANNIVERSARY, DEFAULT_HALF_ANNIVERSARY),
                ): bool,
                vol.Optional(
                    CONF_UNIT_OF_MEASUREMENT,
                    default=self.config_entry.options.get(CONF_UNIT_OF_MEASUREMENT, DEFAULT_UNIT_OF_MEASUREMENT),
                ): str,
                vol.Optional(
                    CONF_ICON_NORMAL,
                    default=self.config_entry.options.get(CONF_ICON_NORMAL, DEFAULT_ICON_NORMAL),
                ): selector.IconSelector(),
                vol.Optional(
                    CONF_ICON_TODAY,
                    default=self.config_entry.options.get(CONF_ICON_TODAY, DEFAULT_ICON_TODAY),
                ): selector.IconSelector(),
                vol.Optional(
                    CONF_SOON,
                    default=self.config_entry.options.get(CONF_SOON, DEFAULT_SOON),
                ): int,
                vol.Optional(
                    CONF_ICON_SOON,
                    default=self.config_entry.options.get(CONF_ICON_SOON, DEFAULT_ICON_SOON),
                ): selector.IconSelector(),
            }
        )
        return self.async_show_form(step_id="init", data_schema=data_schema)


class EmptyOptions(config_entries.OptionsFlow):
    def __init__(self, config_entry):
        self.config_entry = config_entry
