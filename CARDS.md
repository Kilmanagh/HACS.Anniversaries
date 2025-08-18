# Anniversary Custom Cards

This integration includes 4 custom Lovelace cards that provide rich visuals and emoji support for displaying anniversary information.

## Manual Installation Required

After installing the Anniversaries integration, you need to manually register the cards:

1. Go to **Settings** → **Dashboards** → **Resources**
2. Click **+ ADD RESOURCE**
3. Add each card with these URLs:
   - `/local/community/anniversaries/anniversary-timeline-card.js`
   - `/local/community/anniversaries/anniversary-details-card.js`
   - `/local/community/anniversaries/anniversary-calendar-card.js`
   - `/local/community/anniversaries/anniversary-stats-card.js`
4. Set Resource type to **JavaScript Module**
5. Restart Home Assistant

After adding the resources and restarting, the cards will appear in your Lovelace card picker.

**Note**: The `/local/community/anniversaries/` path is automatically registered by the integration and points to the `www/` folder inside the integration directory.

**Alternative URLs to try if the above don't work:**
- `/local/custom_components/anniversaries/www/[card-name].js`
- `/hacsfiles/anniversaries/[card-name].js` (if installed via HACS)

## Card Types

### 1. Anniversary Timeline Card (`anniversary-timeline-card`)
Shows upcoming anniversaries in chronological order with powerful filtering and customization options.

**✨ Key Features:**
- **Category filtering**: Show only specific anniversary types (birthdays, work anniversaries, etc.)
- **Multi-category support**: Display multiple anniversary types in one timeline
- **Category statistics**: Overview with counts, today's events, and milestones
- **Category grouping**: Organize under headers with visual separation
- **Flexible date formatting**: Multiple format styles with locale support
- **Rich attributes**: Smart attribute display based on anniversary category
- **Visual enhancements**: Category badges, theme-aware colors, and icons

**🎯 Important: Configure Anniversary Categories First!**

Before using category filtering, make sure your anniversaries have the correct categories set:

1. Go to **Settings** → **Devices & Services** → **Anniversaries**
2. Click on each anniversary entity
3. Set the **Category** field to the appropriate type:
   - `birthday` - Personal birthdays
   - `anniversary` - Wedding anniversaries, relationship milestones  
   - `memorial` - Memorial dates, remembrance days
   - `holiday` - Personal holidays, cultural celebrations
   - `work` - Work anniversaries, career milestones
   - `achievement` - Graduations, accomplishments
   - `event` - General events, appointments
   - `other` - Custom/uncategorized anniversaries
4. Save and restart Home Assistant

**Basic Configuration:**
```yaml
type: custom:anniversary-timeline-card
title: "Upcoming Anniversaries"  # Optional: auto-generated based on category
max_items: 5
show_icons: true
color_coding: true
```

**Category Filtering Options:**
type: custom:anniversary-timeline-card
date_format: "numeric"
show_day_of_week: true

# Clean without day of week: January 1, 2025
type: custom:anniversary-timeline-card
date_format: "long"
show_day_of_week: false

# Custom ISO format: 2025-01-01
type: custom:anniversary-timeline-card
date_format: "custom"
custom_date_format: "YYYY-MM-DD"
show_day_of_week: false

# European format: 01.01.2025
type: custom:anniversary-timeline-card
date_format: "custom"
custom_date_format: "DD.MM.YYYY"

# German locale: Montag, 1. Januar 2025
type: custom:anniversary-timeline-card
```yaml
# Single Category - Show only birthdays
type: custom:anniversary-timeline-card
category: "birthday"
# Auto-title: "🎂 Upcoming Birthdays"
# Auto-attributes: zodiac_sign, birthstone, generation

# Single Category - Show only work anniversaries  
type: custom:anniversary-timeline-card
category: "work"
# Auto-title: "💼 Work Anniversaries"
# Auto-attributes: current_years, named_anniversary, generation

# Multiple Categories - Show birthdays and anniversaries
type: custom:anniversary-timeline-card
categories: ["birthday", "anniversary"]
# Auto-title: "🎂💍 Multiple Anniversary Types"

# All Categories - Show everything (default)
type: custom:anniversary-timeline-card
# Shows all anniversaries regardless of category
```

**Date Formatting Options:**

