# SwitchBot Meter Time Sync for Home Assistant

A custom Home Assistant integration that allows you to sync the time on your SwitchBot Meter Pro devices over Bluetooth without using the SwitchBot app.

## Problem Solved

The SwitchBot Meter Pro (including the CO2 Monitor variant) has an internal clock that gradually drifts from the correct time. When daylight saving time changes occur, the displayed time becomes even more incorrect. The official solution requires:
1. Installing the SwitchBot mobile app
2. Manually opening the app
3. Connecting to the device via Bluetooth
4. Waiting for automatic sync

This integration eliminates the need for the app by allowing Home Assistant to sync the time directly over Bluetooth.

## Supported Devices

- SwitchBot Meter Pro
- SwitchBot Meter Pro (CO2 Monitor)
- SwitchBot Meter Plus (may work, untested)
- SwitchBot Meter (may work, untested)

## Features

- **Manual Time Sync**: Press a button in Home Assistant to sync time immediately
- **Automatic Time Sync**: Set up automations to sync time on a schedule
- **No Cloud Required**: Works entirely over local Bluetooth
- **No App Required**: No need for the SwitchBot mobile app

## Requirements

- Home Assistant with Bluetooth support
- Python 3.11 or newer
- Bluetooth adapter (built-in or USB dongle)
- SwitchBot Meter device within Bluetooth range

## Installation

### Method 1: Manual Installation

1. Download this repository
2. Copy the `switchbot_meter_time_sync` folder to your Home Assistant `custom_components` directory:
   ```
   /config/custom_components/switchbot_meter_time_sync/
   ```
3. Restart Home Assistant
4. Go to Settings → Devices & Services → Add Integration
5. Search for "SwitchBot Meter Time Sync"
6. Select your device from the list or wait for auto-discovery

### Method 2: HACS Installation (Future)

This integration will be available through HACS once submitted to the default repository.

## Configuration

### Adding the Integration

1. **Via Auto-Discovery (Recommended)**:
   - The integration will automatically discover SwitchBot Meter devices
   - You'll see a notification to configure them
   - Click "Configure" and confirm

2. **Via Manual Setup**:
   - Go to Settings → Devices & Services
   - Click "+ Add Integration"
   - Search for "SwitchBot Meter Time Sync"
   - Select your device from the dropdown

### Getting the Bluetooth MAC Address

If your device doesn't auto-discover:
1. Open the SwitchBot app (if you still have it)
2. Tap on your Meter device
3. Tap the gear icon (Settings)
4. Tap "Device Info"
5. Note the "BLE MAC" address

Alternatively, check your Home Assistant Bluetooth integration logs for discovered devices.

## Usage

### Manual Time Sync

After adding the integration, you'll see a new button entity:
- **Entity**: `button.switchbot_meter_XXXXX_sync_time`
- **Action**: Press the button to sync time immediately

In your dashboard:
1. Add a button card
2. Select the "Sync Time" button entity
3. Press it whenever you want to sync the time

### Automatic Time Sync with Automations

Create an automation to sync time automatically:

#### Example 1: Sync Daily at Midnight

```yaml
automation:
  - alias: "SwitchBot Meter - Daily Time Sync"
    trigger:
      - platform: time
        at: "00:00:00"
    action:
      - service: button.press
        target:
          entity_id: button.switchbot_meter_XXXXX_sync_time
```

#### Example 2: Sync Twice Daily

```yaml
automation:
  - alias: "SwitchBot Meter - Twice Daily Time Sync"
    trigger:
      - platform: time
        at: 
          - "00:00:00"
          - "12:00:00"
    action:
      - service: button.press
        target:
          entity_id: button.switchbot_meter_XXXXX_sync_time
```

#### Example 3: Sync on Daylight Saving Time Changes

```yaml
automation:
  - alias: "SwitchBot Meter - DST Time Sync"
    trigger:
      # Spring forward (second Sunday in March at 2 AM)
      - platform: time
        at: "02:00:00"
      # Fall back (first Sunday in November at 2 AM)  
      - platform: time
        at: "02:00:00"
    condition:
      # Add date conditions for specific DST change dates
      - condition: template
        value_template: >
          {% set now_date = now().date() %}
          {% set year = now().year %}
          {% set march_dst = (year ~ '-03-' ~ (14 - (5 * year / 4 + 1) % 7))|as_datetime.date() %}
          {% set nov_dst = (year ~ '-11-' ~ (7 - (5 * year / 4 + 1) % 7))|as_datetime.date() %}
          {{ now_date == march_dst or now_date == nov_dst }}
    action:
      - service: button.press
        target:
          entity_id: button.switchbot_meter_XXXXX_sync_time
```

