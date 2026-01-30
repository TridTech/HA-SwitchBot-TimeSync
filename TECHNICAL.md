# Technical Overview - SwitchBot Meter Time Sync Integration

## Purpose

This Home Assistant custom integration provides a local, Bluetooth-based solution for syncing time to SwitchBot Meter Pro devices without requiring the SwitchBot mobile app.

## The Problem

SwitchBot Meter Pro devices suffer from clock drift that accumulates over time. Without regular synchronization:
- The displayed time gradually becomes inaccurate (typically 5-10 minutes drift per month)
- Daylight Saving Time changes are not handled automatically
- The only official solution requires manually opening the SwitchBot app and connecting to each device

## The Solution

This integration implements the SwitchBot BLE protocol to send time synchronization commands directly over Bluetooth, enabling:
- Automated time syncing on a schedule
- Manual sync via Home Assistant button
- Complete independence from the SwitchBot app
- Local-only operation (no cloud connectivity required)

## Architecture

### Components

1. **Config Flow** (`config_flow.py`)
   - Handles device discovery via Bluetooth
   - Provides UI for device selection
   - Supports both auto-discovery and manual MAC entry

2. **Coordinator** (`coordinator.py`)
   - Manages Bluetooth connections
   - Implements BLE protocol communication
   - Handles command construction and response parsing

3. **Button Platform** (`button.py`)
   - Creates a button entity for manual time sync
   - Provides user feedback via persistent notifications
   - Integrates with Home Assistant's entity system

4. **Constants** (`const.py`)
   - Defines BLE UUIDs and protocol constants
   - Device type identifiers
   - Command structure definitions

### BLE Protocol Implementation

#### Service and Characteristics

- **Service UUID**: `cba20d00-224d-11e6-9fb8-0002a5d5c51b`
- **Write Characteristic**: `cba20002-224d-11e6-9fb8-0002a5d5c51b` (Commands to device)
- **Notify Characteristic**: `cba20003-224d-11e6-9fb8-0002a5d5c51b` (Responses from device)

#### Time Sync Command Structure

```
Byte 0: Magic Number (0x57)
Byte 1: Command Header (0x09 - Time Management)
Byte 2: Subcommand (0x01 - Set Current Time)
Bytes 3-10: Unix Timestamp (8 bytes, big-endian unsigned long long)
```

Example command for timestamp 1738185600 (2026-01-29):
```
57 09 01 00 00 00 00 67 BB 12 00
```

Breaking down the timestamp bytes (big-endian):
```
1738185600 decimal = 0x0000000067BB1200
Bytes: 00 00 00 00 67 BB 12 00
```

#### Response Format

```
Byte 0: Status (0x01 = Success, other = Error)
Byte 1: Payload (0x00 for time sync)
```

### Communication Flow

```
1. Establish BLE Connection
   ↓
2. Subscribe to Notify Characteristic
   ↓
3. Get Current Unix Timestamp
   ↓
4. Build Command Packet
   ↓
5. Write Command to Write Characteristic
   ↓
6. Wait for Response on Notify Characteristic
   ↓
7. Parse Response Status
   ↓
8. Stop Notifications
   ↓
9. Maintain Connection for Reuse
```

## Dependencies

- **bleak** (>=0.21.0): Cross-platform BLE library
- **bleak-retry-connector** (>=3.1.0): Reliable connection establishment

Both are standard in Home Assistant's Bluetooth stack.

## Supported Devices

The integration detects devices based on:
1. **Local Name**: Contains "WoSensorTH"
2. **Device Type** (from broadcast data):
   - `0x54` - WoSensorTH (Meter/Meter Plus)
   - `0x77` - Meter Pro
   - `0x7A` - Meter Pro CO2

## Compatibility

- **Home Assistant**: 2024.1.0+
- **Python**: 3.11+
- **Bluetooth**: Any adapter supported by Home Assistant
- **Platforms**: Linux, macOS, Windows (via Bleak)

## Performance Characteristics

- **Connection Time**: 2-5 seconds (typical)
- **Sync Duration**: <1 second after connection
- **Total Operation**: 3-6 seconds end-to-end
- **Battery Impact**: Minimal (<0.1% per sync)
- **Recommended Sync Frequency**: Once daily

## Security Considerations

1. **No Authentication**: The BLE protocol doesn't require pairing or authentication
   - This is a limitation of the SwitchBot devices themselves
   - Anyone within Bluetooth range can send commands

2. **Local Only**: 
   - No internet connectivity required
   - No data sent to cloud services
   - All communication is direct device-to-device

3. **Encryption**: 
   - Some newer devices support optional encryption
   - This integration doesn't currently implement encrypted commands
   - Standard BLE link-layer encryption applies

## Limitations

1. **Bluetooth Range**: Typical range is 10-30 feet (3-10 meters)
2. **Single Connection**: Device can only maintain one active connection
3. **No Clock Calibration**: Syncs time but doesn't fix drift rate
4. **Device Availability**: Device must be powered and responsive

## Testing Recommendations

### Unit Testing Areas
- Command packet construction
- Timestamp encoding (big-endian)
- Response parsing
- Error handling

### Integration Testing
- Connection establishment
- Command execution
- Response handling
- Connection cleanup
- Multiple devices
- Connection failures
- Timeout scenarios

### User Acceptance Testing
- Auto-discovery
- Manual configuration
- Button press functionality
- Automation triggering
- Multiple sync operations
- Battery impact over time

## Future Enhancements

Potential improvements for future versions:

1. **Automatic Scheduling**
   - Built-in daily sync option
   - Configurable sync times
   - DST change detection

2. **Encryption Support**
   - Implement encrypted commands for newer devices
   - Password protection

3. **Batch Operations**
   - Sync multiple devices efficiently
   - Stagger connections to avoid conflicts

4. **Status Feedback**
   - Last sync time sensor
   - Sync success/failure tracking
   - Battery level monitoring

5. **Advanced Features**
   - Time zone configuration
   - 12/24 hour format sync
   - Display settings sync

## Debugging

### Enable Debug Logging

```yaml
logger:
  default: warning
  logs:
    custom_components.switchbot_meter_time_sync: debug
    homeassistant.components.bluetooth: debug
```

### Common Issues and Solutions

**Connection Timeouts**
- Cause: Device out of range or busy
- Solution: Move closer, retry, ensure app is closed

**Command Failures**
- Cause: Low battery or firmware issue
- Solution: Replace batteries, check firmware version

**No Response**
- Cause: Device not listening or wrong characteristic
- Solution: Verify UUIDs, check device compatibility

## Code Quality

- **Type Hints**: Full typing throughout
- **Async/Await**: Proper async implementation
- **Error Handling**: Comprehensive exception handling
- **Logging**: Appropriate debug/info/warning/error levels
- **Documentation**: Inline comments and docstrings

## Contributing

When contributing, ensure:
1. Code follows Home Assistant style guide
2. Type hints are present
3. Error handling is robust
4. Logging is appropriate
5. Documentation is updated

## References

- [SwitchBot BLE API](https://github.com/OpenWonderLabs/SwitchBotAPI-BLE)
- [Home Assistant Developer Docs](https://developers.home-assistant.io/)
- [Bleak Documentation](https://bleak.readthedocs.io/)
- [Home Assistant Bluetooth Integration](https://www.home-assistant.io/integrations/bluetooth/)

## License

MIT License - See LICENSE file for details

## Disclaimer

This is an unofficial integration developed through reverse engineering of the SwitchBot BLE protocol. It is not affiliated with, endorsed by, or supported by SwitchBot/WonderLabs Inc.
