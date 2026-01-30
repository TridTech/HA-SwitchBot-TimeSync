#!/bin/bash
# Installation script for SwitchBot Meter Time Sync
# This script copies the integration to your Home Assistant custom_components directory

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}SwitchBot Meter Time Sync - Installation Script${NC}"
echo "=================================================="
echo ""

# Check if running as root (not recommended for HA)
if [ "$EUID" -eq 0 ]; then 
    echo -e "${YELLOW}Warning: Running as root. Make sure this is what you want.${NC}"
fi

# Default Home Assistant config directory
HA_CONFIG_DIR="${HOME}/.homeassistant"

# Check for common HA installations
if [ -d "/config" ]; then
    HA_CONFIG_DIR="/config"
    echo -e "${GREEN}Detected Home Assistant OS/Supervised installation${NC}"
elif [ -d "${HOME}/homeassistant" ]; then
    HA_CONFIG_DIR="${HOME}/homeassistant"
    echo -e "${GREEN}Detected Home Assistant Container installation${NC}"
elif [ -d "${HOME}/.homeassistant" ]; then
    HA_CONFIG_DIR="${HOME}/.homeassistant"
    echo -e "${GREEN}Detected Home Assistant Core installation${NC}"
else
    echo -e "${YELLOW}Could not auto-detect Home Assistant directory${NC}"
    read -p "Enter your Home Assistant config directory path: " HA_CONFIG_DIR
fi

# Verify directory exists
if [ ! -d "$HA_CONFIG_DIR" ]; then
    echo -e "${RED}Error: Directory $HA_CONFIG_DIR does not exist${NC}"
    exit 1
fi

echo -e "Using config directory: ${GREEN}$HA_CONFIG_DIR${NC}"
echo ""

# Create custom_components directory if it doesn't exist
CUSTOM_DIR="$HA_CONFIG_DIR/custom_components"
if [ ! -d "$CUSTOM_DIR" ]; then
    echo "Creating custom_components directory..."
    mkdir -p "$CUSTOM_DIR"
fi

# Get the script's directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Check if integration files exist
if [ ! -f "$SCRIPT_DIR/manifest.json" ]; then
    echo -e "${RED}Error: Integration files not found in current directory${NC}"
    echo "Please run this script from the switchbot_meter_time_sync directory"
    exit 1
fi

# Target directory
TARGET_DIR="$CUSTOM_DIR/switchbot_meter_time_sync"

# Check if already installed
if [ -d "$TARGET_DIR" ]; then
    echo -e "${YELLOW}Integration already installed at: $TARGET_DIR${NC}"
    read -p "Do you want to overwrite? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Installation cancelled."
        exit 0
    fi
    echo "Removing old installation..."
    rm -rf "$TARGET_DIR"
fi

# Copy files
echo "Installing SwitchBot Meter Time Sync..."
cp -r "$SCRIPT_DIR" "$TARGET_DIR"

# Remove unnecessary files from installation
echo "Cleaning up..."
rm -f "$TARGET_DIR/install.sh"
rm -f "$TARGET_DIR/.git" 2>/dev/null
rm -rf "$TARGET_DIR/.github" 2>/dev/null
rm -rf "$TARGET_DIR/examples" 2>/dev/null

# Verify installation
if [ -f "$TARGET_DIR/manifest.json" ]; then
    echo -e "${GREEN}✓ Installation successful!${NC}"
    echo ""
    echo "Files installed to: $TARGET_DIR"
    echo ""
    echo "Next steps:"
    echo "1. Restart Home Assistant"
    echo "2. Go to Settings → Devices & Services → Add Integration"
    echo "3. Search for 'SwitchBot Meter Time Sync'"
    echo "4. Select your device and follow the setup wizard"
    echo ""
    echo "For detailed instructions, see INSTALLATION.md"
    echo "For quick start, see QUICKSTART.md"
else
    echo -e "${RED}✗ Installation failed${NC}"
    exit 1
fi
