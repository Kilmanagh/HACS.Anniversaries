# 🔍 Anniversary Integration Entity Visibility Issue

## 🚨 **Issue Identified:**

**Problem**: Anniversaries with categories other than "other" are disappearing from the integration's entity list in Home Assistant UI, even though they still exist and work in entity lookups.

## 🔧 **Debug Logging Added:**

I've added comprehensive debug logging to help identify the root cause:

### **Added to `sensor.py`:**
- **Entity availability logging**: Shows when entities become unavailable
- **Anniversary data lookup logging**: Shows if anniversary data is found in coordinator
- **Key mismatch detection**: Shows available keys vs requested keys

### **Added to `__init__.py`:**
- **Anniversary loading logging**: Shows each anniversary as it's loaded with category
- **Coordinator creation logging**: Shows all anniversaries in the coordinator
- **Update listener logging**: Shows when anniversaries are updated

## 🔍 **How to Debug:**

1. **Enable debug logging** in Home Assistant:
   ```yaml
   # configuration.yaml
   logger:
     default: info
     logs:
       custom_components.anniversaries: debug
   ```

2. **Restart Home Assistant**

3. **Check the logs** in Settings → System → Logs, look for:
   - `Loaded anniversary: [name] (category: [category]) with key [entry_id]`
   - `Anniversary data not found for key [entry_id]`
   - `Entity [entry_id] is not available - anniversary data is None`

## 🎯 **Most Likely Causes:**

### **Theory 1: Entity Key Mismatch**
The sensor is looking for anniversary data using `entry.entry_id` as the key, but the coordinator might be storing it under a different key.

### **Theory 2: Coordinator State Race Condition**
When anniversaries are updated (especially category changes), there might be a timing issue where:
1. Entity is created with one configuration
2. Configuration is updated (category change)
3. Coordinator is refreshed but entity loses reference to its data

### **Theory 3: Entity Registration Issue**
Home Assistant might be filtering entities based on some property that's affected by the category.

## 🔧 **Potential Fixes to Try:**

### **Fix 1: Force Entity Availability (Quick Test)**
```python
# In sensor.py, change the available property to always return True for testing
@property
def available(self) -> bool:
    """Return if entity is available."""
    return True  # Force availability for debugging
```

### **Fix 2: Add Entity State Fallback**
```python
# In sensor.py, add fallback when anniversary data is missing
@property
def native_value(self) -> int | None:
    """Return the state of the sensor."""
    ann = self.anniversary
    if ann:
        return ann.days_remaining
    else:
        # Fallback: return a default value instead of None
        return 999  # Or some indicator value
```

### **Fix 3: Ensure Entity Registry Consistency**
The issue might be in how entity IDs are being managed when categories change.

## 🚀 **Testing Steps:**

1. **Create a test anniversary** with category "other" - verify it appears in integration UI
2. **Change its category** to "birthday" - check if it disappears
3. **Check logs** for the specific debug messages
4. **Check entity registry** to see if entity still exists but is disabled/hidden

## 📋 **What to Look For in Logs:**

```
# Good case (entity working):
INFO: Loaded anniversary: John's Birthday (category: birthday) with key abc123-def456
DEBUG: Anniversary data found for abc123-def456: John's Birthday, category: birthday

# Bad case (entity missing):
WARNING: Anniversary data not found for key abc123-def456. Available keys: [def789-ghi012, ...]
WARNING: Entity abc123-def456 is not available - anniversary data is None
```

## 🎯 **Next Steps:**

1. **Check the logs** after restart to see the debug output
2. **Try changing a category** from "other" to "birthday" and watch the logs
3. **Report back with the specific log messages** you see

The debug logging will help us pinpoint exactly where the disconnect is happening between the entity and its anniversary data when categories are changed.

## 🔍 **Entity Registry Check:**

You can also check the entity registry in Home Assistant:
- Go to Settings → Devices & Services → Entities
- Search for "anniversary"
- Check if the missing entities are there but disabled/hidden
- Look at their configuration to see if there are any differences
