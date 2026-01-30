#!/usr/bin/env python3
"""
Validation script for SwitchBot Meter Time Sync integration.
Run this to check for common issues before installing.
"""

import os
import sys
import json

def check_file_exists(path, description):
    """Check if a file exists."""
    if os.path.exists(path):
        print(f"✓ {description}: {path}")
        return True
    else:
        print(f"✗ MISSING {description}: {path}")
        return False

def validate_json(path, description):
    """Validate a JSON file."""
    try:
        with open(path, 'r') as f:
            data = json.load(f)
        print(f"✓ {description} is valid JSON")
        return True
    except json.JSONDecodeError as e:
        print(f"✗ {description} has JSON errors: {e}")
        return False
    except Exception as e:
        print(f"✗ Error reading {description}: {e}")
        return False

def check_python_syntax(path, description):
    """Check Python file for syntax errors."""
    try:
        with open(path, 'r') as f:
            compile(f.read(), path, 'exec')
        print(f"✓ {description} has valid Python syntax")
        return True
    except SyntaxError as e:
        print(f"✗ {description} has syntax error: {e}")
        return False
    except Exception as e:
        print(f"✗ Error checking {description}: {e}")
        return False

def main():
    print("="*80)
    print("SwitchBot Meter Time Sync - Integration Validator")
    print("="*80)
    print()
    
    # Get script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    all_ok = True
    
    print("Checking required files...")
    print("-" * 80)
    
    # Check required Python files
    required_files = {
        "__init__.py": "Main integration file",
        "manifest.json": "Integration manifest",
        "const.py": "Constants",
        "config_flow.py": "Config flow",
        "coordinator.py": "Coordinator",
        "button.py": "Button platform",
        "strings.json": "UI strings",
    }
    
    for filename, description in required_files.items():
        path = os.path.join(script_dir, filename)
        if not check_file_exists(path, description):
            all_ok = False
    
    print()
    print("Validating JSON files...")
    print("-" * 80)
    
    # Validate JSON files
    json_files = {
        "manifest.json": "Manifest",
        "strings.json": "Strings",
    }
    
    for filename, description in json_files.items():
        path = os.path.join(script_dir, filename)
        if os.path.exists(path):
            if not validate_json(path, description):
                all_ok = False
    
    # Check translations
    trans_path = os.path.join(script_dir, "translations", "en.json")
    if os.path.exists(trans_path):
        if not validate_json(trans_path, "English translations"):
            all_ok = False
    
    print()
    print("Checking Python syntax...")
    print("-" * 80)
    
    # Check Python files
    python_files = {
        "__init__.py": "Main init",
        "const.py": "Constants",
        "config_flow.py": "Config flow",
        "coordinator.py": "Coordinator",
        "button.py": "Button platform",
    }
    
    for filename, description in python_files.items():
        path = os.path.join(script_dir, filename)
        if os.path.exists(path):
            if not check_python_syntax(path, description):
                all_ok = False
    
    print()
    print("Validating manifest.json content...")
    print("-" * 80)
    
    # Check manifest content
    manifest_path = os.path.join(script_dir, "manifest.json")
    if os.path.exists(manifest_path):
        try:
            with open(manifest_path, 'r') as f:
                manifest = json.load(f)
            
            # Check required fields
            required_fields = ["domain", "name", "version", "config_flow"]
            for field in required_fields:
                if field in manifest:
                    print(f"✓ Manifest has '{field}': {manifest[field]}")
                else:
                    print(f"✗ Manifest missing required field: {field}")
                    all_ok = False
            
            # Check domain matches
            expected_domain = "switchbot_meter_time_sync"
            if manifest.get("domain") == expected_domain:
                print(f"✓ Domain is correct: {expected_domain}")
            else:
                print(f"✗ Domain mismatch. Expected: {expected_domain}, Got: {manifest.get('domain')}")
                all_ok = False
            
            # Check config_flow is true
            if manifest.get("config_flow") is True:
                print("✓ Config flow is enabled")
            else:
                print(f"✗ Config flow should be true, got: {manifest.get('config_flow')}")
                all_ok = False
                
        except Exception as e:
            print(f"✗ Error validating manifest: {e}")
            all_ok = False
    
    print()
    print("Checking constants...")
    print("-" * 80)
    
    # Check const.py has DOMAIN
    const_path = os.path.join(script_dir, "const.py")
    if os.path.exists(const_path):
        try:
            with open(const_path, 'r') as f:
                content = f.read()
            if 'DOMAIN = "switchbot_meter_time_sync"' in content:
                print('✓ DOMAIN constant is correctly defined')
            else:
                print('✗ DOMAIN constant not found or incorrect')
                all_ok = False
        except Exception as e:
            print(f"✗ Error checking constants: {e}")
            all_ok = False
    
    print()
    print("="*80)
    if all_ok:
        print("✓ ALL CHECKS PASSED")
        print()
        print("The integration appears to be valid!")
        print("You can proceed with installation.")
    else:
        print("✗ SOME CHECKS FAILED")
        print()
        print("Please fix the errors above before installing.")
        sys.exit(1)
    print("="*80)

if __name__ == "__main__":
    main()
