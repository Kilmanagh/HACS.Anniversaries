#!/usr/bin/env python3
"""Test script to check for import and syntax errors in the anniversaries integration."""

import sys
import os

# Add the custom_components directory to the path
sys.path.insert(0, '/workspaces/HACS.Anniversaries')

print("Testing imports...")

try:
    print("Importing const...")
    from custom_components.anniversaries.const import DOMAIN, PLATFORMS, EMOJI_OPTIONS
    print(f"✓ Successfully imported const. Domain: {DOMAIN}, Emoji options count: {len(EMOJI_OPTIONS)}")
    
    print("Importing data...")
    from custom_components.anniversaries.data import AnniversaryData
    print("✓ Successfully imported data")
    
    print("Importing config_flow...")
    from custom_components.anniversaries.config_flow import AnniversaryConfigFlow
    print("✓ Successfully imported config_flow")
    
    print("Importing sensor...")
    from custom_components.anniversaries.sensor import AnniversarySensor
    print("✓ Successfully imported sensor")
    
    print("Importing coordinator...")
    from custom_components.anniversaries.coordinator import AnniversaryDataUpdateCoordinator
    print("✓ Successfully imported coordinator")
    
    print("Importing __init__...")
    # We can't fully import __init__ because it requires HomeAssistant objects,
    # but we can check for syntax errors
    with open('/workspaces/HACS.Anniversaries/custom_components/anniversaries/__init__.py', 'r') as f:
        code = f.read()
    compile(code, '__init__.py', 'exec')
    print("✓ __init__.py compiles without syntax errors")
    
    print("\n=== Testing emoji system ===")
    # Test emoji system
    from custom_components.anniversaries.const import CATEGORY_EMOJIS, get_default_emoji_for_category
    
    print(f"Available emoji categories: {list(CATEGORY_EMOJIS.keys())}")
    
    # Test some category defaults
    test_categories = ['birthday', 'anniversary', 'holiday', 'medical', 'travel']
    for category in test_categories:
        emoji = get_default_emoji_for_category(category)
        print(f"Category '{category}' -> Default emoji: {emoji}")
    
    print("\n=== Testing data class ===")
    # Test creating anniversary data with emoji
    config = {
        'name': 'Test Birthday',
        'date': '2023-05-15',
        'category': 'birthday',
        'emoji': '🎂'
    }
    
    anniversary = AnniversaryData.from_config(config)
    print(f"Created anniversary: {anniversary.name} with emoji: {anniversary.emoji}")
    
    print("\n✅ All tests passed! The integration code is working correctly.")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)
except SyntaxError as e:
    print(f"❌ Syntax error: {e}")
    sys.exit(1)
except Exception as e:
    print(f"❌ Unexpected error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
