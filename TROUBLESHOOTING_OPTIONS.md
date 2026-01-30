# Troubleshooting: Configuration Options Not Showing

## Problem: "Configure" Button Missing or Not Working

If you don't see a "Configure" option for your device, or clicking it doesn't show the time offset option, follow these steps.

## Solution 1: Force a Clean Reinstall

The most reliable way to ensure options appear:

```bash
# 1. Remove the integration via UI first
# Settings → Devices & Services → SwitchBot Meter Time Sync → Delete

# 2. Remove files
rm -rf /config/custom_components/switchbot_meter_time_sync

# 3. Restart Home Assistant
ha core restart

# 4. Wait for full restart (check logs)

# 5. Copy new version
cp -r switchbot_meter_time_sync /config/custom_components/

# 6. Restart again
ha core restart

# 7. Re-add the integration
# Settings → Devices & Services → Add Integration → SwitchBot Meter Time Sync
```

## Solution 2: Clear Integration Cache

If reinstall didn't work:

```bash
# WARNING: This will remove ALL integration configurations
# Back up /config/.storage/ first!

# Stop Home Assistant
ha core stop

# Remove config entries cache
rm /config/.storage/core.config_entries

# Start Home Assistant
ha core start

# Re-add all integrations
```

## Solution 3: Check Integration Loaded Correctly

Enable debug logging:

```yaml
# configuration.yaml
logger:
  default: warning
  logs:
    custom_components.switchbot_meter_time_sync: debug
    homeassistant.config_entries: debug
```

Restart HA and check logs for:
- "async_get_options_flow" being called
- Any errors during integration load

## How to Access Configuration Options

Once working, here's where to find the options:

### Method 1: Via Device Page
1. Settings → Devices & Services
2. Click on "SwitchBot Meter Time Sync" integration
3. Click on your device name
4. Look for "Configure" button (may be a gear icon or three dots)
5. Click it

### Method 2: Via Integration Page
1. Settings → Devices & Services
2. Find "SwitchBot Meter Time Sync"
3. Click the three dots (⋮) next to your device
4. Select "Configure" or "Options"

## What the Options Screen Should Look Like

You should see:
```
Time Sync Options
Configure time synchronization settings for this device.

Time offset (hours): [  0  ]

Adjust if device shows incorrect time after sync. Use negative 
values if device is ahead (e.g., -2 if device shows 2 hours ahead). 
Range: -12 to +12 hours.

[Cancel]  [Submit]
```

## Common Issues

### Issue: No "Configure" Button at All

**Cause**: Home Assistant doesn't recognize the options flow

**Solution**:
1. Check `config_flow.py` has `async_get_options_flow` method
2. Ensure `OptionsFlowHandler` class exists
3. Verify `manifest.json` has `"config_flow": true`
4. Do a clean reinstall (Solution 1 above)

### Issue: "Configure" Button Does Nothing

**Cause**: Error in options flow handler

**Solution**:
1. Check Home Assistant logs for errors
2. Look for `AttributeError` or `KeyError`
3. Ensure using version 1.0.5 or later (fixed the AttributeError)

### Issue: Options Don't Save

**Cause**: Update listener not working

**Solution**:
1. Options are saved even if UI doesn't show confirmation
2. Press sync button to test if offset is applied
3. Check logs for "Applied time offset of X hours"

## Verify Options Are Working

Even without seeing the UI, you can verify options work:

### Via Developer Tools

1. Developer Tools → States
2. Find your device entities
3. Look at entity attributes for config options

### Via Logs

With debug logging enabled, sync button will show:
```
Preparing time sync for XX:XX:XX:XX:XX:XX: Local time: 2026-01-29 14:30:00, Offset: -2 hours, Timestamp: 1738177800
```

The "Offset: -2 hours" confirms your setting is applied.

## Manual Configuration (Temporary Workaround)

If UI options don't work, you can manually edit config:

```bash
# Edit the storage file (BACKUP FIRST!)
nano /config/.storage/core.config_entries

# Find your switchbot_meter_time_sync entry
# Add to the "options" section:
"options": {
  "time_offset_hours": -2
}

# Save and restart HA
ha core restart
```

**WARNING**: Manual editing can break things. Only do this as last resort.

## Still Not Working?

If none of the above works:

1. **Capture Full Logs**:
   ```bash
   grep -i "switchbot\|config_flow\|options" /config/home-assistant.log > ~/debug.log
   ```

2. **Check Integration Version**:
   ```bash
   cat /config/custom_components/switchbot_meter_time_sync/manifest.json | grep version
   ```
   Should show: `"version": "1.0.5"` or later

3. **Verify File Contents**:
   ```bash
   grep -c "OptionsFlowHandler" /config/custom_components/switchbot_meter_time_sync/config_flow.py
   ```
   Should show: `2` (class definition and return statement)

4. **Check Python Syntax**:
   ```bash
   python3 -m py_compile /config/custom_components/switchbot_meter_time_sync/config_flow.py
   ```
   Should complete without errors

5. **Report Issue**:
   - Include HA version
   - Include integration version
   - Include relevant log excerpts
   - Describe what happens when you try to access options

## Known Working Setup

This should work on:
- Home Assistant Core 2024.1.0+
- Home Assistant OS / Supervised / Container / Core
- Python 3.11+

If your setup matches and it still doesn't work, it's likely a cache issue - try Solution 1 (clean reinstall).
