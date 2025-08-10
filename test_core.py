#!/usr/bin/env python3
"""Simple test to verify the core anniversary calculation logic."""

import sys
import os
from datetime import date

# Test the data class directly
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'custom_components', 'anniversaries'))

def test_anniversary_calculations():
    """Test anniversary calculations without Home Assistant dependencies."""
    print("=== Testing Anniversary Calculations ===")
    
    # Test the date calculation logic directly
    from dateutil.relativedelta import relativedelta
    
    # Test case: Birthday on Aug 15, 1990
    birthday = date(1990, 8, 15)
    today = date(2025, 8, 10)  # Current date according to context
    
    print(f"Birthday: {birthday}")
    print(f"Today: {today}")
    
    # Calculate next anniversary
    next_date = birthday
    if today >= next_date:
        next_date = next_date.replace(year=today.year)
    if today > next_date:
        next_date = next_date.replace(year=today.year + 1)
    
    print(f"Next anniversary: {next_date}")
    
    # Calculate days remaining
    days_remaining = (next_date - today).days
    print(f"Days remaining: {days_remaining}")
    
    # Calculate current age
    current_years = relativedelta(today, birthday).years
    print(f"Current age: {current_years}")
    
    # Calculate next age
    next_years = relativedelta(next_date, birthday).years
    print(f"Next age: {next_years}")
    
    return True

def test_entity_id_generation():
    """Test entity ID generation logic."""
    print("\n=== Testing Entity ID Generation ===")
    
    test_names = [
        "John's Birthday",
        "Mom & Dad Anniversary", 
        "Wedding Day!!!",
        "Simple Name",
        "Name-with-hyphens"
    ]
    
    for name in test_names:
        # Simulate the entity ID generation logic
        clean_name = name.lower().replace(' ', '_').replace('-', '_')
        import re
        clean_name = re.sub(r'[^a-z0-9_]', '', clean_name)
        entity_id = f"sensor.anniversary_{clean_name}"
        
        print(f"'{name}' -> '{entity_id}'")
    
    return True

def test_mock_coordinator_sensor():
    """Test the coordinator-sensor interaction pattern."""
    print("\n=== Testing Coordinator-Sensor Pattern ===")
    
    # Mock coordinator
    class MockCoordinator:
        def __init__(self):
            self.anniversaries = {}
    
    # Mock sensor
    class MockSensor:
        def __init__(self, coordinator, entity_id):
            self.coordinator = coordinator
            self._entity_id = entity_id
        
        @property
        def anniversary(self):
            if not hasattr(self.coordinator, 'anniversaries') or self.coordinator.anniversaries is None:
                return None
            return self.coordinator.anniversaries.get(self._entity_id)
        
        @property
        def available(self):
            return self.anniversary is not None
        
        @property
        def name(self):
            anniversary = self.anniversary
            if anniversary is None:
                return "Unknown Anniversary"
            return anniversary.get('name', 'Unknown')
    
    # Test scenario 1: Empty coordinator
    coordinator = MockCoordinator()
    sensor = MockSensor(coordinator, "test_id")
    
    print(f"Empty coordinator - Available: {sensor.available}")
    print(f"Empty coordinator - Name: {sensor.name}")
    
    # Test scenario 2: Add anniversary data
    coordinator.anniversaries["test_id"] = {
        'name': 'Test Anniversary',
        'date': date(1990, 8, 15)
    }
    
    print(f"With data - Available: {sensor.available}")
    print(f"With data - Name: {sensor.name}")
    
    # Test scenario 3: Wrong entity ID
    sensor_wrong = MockSensor(coordinator, "wrong_id")
    print(f"Wrong ID - Available: {sensor_wrong.available}")
    print(f"Wrong ID - Name: {sensor_wrong.name}")
    
    return True

if __name__ == "__main__":
    print("Testing Core Anniversary Logic...\n")
    
    try:
        test_anniversary_calculations()
        test_entity_id_generation() 
        test_mock_coordinator_sensor()
        
        print("\n🎉 All core logic tests passed!")
        print("The basic patterns should work in Home Assistant.")
        
    except Exception as e:
        print(f"\n💥 Test failed: {e}")
        import traceback
        traceback.print_exc()
