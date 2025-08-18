# 📋 Anniversary Timeline Card - Quick Reference

## ✅ **CARDS.md Updated - No More "Phase" Confusion!**

### **🎯 Key Improvements Made:**

1. **Removed confusing "Phase 1/2/3" terminology**
2. **Added clear "Configure Anniversary Categories First!" section**
3. **Organized examples by use case instead of development phases**
4. **Added comprehensive configuration reference table**
5. **Highlighted the main issue: Anniversary categories must be set in integration, not card**

### **📝 Clear Instructions Now Provided:**

#### **Step 1: Configure Anniversary Categories** ⚠️ **IMPORTANT FIRST STEP**
```
Settings → Devices & Services → Anniversaries → Edit Anniversary → Set Category
```

#### **Step 2: Use Category Filtering in Card**
```yaml
# Show only birthdays
type: custom:anniversary-timeline-card
category: "birthday"

# Show multiple categories  
type: custom:anniversary-timeline-card
categories: ["birthday", "work"]

# Show everything (no filter)
type: custom:anniversary-timeline-card
```

### **🔧 Complete Configuration Reference:**

```yaml
type: custom:anniversary-timeline-card

# Basic Options
title: "Custom Title"              # Auto-generated if not specified
max_items: 5                       # Number of anniversaries to show
show_icons: true                   # Show category-specific icons
color_coding: true                 # Color-code by days remaining

# Category Filtering (MAIN FEATURE)
category: "birthday"               # Single category filter
categories: ["birthday", "work"]   # Multiple category filter

# Display Enhancements
show_category_badges: true         # Show category badges next to names
category_color_scheme: true        # Use category-specific color themes
show_category_stats: false         # Display category statistics overview
show_category_headers: false       # Show category section headers
group_by_category: false          # Group anniversaries by category
priority_categories: ["birthday"] # Show these categories first

# Date Formatting (v1.3.1 Enhancement)
date_format: "long"               # "long", "short", "numeric", "full", "custom"
show_day_of_week: true            # Add day of week to date display
custom_date_format: "YYYY-MM-DD" # Custom pattern when date_format is "custom"
locale: "en-US"                   # Force specific locale, null = auto-detect

# Debug & Troubleshooting
debug_filtering: false            # Show debug info for troubleshooting
```

### **🎨 Auto-Optimized Settings by Category:**

| Category | Auto-Title | Auto-Attributes | Color Theme |
|----------|------------|----------------|-------------|
| **birthday** | 🎂 Upcoming Birthdays | zodiac_sign, birthstone, generation | Warm rainbow |
| **work** | 💼 Work Anniversaries | current_years, named_anniversary, generation | Professional blue |
| **anniversary** | 💍 Upcoming Anniversaries | current_years, named_anniversary, zodiac_sign | Romantic pink |
| **memorial** | 🌸 Memorial Dates | current_years, birth_flower, generation | Respectful purple |

### **🚀 Popular Use Cases:**

```yaml
# Birthday Card (Most Common)
type: custom:anniversary-timeline-card
category: "birthday"

# Work Dashboard
type: custom:anniversary-timeline-card
category: "work"
show_category_stats: true

# All Anniversaries Overview
type: custom:anniversary-timeline-card
show_category_stats: true
show_category_badges: true

# Multi-Category Personal Dashboard
type: custom:anniversary-timeline-card
categories: ["birthday", "anniversary"]
show_category_headers: true
```

### **🔍 Troubleshooting Category Filtering:**

If your card shows all anniversaries instead of just the filtered category:

1. **Add debug mode** to your card:
   ```yaml
   type: custom:anniversary-timeline-card
   category: "birthday"
   debug_filtering: true
   ```

2. **Check the yellow debug box** - it will show the actual categories of your anniversaries

3. **Fix anniversary categories** in Settings → Devices & Services → Anniversaries

4. **Most common issue**: Anniversaries have `category: "other"` instead of `category: "birthday"`

## ✅ **Documentation Complete!**

The CARDS.md file now provides clear, actionable instructions without confusing "Phase" terminology. Users can easily understand:

- ✅ **How to configure anniversary categories first** (the key step!)
- ✅ **How to use category filtering in cards**
- ✅ **All available configuration options**
- ✅ **How to troubleshoot filtering issues**
- ✅ **Popular use cases and examples**

**The timeline card filtering works perfectly - the issue was just unclear documentation about needing to set anniversary categories in the integration first!**