```yaml
# Long format (default): Monday, January 1, 2025
type: custom:anniversary-timeline-card
date_format: "long"
show_day_of_week: true

# Short format: Monday, Jan 1, 2025
type: custom:anniversary-timeline-card
date_format: "short"
show_day_of_week: true

# Numeric format: Monday, 1/1/2025 (respects locale)
type: custom:anniversary-timeline-card
date_format: "numeric"
show_day_of_week: true

# Full format: Monday, January 1, 2025 (day of week built-in)
type: custom:anniversary-timeline-card
date_format: "full"

# Custom format: 2025-01-01
type: custom:anniversary-timeline-card
date_format: "custom"
custom_date_format: "YYYY-MM-DD"
show_day_of_week: false

# German locale: Montag, 1. Januar 2025
type: custom:anniversary-timeline-card
date_format: "long"
locale: "de-DE"

# Japanese locale: 2025年1月1日月曜日
type: custom:anniversary-timeline-card
date_format: "long"
locale: "ja-JP"
```

**Custom Date Format Patterns:**

| Pattern | Output | Description |
|---------|--------|-------------|
| `YYYY` | 2025 | Full year |
| `YY` | 25 | Short year |
| `MMMM` | January | Full month name |
| `MMM` | Jan | Short month name |
| `MM` | 01 | Month number (padded) |
| `M` | 1 | Month number |
| `DD` | 01 | Day number (padded) |
| `D` | 1 | Day number |
| `dddd` | Monday | Full day name |
| `ddd` | Mon | Short day name |
| `dd` | Mo | Narrow day name |

**Advanced Date Examples:**

```yaml
# Compact: Jan 1 '25
type: custom:anniversary-timeline-card
date_format: "custom"
custom_date_format: "MMM D 'YY"

# Verbose: Monday, the 1st of January, 2025  
type: custom:anniversary-timeline-card
date_format: "custom"
custom_date_format: "dddd, MMMM D, YYYY"

# European style: 01.01.2025
type: custom:anniversary-timeline-card
date_format: "custom"
custom_date_format: "DD.MM.YYYY"

# ISO standard: 2025-01-01
type: custom:anniversary-timeline-card
date_format: "custom"
custom_date_format: "YYYY-MM-DD"
```

**Advanced Timeline Features:**

```yaml
# Multi-Category Timeline with Statistics
type: custom:anniversary-timeline-card
categories: ["birthday", "anniversary", "achievement"]
title: "Personal Celebrations"
show_category_badges: true
show_category_stats: true
max_items: 10

# Category Statistics Dashboard
type: custom:anniversary-timeline-card
show_category_stats: true
show_category_badges: true
category_color_scheme: true
title: "Anniversary Overview"

# Grouped by Category with Headers
type: custom:anniversary-timeline-card
show_category_headers: true
type: custom:anniversary-timeline-card
show_category_headers: true
# Grouped by Category with Headers
type: custom:anniversary-timeline-card
show_category_headers: true
group_by_category: true
show_category_badges: false  # Less cluttered when grouped

# Priority System - Show important categories first
type: custom:anniversary-timeline-card
priority_categories: ["birthday", "anniversary"]
show_category_badges: true
title: "Important Anniversaries First"

# Professional Dashboard
type: custom:anniversary-timeline-card
categories: ["work", "achievement"]
title: "Professional Milestones"
show_category_stats: true
category_color_scheme: true

# Debug Mode - Troubleshoot category filtering
type: custom:anniversary-timeline-card
category: "birthday"
debug_filtering: true
title: "Debug: Should Show Only Birthdays"
```

**All Configuration Options:**

```yaml
type: custom:anniversary-timeline-card

# Basic Options
title: "Custom Title"              # Auto-generated if not specified
max_items: 5                       # Number of anniversaries to show
show_icons: true                   # Show category-specific icons
color_coding: true                 # Color-code by days remaining

# Category Filtering
category: "birthday"               # Single category filter
categories: ["birthday", "work"]   # Multiple category filter
entities: ["sensor.anniversary_*"] # Specific entities (overrides category filters)

# Display Enhancements
show_attributes: ["zodiac_sign", "birthstone"] # Custom attribute list (auto-selected by category if not specified)
show_category_badges: true         # Show category badges next to names
category_color_scheme: true        # Use category-specific color themes
enhanced_attributes: true          # Use rich attribute sets per category

# Advanced Features
show_category_stats: false         # Display category statistics overview
show_category_headers: false       # Show category section headers
group_by_category: false          # Group anniversaries by category
priority_categories: ["birthday"] # Show these categories first
expandable_categories: false      # Collapsible category sections (future feature)
show_category_filter: false       # Interactive category toggles (future feature)

# Date Formatting
date_format: "long"               # "long", "short", "numeric", "full", "custom"
show_day_of_week: true            # Add day of week to date display
custom_date_format: "YYYY-MM-DD" # Custom pattern when date_format is "custom"
locale: "en-US"                   # Force specific locale, null = auto-detect

# Debug
debug_filtering: false            # Show debug info for troubleshooting category filters
```

