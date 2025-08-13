# Anniversary Custom Cards

This integration includes 4 custom Lovelace cards for displaying anniversary information with rich visuals and emojis.

## Card Types

### 1. Anniversary Timeline Card (`anniversary-timeline-card`)
Shows upcoming anniversaries in chronological order with color coding and attribute badges.

**Configuration:**
```yaml
type: custom:anniversary-timeline-card
title: "Upcoming Anniversaries"
max_items: 5
show_attributes: 
  - zodiac_sign
  - birthstone
  - generation
  - named_anniversary
show_icons: true
color_coding: true
# Optional: specify specific entities
entities:
  - sensor.anniversary_birthday_mom
  - sensor.anniversary_wedding_anniversary
```

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

## Installation

The cards are automatically available when you install the Anniversaries integration. No additional installation required!

After installing/updating the integration:
1. Clear your browser cache
2. Add cards to your dashboard using the card picker
3. Look for "Anniversary" cards in the custom cards section

## Example Dashboard Layout

```yaml
views:
  - title: Anniversaries
    cards:
      - type: custom:anniversary-timeline-card
        title: "Coming Up"
        max_items: 3
        
      - type: horizontal-stack
        cards:
          - type: custom:anniversary-details-card
            entity: sensor.anniversary_birthday_mom
            compact_mode: true
          - type: custom:anniversary-details-card
            entity: sensor.anniversary_wedding_anniversary
            compact_mode: true
            
      - type: custom:anniversary-calendar-card
        
      - type: custom:anniversary-stats-card
```
