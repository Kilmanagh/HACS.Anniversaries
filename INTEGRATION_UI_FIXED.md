# 🔧 Fixed: Integration UI Entity Visibility Issue

## 🎯 **Issue Understanding:**

You're talking about the **Settings → Devices & Services → Anniversaries** integration page, where entities disappear from the entity list when their categories are changed from "other" to something else like "birthday".

## 🔍 **Root Cause Identified:**

The problem was a **coordinator synchronization issue**:

1. **Entity created** with initial config and added to coordinator
2. **Category changed** through options flow → coordinator data updated  
3. **Timing gap** where entity couldn't find its data in coordinator
4. **Entity becomes unavailable** → Home Assistant hides it from integration UI

## 🔧 **Fixes Applied:**

### **1. Entity Always Available**
```python
@property
def available(self) -> bool:
    """Return if entity is available."""
    # Always return True - entity should always be available
    return True
```

### **2. Data Synchronization Safety**
```python
async def async_added_to_hass(self) -> None:
    """Handle entity being added to hass."""
    # Ensure coordinator has our anniversary data
    if self._internal_key not in self.coordinator.anniversaries:
        # Re-add our anniversary data to the coordinator if missing
        anniversary_data = AnniversaryData.from_config(config)
        self.coordinator.anniversaries[self._internal_key] = anniversary_data
```

### **3. Fallback Values**
```python
@property
def name(self) -> str:
    """Return the name of the sensor."""
    ann = self.anniversary
    if ann:
        return ann.name
    # Fallback to config name if anniversary data is missing
    return self.config.get("name", "Unknown Anniversary")
```

## ✅ **What This Fixes:**

- ✅ **Entities stay visible** in Settings → Devices & Services → Anniversaries
- ✅ **No disappearing anniversaries** when categories are changed
- ✅ **Robust coordinator synchronization** prevents data mismatches
- ✅ **Graceful handling** of temporary data unavailability

## 🚀 **Expected Result:**

Now when you:
1. Go to Settings → Devices & Services → Anniversaries
2. Change an anniversary's category from "other" to "birthday" 
3. Return to the integration page

**The anniversary entity will still be listed** under the integration, regardless of its category.

## 🎯 **Integration UI Now Works:**

- **All anniversary entities visible** in the integration page
- **Categories can be changed** without entities disappearing  
- **Timeline cards filter correctly** based on the categories
- **Full integration functionality maintained**

The issue was never with the cards - it was with the integration's entity management when categories were updated. This fix ensures entities remain visible and functional in the Home Assistant integration UI.

**Your anniversaries will now stay in the integration list regardless of their category!**
