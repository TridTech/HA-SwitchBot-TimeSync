# Quick Reference - Common Issues

## "No devices found" Error

### Try This First (in order):
1. ✓ Go to Settings → Devices & Services → Bluetooth → Set to **Active** mode
2. ✓ Press and hold button on Meter for 2-3 seconds (Bluetooth icon appears)
3. ✓ Move device within 3 feet of Bluetooth adapter
4. ✓ Wait 30-60 seconds, then try adding integration again

### Still Not Working?
- Remove device from official SwitchBot integration (temporarily)
- Power cycle: Remove batteries, wait 10 sec, reinsert
- Check logs: Settings → System → Logs (look for "switchbot")

## Device Already Added to Official Integration

**Good News**: Both integrations can coexist!
- Official integration = temperature/humidity sensors
- This integration = time sync button

**To add to both**:
1. Remove from official integration
2. Add to this integration
3. Add back to official integration
4. Now you have both!

## Time Sync Fails

### Quick Fixes:
- Move device closer (< 10 feet)
- Close SwitchBot app (device can only connect to one client)
- Replace batteries if low
- Try again (BLE can be temperamental)

## Enable Debug Logging

Add to `configuration.yaml`:
```yaml
logger:
  logs:
    custom_components.switchbot_meter_time_sync: debug
    homeassistant.components.bluetooth: debug
```

Then restart HA and check logs.

## Get Device MAC Address

### Method 1: SwitchBot App
App → Device → Settings → Device Info → BLE MAC

### Method 2: Home Assistant
Settings → Devices & Services → Bluetooth → Look for "WoSensorTH"

## Run Debug Script

```bash
cd /config/custom_components/switchbot_meter_time_sync
python3 debug_discovery.py
```

Shows what your device is advertising.

## Check Bluetooth Status

### In Home Assistant:
Settings → Devices & Services → Bluetooth
- Should show your adapter as Active or Passive
- Change to **Active** for better discovery

### Via Terminal (Advanced):
```bash
bluetoothctl
scan on
# Wait 10 seconds, look for your device
```

## Need More Help?

📘 **TROUBLESHOOTING.md** - Comprehensive troubleshooting guide  
🔧 **INSTALLATION.md** - Detailed installation instructions  
📝 **README.md** - Full documentation  
🐛 **GitHub Issues** - Report bugs with logs  

## Quick Automation

```yaml
automation:
  - alias: "Daily Time Sync"
    trigger:
      - platform: time
        at: "00:00:00"
    action:
      - service: button.press
        target:
          entity_id: button.switchbot_meter_XXXXX_sync_time
```

Replace `XXXXX` with your device ID.

## Verify Installation

Files should be at:
```
/config/custom_components/switchbot_meter_time_sync/
├── __init__.py
├── button.py
├── config_flow.py
├── const.py
├── coordinator.py
├── manifest.json
└── strings.json
```

## Integration Not Showing?

1. Verify files are in correct location (above)
2. Restart Home Assistant
3. Check logs for errors
4. Files must be readable by homeassistant user

## Button Not Appearing?

1. Go to Settings → Devices & Services
2. Find "SwitchBot Meter Time Sync"
3. Click on your device
4. Button entity should be there: `button.switchbot_meter_XXXXX_sync_time`

If not:
- Check logs for errors
- Verify integration loaded successfully
- Try removing and re-adding device

## Battery Issues

Low battery can cause:
- Connection failures
- Slow response
- Timeout errors

**Solution**: Replace with fresh AAA batteries

## Quick Test

After adding device:
1. Find button entity
2. Press it once
3. Wait 5-10 seconds
4. Check your Meter display - time should update
5. Check Home Assistant notifications

Success = Notification saying "Successfully synced time"
Failure = Error notification with details

## Most Common Mistake

❌ **Bluetooth adapter in Passive mode**
✓ **Change to Active mode for discovery**

Settings → Devices & Services → Bluetooth → Configure → Active
