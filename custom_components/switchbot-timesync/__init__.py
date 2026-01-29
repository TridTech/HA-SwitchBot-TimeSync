"""SwitchBot Meter Time Sync Integration."""
from __future__ import annotations

import logging
from datetime import timedelta

from homeassistant.components.bluetooth import (
    BluetoothServiceInfoBleak,
    async_discovered_service_info,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_ADDRESS, Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .const import DOMAIN
from .coordinator import SwitchBotMeterCoordinator

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [Platform.BUTTON]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up SwitchBot Meter Time Sync from a config entry."""
    address = entry.data[CONF_ADDRESS]
    
    # Get the Bluetooth service info
    service_info = None
    for info in async_discovered_service_info(hass):
        if info.address.upper() == address.upper():
            service_info = info
            break
    
    if not service_info:
        _LOGGER.error("Could not find SwitchBot device with address %s", address)
        return False
    
    # Create coordinator
    coordinator = SwitchBotMeterCoordinator(hass, service_info, address)
    
    # Store coordinator
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = coordinator
    
    # Forward entry setup to platforms
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)
    
    return unload_ok
