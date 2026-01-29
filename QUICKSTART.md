# Quick Start Guide

Get your SwitchBot Meter time syncing in 5 minutes!

## Step 1: Install (2 minutes)

1. Copy `switchbot_meter_time_sync` folder to `/config/custom_components/`
2. Restart Home Assistant

## Step 2: Add Device (1 minute)

**Option A - Auto Discovery:**
- Look for notification about discovered SwitchBot device
- Click "Configure"

**Option B - Manual:**
- Settings → Devices & Services → Add Integration
- Search "SwitchBot Meter Time Sync"
- Select your device

## Step 3: Test (30 seconds)

1. Find the new button: `button.switchbot_meter_XXXXX_sync_time`
2. Press it
3. Check your SwitchBot Meter - time should update!

## Step 4: Automate (1 minute)

Add to your `automations.yaml`:

```yaml
automation:
  - alias: "SwitchBot Daily Time Sync"
    trigger:
      - platform: time
        at: "00:00:00"
    action:
      - service: button.press
        target:
          entity_id: button.switchbot_meter_XXXXX_sync_time
```

Replace `XXXXX` with your device's ID.

## Step 5: Dashboard (30 seconds)

1. Edit your dashboard
2. Add a Button card
3. Select `button.switchbot_meter_XXXXX_sync_time`
4. Save

## Done! 🎉

Your SwitchBot Meter will now sync automatically every day at midnight.

## Common Automations

**Twice Daily:**
```yaml
trigger:
  - platform: time
    at: ["00:00:00", "12:00:00"]
```

**Weekly (Sundays):**
```yaml
trigger:
  - platform: time
    at: "03:00:00"
condition:
  - condition: time
    weekday: [sun]
```

**On HA Restart:**
```yaml
trigger:
  - platform: homeassistant
    event: start
action:
  - delay: "00:01:00"
  - service: button.press
    target:
      entity_id: button.switchbot_meter_XXXXX_sync_time
```

## Troubleshooting

**Not working?**
1. Check device is within Bluetooth range
2. Verify Bluetooth integration is active
3. Close SwitchBot app (device can only connect to one client)
4. Check logs: Settings → System → Logs

**Need help?** See INSTALLATION.md for detailed troubleshooting.

## What You Get

✅ No more manual time syncing via app  
✅ Automatic DST adjustments  
✅ Local control (no cloud)  
✅ Set-and-forget automation  

Enjoy!
