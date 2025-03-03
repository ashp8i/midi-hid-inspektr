# MIDI/HID Controller Mapping Documentation Tool

A cross-platform tool for viewing MIDI and HID controller Activity.

## Features

- **Device Detection**: Automatically detects connected MIDI and HID devices
- **Real-time Capture**: Records MIDI/HID messages as you interact with your controller
- **Multiple Export Formats**: Export as HTML, JSON, or CSV
- **Low Footprint**: Efficient Python implementation with minimal resource usage
- **Cross-Platform**: Works on Windows, macOS, and Linux

## Installation

### Windows

1. Download the latest release from the Releases page
2. Run the installer or extract the portable version
3. Launch the application from the Start menu or the extracted folder

### macOS

1. Download the latest .dmg file from the Releases page
2. Open the .dmg file and drag the application to your Applications folder
3. Launch from Applications

### Linux

1. Download the .AppImage or .deb/.rpm package from the Releases page
2. For .AppImage: Make executable with `chmod +x MIDIDocTool.AppImage` and run it
3. For .deb: Install with `sudo dpkg -i midi-doc-tool.deb`
4. For .rpm: Install with `sudo rpm -i midi-doc-tool.rpm`

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

# Instructions for building App Package from source
To build the MIDI-HID-Inspektr project using the build_helper.py script:

Platform Options
python3 build_helper.py build --macos     # Build for macOS
python3 build_helper.py build --windows   # Build for Windows
python3 build_helper.py build --linux     # Build for Linux

Build Types
python3 build_helper.py build --debug     # Debug build with symbols
python3 build_helper.py build --release   # Release build with optimizations
