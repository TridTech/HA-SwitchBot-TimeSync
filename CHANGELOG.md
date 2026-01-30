# Changelog

All notable changes to this project will be documented in this file.

## [1.0.5] - 2026-01-29

### Fixed
- **CRITICAL**: Fixed AttributeError preventing integration removal
  - Changed `self.config_entry` to `self._config_entry` in OptionsFlowHandler
  - This was blocking integration unload/removal
- Improved coordinator shutdown handling
  - Properly disconnects Bluetooth on integration removal
  - Uses `.pop(entry_id, None)` to avoid KeyError on cleanup

### Changed
- Better error handling in unload process

## [1.0.4] - 2026-01-29

### Added
- **Per-device time offset configuration** via UI
  - Each device can have its own offset setting (-12 to +12 hours)
  - Configured through Settings → Devices & Services → [Device] → Configure
  - No more editing const.py for offset!
- Options flow handler for device configuration
- Update listener to apply option changes without restart
- Comprehensive guide: CONFIGURE_OFFSET.md

### Fixed
- **Proper local time handling**: Fixed timestamp conversion
  - Previously: `datetime.now().timestamp()` was converting to UTC behind the scenes
  - Now: Correctly handles local time with proper timezone awareness
- Coordinator now receives config entry for per-device settings

### Changed
- Removed global `DEFAULT_TIME_OFFSET_HOURS` from affecting devices (still exists as default for new devices)
- Better debug logging showing offset being applied

## [1.0.3] - 2026-01-29

### Fixed
- **CRITICAL**: Fixed AttributeError with persistent notifications
  - Changed from `hass.components.persistent_notification.async_create()` (incorrect)
  - To `hass.services.async_call("persistent_notification", "create", ...)` (correct)
- **Timezone handling**: Changed from UTC to local system time
  - Device now receives local time instead of UTC
  - Should reduce timezone-related issues

### Added
- Configurable time offset constant (`DEFAULT_TIME_OFFSET_HOURS`)
  - For users whose devices consistently show wrong time by fixed amount
  - Can be set in `const.py` if needed
- Enhanced debug logging showing exact time being sent
- Documentation for time offset issues (`TIME_OFFSET_ISSUE.md`)

### Changed
- Removed hardcoded -2 hour offset (was device-specific)
- Better logging to help debug time sync issues

## [1.0.2] - 2026-01-29

### Fixed
- **CRITICAL FIX**: Changed timestamp encoding from big-endian to little-endian
  - Previous version set time to January 1st, 2:00 AM
  - Now correctly syncs to current date and time
  - Follows BLE GATT standard for multi-byte fields (little-endian)

## [1.0.1] - 2026-01-29

### Fixed
- Fixed "Invalid handler specified" error by renaming config flow class
- Changed config flow class name from `SwitchBotMeterTimeSyncConfigFlow` to `ConfigFlow`

### Added
- Enhanced device discovery with multiple Bluetooth matchers:
  - Service data UUID matcher
  - Service UUID matcher  
  - Manufacturer ID matcher
  - Local name matcher
- Comprehensive troubleshooting documentation (TROUBLESHOOTING.md)
- Debug discovery script (debug_discovery.py)
- Validation script (validate.py)
- Quick reference guide (QUICK_REFERENCE.md)
- Fix guide for "Invalid handler" error (FIX_INVALID_HANDLER.md)
- English translations file (translations/en.json)

### Improved
- Better device identification logic (checks name, service data, AND manufacturer data)
- More detailed logging for discovery debugging
- Support for both "normal" and "add" modes

## [1.0.0] - 2026-01-29

### Added
- Initial release
- Basic time sync functionality
- Bluetooth discovery
- Button entity for manual sync
- Configuration flow
- Documentation (README, INSTALLATION, QUICKSTART)

## Upgrade Instructions

### From 1.0.1 to 1.0.2

**Critical upgrade - time sync was not working correctly in 1.0.1**

```bash
# Replace the coordinator.py file
cp switchbot_meter_time_sync/coordinator.py /config/custom_components/switchbot_meter_time_sync/

# Update manifest.json
cp switchbot_meter_time_sync/manifest.json /config/custom_components/switchbot_meter_time_sync/

# Restart Home Assistant
ha core restart
```

Or do a complete reinstall:
```bash
rm -rf /config/custom_components/switchbot_meter_time_sync
cp -r switchbot_meter_time_sync /config/custom_components/
ha core restart
```

### From 1.0.0 to 1.0.2

Recommend complete reinstall:
```bash
# Remove old version
rm -rf /config/custom_components/switchbot_meter_time_sync

# Restart to clear cache
ha core restart

# Install new version
cp -r switchbot_meter_time_sync /config/custom_components/

# Restart again
ha core restart
```

## Known Issues

### Version 1.0.0
- Device discovery may fail with default matchers
- "Invalid handler specified" error

### Version 1.0.1
- **Time sync sets wrong time** (January 1st instead of current date) - FIXED IN 1.0.2
- Device discovery improved but may still fail for some devices

### Version 1.0.2
- None known at this time

## Technical Details

### Why Little-Endian?

According to the Bluetooth GATT specification (Volume 3, Part G):
> "Multi-octet fields within the GATT Profile shall be sent least significant octet first (little endian)."

The SwitchBot devices follow this standard for time synchronization commands.

### Timestamp Encoding

**Incorrect (1.0.0, 1.0.1):**
```python
struct.pack('>I', timestamp)  # Big-endian
# Example: 1738185600 (2026-01-29)
# Encoded as: 67 BB 12 00
# Device reads: 00 12 BB 67 = 1227 seconds = Jan 1st, 2:00 AM
```

**Correct (1.0.2):**
```python
struct.pack('<I', timestamp)  # Little-endian
# Example: 1738185600 (2026-01-29)
# Encoded as: 00 12 BB 67
# Device reads: 67 BB 12 00 = 1738185600 = Jan 29, 2026
```
