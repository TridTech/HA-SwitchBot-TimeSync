# Troubleshooting SwitchBot Device Discovery

If your SwitchBot Meter is not being discovered by the integration, follow this guide.

## Common Issues and Solutions

### Issue 1: Device Already Added to Official Integration

**Problem**: If your device is already added to the official SwitchBot Bluetooth integration, it may not appear in this integration's discovery list.

**Solution**: You have two options:

1. **Keep Both Integrations** (Recommended):
   - The official integration provides temperature/humidity sensors
   - This integration only adds time sync functionality
   - Both can coexist peacefully
   - Remove the device from official integration temporarily to add it here, then re-add it
   
2. **Manual Entry**:
   - Get your device's MAC address (see below)
   - Enable debug logging (see below)
   - Look for your device in the logs
   - Contact support with logs if device still not working

### Issue 2: Device Not Discoverable

**Problem**: Device doesn't appear in any integration.

**Solutions**:

1. **Put Device in Pairing Mode**:
   - Remove battery cover
   - Press and hold the button on top for 2-3 seconds
   - Bluetooth icon should appear on the screen
   - Device is now in active advertising mode

2. **Check Bluetooth Adapter Mode**:
   - Go to Settings → Devices & Services → Bluetooth
   - Check if adapter is in "Active" or "Passive" mode
   - **Change to Active mode** for better discovery
   - Active mode sends scan requests, improving discovery

3. **Power Cycle the Device**:
   - Remove batteries
   - Wait 10 seconds
   - Reinsert batteries
   - Device will start advertising

### Issue 3: No Bluetooth Devices Found at All

**Problem**: No devices appear in the device list.

**Solutions**:

1. **Verify Bluetooth is Working**:
   ```bash
   # SSH into Home Assistant or use Terminal add-on
   bluetoothctl
   scan on
   # You should see devices appearing
   # Look for your device's MAC address
   ```

2. **Check Bluetooth Integration**:
   - Settings → Devices & Services → Bluetooth
   - Ensure Bluetooth integration is configured
   - Verify adapter shows as "Active" or "Passive"

3. **Check Device Range**:
   - Move SwitchBot Meter closer to your Bluetooth adapter
   - Ideal range: 1-3 meters (3-10 feet) for testing
   - Remove obstacles (walls, metal objects)

## Debugging Steps

### Step 1: Enable Debug Logging

Add this to your `configuration.yaml`:

```yaml
logger:
  default: warning
  logs:
    custom_components.switchbot_meter_time_sync: debug
    homeassistant.components.bluetooth: debug
```

Restart Home Assistant and check the logs.

### Step 2: Check What Home Assistant Sees

1. Go to Settings → Devices & Services → Bluetooth
2. Look at "Devices" section
3. Find your SwitchBot Meter in the list
4. Note the MAC address

### Step 3: Verify Device is Advertising

Look in the logs for entries like:

```
Bluetooth discovery triggered for device: XX:XX:XX:XX:XX:XX
Discovery info: name=WoSensorTH, rssi=-50
Service data: {'0000fd3d-0000-1000-8000-00805f9b34fb': b'w\x00\xe4'}
Manufacturer data: {2409: b'...'}
```

If you see this, your device is advertising correctly.

### Step 4: Check Device Identification

The integration identifies devices by:

1. **Device Name**: Contains "WoSensorTH" or "WoIOSensorTH"
2. **Service Data UUID**: `0000fd3d-0000-1000-8000-00805f9b34fb` (or short form `0xfd3d`)
3. **Manufacturer ID**: `2409` (0x0969)
4. **Device Type** (in service data):
   - `0x54` or `0x74` - Meter/Meter Plus
   - `0x77` - Meter Pro  
   - `0x7A` - Meter Pro CO2

If your device doesn't match ANY of these, it may not be supported.

## Getting Your Device's MAC Address

### Method 1: SwitchBot App

1. Open SwitchBot app
2. Tap on your Meter device
3. Tap the gear icon (Settings)
4. Tap "Device Info"
5. Look for "BLE MAC" - this is your MAC address
6. Format: `XX:XX:XX:XX:XX:XX`

