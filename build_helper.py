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
        help="Build portable single-file executable (Windows only)",
    )
    parser.add_argument(
        "--installer", action="store_true", help="Build installer (Windows only)"
    )
    parser.add_argument(
        "--project-path",
        help="Path to project directory (defaults to current directory)",
    )
    return parser.parse_args()


def setup_environment(project_path=None):
    """Set up environment variables for the build process"""
    # If project path is provided, add it to PYTHONPATH
    if project_path:
        # Check if the provided path actually exists
        if not os.path.exists(project_path):
            print(f"Warning: The provided path '{project_path}' does not exist.")
            print("Using current directory instead.")
            project_path = os.path.abspath(os.curdir)
        else:
            project_path = os.path.abspath(project_path)
            print(f"Setting PYTHONPATH to: {project_path}")

            # Add to Python path for the current process
            sys.path.insert(0, project_path)

            # Set environment variable for child processes
            os.environ["PYTHONPATH"] = project_path

            # Change to project directory
            os.chdir(project_path)
    else:
        # Get current directory as project path
        project_path = os.path.abspath(os.curdir)
        print(f"Using current directory as project path: {project_path}")
        os.environ["PYTHONPATH"] = project_path

    return project_path


def update_spec_file(platform, version, portable=False, project_path="."):
    """Update the spec file with platform-specific settings"""

    app_name = "MIDI-HID Inspektr"
    file_safe_name = "MIDI-HID-Inspektr"  # No spaces for filenames

    # Check if templates exist
    standard_template_path = os.path.join(
        project_path, "MIDI-HID Inspektr.spec.template"
    )
    portable_template_path = os.path.join(
        project_path, "MIDI-HID Inspektr.spec.portable.template"
    )

    if portable and platform == "windows":
        if not os.path.exists(portable_template_path):
            create_portable_spec_template(portable_template_path)
        spec_template = Path(portable_template_path).read_text()
    else:
        if not os.path.exists(standard_template_path):
            create_standard_spec_template(standard_template_path)
        spec_template = Path(standard_template_path).read_text()

    # Common replacements
    replacements = {
        "{{VERSION}}": version,
        "{{APP_NAME}}": app_name,
        "{{FILE_SAFE_NAME}}": file_safe_name,
    }

    # Platform-specific replacements
    if platform == "macos":
        icon_path = os.path.join(project_path, "resources/icons/app_icon.icns")
        replacements["{{ICON_PATH}}"] = str(
            Path(icon_path).as_posix()
        )  # Convert to forward slashes
        replacements["{{BUNDLE_ID}}"] = "com.yourashp8i.midiinspektr"
    elif platform == "linux":
        icon_path = os.path.join(project_path, "resources/icons/app_icon.png")
        replacements["{{ICON_PATH}}"] = str(
            Path(icon_path).as_posix()
        )  # Convert to forward slashes
        replacements["{{BUNDLE_ID}}"] = ""  # Not used on Linux
    elif platform == "windows":
        icon_path = os.path.join(project_path, "resources/icons/app_icon.ico")
        replacements["{{ICON_PATH}}"] = str(
            Path(icon_path).as_posix()
        )  # Convert to forward slashes
        replacements["{{BUNDLE_ID}}"] = ""  # Not used on Windows

    # Apply replacements
    for key, value in replacements.items():
        spec_template = spec_template.replace(key, str(value))

    # Write platform-specific spec file
    spec_filename = os.path.join(project_path, "MIDI-HID Inspektr.spec")
    if portable and platform == "windows":
        spec_filename = os.path.join(project_path, "MIDI-HID Inspektr.portable.spec")

    with open(spec_filename, "w") as f:
        f.write(spec_template)

    print(f"Updated spec file {spec_filename} for {platform}")
    return spec_filename


def create_standard_spec_template(template_path):
    """Create a standard spec template if it doesn't exist"""
    print(f"Creating standard spec template at {template_path}...")
    template = """# -*- mode: python ; coding: utf-8 -*-

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
    [],
    exclude_binaries=True,
    name='{{APP_NAME}}',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    icon='{{ICON_PATH}}',
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='{{APP_NAME}}',
)
    """
    os.makedirs(os.path.dirname(template_path), exist_ok=True)
    with open(template_path, "w") as f:
        f.write(template)


def create_portable_spec_template(template_path):
    """Create a portable spec template if it doesn't exist"""
    print(f"Creating portable spec template at {template_path}...")
    template = """# -*- mode: python ; coding: utf-8 -*-

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
)
"""
    os.makedirs(os.path.dirname(template_path), exist_ok=True)
    with open(template_path, "w") as f:
        f.write(template)


