# Fixing "Invalid Handler Specified" Error

## What This Error Means

The error `"Config flow could not be loaded: {"message":"Invalid handler specified"}"` means Home Assistant can't load the config flow module for this integration.

## Most Common Causes & Fixes

### 1. Integration Not Properly Installed

**Problem**: Files are in wrong location or incomplete

**Solution**:
```bash
# Check files are in the right place
ls -la /config/custom_components/switchbot_meter_time_sync/

# You should see these files:
# __init__.py
# manifest.json
# const.py
# config_flow.py
# coordinator.py
# button.py
# strings.json
# translations/en.json
```

If files are missing or in wrong location:
```bash
# Remove old installation
rm -rf /config/custom_components/switchbot_meter_time_sync

# Copy fresh files
cp -r /path/to/switchbot_meter_time_sync /config/custom_components/

# Restart Home Assistant
```

### 2. File Permissions Issue

**Problem**: Home Assistant can't read the files

**Solution**:
```bash
# Fix ownership (adjust user if needed)
chown -R homeassistant:homeassistant /config/custom_components/switchbot_meter_time_sync

# Fix permissions
chmod -R 755 /config/custom_components/switchbot_meter_time_sync
chmod 644 /config/custom_components/switchbot_meter_time_sync/*.py
chmod 644 /config/custom_components/switchbot_meter_time_sync/*.json
```

### 3. Python Syntax Error

**Problem**: There's a syntax error in one of the Python files

**Solution**:
```bash
# Run the validation script
cd /config/custom_components/switchbot_meter_time_sync
python3 validate.py

# This will check all files for errors
```

If validation fails, re-download the integration files.

### 4. Cached Configuration

**Problem**: Home Assistant is using cached version with errors

**Solution**:
```bash
# Clear integration cache (Home Assistant OS/Supervised)
rm -rf /config/.storage/core.config_entries

# OR via UI:
# 1. Stop Home Assistant
# 2. Delete /config/.storage/core.config_entries (BACKUP FIRST!)
# 3. Start Home Assistant
# 4. Re-add all integrations
```

**WARNING**: This will remove ALL integration configurations. Only do this as a last resort and backup first!

### 5. Incomplete Restart

**Problem**: Home Assistant didn't fully reload custom components

**Solution**:
1. Go to Settings → System → Restart
2. Choose **"Restart Home Assistant"** (full restart)
3. Wait for full startup (check logs)
4. Try adding integration again

For Home Assistant OS/Supervised:
```bash
ha core restart
```

For Docker:
```bash
docker restart homeassistant
```

## Step-by-Step Fix Procedure

### Step 1: Validate Installation

```bash
cd /config/custom_components/switchbot_meter_time_sync
python3 validate.py
```

If this fails, the files have errors. Re-download them.

### Step 2: Check Home Assistant Logs

```bash
# View recent logs
tail -f /config/home-assistant.log | grep -i switchbot

# Or via UI:
# Settings → System → Logs
# Search for "switchbot"
```

Look for specific error messages about imports or syntax.

### Step 3: Verify Manifest

```bash
cat /config/custom_components/switchbot_meter_time_sync/manifest.json
```

Should show:
```json
{
  "domain": "switchbot_meter_time_sync",
  "config_flow": true,
  ...
}
```

### Step 4: Check Domain Constant

```bash
grep "DOMAIN" /config/custom_components/switchbot_meter_time_sync/const.py
```

Should show:
```python
DOMAIN = "switchbot_meter_time_sync"
```

### Step 5: Verify Config Flow Class

```bash
grep "class.*ConfigFlow" /config/custom_components/switchbot_meter_time_sync/config_flow.py
```

Should show:
```python
class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
```

## Advanced Troubleshooting

### Check Python Import

