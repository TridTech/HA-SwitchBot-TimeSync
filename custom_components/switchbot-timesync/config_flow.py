"""Config flow for SwitchBot Meter Time Sync integration."""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.components.bluetooth import (
    BluetoothServiceInfoBleak,
    async_discovered_service_info,
)
from homeassistant.const import CONF_ADDRESS
from homeassistant.data_entry_flow import FlowResult

from .const import DOMAIN, DEVICE_TYPE_METER, DEVICE_TYPE_METER_PRO, DEVICE_TYPE_METER_PRO_CO2

_LOGGER = logging.getLogger(__name__)


class SwitchBotMeterTimeSyncConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for SwitchBot Meter Time Sync."""

    VERSION = 1

    def __init__(self) -> None:
        """Initialize the config flow."""
        self._discovery_info: BluetoothServiceInfoBleak | None = None
        self._discovered_devices: dict[str, BluetoothServiceInfoBleak] = {}

    async def async_step_bluetooth(
        self, discovery_info: BluetoothServiceInfoBleak
    ) -> FlowResult:
        """Handle the bluetooth discovery step."""
        await self.async_set_unique_id(discovery_info.address)
        self._abort_if_unique_id_configured()
        
        self._discovery_info = discovery_info
        
        # Check if this is a supported SwitchBot Meter device
        if not self._is_supported_device(discovery_info):
            return self.async_abort(reason="not_supported")
        
        return await self.async_step_confirm()

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        if user_input is not None:
            address = user_input[CONF_ADDRESS]
            await self.async_set_unique_id(address)
            self._abort_if_unique_id_configured()
            
            return self.async_create_entry(
                title=f"SwitchBot Meter ({address[-5:]})",
                data={CONF_ADDRESS: address},
            )

        # Scan for SwitchBot devices
        current_addresses = self._async_current_ids()
        for discovery_info in async_discovered_service_info(self.hass):
            address = discovery_info.address
            if address in current_addresses or address in self._discovered_devices:
                continue
            
            if self._is_supported_device(discovery_info):
                self._discovered_devices[address] = discovery_info

        if not self._discovered_devices:
            return self.async_abort(reason="no_devices_found")

        data_schema = vol.Schema(
            {
                vol.Required(CONF_ADDRESS): vol.In(
                    {
                        address: f"{info.name or 'SwitchBot Meter'} ({address})"
                        for address, info in self._discovered_devices.items()
                    }
                ),
            }
        )

        return self.async_show_form(step_id="user", data_schema=data_schema)

    async def async_step_confirm(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Confirm the setup."""
        if user_input is not None or not self.show_advanced_options:
            return self.async_create_entry(
                title=self._discovery_info.name or f"SwitchBot Meter ({self._discovery_info.address[-5:]})",
                data={CONF_ADDRESS: self._discovery_info.address},
            )

        return self.async_show_form(
            step_id="confirm",
            description_placeholders={
                "name": self._discovery_info.name or "SwitchBot Meter",
            },
        )

    def _is_supported_device(self, discovery_info: BluetoothServiceInfoBleak) -> bool:
        """Check if the device is a supported SwitchBot Meter."""
        # Check local name
        if discovery_info.name and "WoSensorTH" in discovery_info.name:
            return True
        
        # Check manufacturer data for device type
        service_data = discovery_info.service_data
        for uuid_str, data in service_data.items():
            if len(data) > 0:
                device_type = data[0] & 0x7F  # Lower 7 bits
                if device_type in (DEVICE_TYPE_METER, DEVICE_TYPE_METER_PRO, DEVICE_TYPE_METER_PRO_CO2):
                    return True
        
        return False
