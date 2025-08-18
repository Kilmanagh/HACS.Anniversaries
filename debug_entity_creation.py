"""
Debug script to check anniversary entity registration and visibility issues
"""

import sys
import os
sys.path.append('/workspaces/HACS.Anniversaries')

from custom_components.anniversaries.data import AnniversaryData
from custom_components.anniversaries.const import *

def test_anniversary_creation():
    """Test creating anniversaries with different categories"""
    
    test_configs = [
        {
            "name": "Test Birthday",
            "date": "1990-05-15",
            "category": "birthday"
        },
        {
            "name": "Test Work Anniversary", 
            "date": "2020-08-01",
            "category": "work"
        },
        {
            "name": "Test Other Anniversary",
            "date": "2021-12-25", 
            "category": "other"
        }
    ]
    
    print("🔍 Testing Anniversary Data Creation:")
    print("=" * 50)
    
    for config in test_configs:
        try:
            anniversary = AnniversaryData.from_config(config)
            print(f"✅ SUCCESS: {anniversary.name}")
            print(f"   Category: {anniversary.category}")
            print(f"   Date: {anniversary.date}")
            print(f"   Days remaining: {anniversary.days_remaining}")
            print(f"   Available: {anniversary is not None}")
            print(f"   Icon: {anniversary.category_default_icon}")
            print()
        except Exception as e:
            print(f"❌ ERROR: {config['name']} - {e}")
            print()

if __name__ == "__main__":
    test_anniversary_creation()