### Method 2: Home Assistant Bluetooth Integration

1. Go to Settings → Devices & Services → Bluetooth
2. Click "Devices"
3. Look for device with name containing "WoSensorTH"
4. MAC address is shown next to device name

### Method 3: bluetoothctl (Advanced)

```bash
# SSH into Home Assistant
bluetoothctl
scan on
# Wait 10 seconds
# Look for devices with name "WoSensorTH" or similar
# MAC address is shown before the name
```

## Manual Device Entry (Future Feature)

Currently, the integration does not support manual MAC address entry. If your device is not auto-discovered, please:

1. Enable debug logging (see above)
2. Collect logs showing what data your device is advertising
3. Open a GitHub issue with:
   - Full debug logs
   - Device model (Meter, Meter Plus, Meter Pro, Meter Pro CO2)
   - MAC address (last 3 octets only for privacy)
   - Home Assistant version

## Advanced Troubleshooting

### Check Bluetooth Adapter Capabilities

Some Bluetooth adapters don't support all features:

1. **Check adapter info**:
   ```bash
   hciconfig -a
   # Look for "UP RUNNING" status
   ```

2. **Test scanning**:
   ```bash
   sudo hcitool lescan
   # Should show BLE devices
   # Press Ctrl+C to stop
   ```

3. **Check interference**:
   - Disable WiFi temporarily (if on 2.4GHz)
   - Move away from microwave ovens
   - Disable other Bluetooth devices

### Verify Service Data Format

If your device is advertising but not recognized, check the service data format:

Expected format (from logs):
```
Service data: {
  '0000fd3d-0000-1000-8000-00805f9b34fb': b'w\x00\xe4'
}
```

The first byte (`w` = `0x77`) is the device type:
- `0x54` (`T`) - Meter normal mode
- `0x74` (`t`) - Meter add mode  
- `0x77` (`w`) - Meter Pro
- `0x7A` (`z`) - Meter Pro CO2

If your device shows a different value, it might be a newer model not yet supported.

### Factory Reset Device (Last Resort)

**WARNING**: This will erase all device settings and remove it from the SwitchBot app.

1. Remove batteries
2. Press and hold button
3. Insert batteries while holding button
4. Keep holding for 10 seconds
5. Release button
6. Device will reset

After reset, the device should advertise aggressively for pairing.

## Known Limitations

1. **Outdoor Meter (W3400010)**: Uses slightly different advertising format, may not be detected properly
2. **Encrypted Devices**: Some newer Meter models use encryption, which may cause issues
3. **Cloud-Only Devices**: Some devices only work via SwitchBot Hub and don't support direct BLE control

## Still Not Working?

If you've tried everything above and it's still not working:

1. **Capture Detailed Logs**:
   ```yaml
   logger:
     default: info
     logs:
       custom_components.switchbot_meter_time_sync: debug
       homeassistant.components.bluetooth: debug
       homeassistant.components.bluetooth.scanner: debug
   ```

2. **Collect Information**:
   - Home Assistant version
   - Bluetooth adapter model
   - SwitchBot device model and firmware version
   - Full debug logs (remove MAC address for privacy)

3. **Open GitHub Issue**:
   - Provide all information above
   - Describe steps you've already tried
   - Include relevant log excerpts

## Additional Resources

- [Home Assistant Bluetooth Troubleshooting](https://www.home-assistant.io/integrations/bluetooth/#troubleshooting)
- [SwitchBot BLE API Documentation](https://github.com/OpenWonderLabs/SwitchBotAPI-BLE)
- [Bluetooth LE Overview](https://www.bluetooth.com/learn-about-bluetooth/low-energy/)

## Tips for Success

1. **Start Close**: Begin with device right next to Bluetooth adapter
2. **Active Mode**: Use Active scanning mode in Bluetooth integration
3. **One at a Time**: Add devices one at a time for easier troubleshooting
4. **Be Patient**: BLE discovery can take 30-60 seconds
5. **Fresh Batteries**: Low battery can cause connection issues
