#!/usr/bin/env python3
"""
Build helper script for cross-platform builds.
Usage: python build_helper.py --platform [macos|linux|windows] --version [VERSION] [--portable] [--installer]
"""

import os
import sys
import argparse
import shutil
import subprocess
import uuid
from pathlib import Path


def parse_args():
    parser = argparse.ArgumentParser(
        description="Build MIDI/HID Inspektr for different platforms"
    )
    parser.add_argument(
        "--platform",
        choices=["macos", "linux", "windows"],
        required=True,
        help="Platform to build for",
    )
    parser.add_argument("--version", required=True, help="Version string")
    parser.add_argument(
        "--portable", 
        action="store_true", 
        help="Build portable single-file executable (Windows only)"
    )
    parser.add_argument(
        "--installer", 
        action="store_true", 
        help="Build installer (Windows only)"
    )
    return parser.parse_args()


def update_spec_file(platform, version, portable=False):
    """Update the spec file with platform-specific settings"""

    app_name = "MIDI-HID Inspektr"
    file_safe_name = "MIDI-HID-Inspektr"  # No spaces for filenames
    
    if portable and platform == "windows":
        spec_template = Path("MIDI-HID Inspektr.spec.portable.template").read_text()
    else:
        spec_template = Path("MIDI-HID Inspektr.spec.template").read_text()

    # Common replacements
    replacements = {
        "{{VERSION}}": version,
        "{{APP_NAME}}": app_name,
        "{{FILE_SAFE_NAME}}": file_safe_name,
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
        spec_template = spec_template.replace(key, str(value))

    # Write platform-specific spec file
    spec_filename = "MIDI-HID Inspektr.spec"
    if portable and platform == "windows":
        spec_filename = "MIDI-HID Inspektr.portable.spec"
        
    with open(spec_filename, "w") as f:
        f.write(spec_template)

    print(f"Updated spec file {spec_filename} for {platform}")
    return spec_filename


def create_inno_setup_script(version):
    """Create Inno Setup script for Windows installer"""
    app_name = "MIDI-HID Inspektr"
    file_safe_name = "MIDI-HID-Inspektr"
    publisher = "YourAshp8i"
    website = "https://github.com/yourashp8i/midi-hid-inspektr"
    
    # Create a UUID for the app if it doesn't exist
    app_guid_file = Path(".app_guid")
    if app_guid_file.exists():
        app_guid = app_guid_file.read_text().strip()
    else:
        app_guid = str(uuid.uuid4())
        app_guid_file.write_text(app_guid)
    
    inno_script = f"""
#define MyAppName "{app_name}"
#define MyAppVersion "{version}"
#define MyAppPublisher "{publisher}"
#define MyAppURL "{website}"
#define MyAppExeName "{app_name}.exe"

[Setup]
AppId={{{{{app_guid}}}}}
AppName={{#MyAppName}}
AppVersion={{#MyAppVersion}}
AppPublisher={{#MyAppPublisher}}
AppPublisherURL={{#MyAppURL}}
AppSupportURL={{#MyAppURL}}
AppUpdatesURL={{#MyAppURL}}
DefaultDirName={{autopf}}\\{{#MyAppName}}
DefaultGroupName={{#MyAppName}}
AllowNoIcons=yes
; Create license file from README if it doesn't exist
; LicenseFile=LICENSE.txt
OutputDir=installer
OutputBaseFilename={file_safe_name}-{version}-Setup
SetupIconFile=resources/icons/app_icon.ico
Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{{cm:CreateDesktopIcon}}"; GroupDescription: "{{cm:AdditionalIcons}}"; Flags: unchecked

[Files]
Source: "dist\\{app_name}\\*"; DestDir: "{{app}}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{{group}}\\{{#MyAppName}}"; Filename: "{{app}}\\{{#MyAppExeName}}"
Name: "{{group}}\\{{cm:UninstallProgram,{{#MyAppName}}}}"; Filename: "{{uninstallexe}}"
Name: "{{autodesktop}}\\{{#MyAppName}}"; Filename: "{{app}}\\{{#MyAppExeName}}"; Tasks: desktopicon

[Run]
Filename: "{{app}}\\{{#MyAppExeName}}"; Description: "{{cm:LaunchProgram,{{#StringChange(MyAppName, '&', '&&')}}}}"; Flags: nowait postinstall skipifsilent
    """
    
    os.makedirs("installer", exist_ok=True)
    inno_script_path = "installer/setup.iss"
    with open(inno_script_path, "w") as f:
        f.write(inno_script)
    
    print(f"Created Inno Setup script: {inno_script_path}")
    return inno_script_path


def build_windows(version, portable=False, installer=False):
    """Build Windows application"""
    app_name = "MIDI-HID Inspektr"
    file_safe_name = "MIDI-HID-Inspektr"
    
    # Clean build directories
    if os.path.exists("dist"):
        shutil.rmtree("dist")
    if os.path.exists("build"):
        shutil.rmtree("build")
    
    # Create portable spec template if it doesn't exist
    portable_spec_template = Path("MIDI-HID Inspektr.spec.portable.template")
    if not portable_spec_template.exists() and portable:
        print("Creating portable spec template...")
        # This template is modified for --onefile mode
        portable_template = """# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('resources', 'resources'),
        # Add other data files your app needs
    ],
    hiddenimports=[
        'PySide6.QtSvg',
        'PySide6.QtXml',
        'rtmidi',
        'hid',
        # Add other hidden imports
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='{{APP_NAME}}',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    icon='{{ICON_PATH}}',
    version='{{VERSION}}',
)
"""
        portable_spec_template.write_text(portable_template)
    
    # Build standard version (directory structure)
    if not portable or installer:
        spec_file = update_spec_file("windows", version)
        print("Building standard Windows version...")
        subprocess.run(["pyinstaller", "--clean", spec_file], check=True)
        print("Standard Windows build completed")
    
    # Build portable version
    if portable:
        portable_spec_file = update_spec_file("windows", version, portable=True)
        print("Building portable Windows version...")
        subprocess.run(["pyinstaller", "--clean", portable_spec_file], check=True)
        # Rename output to include portable in the name
        portable_exe = f"dist/{app_name}.exe"
        if os.path.exists(portable_exe):
            portable_output = f"dist/{file_safe_name}-{version}-Portable.exe"
            shutil.move(portable_exe, portable_output)
            print(f"Created portable executable: {portable_output}")
    
    # Create installer if requested
    if installer:
        print("Creating Windows installer...")
        inno_script = create_inno_setup_script(version)
        
        # Check if Inno Setup is installed
        inno_compiler = None
        possible_paths = [
            r"C:\Program Files (x86)\Inno Setup 6\ISCC.exe",
            r"C:\Program Files\Inno Setup 6\ISCC.exe",
            # Add other possible paths
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                inno_compiler = path
                break
        
        if inno_compiler:
            print(f"Building installer using Inno Setup: {inno_compiler}")
            subprocess.run([inno_compiler, inno_script], check=True)
            print(f"Installer created: installer/{file_safe_name}-{version}-Setup.exe")
        else:
            print("Inno Setup not found. Please install Inno Setup and add it to PATH.")
            print(f"Manually compile the installer script: {inno_script}")


def build(platform, version, portable=False, installer=False):
    """Build the application for the specified platform"""
    if platform == "windows":
        build_windows(version, portable, installer)
    else:
        # For macOS and Linux, use the standard build process
        spec_file = update_spec_file(platform, version)
        
        # Ensure clean build
        if os.path.exists("dist"):
            shutil.rmtree("dist")
        if os.path.exists("build"):
            shutil.rmtree("build")
        
        # Build command
        cmd = ["pyinstaller", "--clean", spec_file]
        
        # Run build
        print(f"Building for {platform}...")
        subprocess.run(cmd, check=True)
        print(f"Build completed for {platform}")


def main():
    args = parse_args()
    
    # Validate Windows-specific options
    if args.platform != "windows" and (args.portable or args.installer):
        print("Warning: --portable and --installer options are only available for Windows")
    
    build(args.platform, args.version, args.portable, args.installer)


if __name__ == "__main__":
    main()