#!/usr/bin/env python3
"""
SwitchBot Meter Device Discovery Debug Script

This script helps identify why your SwitchBot Meter might not be discovered.
Run this on your Home Assistant system to see what your device is advertising.

Usage:
  python3 debug_discovery.py

Requirements:
  - bleak library (pip install bleak)
  - Run with sufficient permissions for Bluetooth access
"""

import asyncio
import logging
from bleak import BleakScanner
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

SWITCHBOT_SERVICE_UUID = "cba20d00-224d-11e6-9fb8-0002a5d5c51b"
SWITCHBOT_SERVICE_DATA_UUID = "0000fd3d-0000-1000-8000-00805f9b34fb"
SWITCHBOT_MANUFACTURER_ID = 2409

DEVICE_TYPES = {
    0x54: "Meter/Meter Plus (Normal Mode)",
    0x74: "Meter/Meter Plus (Add Mode)",
    0x77: "Meter Pro",
    0x7A: "Meter Pro CO2",
}


def analyze_device(device, advertisement_data):
    """Analyze a BLE device to check if it's a SwitchBot Meter."""
    
    is_switchbot = False
    reasons = []
    
    print(f"\n{'='*80}")
    print(f"Device: {device.address}")
    print(f"Name: {device.name or 'Unknown'}")
    print(f"RSSI: {advertisement_data.rssi} dBm")
    print(f"-" * 80)
    
    # Check 1: Device name
    if device.name and ("WoSensorTH" in device.name or "WoIOSensorTH" in device.name):
        is_switchbot = True
        reasons.append(f"✓ Device name matches: {device.name}")
        print(f"  ✓ Name contains 'WoSensorTH': {device.name}")
    else:
        print(f"  ✗ Name does not contain 'WoSensorTH': {device.name}")
    
    # Check 2: Service UUIDs
    if advertisement_data.service_uuids:
        print(f"\n  Service UUIDs:")
        for uuid in advertisement_data.service_uuids:
            print(f"    - {uuid}")
            if SWITCHBOT_SERVICE_UUID.lower() in uuid.lower():
                is_switchbot = True
                reasons.append(f"✓ Service UUID matches: {uuid}")
    else:
        print(f"  ✗ No service UUIDs advertised")
    
    # Check 3: Service Data
    if advertisement_data.service_data:
        print(f"\n  Service Data:")
        for uuid, data in advertisement_data.service_data.items():
            data_hex = data.hex()
            print(f"    UUID: {uuid}")
            print(f"    Data: {data_hex} ({len(data)} bytes)")
            
            # Check for SwitchBot service data UUID
            if "fd3d" in uuid.lower() or SWITCHBOT_SERVICE_DATA_UUID.lower() in uuid.lower():
                is_switchbot = True
                reasons.append(f"✓ Service data UUID matches: {uuid}")
                
                # Parse device type
                if len(data) > 0:
                    device_type = data[0] & 0x7F
                    device_type_name = DEVICE_TYPES.get(device_type, f"Unknown (0x{device_type:02x})")
                    print(f"    Device Type: {device_type_name}")
                    
                    if device_type in DEVICE_TYPES:
                        reasons.append(f"✓ Device type recognized: {device_type_name}")
                    else:
                        print(f"    ⚠ Unknown device type: 0x{device_type:02x}")
                
                # Parse battery (if present)
                if len(data) > 2:
                    battery = data[2] & 0x7F
                    print(f"    Battery: {battery}%")
    else:
        print(f"  ✗ No service data advertised")
    
    # Check 4: Manufacturer Data
    if advertisement_data.manufacturer_data:
        print(f"\n  Manufacturer Data:")
        for mfr_id, data in advertisement_data.manufacturer_data.items():
            data_hex = data.hex()
            print(f"    Manufacturer ID: {mfr_id} (0x{mfr_id:04x})")
            print(f"    Data: {data_hex} ({len(data)} bytes)")
            
            if mfr_id == SWITCHBOT_MANUFACTURER_ID:
                is_switchbot = True
                reasons.append(f"✓ Manufacturer ID matches SwitchBot: {mfr_id}")
                
                # Try to parse temperature/humidity from manufacturer data
                if len(data) >= 13:
                    try:
                        # Outdoor Meter format
                        byte10 = data[10]
                        byte11 = data[11]
                        byte12 = data[12]
                        
                        temp_c = ((byte10 & 0x0F) * 0.1 + (byte11 & 0x7F))
                        if (byte11 & 0x80) == 0:
                            temp_c = -temp_c
                        humidity = byte12 & 0x7F
                        
                        print(f"    Temperature: {temp_c:.1f}°C")
                        print(f"    Humidity: {humidity}%")
                    except Exception as e:
                        print(f"    Could not parse sensor data: {e}")
    else:
        print(f"  ✗ No manufacturer data advertised")
    
    # Summary
    print(f"\n  {'='*76}")
    if is_switchbot:
        print(f"  ✓ THIS APPEARS TO BE A SWITCHBOT METER")
        print(f"\n  Detection reasons:")
        for reason in reasons:
            print(f"    - {reason}")
    else:
        print(f"  ✗ THIS DOES NOT APPEAR TO BE A SWITCHBOT METER")
        print(f"    The device did not match any SwitchBot identification criteria.")
    print(f"  {'='*76}")
    
    return is_switchbot


async def scan_for_switchbot():
    """Scan for BLE devices and identify potential SwitchBot Meters."""
    
    print("\n" + "="*80)
    print("SwitchBot Meter Discovery Debug Tool")
    print("="*80)
    print("\nScanning for Bluetooth devices...")
    print("This will take about 10 seconds...\n")
    
    switchbot_count = 0
    total_count = 0
    
    def detection_callback(device, advertisement_data):
        nonlocal switchbot_count, total_count
        total_count += 1
        
        if analyze_device(device, advertisement_data):
            switchbot_count += 1
    
    scanner = BleakScanner(detection_callback=detection_callback)
    
    await scanner.start()
    await asyncio.sleep(10)
    await scanner.stop()
    
    print("\n" + "="*80)
    print("SCAN COMPLETE")
    print("="*80)
    print(f"Total devices found: {total_count}")
    print(f"SwitchBot Meters found: {switchbot_count}")
    
    if switchbot_count == 0:
        print("\n⚠ NO SWITCHBOT METERS DETECTED")
        print("\nTroubleshooting tips:")
        print("1. Make sure your SwitchBot Meter has batteries installed")
        print("2. Press and hold the button on top for 2-3 seconds to enter pairing mode")
        print("3. Move the device closer to your Bluetooth adapter")
        print("4. Remove the device from the SwitchBot app temporarily")
        print("5. Try a factory reset (see documentation)")
    else:
        print(f"\n✓ Found {switchbot_count} SwitchBot Meter(s)")
        print("\nIf the integration still can't find your device:")
        print("1. Copy the MAC address from above")
        print("2. Check Home Assistant logs with debug enabled")
        print("3. Open a GitHub issue with this output")
    
    print("\n")


if __name__ == "__main__":
    try:
        asyncio.run(scan_for_switchbot())
    except KeyboardInterrupt:
        print("\n\nScan interrupted by user")
    except Exception as e:
        print(f"\n\nError: {e}")
        print("\nMake sure you have the required dependencies:")
        print("  pip install bleak")
