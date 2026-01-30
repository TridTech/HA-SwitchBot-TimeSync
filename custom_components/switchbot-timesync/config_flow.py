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
from homeassistant.core import callback

from .const import (
    DOMAIN,
    DEVICE_TYPE_METER,
    DEVICE_TYPE_METER_ADD,
    DEVICE_TYPE_METER_PRO,
    DEVICE_TYPE_METER_PRO_CO2,
    MANUFACTURER_ID,
    SERVICE_DATA_UUID,
    CONF_TIME_OFFSET,
    DEFAULT_TIME_OFFSET_HOURS,
)

_LOGGER = logging.getLogger(__name__)


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for SwitchBot Meter Time Sync."""

    VERSION = 1

    def __init__(self) -> None:
        """Initialize the config flow."""
        self._discovery_info: BluetoothServiceInfoBleak | None = None
        self._discovered_devices: dict[str, BluetoothServiceInfoBleak] = {}

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> OptionsFlowHandler:
        """Get the options flow for this handler."""
        return OptionsFlowHandler(config_entry)

    async def async_step_bluetooth(
        self, discovery_info: BluetoothServiceInfoBleak
    ) -> FlowResult:
        """Handle the bluetooth discovery step."""
        _LOGGER.debug("Bluetooth discovery triggered for device: %s", discovery_info.address)
        _LOGGER.debug("Discovery info: name=%s, rssi=%s", discovery_info.name, discovery_info.rssi)
        _LOGGER.debug("Service data: %s", discovery_info.service_data)
        _LOGGER.debug("Manufacturer data: %s", discovery_info.manufacturer_data)
        
        await self.async_set_unique_id(discovery_info.address)
        self._abort_if_unique_id_configured()
        
        self._discovery_info = discovery_info
        
        # Check if this is a supported SwitchBot Meter device
        if not self._is_supported_device(discovery_info):
            _LOGGER.debug("Device %s is not a supported SwitchBot Meter", discovery_info.address)
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
            
            # Get device info for title
            device_info = self._discovered_devices.get(address)
            if device_info:
                title = self._get_device_title(device_info)
            else:
                title = f"SwitchBot Meter ({address[-5:]})"
            
            return self.async_create_entry(
                title=title,
                data={CONF_ADDRESS: address},
            )

        # Scan for SwitchBot devices
        current_addresses = self._async_current_ids()
        discovered_count = 0
        
        for discovery_info in async_discovered_service_info(self.hass):
            address = discovery_info.address
            if address in current_addresses or address in self._discovered_devices:
                continue
            
            _LOGGER.debug("Checking device %s: %s", address, discovery_info.name)
            
            if self._is_supported_device(discovery_info):
                self._discovered_devices[address] = discovery_info
                discovered_count += 1
                _LOGGER.info("Found SwitchBot Meter: %s (%s)", address, discovery_info.name)

        _LOGGER.debug("Found %d SwitchBot Meter devices", discovered_count)

        if not self._discovered_devices:
            return self.async_abort(reason="no_devices_found")

        data_schema = vol.Schema(
            {
                vol.Required(CONF_ADDRESS): vol.In(
                    {
                        address: self._get_device_display_name(info)
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
            title = self._get_device_title(self._discovery_info)
            return self.async_create_entry(
                title=title,
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
        # Method 1: Check local name
        if discovery_info.name:
            name_lower = discovery_info.name.lower()
            if "wosensorth" in name_lower or "woiosensorth" in name_lower:
                _LOGGER.debug("Device identified by name: %s", discovery_info.name)
                return True
        
        # Method 2: Check service data for device type
        for uuid_str, data in discovery_info.service_data.items():
            # Check for the short UUID (fd3d) or full UUID
            if "fd3d" in uuid_str.lower() or SERVICE_DATA_UUID.lower() in uuid_str.lower():
                if len(data) > 0:
                    device_type = data[0] & 0x7F  # Lower 7 bits
                    _LOGGER.debug("Service data UUID %s, device type: 0x%02x", uuid_str, device_type)
                    if device_type in (
                        DEVICE_TYPE_METER,
                        DEVICE_TYPE_METER_ADD,
                        DEVICE_TYPE_METER_PRO,
                        DEVICE_TYPE_METER_PRO_CO2,
                    ):
                        _LOGGER.debug("Device identified by service data type: 0x%02x", device_type)
                        return True
        
        # Method 3: Check manufacturer data
        for mfr_id, data in discovery_info.manufacturer_data.items():
            if mfr_id == MANUFACTURER_ID and len(data) >= 12:
                # SwitchBot Meter devices have specific manufacturer data patterns
                _LOGGER.debug("Device has SwitchBot manufacturer ID: %d", mfr_id)
                # This could be a Meter device, accept it
                return True
        
        return False

    def _get_device_type_name(self, discovery_info: BluetoothServiceInfoBleak) -> str:
        """Get a friendly device type name."""
        for uuid_str, data in discovery_info.service_data.items():
            if "fd3d" in uuid_str.lower() and len(data) > 0:
                device_type = data[0] & 0x7F
                if device_type in (DEVICE_TYPE_METER, DEVICE_TYPE_METER_ADD):
                    return "Meter/Meter Plus"
                elif device_type == DEVICE_TYPE_METER_PRO:
                    return "Meter Pro"
                elif device_type == DEVICE_TYPE_METER_PRO_CO2:
                    return "Meter Pro CO2"
        
        return "Meter"

    def _get_device_display_name(self, discovery_info: BluetoothServiceInfoBleak) -> str:
        """Get display name for device selection."""
        device_type = self._get_device_type_name(discovery_info)
        name = discovery_info.name or device_type
        address_short = discovery_info.address[-8:].replace(":", "")
        return f"{name} ({address_short})"

    def _get_device_title(self, discovery_info: BluetoothServiceInfoBleak) -> str:
        """Get title for the config entry."""
        device_type = self._get_device_type_name(discovery_info)
        address_short = discovery_info.address[-8:].replace(":", "")
        return f"SwitchBot {device_type} ({address_short})"


class OptionsFlowHandler(config_entries.OptionsFlow):
    """Handle options flow for SwitchBot Meter Time Sync."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Optional(
                        CONF_TIME_OFFSET,
                        default=self.config_entry.options.get(
                            CONF_TIME_OFFSET, DEFAULT_TIME_OFFSET_HOURS
                        ),
                    ): vol.All(vol.Coerce(int), vol.Range(min=-12, max=12)),
                }
            ),
        )
