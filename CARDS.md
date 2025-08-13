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

## Installation & Usage

The cards are automatically available when you install the Anniversaries integration. No additional installation required!

### Step-by-Step Usage:

#### 1. Install/Update the Integration
- Install Anniversaries via HACS or update to the latest version
- Restart Home Assistant

#### 2. Clear Browser Cache
- **Chrome/Edge**: Press `Ctrl+Shift+R` (Windows) or `Cmd+Shift+R` (Mac)
- **Firefox**: Press `Ctrl+F5` or `Cmd+Shift+R`
- **Safari**: Press `Cmd+Option+R`

#### 3. Add Cards to Your Dashboard

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

#### 4. Configure Your Cards
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
- Verify you've cleared browser cache
- Check browser console (F12) for JavaScript errors
- Make sure integration is updated to latest version
- Try refreshing the page (`F5`)

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
