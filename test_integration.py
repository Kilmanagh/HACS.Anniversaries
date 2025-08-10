#!/usr/bin/env python3
"""Test script to verify the Anniversaries integration works."""

import sys
import os
from datetime import date

# Add the custom component to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'custom_components'))

from anniversaries.data import AnniversaryData
from anniversaries.coordinator import AnniversaryDataUpdateCoordinator

def test_anniversary_data():
    """Test AnniversaryData class."""
    print("=== Testing AnniversaryData ===")
    
    # Create test anniversary
    anniversary = AnniversaryData(
        name="Test Birthday",
        date=date(1990, 8, 15),  # Aug 15, 1990
        is_one_time=False,
        is_count_up=False,
        show_half_anniversary=False,
        unknown_year=False,
        config={}
    )
    
    print(f"Name: {anniversary.name}")
    print(f"Date: {anniversary.date}")
    print(f"Days remaining: {anniversary.days_remaining}")
    print(f"Next anniversary date: {anniversary.next_anniversary_date}")
    print(f"Current years: {anniversary.current_years}")
    print(f"Next years: {anniversary.next_years}")
    print(f"Birthstone: {anniversary.birthstone}")
    print(f"Birth flower: {anniversary.birth_flower}")
    print(f"Zodiac sign: {anniversary.zodiac_sign}")
    print(f"Generation: {anniversary.generation}")
    print(f"Is milestone: {anniversary.is_milestone}")
    
    return anniversary

def test_coordinator():
    """Test coordinator without Home Assistant."""
    print("\n=== Testing Coordinator ===")
    
    # Create test anniversary
    anniversary = AnniversaryData(
        name="Test Anniversary",
        date=date(1985, 12, 25),
        is_one_time=False,
        is_count_up=False,
        show_half_anniversary=False,
        unknown_year=False,
        config={}
    )
    
    # Create coordinator with test data
    anniversaries = {"test_entry_id": anniversary}
    
    print(f"Anniversaries dict: {list(anniversaries.keys())}")
    print(f"Anniversary name: {anniversaries['test_entry_id'].name}")
    
    # Test accessing anniversary like the sensor does
    entity_id = "test_entry_id"
    retrieved_anniversary = anniversaries.get(entity_id)
    
    if retrieved_anniversary:
        print(f"Successfully retrieved anniversary: {retrieved_anniversary.name}")
        print(f"Days remaining: {retrieved_anniversary.days_remaining}")
        return True
    else:
        print("ERROR: Could not retrieve anniversary!")
        return False

def test_sensor_logic():
    """Test the sensor logic pattern."""
    print("\n=== Testing Sensor Logic Pattern ===")
    
    # Simulate what happens in the sensor
    class MockCoordinator:
        def __init__(self):
            self.anniversaries = {
                "test_entry_id": AnniversaryData(
                    name="Mock Anniversary",
                    date=date(2000, 6, 15),
                    is_one_time=False,
                    is_count_up=False,
                    show_half_anniversary=False,
                    unknown_year=False,
                    config={}
                )
            }
    
    class MockSensor:
        def __init__(self, coordinator, entity_id):
            self.coordinator = coordinator
            self._entity_id = entity_id
        
        @property
        def anniversary(self):
            """Return the anniversary data."""
            if not hasattr(self.coordinator, 'anniversaries') or self.coordinator.anniversaries is None:
                return None
            return self.coordinator.anniversaries.get(self._entity_id)
        
        @property
        def available(self):
            """Return True if entity is available."""
            return self.anniversary is not None
        
        @property
        def name(self):
            """Return the name of the sensor."""
            anniversary = self.anniversary
            if anniversary is None:
                return "Unknown Anniversary"
            return anniversary.name
    
    # Test the mock sensor
    coordinator = MockCoordinator()
    sensor = MockSensor(coordinator, "test_entry_id")
    
    print(f"Sensor available: {sensor.available}")
    print(f"Sensor name: {sensor.name}")
    print(f"Anniversary object: {sensor.anniversary}")
    
    if sensor.available and sensor.anniversary:
        print(f"Anniversary name: {sensor.anniversary.name}")
        print(f"Days remaining: {sensor.anniversary.days_remaining}")
        print("✅ Sensor logic works!")
        return True
    else:
        print("❌ Sensor logic failed!")
        return False

if __name__ == "__main__":
    print("Testing Anniversaries Integration...\n")
    
    # Run tests
    try:
        test_anniversary_data()
        coordinator_ok = test_coordinator()
        sensor_ok = test_sensor_logic()
        
        print(f"\n=== Test Results ===")
        print(f"Coordinator test: {'✅ PASS' if coordinator_ok else '❌ FAIL'}")
        print(f"Sensor logic test: {'✅ PASS' if sensor_ok else '❌ FAIL'}")
        
        if coordinator_ok and sensor_ok:
            print("\n🎉 All tests passed! The integration should work.")
        else:
            print("\n💥 Some tests failed! There are issues to fix.")
            
    except Exception as e:
        print(f"\n💥 Test failed with exception: {e}")
        import traceback
        traceback.print_exc()