#### Example 4: Sync When Home Assistant Starts

```yaml
automation:
  - alias: "SwitchBot Meter - Sync on HA Start"
    trigger:
      - platform: homeassistant
        event: start
    action:
      - delay: "00:01:00"  # Wait for Bluetooth to initialize
      - service: button.press
        target:
          entity_id: button.switchbot_meter_XXXXX_sync_time
```

## How It Works

This integration uses the SwitchBot BLE (Bluetooth Low Energy) protocol to communicate directly with the device:

1. **Connection**: Establishes a BLE connection using the device's MAC address
2. **Command Format**: Sends a time sync command following SwitchBot's protocol:
   - Magic number: `0x57`
   - Command header: `0x09` (time management)
   - Subcommand: `0x01` (set current time)
   - Payload: Unix timestamp (4 bytes, big endian)
3. **Response**: Waits for device confirmation (status `0x01` = success)
4. **Disconnection**: Cleanly disconnects after sync

### BLE Protocol Details

The integration uses these UUIDs:
- **Service UUID**: `cba20d00-224d-11e6-9fb8-0002a5d5c51b`
- **Write Characteristic**: `cba20002-224d-11e6-9fb8-0002a5d5c51b`
- **Notify Characteristic**: `cba20003-224d-11e6-9fb8-0002a5d5c51b`

## Troubleshooting

### Device Not Discovered

1. **Check Bluetooth**: Ensure your Bluetooth adapter is working in Home Assistant
2. **Range**: Move the device closer to your Bluetooth adapter
3. **Interference**: Check for Bluetooth interference from other devices
4. **Restart**: Restart Home Assistant and the Bluetooth integration

### Time Sync Fails

1. **Connection Issues**: 
   - Device may be too far from Bluetooth adapter
   - Try pressing the button again
   - Check Home Assistant logs for detailed errors

2. **Battery Low**: 
   - Low battery can cause connection issues
   - Replace batteries if needed

3. **Device Busy**:
   - Device may be connected to SwitchBot app
   - Close the app and try again

### Checking Logs

Enable debug logging to troubleshoot:

```yaml
logger:
  default: warning
  logs:
    custom_components.switchbot_meter_time_sync: debug
```

View logs in Settings → System → Logs

## Known Limitations

1. **Bluetooth Range**: Device must be within Bluetooth range (typically 10-30 feet)
2. **One Connection**: Device can only be connected to one client at a time
3. **No Clock Calibration**: This doesn't fix clock drift, only syncs the current time
4. **Battery Impact**: Minimal, but frequent syncing may slightly impact battery life

## FAQ

**Q: Do I still need the SwitchBot app?**  
A: No, once you've initially set up the device, you can remove the app entirely.

**Q: Will this work with SwitchBot Hub?**  
A: This integration works over Bluetooth only, not through the Hub. However, you can use both simultaneously.

**Q: How often should I sync?**  
A: Once daily is typically sufficient. Twice daily if you need precise timing.

**Q: Does this affect the main SwitchBot integration?**  
A: No, this is completely separate and can coexist with the official integration.

**Q: Can I sync multiple devices?**  
A: Yes, add each device separately through the integration.

## Technical References

- [SwitchBot BLE API Documentation](https://github.com/OpenWonderLabs/SwitchBotAPI-BLE)
- [Home Assistant Developer Docs](https://developers.home-assistant.io/)
- [Bleak (BLE Library)](https://github.com/hbldh/bleak)

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License.

## Credits

- Protocol information from [OpenWonderLabs/SwitchBotAPI-BLE](https://github.com/OpenWonderLabs/SwitchBotAPI-BLE)
- Inspired by the need for local control without cloud services

## Support

For issues and feature requests, please use the GitHub issue tracker.

## Disclaimer

This is an unofficial integration and is not affiliated with or endorsed by SwitchBot/WonderLabs.
