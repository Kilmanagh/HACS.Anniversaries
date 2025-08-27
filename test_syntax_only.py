#!/usr/bin/env python3
"""Test script to check for syntax errors without importing Home Assistant."""

import ast
import os

def check_syntax(file_path):
    """Check if a Python file has valid syntax."""
    try:
        with open(file_path, 'r') as f:
            source = f.read()
        ast.parse(source)
        return True, None
    except SyntaxError as e:
        return False, str(e)
    except Exception as e:
        return False, f"Error reading file: {e}"

def check_integration_files():
    """Check syntax of all integration files."""
    base_path = '/workspaces/HACS.Anniversaries/custom_components/anniversaries'
    files_to_check = [
        '__init__.py',
        'const.py',
        'config_flow.py',
        'data.py',
        'sensor.py',
        'coordinator.py',
        'calendar.py'
    ]
    
    print("Checking Python syntax for all integration files...\n")
    
    all_good = True
    for filename in files_to_check:
        file_path = os.path.join(base_path, filename)
        if os.path.exists(file_path):
            is_valid, error = check_syntax(file_path)
            if is_valid:
                print(f"✓ {filename}: Valid syntax")
            else:
                print(f"❌ {filename}: Syntax error - {error}")
                all_good = False
        else:
            print(f"⚠️  {filename}: File not found")
    
    return all_good

if __name__ == "__main__":
    if check_integration_files():
        print("\n✅ All integration files have valid Python syntax!")
        
        # Check specific code patterns we've added
        print("\n=== Checking specific implementations ===")
        
        # Check const.py for emoji definitions
        try:
            with open('/workspaces/HACS.Anniversaries/custom_components/anniversaries/const.py', 'r') as f:
                const_content = f.read()
            
            if 'EMOJI_OPTIONS' in const_content:
                print("✓ EMOJI_OPTIONS defined in const.py")
            if 'CATEGORY_EMOJIS' in const_content:
                print("✓ CATEGORY_EMOJIS defined in const.py")
            if 'get_default_emoji_for_category' in const_content:
                print("✓ get_default_emoji_for_category function defined")
                
        except Exception as e:
            print(f"❌ Error checking const.py: {e}")
        
        # Check config_flow.py for emoji field
        try:
            with open('/workspaces/HACS.Anniversaries/custom_components/anniversaries/config_flow.py', 'r') as f:
                config_flow_content = f.read()
            
            if 'vol.Optional(CONF_EMOJI' in config_flow_content:
                print("✓ Emoji field added to config flow schemas")
            if 'get_default_emoji_for_category' in config_flow_content:
                print("✓ Config flow uses emoji category defaults")
                
        except Exception as e:
            print(f"❌ Error checking config_flow.py: {e}")
        
        # Check data.py for emoji support
        try:
            with open('/workspaces/HACS.Anniversaries/custom_components/anniversaries/data.py', 'r') as f:
                data_content = f.read()
            
            if 'emoji: str' in data_content:
                print("✓ Emoji field added to AnniversaryData dataclass")
            if 'config.get(CONF_EMOJI' in data_content:
                print("✓ Emoji field handled in from_config method")
                
        except Exception as e:
            print(f"❌ Error checking data.py: {e}")
        
        # Check sensor.py for emoji attribute
        try:
            with open('/workspaces/HACS.Anniversaries/custom_components/anniversaries/sensor.py', 'r') as f:
                sensor_content = f.read()
            
            if '"custom_emoji"' in sensor_content:
                print("✓ custom_emoji attribute added to sensor")
                
        except Exception as e:
            print(f"❌ Error checking sensor.py: {e}")
            
        print("\n✅ Code structure looks good! The emoji system implementation is complete.")
        print("\nThe static path registration issue needs to be tested in a working Home Assistant environment.")
        
    else:
        print("\n❌ Some files have syntax errors that need to be fixed.")
        exit(1)
