# Anniversaries



The 'anniversaries' component is a Home Assistant custom sensor which counts down to a recurring date such as birthdays, but can be used for any anniversary which occurs annually on the same date.

Any anniversaries entries configured will be added to the home assistant calendar. This also generates the `calendar.anniversaries` entity, which shows information about the next configured anniversary. _N.B. At the moment, only the next occurrence of the anniversaries are added to the calendar_



The 'anniversaries' component is a Home Assistant custom sensor which counts down to a recurring date such as birthdays, but can be used for any anniversary which occurs annually on the same date.

Any anniversaries entries configured will be added to the home assistant calendar. This also generates the `calendar.anniversaries` entity, which shows information about the next configured anniversary. _N.B. At the moment, only the next occurrence of the anniversaries are added to the calendar_

## ✨ Custom Lovelace Cards

This integration includes **4 custom Lovelace cards** with rich emoji/icon support:

- 🗓️ **Timeline Card**: Chronological list with color coding and attribute badges
- 🌟 **Details Card**: Rich single-anniversary view with animations and backgrounds  
- 📅 **Calendar Card**: Interactive mini calendar with clickable dates
- 📊 **Stats Card**: Summary statistics and distribution charts

**Installation Notes**: 
- Cards are automatically installed to `\config\www\community\anniversaries\` via HACS
- **Manual resource registration required** in Settings → Dashboards → Resources
- **For developers**: Copy updated files manually to `\config\www\community\anniversaries\` for testing
- See [CARDS.md](CARDS.md) for complete installation and configuration instructions

## 🎯 Features

- ✅ **Automatic entity ID prefixing** with `anniversary_` for better organization
- ✅ **Rich attributes**: zodiac signs ♈, birthstones 💎, generations 👥, milestones 🌟
- ✅ **"Since last" tracking**: Always-available attributes to track time since last anniversary
- ✅ **Category system**: Organize anniversaries by type with automatic icons 🎂💍🌹
- ✅ **Calendar integration** with anniversary events
- ✅ **Custom Lovelace cards** with animations and emoji support
- ✅ **Upcoming anniversaries sensor** for dashboard summaries
- ✅ **Half-anniversary support** for special dates
- ✅ **One-time events** for non-recurring dates
- ✅ **Multi-language support** with translations

## 🚀 New Features & Improvements

- Expanded emoji selection: Now includes family, generations, community, travel/adventure, accessibility, music, and more
- Universal color scheme for timeline cards: Red (today) → Orange (this week) → Green (this month) → Blue (future)
- Duplicate emojis removed for clarity and easier selection
- Fixed corrupted emojis and improved category icons for all cards
- Category icons now match the latest emoji assignments in const.py

## 📝 Emoji Categories
- Basic celebrations, Religious & Spiritual, Love & Relationships, Seasons, Travel & Vacations, Health & Medical, Work & Career, Home & Life, Animals & Pets, Hobbies & Interests, General & Time, Family & Generations, Community & Social, Travel & Adventure

See the integration for the full emoji list and category details.

## 🆕 Latest Updates

**Timeline Card v1.3.2** - Critical configuration fixes:
- 🔧 **Card registration fix**: All cards now properly register with `custom:` prefix for correct YAML parsing
- ⚙️ **Configuration validation**: Fixed category filtering and date formatting not working due to config issues
- 🔄 **Race condition fixes**: Improved timing between configuration and Home Assistant state initialization
- 🛠️ **Enhanced debugging**: Better error handling and fallback logic for date formatting
- ⚠️ **Breaking change**: After updating, restart Home Assistant and hard refresh browser (Ctrl+F5) to clear cache

**Timeline Card v1.3.1** - Enhanced date formatting options:
- 📅 **Flexible date formats**: `long`, `short`, `numeric`, `full`, and `custom` patterns
- 🌍 **Locale support**: Force specific locales (German, French, Japanese, etc.) or auto-detect
- 📆 **Day of week control**: Toggle day names on/off independently
- 🎨 **Custom patterns**: Create your own date formats (ISO: `YYYY-MM-DD`, European: `DD.MM.YYYY`, etc.)
- 🔧 **User choice**: Default to beautiful long format while allowing full customization

**Timeline Card v1.3.0** - Advanced options with multi-category support:
- 🎯 **Multi-category timelines**: Display multiple anniversary types in one card (`categories: ["birthday", "anniversary"]`)
- 📊 **Category statistics**: Overview with counts, today's events, and milestones
- 🗂️ **Category grouping**: Organize under headers with visual separation (`group_by_category: true`)
- ⭐ **Priority categories**: Show important types first (`priority_categories: ["birthday"]`)
- 🎂 **Birthday excellence preserved**: Original zodiac/birthstone experience unchanged

**Timeline Card v1.2.0** - Enhanced category system:
- ✨ **Enhanced attributes**: All categories now have rich, meaningful attributes (not just birthdays!)
- 🏷️ **Category badges**: Visual indicators for easy category identification  
- 🎨 **Theme-aware colors**: Category-specific color schemes that match anniversary type
- � **Preserved excellence**: Birthday timeline remains as awesome as ever with unchanged attributes
- 📅 **Long date format**: Dates display in local language (e.g., "January 1, 2025")
- � **Smart defaults**: Auto-titles, icons, and attributes based on category selection

**Example**: Birthday timeline keeps `zodiac_sign`, `birthstone`, `generation` while work anniversaries get `current_years`, `named_anniversary`, `generation` with professional blue theme.

**Timeline Card v1.1.0** - Category filtering foundation:
- 🎯 **Category filtering**: Show only specific anniversary types per card
- 🏷️ **8 category types**: birthday, anniversary, memorial, holiday, work, achievement, event, other

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
   [latest release](https://github.com/).
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
- **Flexible date formatting**: Choose from `long`, `short`, `numeric`, `full`, or custom patterns with locale support
- **Multi-category support**: Display multiple anniversary types in one timeline (`categories: ["birthday", "work"]`)
- **Category statistics**: Overview with counts, today's events, and milestones (`show_category_stats: true`)
- **Category grouping**: Organize under headers with visual separation (`group_by_category: true`)
- **Priority categories**: Show important types first (`priority_categories: ["birthday"]`)
- **Enhanced category system**: All categories now have rich attributes (not just birthdays!)
- **Category badges**: Visual indicators with emoji for easy identification
- **Theme-aware colors**: Category-specific color schemes (romantic pink, professional blue, etc.)
- **Category filtering**: Display only specific anniversary types (birthdays, work anniversaries, etc.)
- **Smart category defaults**: Automatic titles, icons, and attributes based on category selection
- **Preserved birthday excellence**: Original birthday experience unchanged with zodiac ♈, birthstone 💎, generation 👥

**Category Examples**:
```yaml
# Birthday-focused timeline (unchanged excellence!)
type: custom:anniversary-timeline-card
category: "birthday"
# Auto-title: "🎂 Upcoming Birthdays"
# Auto-attributes: zodiac_sign, birthstone, generation

