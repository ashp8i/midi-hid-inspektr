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
    background_path = os.path.join(project_path, "resources/images/dmg_background.png")

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


def create_linux_packages(app_path, version, project_path="."):
    """Create various Linux packages (.deb, .rpm, AppImage)"""
    import subprocess
    import os
    import shutil
    import tempfile
    from pathlib import Path

    app_name = "MIDI-HID Inspektr"
    file_safe_name = (
        "midi-hid-inspektr"  # Linux package names should be lowercase with hyphens
    )
    description = "Tool for inspecting MIDI and HID devices"
    maintainer = "YourAshp8i <your.email@example.com>"
    website = "https://github.com/yourashp8i/midi-hid-inspektr"
    license_type = "MIT"  # Adjust according to your project

    print("Creating Linux packages...")
    results = {}

    # Prepare desktop entry
    desktop_file_content = f"""[Desktop Entry]
Name={app_name}
Comment={description}
Exec=/usr/bin/{file_safe_name}
Icon=/usr/share/pixmaps/{file_safe_name}.png
Terminal=false
Type=Application
Categories=Utility;AudioVideo;Music;
Keywords=MIDI;HID;USB;Inspector;
"""

    # Create a temp directory for packaging
    temp_dir = os.path.join(project_path, "linux_packaging")
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    os.makedirs(temp_dir, exist_ok=True)

    # Create desktop file
    desktop_file_path = os.path.join(temp_dir, f"{file_safe_name}.desktop")
    with open(desktop_file_path, "w") as f:
        f.write(desktop_file_content)

    # Copy icon for packaging
    icon_source = os.path.join(project_path, "resources/icons/app_icon.png")
    icon_dest = os.path.join(temp_dir, f"{file_safe_name}.png")
    shutil.copy(icon_source, icon_dest)

    # Create .deb package using fpm if available
    try:
        print("Creating .deb package...")
        deb_path = os.path.join(project_path, f"{file_safe_name}_{version}_amd64.deb")

        # Make sure the app binary is executable
        app_binary = os.path.join(app_path, app_name)
        if os.path.exists(app_binary):
            os.chmod(app_binary, 0o755)

        # Build .deb package using fpm
        cmd = [
            "fpm",
            "-s",
            "dir",
            "-t",
            "deb",
            "-n",
            file_safe_name,
            "-v",
            version,
            "--description",
            description,
            "--url",
            website,
            "--maintainer",
            maintainer,
            "--license",
            license_type,
            "--category",
            "utils",
            "--deb-no-default-config-files",
            f"{app_path}/={'/usr/lib/' + file_safe_name}",
            f"{desktop_file_path}=/usr/share/applications/{file_safe_name}.desktop",
            f"{icon_dest}=/usr/share/pixmaps/{file_safe_name}.png",
        ]

        # Create a wrapper script that launches the application
        wrapper_script = os.path.join(temp_dir, file_safe_name)
        with open(wrapper_script, "w") as f:
            f.write(
                f"""#!/bin/sh
exec /usr/lib/{file_safe_name}/{app_name} "$@"
"""
            )
        os.chmod(wrapper_script, 0o755)

        # Add the wrapper script to the package
        cmd.append(f"{wrapper_script}=/usr/bin/{file_safe_name}")

        # Run fpm to create the .deb package
        subprocess.run(cmd, check=True)
        results["deb"] = deb_path
        print(f"Created .deb package: {deb_path}")

        # Create .rpm package based on the .deb
        print("Creating .rpm package...")
        rpm_path = os.path.join(
            project_path, f"{file_safe_name}-{version}-1.x86_64.rpm"
        )
        rpm_cmd = ["fpm", "-s", "deb", "-t", "rpm", deb_path]
        subprocess.run(rpm_cmd, check=True)
        results["rpm"] = rpm_path
        print(f"Created .rpm package: {rpm_path}")

    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print(f"Error creating .deb/.rpm packages: {e}")
        print("Make sure 'fpm' is installed: gem install fpm")

    # Create AppImage if appimagetool is available
    try:
        print("Creating AppImage...")
        # Set up AppDir structure
        appdir = os.path.join(temp_dir, "AppDir")
        os.makedirs(appdir, exist_ok=True)

        # Copy the app to AppDir
        app_dest = os.path.join(appdir, "usr")
        os.makedirs(app_dest, exist_ok=True)
        shutil.copytree(app_path, os.path.join(app_dest, "bin", app_name))

        # Create .desktop file in AppDir
        os.makedirs(os.path.join(appdir, "usr/share/applications"), exist_ok=True)
        shutil.copy(desktop_file_path, os.path.join(appdir, "usr/share/applications/"))

        # Copy icon to AppDir
        os.makedirs(
            os.path.join(appdir, "usr/share/icons/hicolor/256x256/apps"), exist_ok=True
        )
        shutil.copy(
            icon_source,
            os.path.join(
                appdir, f"usr/share/icons/hicolor/256x256/apps/{file_safe_name}.png"
            ),
        )

        # Create AppRun script
        apprun_path = os.path.join(appdir, "AppRun")
        with open(apprun_path, "w") as f:
            f.write(
                f"""#!/bin/sh
SELF=$(readlink -f "$0")
HERE=$(dirname "$SELF")
export PATH="$HERE/usr/bin:$PATH"
export LD_LIBRARY_PATH="$HERE/usr/lib:$LD_LIBRARY_PATH"
exec "$HERE/usr/bin/{app_name}/{app_name}" "$@"
"""
            )
        os.chmod(apprun_path, 0o755)

        # Create symlinks in AppDir root
        os.symlink(
            f"usr/share/icons/hicolor/256x256/apps/{file_safe_name}.png",
            os.path.join(appdir, f"{file_safe_name}.png"),
        )
        os.symlink(
            f"usr/share/applications/{file_safe_name}.desktop",
            os.path.join(appdir, f"{file_safe_name}.desktop"),
        )

        # Run appimagetool
        appimage_path = os.path.join(
            project_path, f"{file_safe_name}-{version}-x86_64.AppImage"
        )
        subprocess.run(["appimagetool", appdir, appimage_path], check=True)
        results["appimage"] = appimage_path
        print(f"Created AppImage: {appimage_path}")

    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print(f"Error creating AppImage: {e}")
        print(
            "Make sure 'appimagetool' is installed: https://github.com/AppImage/AppImageKit/releases"
        )

    # Clean up
    try:
        shutil.rmtree(temp_dir)
    except:
        print(f"Warning: Could not clean up temporary directory: {temp_dir}")

    return results


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


