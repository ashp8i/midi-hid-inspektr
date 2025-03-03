#!/usr/bin/env python3
"""
Build helper script for cross-platform builds.
Usage: python build_helper.py --platform [macos|linux|windows] --version [VERSION]
"""

import os
import sys
import argparse
import shutil
import subprocess
from pathlib import Path

def parse_args():
    parser = argparse.ArgumentParser(description='Build MIDI/HID Inspektr for different platforms')
    parser.add_argument('--platform', choices=['macos', 'linux', 'windows'], required=True,
                        help='Platform to build for')
    parser.add_argument('--version', required=True, help='Version string')
    return parser.parse_args()

def update_spec_file(platform, version):
    """Update the spec file with platform-specific settings"""
    
    spec_template = Path("MIDI-HID Inspektr.spec.template").read_text()
    
    # Common replacements
    replacements = {
        "{{VERSION}}": version,
        "{{APP_NAME}}": "MIDI-HID Inspektr",
    }
    
    # Platform-specific replacements
    if platform == "macos":
        replacements["{{ICON_PATH}}"] = "resources/icons/app_icon.icns"
        replacements["{{BUNDLE_ID}}"] = "com.yourashp8i.midiinspektr"
    elif platform == "linux":
        replacements["{{ICON_PATH}}"] = "resources/icons/app_icon.png"
        replacements["{{BUNDLE_ID}}"] = ""  # Not used on Linux
    elif platform == "windows":
        replacements["{{ICON_PATH}}"] = "resources/icons/app_icon.ico"
        replacements["{{BUNDLE_ID}}"] = ""  # Not used on Windows
    
    # Apply replacements
    for key, value in replacements.items():
        spec_template = spec_template.replace(key, value)
    
    # Write platform-specific spec file
    with open("MIDI-HID Inspektr.spec", "w") as f:
        f.write(spec_template)
    
    print(f"Updated spec file for {platform}")

def build(platform, version):
    """Build the application using PyInstaller"""
    update_spec_file(platform, version)
    
    # Ensure clean build
    if os.path.exists("dist"):
        shutil.rmtree("dist")
    if os.path.exists("build"):
        shutil.rmtree("build")
    
    # Build command
    cmd = ["pyinstaller", "--clean", "MIDI-HID Inspektr.spec"]
    
    # Run build
    print(f"Building for {platform}...")
    subprocess.run(cmd, check=True)
    print(f"Build completed for {platform}")

def main():
    args = parse_args()
    build(args.platform, args.version)

if __name__ == "__main__":
    main()