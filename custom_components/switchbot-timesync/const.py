"""Constants for the SwitchBot Meter Time Sync integration."""

DOMAIN = "switchbot_meter_time_sync"

# SwitchBot BLE UUIDs
SERVICE_UUID = "cba20d00-224d-11e6-9fb8-0002a5d5c51b"
WRITE_CHARACTERISTIC_UUID = "cba20002-224d-11e6-9fb8-0002a5d5c51b"
NOTIFY_CHARACTERISTIC_UUID = "cba20003-224d-11e6-9fb8-0002a5d5c51b"

# Service data UUID (short form: 0xfd3d, long form below)
SERVICE_DATA_UUID = "0000fd3d-0000-1000-8000-00805f9b34fb"

# Manufacturer ID for SwitchBot
MANUFACTURER_ID = 2409  # 0x0969

# Command constants
COMMAND_MAGIC_NUMBER = 0x57
COMMAND_HEADER = 0x09  # Time management command
SUBCMD_SET_TIME = 0x01

# Device types in broadcast (from service data byte 0, lower 7 bits)
DEVICE_TYPE_METER = 0x54  # 'T' - WoSensorTH (Meter/Meter Plus) Normal Mode
DEVICE_TYPE_METER_ADD = 0x74  # 't' - WoSensorTH Add Mode  
DEVICE_TYPE_METER_PRO = 0x77  # 'w' - Meter Pro (W3400010)
DEVICE_TYPE_METER_PRO_CO2 = 0x7A  # 'z' - Meter Pro CO2