**Category-Specific Auto-Settings:**

When you specify a category, the card automatically optimizes settings:

| Category | Auto-Title | Auto-Attributes | Color Theme |
|----------|------------|----------------|-------------|
| **birthday** | 🎂 Upcoming Birthdays | zodiac_sign, birthstone, generation | Warm rainbow |
| **anniversary** | 💍 Upcoming Anniversaries | current_years, named_anniversary, zodiac_sign | Romantic pink |
| **memorial** | 🌸 Memorial Dates | current_years, birth_flower, generation | Respectful purple |
| **holiday** | 🎉 Upcoming Holidays | current_years, generation, named_anniversary | Festive orange |
| **work** | 💼 Work Anniversaries | current_years, named_anniversary, generation | Professional blue |
| **achievement** | 🏆 Achievement Anniversaries | current_years, named_anniversary, generation | Success green |
| **event** | 📅 Upcoming Events | current_years, named_anniversary, generation | Neutral gray |
| **other** | 📋 Other Anniversaries | current_years, zodiac_sign, birthstone | Neutral brown |

### 2. Anniversary Details Card (`anniversary-details-card`)
Detailed view of a single anniversary with rich attributes and animations.

**Configuration:**
```yaml
type: custom:anniversary-details-card
entity: sensor.anniversary_birthday_mom
show_attributes: true
show_background: true
show_animation: true
compact_mode: false
```

### 3. Anniversary Calendar Card (`anniversary-calendar-card`)
Mini calendar view highlighting anniversary dates with popup details.

**Configuration:**
```yaml
type: custom:anniversary-calendar-card
title: "Anniversary Calendar"
show_navigation: true
show_details_popup: true
# Optional: specify specific entities
entities:
  - sensor.anniversary_birthday_mom
  - sensor.anniversary_wedding_anniversary
```

### 4. Anniversary Stats Card (`anniversary-stats-card`)
Summary statistics and overview of all anniversaries.

**Configuration:**
```yaml
type: custom:anniversary-stats-card
title: "Anniversary Statistics"
show_next_3: true
show_stats: true
show_charts: true
```

## Features

### Icons & Emojis
- 🎂 Birthdays
- 💍 Weddings/anniversaries  
- 🌟 Milestones
- 💎 Gemstones for birthstones
- ♈♉♊ Zodiac symbols
- 🌸🌹🌻 Birth flowers
- 📅 Calendar/date icons

### Attributes Supported
- Days remaining, weeks remaining
- Next anniversary date, current years, next years
- Zodiac sign, birthstone, birth flower, generation
- Named anniversaries (Silver, Golden, etc.)
- Milestone indicators
- Half anniversary data

### Color Coding
- **Red**: Today (0 days)
- **Orange**: This week (1-7 days)
- **Yellow**: This month (8-30 days)
- **Green**: Future (30+ days)

### Animations
- Pulse animation for today's anniversaries
- Sparkle effect for milestones
- Celebration overlay for special occasions

## Installation & Usage

The cards need to be manually registered in Home Assistant since they're part of a custom integration.

### Step-by-Step Setup:

#### 1. Install/Update the Integration
- Install Anniversaries via HACS or update to the latest version
- Restart Home Assistant

#### 2. Register the Custom Cards
You need to add the card JavaScript files as resources in Home Assistant:

**Method A: Via UI (Recommended)**
1. Go to **Settings** → **Dashboards** 
2. Click the **⋮** menu (three dots) in top right
3. Click **Resources**
4. Click **Add Resource** and add these one by one:

```
/local/custom_components/anniversaries/www/anniversary-timeline-card.js
/local/custom_components/anniversaries/www/anniversary-details-card.js  
/local/custom_components/anniversaries/www/anniversary-calendar-card.js
/local/custom_components/anniversaries/www/anniversary-stats-card.js
```

- Set **Resource type** to **JavaScript module** for each
- Click **Create** for each resource

**Method B: Via YAML Configuration**
Add this to your `configuration.yaml`:

