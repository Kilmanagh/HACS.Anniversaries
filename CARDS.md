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
