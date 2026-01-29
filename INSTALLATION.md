# Installation Guide

## Prerequisites

Before installing, ensure you have:

1. **Home Assistant** 2024.1.0 or newer
2. **Bluetooth Adapter** configured in Home Assistant
3. **Python 3.11+** (usually already installed with HA)
4. **SwitchBot Meter** device nearby

## Verify Bluetooth Setup

1. Go to **Settings** → **Devices & Services**
2. Check that **Bluetooth** integration is installed and working
3. Verify your adapter is shown as "Active" or "Passive"

If Bluetooth is not set up:
1. Click **Add Integration**
2. Search for "Bluetooth"
3. Follow the setup wizard

## Installation Methods

### Method 1: Manual Installation (Recommended for testing)

1. **Download the Integration**
   - Download this repository as a ZIP file
   - Extract it to a temporary location

2. **Copy Files**
   ```bash
   # Navigate to your Home Assistant config directory
   cd /config
   
   # Create custom_components directory if it doesn't exist
   mkdir -p custom_components
   
   # Copy the integration
   cp -r /path/to/extracted/switchbot_meter_time_sync custom_components/
   ```

3. **Verify Structure**
   Your directory should look like:
   ```
   /config/
   ├── custom_components/
   │   └── switchbot_meter_time_sync/
   │       ├── __init__.py
   │       ├── button.py
   │       ├── config_flow.py
   │       ├── const.py
   │       ├── coordinator.py
   │       ├── manifest.json
   │       └── strings.json
   ```

4. **Restart Home Assistant**
   - Go to **Settings** → **System** → **Restart**
   - Or use: Settings → Developer Tools → YAML → Restart

### Method 2: HACS (Future)

This integration will be available through HACS after community testing.

1. Open HACS
2. Click on Integrations
3. Click the three dots in the top right
4. Select "Custom repositories"
5. Add this repository URL
6. Select "Integration" as category
7. Click "Add"
8. Find "SwitchBot Meter Time Sync" and install

## Configuration

### Option A: Automatic Discovery

1. After restart, go to **Settings** → **Devices & Services**
2. You should see a notification about discovered SwitchBot devices
3. Click **Configure**
4. Confirm the device
5. Done!

### Option B: Manual Configuration

1. Go to **Settings** → **Devices & Services**
2. Click **Add Integration** (+ button)
3. Search for "SwitchBot Meter Time Sync"
4. Select your device from the dropdown
5. Click **Submit**

## Finding Your Device

If your device doesn't appear:

1. **Press the Button**
   - Press and hold the button on your SwitchBot Meter for 2 seconds
   - This puts it in pairing mode (Bluetooth icon appears on screen)

2. **Check Bluetooth Logs**
   ```yaml
   # Add to configuration.yaml
   logger:
     default: warning
     logs:
       homeassistant.components.bluetooth: debug
   ```
   Restart HA and check logs for your device's MAC address

3. **Use SwitchBot App (if needed)**
   - Open the app
   - Tap your Meter device
   - Settings → Device Info → BLE MAC
   - Note the MAC address (format: XX:XX:XX:XX:XX:XX)

## Post-Installation

### Verify Installation

1. Go to **Settings** → **Devices & Services**
2. Find "SwitchBot Meter Time Sync"
3. Click on it
4. You should see your device listed

### Test the Button

1. Go to **Settings** → **Devices & Services** → **SwitchBot Meter Time Sync**
2. Click on your device
3. Find the "Sync Time" button entity
4. Click it
5. Check your SwitchBot Meter - the time should update within 5 seconds

### Add to Dashboard

1. Edit your dashboard
2. Add a new card (button type)
3. Select the entity: `button.switchbot_meter_XXXXX_sync_time`
4. Customize as desired
5. Save

### Set Up Automation

See the `examples/automations.yaml` file for examples.

Basic example:
```yaml
automation:
  - alias: "Daily SwitchBot Time Sync"
    trigger:
      - platform: time
        at: "00:00:00"
    action:
      - service: button.press
        target:
          entity_id: button.switchbot_meter_XXXXX_sync_time
```

## Troubleshooting

### Integration Not Showing Up

**Problem**: Integration doesn't appear in the Add Integration dialog

**Solutions**:
1. Verify files are in correct location: `/config/custom_components/switchbot_meter_time_sync/`
2. Check file permissions (should be readable by HA user)
3. Restart Home Assistant again
4. Check logs for errors: Settings → System → Logs
5. Enable debug logging:
   ```yaml
   logger:
     default: warning
     logs:
       custom_components.switchbot_meter_time_sync: debug
   ```

### Device Not Discovered

**Problem**: No devices appear in the device list

**Solutions**:
1. Ensure device is powered on (check battery)
2. Move device closer to Bluetooth adapter
3. Put device in pairing mode (hold button for 2 seconds)
4. Check Bluetooth integration is active
5. Try manual entry with MAC address

### Connection Failures

**Problem**: Time sync button fails or times out

**Solutions**:
1. **Check Range**: Move device closer to Bluetooth adapter
2. **Check Battery**: Low battery can cause connection issues
3. **Check Interference**: 
   - Disable other Bluetooth devices temporarily
   - Move away from WiFi router
4. **Close SwitchBot App**: Device can only connect to one client at a time
5. **Restart Bluetooth**: 
   - Settings → Devices & Services → Bluetooth → Options → Restart

### Time Doesn't Update

**Problem**: Button press succeeds but time doesn't change

**Solutions**:
1. Wait 10-15 seconds after pressing (device may take time to update display)
2. Check the response in logs for error codes
3. Try pressing the physical button on the device (this should refresh display)
4. Verify your Home Assistant time is correct

### Multiple Devices Issues

**Problem**: Only one device works when you have multiple Meters

**Solutions**:
1. Add each device separately through the integration
2. Ensure each has unique MAC address
3. In automations, target each device specifically
4. Consider adding delays between syncs if syncing multiple devices

## Advanced Configuration

### Custom Bluetooth Adapter

If you have multiple Bluetooth adapters:

1. Go to **Settings** → **Devices & Services** → **Bluetooth**
2. Configure which adapter to use
3. Set to "Active" mode for better connectivity

### Performance Tuning

For faster connections, ensure:
1. Bluetooth adapter is in Active mode
2. Device is within 10-15 feet of adapter
3. No physical obstructions (walls, metal objects)
4. Minimal Bluetooth interference

### Battery Conservation

To minimize battery impact:
- Sync once daily instead of multiple times
- Avoid rapid repeated syncs
- Use time-based triggers rather than state-based

## Uninstallation

If you need to remove the integration:

1. **Remove Integration**:
   - Settings → Devices & Services
   - Find "SwitchBot Meter Time Sync"
   - Click three dots → Delete

2. **Remove Files**:
   ```bash
   rm -rf /config/custom_components/switchbot_meter_time_sync
   ```

3. **Restart Home Assistant**

4. **Clean Up** (optional):
   - Remove automation entries
   - Remove dashboard cards
   - Remove from configuration.yaml (if added)

## Getting Help

If you encounter issues:

1. **Check Logs**: Settings → System → Logs
2. **Enable Debug Logging**: See troubleshooting section
3. **GitHub Issues**: Report bugs with:
   - Home Assistant version
   - Integration version
   - Device model
   - Full error logs
   - Steps to reproduce

## Next Steps

- Set up an automation for automatic syncing
- Add the button to your dashboard
- Configure notifications (optional)
- Test with different sync schedules

Enjoy your automatically synced SwitchBot Meter!
