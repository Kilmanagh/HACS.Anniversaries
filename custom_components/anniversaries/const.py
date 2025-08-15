"""Constants for the Anniversaries integration."""
from homeassistant.const import CONF_NAME
import homeassistant.helpers.config_validation as cv
import voluptuous as vol

# Base component constants
DOMAIN = "anniversaries"
ATTRIBUTION = "Sensor data calculated by Anniversaries Integration"

# Platforms
PLATFORMS = ["sensor", "calendar"]
CALENDAR_PLATFORM = "calendar"
SENSOR_PLATFORM = "sensor"

# Configuration
CONF_DATE = "date"
CONF_DATE_TEMPLATE = "date_template"
CONF_ICON_NORMAL = "icon_normal"
CONF_ICON_TODAY = "icon_today"
CONF_ICON_SOON = "icon_soon"
CONF_SENSORS = "sensors"
CONF_SOON = "days_as_soon"
CONF_HALF_ANNIVERSARY = "show_half_anniversary"
CONF_UNIT_OF_MEASUREMENT = "unit_of_measurement"
CONF_ONE_TIME = "one_time"
CONF_COUNT_UP = "count_up"

# Defaults
DEFAULT_ICON_NORMAL = "mdi:calendar-blank"
DEFAULT_ICON_TODAY = "mdi:calendar-star"
DEFAULT_ICON_SOON = "mdi:calendar"
DEFAULT_SOON = 1
DEFAULT_HALF_ANNIVERSARY = False
DEFAULT_UNIT_OF_MEASUREMENT = "Days"
DEFAULT_ONE_TIME = False
DEFAULT_COUNT_UP = False

# Attributes
ATTR_YEARS_NEXT = "years_at_anniversary"
ATTR_YEARS_CURRENT = "current_years"
ATTR_DATE = "date"
ATTR_NEXT_DATE = "next_date"
ATTR_WEEKS = "weeks_remaining"
ATTR_HALF_DATE = "half_anniversary_date"
ATTR_HALF_DAYS = "days_until_half_anniversary"
ATTR_ZODIAC_SIGN = "zodiac_sign"
ATTR_NAMED_ANNIVERSARY = "named_anniversary"
ATTR_IS_MILESTONE = "is_milestone"
ATTR_GENERATION = "generation"
ATTR_BIRTHSTONE = "birthstone"
ATTR_BIRTH_FLOWER = "birth_flower"

# Configuration
CONF_UPCOMING_ANNIVERSARIES_SENSOR = "upcoming_anniversaries_sensor"
CONF_ENABLE_SUMMARY_SENSOR = "enable_summary_sensor"

# Schema
CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.Schema(
            {
                vol.Optional(CONF_SENSORS): vol.All(
                    cv.ensure_list,
                    [
                        vol.Schema(
                            {
                                vol.Required(CONF_NAME): cv.string,
                                vol.Optional(CONF_DATE): cv.string,
                                vol.Optional(CONF_DATE_TEMPLATE): cv.string,
                                vol.Optional(CONF_SOON, default=DEFAULT_SOON): cv.positive_int,
                                vol.Optional(CONF_ICON_NORMAL, default=DEFAULT_ICON_NORMAL): cv.icon,
                                vol.Optional(CONF_ICON_TODAY, default=DEFAULT_ICON_TODAY): cv.icon,
                                vol.Optional(CONF_ICON_SOON, default=DEFAULT_ICON_SOON): cv.icon,
                                vol.Optional(CONF_HALF_ANNIVERSARY, default=DEFAULT_HALF_ANNIVERSARY): cv.boolean,
                                vol.Optional(CONF_UNIT_OF_MEASUREMENT, default=DEFAULT_UNIT_OF_MEASUREMENT): cv.string,
                                vol.Optional(CONF_ONE_TIME, default=DEFAULT_ONE_TIME): cv.boolean,
                                vol.Optional(CONF_COUNT_UP, default=DEFAULT_COUNT_UP): cv.boolean,
                            }
                        )
                    ],
                )
            }
        )
    },
    extra=vol.ALLOW_EXTRA,
)
