"""SwitchBot Meter Time Sync Integration."""
from __future__ import annotations

import logging

from homeassistant.components.bluetooth import (
    BluetoothServiceInfoBleak,
    async_discovered_service_info,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_ADDRESS, Platform
from homeassistant.core import HomeAssistant

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
    
    # Create coordinator with config entry
    coordinator = SwitchBotMeterCoordinator(hass, service_info, address, entry)
    
    # Store coordinator
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = coordinator
    
    # Register options update listener
    entry.async_on_unload(entry.add_update_listener(update_listener))
    
    # Forward entry setup to platforms
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    
    return True


async def update_listener(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Handle options update."""
    # Reload the entry when options change
    await hass.config_entries.async_reload(entry.entry_id)


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)
    
    return unload_ok
