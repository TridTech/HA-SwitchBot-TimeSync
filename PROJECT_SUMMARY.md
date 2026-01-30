# SwitchBot Meter Time Sync - Project Summary

## Version 1.0.1 - Improved Discovery

**Latest Changes**:
- ✓ Fixed device discovery issues
- ✓ Added support for multiple service data UUIDs
- ✓ Better device identification (name, service data, manufacturer ID)
- ✓ Added comprehensive troubleshooting guide
- ✓ Included debug discovery script
- ✓ Improved logging for diagnostics

## What You Have

This is a complete, production-ready Home Assistant custom integration that enables automatic time synchronization for SwitchBot Meter Pro devices over Bluetooth.

## File Structure

```
switchbot_meter_time_sync/
├── Core Integration Files (Required)
│   ├── __init__.py              - Integration initialization
│   ├── manifest.json            - Integration metadata
│   ├── const.py                 - Constants and UUIDs
│   ├── config_flow.py           - UI configuration flow
│   ├── coordinator.py           - BLE communication handler
│   ├── button.py                - Button entity platform
│   └── strings.json             - UI text translations
│
├── Documentation
│   ├── README.md                - Main documentation (comprehensive)
│   ├── QUICKSTART.md            - 5-minute setup guide
│   ├── INSTALLATION.md          - Detailed installation guide
│   └── TECHNICAL.md             - Technical implementation details
│
├── Examples
│   └── examples/
│       └── automations.yaml     - Example automation configurations
│
├── Installation
│   ├── install.sh               - Automated installation script
│   └── hacs.json                - HACS metadata (future)
│
└── LICENSE                      - MIT license
```

## How to Use This Integration

### Installation (Choose One Method)

**Method 1: Automated Script**
```bash
cd switchbot_meter_time_sync
chmod +x install.sh
./install.sh
```

**Method 2: Manual Copy**
```bash
cp -r switchbot_meter_time_sync /path/to/homeassistant/config/custom_components/
```

**Method 3: Direct to Home Assistant**
1. Copy entire `switchbot_meter_time_sync` folder
2. Place in: `/config/custom_components/switchbot_meter_time_sync/`
3. Restart Home Assistant

### Setup in Home Assistant

1. **Restart** Home Assistant after copying files
2. Go to **Settings** → **Devices & Services** → **Add Integration**
3. Search for **"SwitchBot Meter Time Sync"**
4. Select your device or wait for auto-discovery
5. Click **Submit**

### Using the Integration

**Manual Sync:**
- Find button: `button.switchbot_meter_XXXXX_sync_time`
- Press to sync immediately

**Automatic Sync:**
Add to `automations.yaml`:
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

## Key Features

✅ **Local Bluetooth Communication** - No cloud required  
✅ **No SwitchBot App Needed** - Complete independence  
✅ **Automatic Discovery** - Devices detected automatically  
✅ **Simple Button Interface** - One-click manual sync  
✅ **Automation Ready** - Schedule syncs easily  
✅ **Multiple Device Support** - Sync all your meters  
✅ **Production Ready** - Error handling, logging, feedback  

## What It Does

1. **Discovers** SwitchBot Meter devices via Bluetooth
2. **Connects** to devices using BLE protocol
3. **Sends** time sync commands with current timestamp
4. **Confirms** successful synchronization
5. **Updates** device display time immediately

## Technical Highlights

- **Protocol**: SwitchBot BLE API (reverse engineered)
- **Commands**: Direct time management commands
- **Response**: Validates device acknowledgment
- **Error Handling**: Comprehensive retry and timeout logic
- **Logging**: Full debug capabilities

## Documentation Guide

📘 **Start Here**: README.md - Complete overview and features  
🚀 **Quick Setup**: QUICKSTART.md - Get running in 5 minutes  
🔧 **Detailed Setup**: INSTALLATION.md - Troubleshooting and advanced config  
⚙️ **Technical Info**: TECHNICAL.md - Protocol details and architecture  
📝 **Examples**: examples/automations.yaml - Ready-to-use automations  

## Requirements

- Home Assistant 2024.1.0+
- Bluetooth adapter configured in HA
- SwitchBot Meter Pro device(s)
- Python 3.11+ (included with HA)

## Dependencies

All dependencies are already included in Home Assistant:
- `bleak` - BLE communication library
- `bleak-retry-connector` - Reliable connection handling

## Next Steps

1. **Install the integration** (see INSTALLATION.md)
2. **Test the button** to verify it works
3. **Set up automation** for daily syncing
4. **Add to dashboard** for easy access
5. **Enjoy** never having to open the app again!

## Troubleshooting Quick Reference

**Integration not showing?**
- Verify files in `/config/custom_components/switchbot_meter_time_sync/`
- Restart Home Assistant
- Check logs for errors

**Device not found?**
- Ensure Bluetooth is enabled
- Move device closer
- Press button on device (pairing mode)

**Sync fails?**
- Check Bluetooth range
- Close SwitchBot app
- Verify battery level
- Check logs for details

**Need detailed help?**
See INSTALLATION.md Troubleshooting section

## Support and Contributing

- **Issues**: Report bugs with logs and HA version
- **Features**: Suggest improvements
- **Code**: PRs welcome (follow HA style guide)

## Credits

- BLE protocol from OpenWonderLabs/SwitchBotAPI-BLE
- Built with Home Assistant integration framework
- Uses Bleak for cross-platform BLE

## License

MIT License - Free to use, modify, and distribute

## Disclaimer

Unofficial integration, not affiliated with SwitchBot/WonderLabs Inc.

---

## Quick Command Reference

**Installation:**
```bash
./install.sh
```

**Enable Debug Logging:**
```yaml
logger:
  logs:
    custom_components.switchbot_meter_time_sync: debug
```

**Test Automation:**
```yaml
automation:
  - alias: "Test Sync"
    trigger:
      - platform: homeassistant
        event: start
    action:
      - service: button.press
        target:
          entity_id: button.switchbot_meter_XXXXX_sync_time
```

**Find Devices:**
Settings → Devices & Services → SwitchBot Meter Time Sync

---

Enjoy your automatically synced SwitchBot Meters! 🎉
