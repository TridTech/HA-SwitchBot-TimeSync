# Quick Update Guide - Version 1.0.2

## Critical Fix: Time Sync Now Works Correctly

**If you installed version 1.0.0 or 1.0.1, the time sync was setting the wrong date (January 1st). Please update immediately.**

## What Was Wrong?

The timestamp was being encoded in big-endian instead of little-endian, causing the device to misinterpret the time. This has been fixed in version 1.0.2.

## How to Update

### Option 1: Replace Just the Fixed File (Fastest)

```bash
# Navigate to your integration directory
cd /config/custom_components/switchbot_meter_time_sync

# Backup the old file (optional)
cp coordinator.py coordinator.py.backup

# Replace with new version
# (Upload the new coordinator.py from version 1.0.2)

# Restart Home Assistant
ha core restart
```

### Option 2: Full Reinstall (Recommended)

```bash
# Remove old version
rm -rf /config/custom_components/switchbot_meter_time_sync

# Restart to clear cache
ha core restart

# Copy new version
cp -r /path/to/new/switchbot_meter_time_sync /config/custom_components/

# Restart again
ha core restart
```

### Option 3: Via File Editor (Home Assistant OS)

If you're using the File Editor add-on:

1. Navigate to `/config/custom_components/switchbot_meter_time_sync/coordinator.py`
2. Find line 91 (around line 91):
   ```python
   command.extend(struct.pack('>I', timestamp))
   ```
3. Change it to:
   ```python
   command.extend(struct.pack('<I', timestamp))
   ```
4. Find line 83 comment and update it too:
   ```python
   # Format: 0x57 (magic) + 0x09 (time cmd) + 0x01 (subcmd) + timestamp (4 bytes, LITTLE endian)
   ```
5. Save the file
6. Restart Home Assistant: Settings → System → Restart

## Verify the Fix

After updating:

1. Press the time sync button
2. Check your SwitchBot Meter display
3. The time should now show the **current date and time**
4. No longer showing January 1st at 2:00 AM

## What Changed Technically?

**Before (Wrong):**
```python
struct.pack('>I', timestamp)  # Big-endian
```

**After (Correct):**
```python
struct.pack('<I', timestamp)  # Little-endian (BLE GATT standard)
```

The `>` means big-endian (most significant byte first)  
The `<` means little-endian (least significant byte first)

BLE GATT protocol requires little-endian for multi-byte fields.

## No Other Changes Needed

- Your device configuration stays the same
- Automations continue to work
- No need to re-add the device

Just update the file and restart!

## Questions?

See [CHANGELOG.md](CHANGELOG.md) for full technical details.