# def create_flatpak_manifest(version, project_path="."):
#     """Create a Flatpak manifest for the application"""
#     import json
#     import os
    
#     app_name = "MIDI-HID Inspektr"
#     app_id = "com.yourashp8i.MIDIHIDInspektr"
#     file_safe_name = "midi-hid-inspektr"
    
#     # Create the flatpak manifest
#     manifest = {
#         "app-id": app_id,
#         "runtime": "org.freedesktop.Platform",
#         "runtime-version": "22.08",
#         "sdk": "org.freedesktop.Sdk",
#         "command": file_safe_name,
#         "finish-args": [
#             "--share=ipc",
#             "--socket=x11",
#             "--socket=wayland",
#             "--device=all",    # For USB/MIDI/HID device access
#             "--filesystem=host",
#             "--share=network"
#         ],
#         "modules": [
#             {
#                 "name": file_safe_name,
#                 "buildsystem": "simple",
#                 "build-commands": [
#                     f"install -D {file_safe_name} /app/bin/{file_safe_name}",
#                     f"install -D {file_safe_name}.desktop /app/share/applications/{app_id}.desktop",
#                     f"install -D {file_safe_name}.png /app/share/icons/hicolor/256x256/apps/{app_id}.png"
#                 ],
#                 "sources": [
#                     {
#                         "type": "file",
#                         "path": f"dist/{app_name}/{app_name}",
#                         "dest-filename": file_safe_name 
#                     },
#                     {
#                         "type": "file",
#                         "path": f"linux_packaging/{file_safe_name}.desktop",
#                         "dest-filename": f"{file_safe_name}.desktop"
#                     },
#                     {
#                         "type": "file",
#                         "path": "resources/icons/app_icon.png",
#                         "dest-filename": f"{file_safe_name}.png"
#                     }
#                 ]
#             }
#         ]
#     }
    
#     # Create flatpak directory
#     flatpak_dir = os.path.join(project_path, "flatpak")
#     os.makedirs(flatpak_dir, exist_ok=True)
    
#     # Write manifest file
#     manifest_path = os.path.join(flatpak_dir, f"{app_id}.json")
#     with open(manifest_path, "w") as f:
#         json.dump(manifest, f, indent=4)
    
#     print(f"Created Flatpak manifest: {manifest_path}")
    
#     # Create instructions file
#     instructions_path = os.path.join(flatpak_dir, "README.md")
    
#     instructions_content = f"""# Flatpak Build Instructions for {app_name}


def build(platform, version, portable=False, installer=False, project_path="."):
    """Build the application for the specified platform"""
    if platform == "windows":
        build_windows(version, portable, installer, project_path)
    else:
        # For macOS and Linux, use the standard build process
        spec_file = update_spec_file(platform, version, project_path=project_path)
        app_name = "MIDI-HID Inspektr"
        file_safe_name = "MIDI-HID-Inspektr"

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

        # For macOS, create DMG
        if platform == "macos":
            app_path = os.path.join(project_path, "dist", f"{app_name}.app")
            if os.path.exists(app_path):
                print("Creating macOS DMG installer...")
                dmg_path = create_macos_dmg(app_path, version, project_path)
                print(f"DMG created at: {dmg_path}")
            else:
                print(f"Error: .app package not found at {app_path}")

        # For Linux, create packages
        elif platform == "linux":
            app_path = os.path.join(project_path, "dist", app_name)
            if os.path.exists(app_path):
                print("Creating Linux packages...")
                packages = create_linux_packages(app_path, version, project_path)

                # Print summary of created packages
                print("\nLinux packages created:")
                for pkg_type, path in packages.items():
                    print(f"- {pkg_type.upper()}: {path}")
            else:
                print(f"Error: Application directory not found at {app_path}")


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