```yaml
lovelace:
  resources:
    - url: /local/custom_components/anniversaries/www/anniversary-timeline-card.js
      type: module
    - url: /local/custom_components/anniversaries/www/anniversary-details-card.js
      type: module
    - url: /local/custom_components/anniversaries/www/anniversary-calendar-card.js
      type: module
    - url: /local/custom_components/anniversaries/www/anniversary-stats-card.js
      type: module
```

#### 3. Clear Browser Cache & Restart
- **Clear browser cache**: Press `Ctrl+Shift+R` (Windows) or `Cmd+Shift+R` (Mac)
- **Restart Home Assistant** to load the new resources

#### 4. Add Cards to Your Dashboard

**Now the cards will be available in the card picker:**

**Method A: Visual Card Picker (Recommended)**
1. Go to your dashboard and click **Edit Dashboard**
2. Click **Add Card**
3. Scroll down to **Custom Cards** section
4. Look for cards starting with "Anniversary":
   - Anniversary Timeline Card
   - Anniversary Details Card  
   - Anniversary Calendar Card
   - Anniversary Stats Card
5. Click on your desired card
6. Configure options in the visual editor
7. Click **Save**

**Method B: YAML Mode**
1. Go to your dashboard and click **Edit Dashboard**
2. Click **Add Card** 
3. Choose **Manual Card** or click the YAML editor icon
4. Paste one of the example configurations below
5. Modify as needed and click **Save**

#### 5. Configure Your Cards
Each card has different configuration options - see the examples below for the full syntax.

### Quick Start Examples

Copy and paste these into the YAML card editor:

**Simple Timeline:**
```yaml
type: custom:anniversary-timeline-card
title: "Next Anniversaries"
max_items: 5
```

**Birthday Details:**
```yaml
type: custom:anniversary-details-card
entity: sensor.anniversary_mom_birthday_123abc
```

**Mini Calendar:**
```yaml
type: custom:anniversary-calendar-card
```

**Statistics Overview:**
```yaml
type: custom:anniversary-stats-card
```

## Example Dashboard Layout

### Troubleshooting

**Cards not showing up in picker:**
- Verify you've **registered the resources** in Settings → Dashboards → Resources
- Check that all 4 JavaScript files are listed with type "JavaScript module"
- Clear browser cache (Ctrl+Shift+R) and restart Home Assistant
- Check browser console (F12) for JavaScript errors

**"Cannot find card" errors:**
- Ensure resource URLs are correct: `/local/custom_components/anniversaries/www/[filename].js`
- Verify files exist by visiting the URL directly in browser
- Make sure integration is installed and running properly

**Cards not working properly:**
- Ensure your anniversary sensors exist and are working
- Check entity names in your card configuration
- Verify the card type names are correct (e.g., `custom:anniversary-timeline-card`)

**Configuration errors:**
- Use the visual card editor when possible - it validates options
- Check YAML syntax if editing manually
- Start with the simple examples above and add options gradually

## Complete Dashboard Example

Here's a full dashboard layout showing all card types:

```yaml
views:
  - title: Anniversaries
    path: anniversaries
    cards:
      # Quick overview at the top
      - type: custom:anniversary-stats-card
        title: "Anniversary Overview"
        show_next_3: true
        show_stats: true
        
      # Timeline of upcoming events
      - type: custom:anniversary-timeline-card
        title: "Coming Up"
        max_items: 5
        show_attributes: 
          - zodiac_sign
          - birthstone
          - generation
        
      # Side-by-side detail cards
      - type: horizontal-stack
        cards:
          - type: custom:anniversary-details-card
            entity: sensor.anniversary_mom_birthday_abc123
            compact_mode: true
          - type: custom:anniversary-details-card  
            entity: sensor.anniversary_wedding_anniversary_def456
            compact_mode: true
            
      # Calendar view
      - type: custom:anniversary-calendar-card
        title: "Anniversary Calendar"
        
      # Full detail card for special anniversary
      - type: custom:anniversary-details-card
        entity: sensor.anniversary_graduation_day_ghi789
        show_background: true
        show_animation: true
```

### Pro Tips

- **Mix and match**: Use timeline + details cards for a complete view
- **Compact mode**: Perfect for horizontal stacks and smaller spaces  
- **Entity filtering**: Specify exact entities in timeline/calendar cards for custom grouping
- **Color coordination**: Cards automatically color-code by urgency across all card types
- **Mobile friendly**: All cards are responsive and work great on phones/tablets
