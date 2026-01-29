"""Coordinator for SwitchBot Meter Time Sync."""
from __future__ import annotations

import asyncio
import logging
import struct
from datetime import datetime, timezone, timedelta
from typing import Any

from bleak import BleakClient, BleakError
from bleak_retry_connector import establish_connection

from homeassistant.components.bluetooth import BluetoothServiceInfoBleak
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .const import (
    COMMAND_HEADER,
    COMMAND_MAGIC_NUMBER,
    NOTIFY_CHARACTERISTIC_UUID,
    SUBCMD_SET_TIME,
    WRITE_CHARACTERISTIC_UUID,
)

_LOGGER = logging.getLogger(__name__)


class SwitchBotMeterCoordinator(DataUpdateCoordinator):
    """Class to manage fetching SwitchBot data."""

    def __init__(
        self,
        hass: HomeAssistant,
        service_info: BluetoothServiceInfoBleak,
        address: str,
    ) -> None:
        """Initialize."""
        super().__init__(
            hass,
            _LOGGER,
            name=f"SwitchBot Meter {address}",
        )
        self._service_info = service_info
        self._address = address
        self._client: BleakClient | None = None

    async def _async_connect(self) -> BleakClient:
        """Connect to the device."""
        if self._client and self._client.is_connected:
            return self._client

        _LOGGER.debug("Connecting to %s", self._address)
        
        try:
            self._client = await establish_connection(
                BleakClient,
                self._service_info.device,
                self._address,
                max_attempts=3,
            )
            _LOGGER.debug("Connected to %s", self._address)
            return self._client
        except (BleakError, asyncio.TimeoutError) as ex:
            _LOGGER.error("Error connecting to %s: %s", self._address, ex)
            raise

    async def _async_disconnect(self) -> None:
        """Disconnect from the device."""
        if self._client and self._client.is_connected:
            await self._client.disconnect()
            _LOGGER.debug("Disconnected from %s", self._address)

    async def async_sync_time(self) -> bool:
        """Sync time to the SwitchBot Meter."""
        try:
            client = await self._async_connect()
            
            # Get an aware datetime object for the local time zone
            local_aware_datetime = datetime.now().astimezone()
            
            # Get the UTC offset as a timedelta object
            offset_timedelta = local_aware_datetime.utcoffset()
            
            # Get current time as Unix timestamp
            now = datetime.now(timezone.utc)
            final = now + offset_timedelta - timedelta(hours=2)
            timestamp = int(final.timestamp())
            
            # Build the command packet
            # Format: 0x57 (magic) + 0x09 (time cmd) + 0x01 (subcmd) + timestamp (4 bytes, big endian)
            command = bytearray([
                COMMAND_MAGIC_NUMBER,
                COMMAND_HEADER,
                SUBCMD_SET_TIME,
            ])
            
            # Add timestamp as 4 bytes in big endian
            command.extend(struct.pack('>Q', timestamp))
            
            _LOGGER.debug(
                "Sending time sync command to %s: %s (timestamp: %d)",
                self._address,
                command.hex(),
                timestamp,
            )
            
            # Subscribe to notifications to receive response
            response_received = asyncio.Event()
            response_data = bytearray()
            
            def notification_handler(sender, data):
                nonlocal response_data
                response_data = bytearray(data)
                response_received.set()
            
            await client.start_notify(NOTIFY_CHARACTERISTIC_UUID, notification_handler)
            
            # Send the command
            await client.write_gatt_char(
                WRITE_CHARACTERISTIC_UUID,
                command,
                response=False,
            )
            
            # Wait for response with timeout
            try:
                await asyncio.wait_for(response_received.wait(), timeout=5.0)
                
                # Check response
                # Expected response: Status byte 0x01 (success), payload 0x00
                if len(response_data) >= 1:
                    status = response_data[0]
                    if status == 0x01:
                        _LOGGER.info("Successfully synced time to %s", self._address)
                        return True
                    else:
                        _LOGGER.warning(
                            "Time sync failed with status 0x%02x for %s",
                            status,
                            self._address,
                        )
                        return False
                else:
                    _LOGGER.warning("Received empty response from %s", self._address)
                    return False
                    
            except asyncio.TimeoutError:
                _LOGGER.warning("Timeout waiting for response from %s", self._address)
                return False
            finally:
                try:
                    await client.stop_notify(NOTIFY_CHARACTERISTIC_UUID)
                except Exception as ex:
                    _LOGGER.debug("Error stopping notifications: %s", ex)
            
        except Exception as ex:
            _LOGGER.error("Error syncing time to %s: %s", self._address, ex)
            return False
        finally:
            # Keep connection open for potential quick re-use
            # It will timeout and disconnect automatically
            pass

    async def async_shutdown(self) -> None:
        """Shutdown the coordinator."""
        await self._async_disconnect()
