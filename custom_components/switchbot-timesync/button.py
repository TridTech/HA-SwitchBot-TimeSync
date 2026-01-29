"""Support for SwitchBot Meter time sync button."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.button import ButtonEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_ADDRESS
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .coordinator import SwitchBotMeterCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up SwitchBot Meter time sync button."""
    coordinator: SwitchBotMeterCoordinator = hass.data[DOMAIN][entry.entry_id]
    
    async_add_entities([SwitchBotMeterTimeSyncButton(coordinator, entry)])


class SwitchBotMeterTimeSyncButton(ButtonEntity):
    """Representation of a SwitchBot Meter time sync button."""

    _attr_has_entity_name = True
    _attr_name = "Sync Time"
    _attr_icon = "mdi:clock-sync"

    def __init__(
        self,
        coordinator: SwitchBotMeterCoordinator,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the button."""
        self._coordinator = coordinator
        self._address = entry.data[CONF_ADDRESS]
        self._attr_unique_id = f"{entry.entry_id}_time_sync"

    @property
    def device_info(self) -> DeviceInfo:
        """Return device info."""
        return DeviceInfo(
            identifiers={(DOMAIN, self._address)},
            name=f"SwitchBot Meter {self._address[-5:]}",
            manufacturer="SwitchBot",
            model="Meter Pro",
            connections={("bluetooth", self._address)},
        )

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return True

    async def async_press(self) -> None:
        """Handle the button press."""
        _LOGGER.info("Time sync button pressed for %s", self._address)
        success = await self._coordinator.async_sync_time()
        
        if success:
            self.hass.components.persistent_notification.async_create(
                f"Successfully synced time to SwitchBot Meter {self._address[-5:]}",
                title="SwitchBot Time Sync",
            )
        else:
            self.hass.components.persistent_notification.async_create(
                f"Failed to sync time to SwitchBot Meter {self._address[-5:]}. "
                "Please ensure the device is in range and try again.",
                title="SwitchBot Time Sync Error",
            )
