import pytest
import sys, os
sys.path.insert(0, os.path.abspath('.'))
from datetime import date
from types import SimpleNamespace

# Lightweight mocks to avoid pulling full HA core. We monkeypatch only members
# actually accessed by our classes.

class MockHass(SimpleNamespace):
    def __init__(self):
        super().__init__(data={})

class DummyEntityRegistry:
    def __init__(self):
        self.updated = []
    def async_update_entity(self, old_id, new_entity_id=None, **_):
        self.updated.append((old_id, new_entity_id))

def fake_async_get(hass):  # noqa: D401
    return hass._entity_registry

# Patch points inside modules under test
import custom_components.anniversaries.sensor as sensor_mod
import custom_components.anniversaries.calendar as calendar_mod
from custom_components.anniversaries.data import AnniversaryData

class DummyCoordinator(SimpleNamespace):
    def __init__(self):
        super().__init__(anniversaries={})

class DummyConfigEntry(SimpleNamespace):
    def __init__(self, entry_id: str, data: dict):
        super().__init__(entry_id=entry_id, data=data, options={}, title=data.get('name'))
    def add_update_listener(self, *_, **__):
        return lambda: None

@pytest.mark.asyncio
async def test_prefix_enforcement():
    hass = MockHass()
    hass._entity_registry = DummyEntityRegistry()
    # monkeypatch entity_registry accessor
    sensor_mod.er.async_get = fake_async_get  # type: ignore[attr-defined]
    calendar_mod.er.async_get = fake_async_get  # type: ignore[attr-defined]

    coordinator = DummyCoordinator()
    entry_id = '1234-abcd'
    ann = AnniversaryData(name='Michaels Birthday', date=date(1990,5,1))
    coordinator.anniversaries[entry_id] = ann
    entry = DummyConfigEntry(entry_id, {'name': 'Michaels Birthday'})

    sensor = sensor_mod.AnniversarySensor(coordinator, entry_id, entry)
    sensor.hass = hass
    sensor.entity_id = 'sensor.michaels_birthday'
    await sensor.async_added_to_hass()
    assert sensor.entity_id.startswith('sensor.anniversary_')
    assert any('sensor.michaels_birthday' in old for old, _ in hass._entity_registry.updated)

    cal = calendar_mod.AnniversaryCalendar(coordinator, entry_id, entry)
    cal.hass = hass
    cal.entity_id = 'calendar.michaels_birthday'
    await cal.async_added_to_hass()
    assert cal.entity_id.startswith('calendar.anniversary_')

@pytest.mark.asyncio
async def test_upcoming_sensor_prefix():
    hass = MockHass()
    hass._entity_registry = DummyEntityRegistry()
    sensor_mod.er.async_get = fake_async_get  # type: ignore[attr-defined]
    up = sensor_mod.UpcomingAnniversariesSensor(DummyCoordinator())
    up.hass = hass
    up.entity_id = 'sensor.upcoming_anniversaries'
    await up.async_added_to_hass()
    assert up.entity_id.startswith('sensor.anniversary_')
