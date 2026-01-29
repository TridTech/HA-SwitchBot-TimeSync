"""Constants for the SwitchBot Meter Time Sync integration."""

DOMAIN = "switchbot_meter_time_sync"

# SwitchBot BLE UUIDs
SERVICE_UUID = "cba20d00-224d-11e6-9fb8-0002a5d5c51b"
WRITE_CHARACTERISTIC_UUID = "cba20002-224d-11e6-9fb8-0002a5d5c51b"
NOTIFY_CHARACTERISTIC_UUID = "cba20003-224d-11e6-9fb8-0002a5d5c51b"

# Command constants
COMMAND_MAGIC_NUMBER = 0x57
COMMAND_HEADER = 0x09  # Time management command
SUBCMD_SET_TIME = 0x01

# Device types in broadcast
DEVICE_TYPE_METER = 0x54  # 'T' - WoSensorTH (Meter/Meter Plus)
DEVICE_TYPE_METER_PRO = 0x77  # 'w' - Meter Pro
DEVICE_TYPE_METER_PRO_CO2 = 0x7A  # 'z' - Meter Pro CO2