# Work anniversaries with enhanced attributes
type: custom:anniversary-timeline-card
category: "work"
title: "Team Milestones"
# Auto-attributes: current_years, named_anniversary, generation
# Theme: professional blue colors

# Memorial dates with respectful theme
type: custom:anniversary-timeline-card
category: "memorial"  
# Auto-attributes: current_years, birth_flower, generation
# Theme: gentle purple colors
```

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

### 🎉 Holiday Timeline Card

The **Holiday Timeline Card** displays upcoming holidays in chronological order, with:
- **Universal color scheme**: Red (today) → Orange (this week) → Green (this month) → Blue (future)
- **Emoji support**: Choose from a comprehensive emoji list for each holiday (🎄🎃🦃🎉 etc.)
- **Category filtering**: Only shows entities with the 'holiday' category
- **Attribute badges**: Displays relevant attributes for each holiday
- **Customizable display**: Title, max items, date format, icons, and more

**Example configuration:**
```yaml
- type: custom:holiday-timeline-card
  title: "🎉 Upcoming Holidays"
  max_items: 5
  date_format: long
  show_day_of_week: true
  show_icons: true
  color_coding: true
```

**Features:**
- Chronological list of holidays with days remaining
- Color-coded urgency for each event
- Rich emoji and icon support
- Debug mode for troubleshooting entity filtering

See the integration and card file for advanced options and details.

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
| `category` | Yes | Category type: `birthday`, `anniversary`, `memorial`, `holiday`, `work`, `achievement`, `event`, or `other`. Affects default icon. **Default**: `other`
| `one_time` | Yes | `true` or `false`. For a one-time event (non-recurring). **Default**: `false`
| `show_half_anniversary` | Yes | `true` or `false`. Enables the half-anniversary attributes. **Default**: `false`
| `unit_of_measurement` | Yes | Your choice of label for the sensor's unit. The sensor always returns days, but this allows for localization. **Default**: `Days`
| `icon_normal` | Yes | The icon to display for the sensor in its normal state. Uses category-specific icon if not specified. **Default**: Category-specific
| `icon_today` | Yes | The icon to display when the anniversary is today. **Default**: `mdi:calendar-star`
| `days_as_soon` | Yes | The number of days in advance to display the "soon" icon. **Default**: 1
| `icon_soon` | Yes | The icon to display when the anniversary is "soon". **Default**: `mdi:calendar`

#### Options

After creating an anniversary, you can click "Configure" to access additional options:

|Parameter |Optional|Description
|:----------|----------|------------
| `upcoming_anniversaries_sensor` | Yes | `true` or `false`. Enables a summary sensor showing the next 5 upcoming anniversaries. **Default**: `false`

### Category-Specific Default Icons

When no custom icon is specified, the integration automatically uses category-appropriate icons:

| Category | Icon | Description |
|:---------|:-----|:------------|
| 🎂 `birthday` | `mdi:cake-variant` | Personal birthdays |
| 💍 `anniversary` | `mdi:heart` | Wedding anniversaries, relationship milestones |
| 🌹 `memorial` | `mdi:flower` | Memorial dates, remembrance days |
| ⭐ `holiday` | `mdi:calendar-star` | Personal holidays, cultural celebrations |
| 💼 `work` | `mdi:briefcase` | Work anniversaries, career milestones |
| 🏆 `achievement` | `mdi:trophy` | Graduations, accomplishments |
| ✅ `event` | `mdi:calendar-check` | General events, appointments |
| 📅 `other` | `mdi:calendar-blank` | Custom/uncategorized anniversaries |

## State and Attributes

### Individual Anniversary Sensor (`sensor.anniversary_...`)

#### State

* The number of days remaining until the next occurrence.

#### Attributes

* `years_at_anniversary`: Number of years that will have passed at the next anniversary (not displayed if year is unknown).
* `current_years`: Current age in years (not displayed if year is unknown).
* `category`: The category type of the anniversary (birthday, anniversary, memorial, etc.).
* `days_since_last`: Days since last anniversary (positive for recurring) or days since/until one-time event (negative if future).
* `last_anniversary_date`: The date of the last anniversary occurrence.
* `years_since_last`: Years since last anniversary (not displayed if year is unknown).
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
- Verify files exist at `/local/community/anniversaries/[filename].js` (for HACS)

**Display Precision option showing for anniversary sensors:**
- This has been fixed in recent versions - anniversary sensors now use `SensorDeviceClass.DURATION`
- Update to the latest version to remove the irrelevant precision option

**Entity IDs not using anniversary_ prefix:**
- The integration automatically migrates entities on startup
- Check Configuration → Entities to verify the new entity IDs
- Old automations/scripts may need entity ID updates

## 🔧 Development & Testing

**For developers working with this integration:**

### Local Development Setup
1. **Clone repository** to development environment
2. **Edit files** in `custom_components/anniversaries/www/` 
3. **Copy updated files** to Home Assistant at `\config\www\community\anniversaries\`
4. **Hard refresh browser** (Ctrl+Shift+R) to bypass cache
5. **Check browser console** (F12) for debug messages

### File Deployment
- **HACS users**: Files auto-install to `\config\www\community\anniversaries\`
- **Manual testing**: Copy workspace files to live HA instance
- **Resource URLs**: Use `/local/community/anniversaries/[filename].js`
- **Cache issues**: Always hard refresh after file changes

### Debugging Cards
- Browser console (F12) shows card loading and configuration issues
- Check resource registration in Settings → Dashboards → Resources
- Verify card types use `custom:` prefix (e.g., `custom:anniversary-timeline-card`)