```bash
cd /config/custom_components/switchbot_meter_time_sync
python3 << EOF
import sys
sys.path.insert(0, '/config/custom_components')

try:
    from switchbot_meter_time_sync import const
    print(f"✓ Constants loaded, DOMAIN = {const.DOMAIN}")
except Exception as e:
    print(f"✗ Error loading constants: {e}")

try:
    from switchbot_meter_time_sync import config_flow
    print(f"✓ Config flow loaded")
except Exception as e:
    print(f"✗ Error loading config flow: {e}")
EOF
```

### Enable Debug Logging

Add to `configuration.yaml`:
```yaml
logger:
  default: warning
  logs:
    homeassistant.config_entries: debug
    homeassistant.loader: debug
    custom_components.switchbot_meter_time_sync: debug
```

Restart and check logs for detailed error messages.

### Check for Conflicting Integrations

If you have another custom integration with similar code:
```bash
# Search for domain conflicts
grep -r "switchbot_meter_time_sync" /config/custom_components/
```

Should only show results in the switchbot_meter_time_sync directory.

## Clean Reinstall Procedure

If nothing else works:

```bash
# 1. Remove integration via UI
#    Settings → Devices & Services → Find integration → Delete

# 2. Remove files
rm -rf /config/custom_components/switchbot_meter_time_sync

# 3. Restart Home Assistant
ha core restart  # or via UI

# 4. Verify removal
ls /config/custom_components/switchbot_meter_time_sync
# Should show: No such file or directory

# 5. Copy fresh files
cp -r /path/to/switchbot_meter_time_sync /config/custom_components/

# 6. Validate
cd /config/custom_components/switchbot_meter_time_sync
python3 validate.py

# 7. Restart again
ha core restart

# 8. Add integration via UI
```

## Version 1.0.1 Specific Fix

**If upgrading from version 1.0.0**:

The config flow class name changed from `SwitchBotMeterTimeSyncConfigFlow` to `ConfigFlow`. 

This requires a clean reinstall:
```bash
# Remove old version completely
rm -rf /config/custom_components/switchbot_meter_time_sync

# Restart
ha core restart

# Install new version
cp -r /path/to/switchbot_meter_time_sync /config/custom_components/

# Restart again
ha core restart
```

## Still Getting the Error?

If you've tried everything above and still get "Invalid handler specified":

1. **Capture Full Logs**:
   ```bash
   grep -A 20 "switchbot_meter_time_sync" /config/home-assistant.log > ~/switchbot_error.log
   ```

2. **Check Home Assistant Version**:
   ```bash
   ha core info
   # Or: Settings → System → About
   ```
   
   This integration requires HA 2024.1.0+

3. **Verify Python Version**:
   ```bash
   python3 --version
   # Should be 3.11 or higher
   ```

4. **Check Disk Space**:
   ```bash
   df -h /config
   # Make sure you have free space
   ```

5. **Open GitHub Issue**:
   - Include Home Assistant version
   - Include output of `validate.py`
   - Include relevant logs (remove sensitive info)
   - Describe installation method used

## Quick Checklist

Before asking for help, verify:

- [ ] Files are in `/config/custom_components/switchbot_meter_time_sync/`
- [ ] `validate.py` passes all checks
- [ ] Home Assistant restarted FULLY (not just config reload)
- [ ] No other integration using same domain name
- [ ] File permissions are correct (readable by HA)
- [ ] Home Assistant version is 2024.1.0 or newer
- [ ] No syntax errors in log files

## Common Mistakes

❌ **Wrong location**: `custom_components/custom_components/switchbot_meter_time_sync`  
✅ **Correct**: `custom_components/switchbot_meter_time_sync`

❌ **Config reload only** (Developer Tools → YAML → Reload)  
✅ **Full restart** (Settings → System → Restart)

❌ **Missing translations folder**  
✅ **Has**: `translations/en.json`

❌ **Wrong file permissions** (chmod 600)  
✅ **Correct**: Files chmod 644, directories chmod 755

❌ **Old cached version**  
✅ **Clean install** after removing old version
