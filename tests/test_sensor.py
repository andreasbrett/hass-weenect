"""Tests for the sensor platform."""

import pytest
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.weenect.const import ATTRIBUTION, DOMAIN
from tests.const import MOCK_CONFIG


@pytest.mark.usefixtures("get_trackers")
async def test_sensor(hass):
    """Test that sensor works."""
    config_entry = MockConfigEntry(domain=DOMAIN, data=MOCK_CONFIG, entry_id="test")
    config_entry.add_to_hass(hass)

    await hass.config_entries.async_setup(config_entry.entry_id)

    await hass.async_block_till_done()

    assert (
        hass.states.get("sensor.test_sensor_mode").attributes["attribution"]
        == ATTRIBUTION
    )
    assert hass.states.get("sensor.test_sensor_mode").attributes["id"] == 100000
    assert (
        hass.states.get("sensor.test_sensor_mode").attributes["sim"]
        == "8849390213023093728"
    )
    assert (
        hass.states.get("sensor.test_sensor_mode").attributes["imei"]
        == "160389554842512"
    )

    assert hass.states.get("sensor.test_last_update_rate").state == "10M"
    assert hass.states.get("sensor.test_sensor_mode").state == "normal"
    assert hass.states.get("sensor.test_last_sensor_mode").state == "normal"
    assert hass.states.get("sensor.test_battery").state == "95"
    assert hass.states.get("sensor.test_cell_tower_id").state == "26233-B7AD-E77B"
    assert hass.states.get("sensor.test_gsm_strength").state == "17"
    assert (
        hass.states.get("sensor.test_last_message_received").state
        == "2021-04-15T08:29:28+00:00"
    )
    assert hass.states.get("sensor.test_gps_satellites").state == "0"


@pytest.mark.usefixtures("get_trackers")
async def test_device_class_does_not_return_string_for_its_state(hass, caplog):
    """Test that sensor works."""
    config_entry = MockConfigEntry(domain=DOMAIN, data=MOCK_CONFIG, entry_id="test")
    config_entry.add_to_hass(hass)

    await hass.config_entries.async_setup(config_entry.entry_id)

    await hass.async_block_till_done()

    assert (
        "is providing a string for its state, while the device class is"
        not in caplog.text
    )


@pytest.mark.usefixtures("get_trackers_last_message_none")
async def test_sensor_with_last_message_none(hass):
    """Test that the special timestamp sensor works for a None value ."""
    config_entry = MockConfigEntry(domain=DOMAIN, data=MOCK_CONFIG, entry_id="test")
    config_entry.add_to_hass(hass)

    await hass.config_entries.async_setup(config_entry.entry_id)

    await hass.async_block_till_done()

    assert hass.states.get("sensor.test_last_message_received").state == "unknown"