def create_inno_setup_script(version, project_path="."):
    """Create Inno Setup script for Windows installer"""
    app_name = "MIDI-HID Inspektr"
    file_safe_name = "MIDI-HID-Inspektr"
    publisher = "YourAshp8i"
    website = "https://github.com/yourashp8i/midi-hid-inspektr"

    # Create a UUID for the app if it doesn't exist
    app_guid_file = Path(os.path.join(project_path, ".app_guid"))
    if app_guid_file.exists():
        app_guid = app_guid_file.read_text().strip()
    else:
        app_guid = str(uuid.uuid4())
        app_guid_file.write_text(app_guid)

    # Paths
    dist_path = os.path.join(project_path, "dist", app_name)
    icon_path = os.path.join(project_path, "resources/icons/app_icon.ico")

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
OutputDir={os.path.join(project_path, "installer")}
OutputBaseFilename={file_safe_name}-{version}-Setup
SetupIconFile={icon_path}
Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{{cm:CreateDesktopIcon}}"; GroupDescription: "{{cm:AdditionalIcons}}"; Flags: unchecked

[Files]
Source: "{dist_path}\\*"; DestDir: "{{app}}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{{group}}\\{{#MyAppName}}"; Filename: "{{app}}\\{{#MyAppExeName}}"
Name: "{{group}}\\{{cm:UninstallProgram,{{#MyAppName}}}}"; Filename: "{{uninstallexe}}"
Name: "{{autodesktop}}\\{{#MyAppName}}"; Filename: "{{app}}\\{{#MyAppExeName}}"; Tasks: desktopicon

