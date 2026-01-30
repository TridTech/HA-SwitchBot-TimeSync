# Time Offset Issue and Solution

## The Problem

Some users have reported that after syncing, their SwitchBot Meter displays a time that's off by a few hours (commonly 2 hours). This appears to be related to how different device firmware versions or models interpret the timestamp.

## Why This Happens

There are several possible causes:

1. **Timezone Interpretation**: Some devices may interpret the Unix timestamp as UTC while others interpret it as local time
2. **Firmware Differences**: Different firmware versions may handle time differently
3. **Daylight Saving Time**: The device may or may not account for DST automatically
4. **Regional Variants**: Different regional models may have different behavior

## Current Solution (v1.0.3)

The integration now:
- Uses **local system time** (not UTC) when syncing
- Provides a configurable time offset if needed
- Logs the time being sent for debugging

## If Your Time Is Still Off

### Quick Fix: Manual Offset

If your device consistently shows the wrong time by a fixed amount (e.g., 2 hours fast), you can add an offset.

Edit `/config/custom_components/switchbot_meter_time_sync/const.py`:

```python
# Change this line (near the bottom):
DEFAULT_TIME_OFFSET_HOURS = 0

# To your needed offset (negative if device is fast, positive if slow):
DEFAULT_TIME_OFFSET_HOURS = -2  # If device is 2 hours ahead
# or
DEFAULT_TIME_OFFSET_HOURS = 2   # If device is 2 hours behind
```

Then restart Home Assistant.

### Understanding Your Offset

**If your device shows a time that's:**
- **2 hours ahead** → Use `DEFAULT_TIME_OFFSET_HOURS = -2`
- **2 hours behind** → Use `DEFAULT_TIME_OFFSET_HOURS = 2`
- **1 hour ahead** → Use `DEFAULT_TIME_OFFSET_HOURS = -1`

### Check Your Home Assistant Timezone

First, verify your Home Assistant timezone is correct:

1. Go to Settings → System → General
2. Check "Time zone" setting
3. Make sure it matches your actual location

If this is wrong, fix it first, then test time sync again.

## Debugging Time Issues

### Enable Debug Logging

Add to `configuration.yaml`:
```yaml
logger:
  logs:
    custom_components.switchbot_meter_time_sync: debug
```

Restart HA, then press the sync button. Check logs for:
```
Preparing time sync for XX:XX:XX:XX:XX:XX: Local time: 2026-01-29 14:30:00, Timestamp: 1738185000
```

This shows what time is being sent to the device.

### Compare Times

1. Note your system time: `date`
2. Press sync button
3. Check device display immediately
4. Calculate the difference

### Common Scenarios

**Scenario 1: Device shows UTC instead of local time**
- Your system time: 2:00 PM PST (UTC-8)
- Device shows: 10:00 PM
- Difference: +8 hours
- Solution: Check if device has timezone setting in app

**Scenario 2: DST confusion**
- Your time: 2:00 PM PDT (UTC-7)
- Device shows: 3:00 PM or 1:00 PM
- Difference: ±1 hour
- Solution: May need to wait for DST change, or use offset

**Scenario 3: Fixed 2-hour offset**
- Your time: 2:00 PM
- Device shows: 4:00 PM
- Difference: +2 hours consistently
- Solution: Use `DEFAULT_TIME_OFFSET_HOURS = -2`

## Future Improvements

We're working on adding:
1. **Per-device offset configuration** (via UI)
2. **Automatic offset detection**
3. **Timezone configuration option**
4. **Device firmware detection** to apply known quirks

## Technical Details

### How Time Is Sent

```python
# Get local system time
now = datetime.now()  # e.g., 2026-01-29 14:30:00

# Convert to Unix timestamp (seconds since Jan 1, 1970 UTC)
timestamp = int(now.timestamp())  # e.g., 1738185000

# Apply any configured offset
if offset != 0:
    from datetime import timedelta
    now = now + timedelta(hours=offset)
    timestamp = int(now.timestamp())

# Encode as 4-byte little-endian integer
bytes = struct.pack('<I', timestamp)  # e.g., 0x98 0x12 0xAB 0x67

# Send to device
```

### What the Device Does

The device receives the 4-byte timestamp and:
1. Decodes it as a little-endian integer
2. Interprets it as seconds since Unix epoch
3. Converts to date/time based on its internal timezone logic
4. Displays on screen

Different firmware versions may handle step 3 differently.

## Reporting Issues

If you have persistent time issues, please report:

1. **Device Model**: Exact model number (e.g., W3400010)
2. **Firmware Version**: Check in SwitchBot app
3. **Your Timezone**: e.g., "America/Los_Angeles"
4. **HA Timezone Setting**: Settings → System → General
5. **Time Difference**: How many hours off is the device?
6. **Debug Logs**: Include the "Preparing time sync" log line

This helps us understand if there are model-specific quirks.

## Known Working Configurations

Please report your working config:

| Device Model | Firmware | Timezone | Offset Needed | Notes |
|--------------|----------|----------|---------------|-------|
| W3400010 | 1.0 | PST (UTC-8) | -2 hours | Consistently 2h fast |
| *Your device* | | | | |

## Workaround: Manual Time Set

If automatic sync continues to have issues, you can:

1. Use the SwitchBot app to set time manually (syncs correctly)
2. Use this integration only for quick corrections
3. Set automation to sync less frequently

Or open a GitHub issue for help debugging your specific case.
