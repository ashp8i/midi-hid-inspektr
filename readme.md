# MIDI/HID Inspektr

A cross-platform tool for viewing MIDI and HID controller Activity.

## Features

- **Device Detection**: Automatically detects connected MIDI and HID devices
- **Real-time Capture**: Records MIDI/HID messages as you interact with your controller
- **Low Footprint**: Efficient Python implementation with minimal resource usage
- **Cross-Platform**: Works on Windows, macOS, and Linux

## Installation

### Windows

1. Download the latest release from the Releases page
<!-- 2. Run the installer or extract the portable version -->
2. Run the extract the portable version
3. Launch the application from the Start menu or the extracted folder

### macOS

1. Download the latest .dmg file from the Releases page
2. Open the .dmg file and drag the application to your Applications folder
3. Launch from Applications

### Linux

1. Download the .AppImage or .deb/.rpm package from the Releases page
<!-- 2. For .AppImage: Make executable with `chmod +x MIDIDocTool.AppImage` and run it
3. For .deb: Install with `sudo dpkg -i midi-doc-tool.deb`
4. For .rpm: Install with `sudo rpm -i midi-doc-tool.rpm` -->

### From Source

Requirements:
- Python 3.7 or higher
- UV package manager (recommended) or pip

```bash
# Clone the repository
git clone https://github.com/ashp8i//midi-hid-inspektr.git
cd midi-doc-tool

# Create and activate virtual environment with UV
python -m uv venv .venv
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate

# Install dependencies
uv pip install -r requirements.txt

# Run the application
python main.py
```

# Instructions for building App Package from source
To build the MIDI-HID-Inspektr project using the build_helper.py script:

## MIDI-HID-Inspektr Build Instructions

```bash
pip install pyinstaller
or
pip install -r build-requirements.txt

# Build for macOS
python3 build_helper.py --platform macos --version 1.0.0

# Build standard Windows app
python build_helper.py --platform windows --version 1.0.0

# Build portable Windows executable
python build_helper.py --platform windows --version 1.0.0 --portable

# Build Windows installer
python build_helper.py --platform windows --version 1.0.0 --installer

# Build both portable executable and installer
python build_helper.py --platform windows --version 1.0.0 --portable --installer

# Build for Linux
python3 build_helper.py --platform linux --version 1.0.0
```