[Run]
Filename: "{{app}}\\{{#MyAppExeName}}"; Description: "{{cm:LaunchProgram,{{#StringChange(MyAppName, '&', '&&')}}}}"; Flags: nowait postinstall skipifsilent
    """

    installer_dir = os.path.join(project_path, "installer")
    os.makedirs(installer_dir, exist_ok=True)
    inno_script_path = os.path.join(installer_dir, "setup.iss")
    with open(inno_script_path, "w") as f:
        f.write(inno_script)

    print(f"Created Inno Setup script: {inno_script_path}")
    return inno_script_path


def create_macos_dmg(app_path, version, project_path="."):
    """Create a DMG installer for macOS"""
    app_name = "MIDI-HID Inspektr"
    dmg_name = f"MIDI-HID-Inspektr-{version}"

    # Create a directory for DMG resources if it doesn't exist
    dmg_resources = os.path.join(project_path, "dmg_resources")
    os.makedirs(dmg_resources, exist_ok=True)

    # Path to the background image (create this 540x380 pixel image)
    background_path = os.path.join(project_path, "resources/dmg_background.png")

    # Build the DMG command
    cmd = [
        "create-dmg",
        "--volname",
        f"{app_name} Installer",
        "--background",
        background_path,
        "--window-pos",
        "200",
        "120",
        "--window-size",
        "540",
        "380",
        "--icon-size",
        "100",
        "--icon",
        f"{app_name}.app",
        "140",
        "150",
        "--app-drop-link",
        "400",
        "150",
        "--no-internet-enable",
        f"{dmg_name}.dmg",
        app_path,
    ]

    try:
        # Execute the command
        print(f"Creating DMG for {app_name}...")
        subprocess.run(cmd, check=True)
        print(f"DMG created: {dmg_name}.dmg")
        return os.path.abspath(f"{dmg_name}.dmg")
    except subprocess.CalledProcessError as e:
        print(f"Failed to create DMG: {e}")
        return None


# Alternative version using hdiutil (if you prefer this option)
def create_macos_dmg_with_hdiutil(app_path, version, project_path="."):
    """Create a basic DMG installer using hdiutil"""
    app_name = "MIDI-HID Inspektr"
    dmg_name = f"MIDI-HID-Inspektr-{version}"

    # Create a temporary directory
    temp_dir = os.path.join(project_path, "temp_dmg")
    os.makedirs(temp_dir, exist_ok=True)

    # Copy the .app to the temporary directory
    app_in_temp = os.path.join(temp_dir, f"{app_name}.app")
    if os.path.exists(app_in_temp):
        shutil.rmtree(app_in_temp)
    shutil.copytree(app_path, app_in_temp)

    # Create a symbolic link to /Applications
    applications_link = os.path.join(temp_dir, "Applications")
    if os.path.exists(applications_link):
        os.remove(applications_link)
    os.symlink("/Applications", applications_link)

    # Create the DMG
    dmg_path = os.path.join(project_path, f"{dmg_name}.dmg")
    if os.path.exists(dmg_path):
        os.remove(dmg_path)

    subprocess.run(
        [
            "hdiutil",
            "create",
            "-volname",
            f"{app_name} Installer",
            "-srcfolder",
            temp_dir,
            "-ov",
            "-format",
            "UDZO",
            dmg_path,
        ],
        check=True,
    )

    # Clean up
    shutil.rmtree(temp_dir)

    print(f"DMG created: {dmg_path}")
    return os.path.abspath(dmg_path)


def build_macos(version, project_path="."):
    # Update spec file
    spec_file = update_spec_file("macos", version, project_path=project_path)

    # Build with PyInstaller
    build_command = ["pyinstaller", "--clean", spec_file]
    subprocess.run(build_command, check=True)

    # Locate the .app file in the dist directory
    app_path = os.path.join(project_path, "dist", "MIDI-HID Inspektr.app")

    # Create DMG
    dmg_path = create_macos_dmg(app_path, version, project_path)
    # Or if you prefer the hdiutil version:
    # dmg_path = create_macos_dmg_with_hdiutil(app_path, version, project_path)

    # Return paths to built artifacts
    return {"app": app_path, "dmg": dmg_path}


def build_windows(version, portable=False, installer=False, project_path="."):
    """Build Windows application"""
    app_name = "MIDI-HID Inspektr"
    file_safe_name = "MIDI-HID-Inspektr"

    # Clean build directories
    dist_dir = os.path.join(project_path, "dist")
    build_dir = os.path.join(project_path, "build")

    if os.path.exists(dist_dir):
        shutil.rmtree(dist_dir)
    if os.path.exists(build_dir):
        shutil.rmtree(build_dir)

    # Build standard version (directory structure)
    if not portable or installer:
        spec_file = update_spec_file("windows", version, project_path=project_path)
        print("Building standard Windows version...")
        subprocess.run(["pyinstaller", "--clean", spec_file], check=True)
        print("Standard Windows build completed")

    # Build portable version
    if portable:
        portable_spec_file = update_spec_file(
            "windows", version, portable=True, project_path=project_path
        )
        print("Building portable Windows version...")
        subprocess.run(["pyinstaller", "--clean", portable_spec_file], check=True)
        # Rename output to include portable in the name
        portable_exe = os.path.join(project_path, f"dist/{app_name}.exe")
        if os.path.exists(portable_exe):
            portable_output = os.path.join(
                project_path, f"dist/{file_safe_name}-{version}-Portable.exe"
            )
            shutil.move(portable_exe, portable_output)
            print(f"Created portable executable: {portable_output}")

    # Create installer if requested
    if installer:
        print("Creating Windows installer...")
        inno_script = create_inno_setup_script(version, project_path=project_path)

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
            print(
                f"Installer created: {os.path.join(project_path, 'installer', f'{file_safe_name}-{version}-Setup.exe')}"
            )
        else:
            print("Inno Setup not found. Please install Inno Setup and add it to PATH.")
            print(f"Manually compile the installer script: {inno_script}")


def build(platform, version, portable=False, installer=False, project_path="."):
    """Build the application for the specified platform"""
    if platform == "windows":
        build_windows(version, portable, installer, project_path)
    else:
        # For macOS and Linux, use the standard build process
        spec_file = update_spec_file(platform, version, project_path=project_path)

        # Ensure clean build
        dist_dir = os.path.join(project_path, "dist")
        build_dir = os.path.join(project_path, "build")

        if os.path.exists(dist_dir):
            shutil.rmtree(dist_dir)
        if os.path.exists(build_dir):
            shutil.rmtree(build_dir)

        # Build command
        cmd = ["pyinstaller", "--clean", spec_file]

        # Run build
        print(f"Building for {platform}...")
        subprocess.run(cmd, check=True)
        print(f"Build completed for {platform}")


def main():
    args = parse_args()

    # Set up the environment
    project_path = setup_environment(args.project_path)

    # Validate Windows-specific options
    if args.platform != "windows" and (args.portable or args.installer):
        print(
            "Warning: --portable and --installer options are only available for Windows"
        )

    build(args.platform, args.version, args.portable, args.installer, project_path)


if __name__ == "__main__":
    main()
