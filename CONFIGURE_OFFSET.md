# Configuring Per-Device Time Offset

## Version 1.0.4 Feature: Device-Specific Time Offset

Each SwitchBot Meter device can now have its own time offset configured through the Home Assistant UI.

## Why You Might Need This

Some SwitchBot Meter devices show incorrect time after sync due to:
- Firmware differences between device models
- Regional variants handling timestamps differently
- Timezone interpretation quirks

## How to Configure Time Offset

### Step 1: Identify the Offset Needed

1. **Sync time** using the button
2. **Check your device** display immediately
3. **Calculate the difference**:
   - Device shows 4:00 PM, actual time is 2:00 PM → Device is **2 hours ahead** → Use offset **-2**
   - Device shows 12:00 PM, actual time is 2:00 PM → Device is **2 hours behind** → Use offset **+2**

### Step 2: Configure via UI

1. Go to **Settings** → **Devices & Services**
2. Find **SwitchBot Meter Time Sync**
3. Click on your device
4. Click **Configure** (gear icon)
5. Enter **Time offset (hours)**:
   - **Negative** if device is ahead (e.g., `-2` if 2 hours fast)
   - **Positive** if device is behind (e.g., `+2` if 2 hours slow)
   - **Zero** (default) for no offset
6. Click **Submit**

### Step 3: Test

1. Press the time sync button again
2. Check device display
3. Time should now be correct!

## Examples

### Example 1: Device Shows 2 Hours Ahead

**Scenario:**
- Your time: 2:00 PM
- Device shows: 4:00 PM
- Difference: Device is 2 hours ahead

**Solution:**
- Set time offset to: **-2**

**What happens:**
- Integration sends: Current time minus 2 hours (12:00 PM timestamp)
- Device adds its quirk: 12:00 PM + 2 hours = 2:00 PM ✓

### Example 2: Device Shows 1 Hour Behind

**Scenario:**
- Your time: 2:00 PM
- Device shows: 1:00 PM
- Difference: Device is 1 hour behind

**Solution:**
- Set time offset to: **+1**

**What happens:**
- Integration sends: Current time plus 1 hour (3:00 PM timestamp)
- Device interprets: 3:00 PM - 1 hour = 2:00 PM ✓

### Example 3: Multiple Devices, Different Offsets

**Device 1 (Bedroom):**
- Shows 2 hours ahead → Configure offset: **-2**

**Device 2 (Kitchen):**
- Shows correct time → Configure offset: **0** (default)

**Device 3 (Garage):**
- Shows 1 hour behind → Configure offset: **+1**

Each device remembers its own setting!

## Technical Details

### How It Works

```python
# Without offset (device showing wrong time)
local_time = datetime.now()  # 2:00 PM
timestamp = local_time.timestamp()
send_to_device(timestamp)
# Device interprets it as 4:00 PM (oops!)

# With offset of -2
local_time = datetime.now()  # 2:00 PM
adjusted = local_time + timedelta(hours=-2)  # 12:00 PM
timestamp = adjusted.timestamp()
send_to_device(timestamp)
# Device adds its quirk: 12:00 PM + 2 hours = 2:00 PM ✓
```

### Allowed Range

- **Minimum**: -12 hours
- **Maximum**: +12 hours
- **Default**: 0 hours (no offset)

This covers all possible timezone offsets worldwide.

## Troubleshooting

### Offset Doesn't Help

If adjusting the offset doesn't fix the time:

1. **Check Home Assistant timezone**:
   - Settings → System → General → Time zone
   - Must match your actual location

2. **Check for DST issues**:
   - Some devices handle daylight saving time differently
   - May need to adjust offset when DST changes

3. **Try the SwitchBot app**:
   - If app sync works but integration doesn't, report as bug
   - Include device model and firmware version

### Time Drifts Over Days

If time is correct initially but drifts:
- This is clock drift, not offset issue
- Solution: Sync more frequently (twice daily instead of daily)
- Or replace device batteries (low battery affects clock)

### Different Devices Need Different Offsets

This is normal! Different firmware versions or models may behave differently. That's exactly why we made it per-device configurable.

## Resetting to Default

To remove the offset:

1. Go to device configuration
2. Set time offset to: **0**
3. Submit

Or remove and re-add the device (offset defaults to 0).

## FAQ

**Q: Do I need to restart HA after changing offset?**  
A: No! Changes apply immediately. Just press sync button to test.

**Q: Can I have negative offsets?**  
A: Yes! Use negative values if device is ahead of actual time.

**Q: Will automations use the offset?**  
A: Yes, every sync (manual or automated) uses the configured offset.

**Q: Can I change offset later?**  
A: Yes, anytime through device configuration.

**Q: What if I don't know my offset?**  
A: Start with 0, sync, check device, calculate difference, configure offset.

## Reporting Your Configuration

Help us understand device quirks! Report your working config:

**Template:**
```
Device Model: [e.g., W3400010]
Firmware: [from app]
Region: [US/EU/JP/etc]
Offset Needed: [hours]
Works Correctly: [Yes/No]
```

Post in GitHub issues to help others with same device!

## Advanced: Automation with Offset

Your automations don't need to change:

```yaml
automation:
  - alias: "Daily Time Sync"
    trigger:
      - platform: time
        at: "00:00:00"
    action:
      - service: button.press
        target:
          entity_id: button.switchbot_meter_xxxxx_sync_time
```

The offset is automatically applied during every sync.

## Version History

- **v1.0.0-1.0.2**: No offset support
- **v1.0.3**: Global offset in const.py (all devices same)
- **v1.0.4**: Per-device offset via UI (each device independent) ✓
