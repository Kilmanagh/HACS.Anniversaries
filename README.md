# Anniversaries

[![HACS](https://img.shields.io/badge/HACS-Default-orange.svg)](https://github.com/custom-components/hacs)
[![GitHub release (latest by date)](https://img.shields.io/github/v/release/pinkywafer/Anniversaries)](https://github.com/pinkywafer/Anniversaries/releases)
![GitHub Release Date](https://img.shields.io/github/release-date/pinkywafer/Anniversaries)
[![GitHub](https://img.shields.io/github/license/pinkywafer/Anniversaries)](LICENSE)

[![Maintenance](https://img.shields.io/badge/Maintained%3F-Yes-brightgreen.svg)](https://github.com/pinkywafer/Anniversaries/graphs/commit-activity)
[![GitHub issues](https://img.shields.io/github/issues/pinkywafer/Anniversaries)](https://github.com/pinkywafer/Anniversaries/issues)

[![Buy me a coffee](https://img.shields.io/static/v1.svg?label=Buy%20me%20a%20coffee&logo=buy%20me%20a%20coffee&logoColor=white&labelColor=ff69b4&message=donate&color=Black)](https://www.buymeacoffee.com/V3q9id4)

[![Support Pinkywafer on Patreon][patreon-shield]][patreon]

The 'anniversaries' component is a Home Assistant custom sensor which counts down to a recurring date such as birthdays, but can be used for any anniversary which occurs annually on the same date.

Any anniversaries entries configured will be added to the home assistant calendar. This also generates the `calendar.anniversaries` entity, which shows information about the next configured anniversary. _N.B. At the moment, only the next occurrence of the anniversaries are added to the calendar_

[![Support Pinkywafer on Patreon][patreon-shield]][patreon]

The 'anniversaries' component is a Home Assistant custom sensor which counts down to a recurring date such as birthdays, but can be used for any anniversary which occurs annually on the same date.

Any anniversaries entries configured will be added to the home assistant calendar. This also generates the `calendar.anniversaries` entity, which shows information about the next configured anniversary. _N.B. At the moment, only the next occurrence of the anniversaries are added to the calendar_

## ✨ Custom Lovelace Cards

This integration includes **4 custom Lovelace cards** that are **automatically loaded** when you install the integration:

- 🗓️ **Timeline Card**: Chronological list with color coding and attribute badges
- 🌟 **Details Card**: Rich single-anniversary view with animations and backgrounds  
- 📅 **Calendar Card**: Interactive mini calendar with clickable dates
- 📊 **Stats Card**: Summary statistics and distribution charts

The cards will automatically appear in your Lovelace card picker after installing the integration. See [CARDS.md](CARDS.md) for detailed configuration options.

## 🎯 Features

- ✅ **Automatic entity ID prefixing** with `anniversary_` for better organization
- ✅ **Rich attributes**: zodiac signs ♈, birthstones 💎, generations 👥, milestones 🌟
- ✅ **Calendar integration** with anniversary events
- ✅ **Custom Lovelace cards** with animations and emoji support
- ✅ **Upcoming anniversaries sensor** for dashboard summaries
- ✅ **Half-anniversary support** for special dates
- ✅ **Count-up mode** to track years since events
- ✅ **One-time events** for non-recurring dates
- ✅ **Multi-language support** with translations

## Table of Contents

* [Installation](#installation)
  * [Manual Installation](#manual-installation)
  * [Installation via HACS](#installation-via-hacs)
* [Custom Lovelace Cards](#custom-lovelace-cards)
* [Configuration](#configuration)
  * [Configuration Parameters](#configuration-parameters)
* [State and Attributes](#state-and-attributes)
  * [State](#state)
  * [Attributes](#attributes)
  * [Notes about unit of measurement](#notes-about-unit-of-measurement)
* [Entity ID Management](#entity-id-management)
* [Troubleshooting](#troubleshooting)

## Installation

### MANUAL INSTALLATION

1. Download the `anniversaries.zip` file from the
   [latest release](https://github.com/pinkywafer/anniversaries/releases/latest).
2. Unpack the release and copy the `custom_components/anniversaries` directory
   into the `custom_components` directory of your Home Assistant
   installation.
3. Configure the `anniversaries` sensor.
4. Restart Home Assistant.

### INSTALLATION VIA HACS

1. Ensure that [HACS](https://custom-components.github.io/hacs/) is installed.
2. Search for and install the "anniversaries" integration.
3. Configure the `anniversaries` sensor.
4. Restart Home Assistant.
5. **Register custom cards** - go to Settings → Dashboards → Resources and add the card JavaScript files (see [CARDS.md](CARDS.md) for details)

## Custom Lovelace Cards

This integration includes 4 beautiful custom cards that automatically install with the integration:

### 🗓️ Timeline Card (`anniversary-timeline-card`)
Shows upcoming anniversaries in chronological order with:
- Color coding by urgency (red=today, orange=week, yellow=month, green=future)
- Optional attribute badges (zodiac ♈, birthstone 💎, generation 👥)
- Smart emoji icons (🎂 birthdays, 💍 weddings, 📅 general)

### 🌟 Details Card (`anniversary-details-card`)  
Rich single-anniversary view featuring:
- Dynamic background gradients based on days remaining
- Pulse animation for today's anniversaries, sparkle for milestones
- All anniversary attributes displayed beautifully
- Compact mode option

### 📅 Calendar Card (`anniversary-calendar-card`)
Interactive mini calendar with:
- Anniversary dates highlighted with visual indicators
- Click dates for popup details
- Month navigation controls
- Support for multiple anniversaries per day

### 📊 Stats Card (`anniversary-stats-card`)
Comprehensive overview including:
- Summary statistics (total, today, this week, month, milestones)  
- Next 3 upcoming anniversaries
- Distribution charts (zodiac signs, generations)
- Quick insights and trends

**For detailed card configuration and examples, see [CARDS.md](CARDS.md)**

## Configuration

Anniversaries can be configured on the integrations menu or in configuration.yaml

### Config Flow

In Configuration/Integrations click on the + button, select Anniversaries and configure the options on the form.

### configuration.yaml

Add `anniversaries` sensor in your `configuration.yaml`. The following example adds two sensors - Shakespeare's birthday and wedding anniversary!

```yaml
# Example configuration.yaml entry

anniversaries:
  sensors:
  - name: Shakespeare's Birthday
    date: '1564-04-23'
  - name: Shakespeare's Wedding Anniversary
    date: '1582-11-27'
```

### CONFIGURATION PARAMETERS

Anniversaries are configured through the UI. The YAML configuration is deprecated, but still supported.

#### YAML Only Configuration

The following options are only available when configuring anniversaries in `configuration.yaml`:

|Parameter |Optional|Description
|:----------|----------|------------
|`date_template` | Yes | Template to evaluate date from. The template must return a string in either `'YYYY-MM-DD'` or `'MM-DD'` format, ie: `date_template: '{{ states("input_datetime.your_input_datetime") \| string }}'`

#### Main Configuration

When adding an anniversary, you will be presented with the following options:

|Parameter |Optional|Description
|:----------|----------|------------
| `name` | No | Friendly name for the anniversary.
|`date` | No | The date of the anniversary in `YYYY-MM-DD` or `MM-DD` format.
| `count_up` | Yes | `true` or `false`. Changes the sensor to count up from the anniversary date. **Default**: `false`
| `one_time` | Yes | `true` or `false`. For a one-time event (non-recurring). **Default**: `false`
| `show_half_anniversary` | Yes | `true` or `false`. Enables the half-anniversary attributes. **Default**: `false`
| `unit_of_measurement` | Yes | Your choice of label for the sensor's unit. The sensor always returns days, but this allows for localization. **Default**: `Days`
| `icon_normal` | Yes | The icon to display for the sensor in its normal state. **Default**:  `mdi:calendar-blank`
| `icon_today` | Yes | The icon to display when the anniversary is today. **Default**: `mdi:calendar-star`
| `days_as_soon` | Yes | The number of days in advance to display the "soon" icon. **Default**: 1
| `icon_soon` | Yes | The icon to display when the anniversary is "soon". **Default**: `mdi:calendar`

#### Options

After creating an anniversary, you can click "Configure" to access additional options:

|Parameter |Optional|Description
|:----------|----------|------------
| `upcoming_anniversaries_sensor` | Yes | `true` or `false`. Enables a summary sensor showing the next 5 upcoming anniversaries. **Default**: `false`

## State and Attributes

### Individual Anniversary Sensor (`sensor.anniversary_...`)

#### State

* The number of days remaining until the next occurrence (or days since the last occurrence if `count_up` is enabled).

#### Attributes

* `years_at_anniversary`: Number of years that will have passed at the next anniversary (not displayed if year is unknown).
* `current_years`: Current age in years (not displayed if year is unknown).
* `date`: The date of the first occurrence (not displayed if year is unknown).
* `next_date`: The date of the next occurrence.
* `weeks_remaining`: The number of weeks until the anniversary.
* `zodiac_sign`: The Western zodiac sign for the anniversary date.
* `named_anniversary`: The traditional name for the anniversary (e.g., "Silver", "Golden"), if applicable.
* `is_milestone`: `true` if the anniversary is a significant milestone (e.g., 10, 25, 50 years).
* `generation`: The generational name (e.g., "Millennial", "Gen X") if the birth year is known.
* `birthstone`: The birthstone for the anniversary month.
* `birth_flower`: The birth flower for the anniversary month.
* `half_anniversary_date`: The date of the next half anniversary, if enabled.
* `days_until_half_anniversary`: The number of days until the next half anniversary, if enabled.

### Upcoming Anniversaries Sensor (`sensor.upcoming_anniversaries`)

This sensor is created if you enable it in the options.

#### State

* The name of the next upcoming anniversary.

#### Attributes

* `upcoming`: A list of the next 5 upcoming anniversaries, with each item containing:
    * `name`: The name of the anniversary.
    * `date`: The date of the next occurrence.
    * `days_remaining`: The number of days until the anniversary.

### Notes about unit of measurement

Unit_of_measurement is *not* translate-able.
You can, however, change the text for unit of measurement in the configuration.  NB the sensor will always report in days, this just allows you to represent this in your own language.

## Entity ID Management

All anniversary entities automatically use the `anniversary_` prefix for better organization:

- **Sensors**: `sensor.anniversary_mom_birthday_abc123`
- **Calendars**: `calendar.anniversary_mom_birthday_abc123`  
- **Summary Sensor**: `sensor.anniversary_upcoming_anniversaries` (when enabled)

### Automatic Migration
The integration automatically migrates existing entities to use the proper prefix. Entity IDs are updated during the migration process to ensure consistency.

## Troubleshooting

### Common Issues

**IndentationError or SyntaxError during setup:**
- Clear the integration's Python cache: `rm -rf /config/custom_components/anniversaries/__pycache__`
- Restart Home Assistant
- Ensure you have the latest version from HACS

**Custom cards not appearing:**
- Register the card resources in Settings → Dashboards → Resources first
- Add each JavaScript file with type "JavaScript module"  
- Clear your browser cache (Ctrl+F5 or Cmd+Shift+R)
- Verify files exist at `/local/custom_components/anniversaries/www/[filename].js`

**Display Precision option showing for anniversary sensors:**
- This has been fixed in recent versions - anniversary sensors now use `SensorDeviceClass.DURATION`
- Update to the latest version to remove the irrelevant precision option

**Entity IDs not using anniversary_ prefix:**
- The integration automatically migrates entities on startup
- Check Configuration → Entities to verify the new entity IDs
- Old automations/scripts may need entity ID updates

[patreon-shield]: https://c5.patreon.com/external/logo/become_a_patron_button.png
[patreon]: https://www.patreon.com/pinkywafer
