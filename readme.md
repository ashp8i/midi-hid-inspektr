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

## Building from Source

### Prerequisites

#### All Platforms
- Python 3.7 or higher
- UV package manager (recommended) or pip

#### Windows-specific Requirements
- **Visual Studio Community Edition** with "Python Development" workload installed
  - This is required to build native dependencies like python-rtmidi
  - During Visual Studio installation, be sure to select the "Python development" workload
- **Inno Setup** (optional, only needed for building installers)
  - Download from [jrsoftware.org/isdl.php](https://jrsoftware.org/isdl.php)

#### macOS-specific Requirements
- Xcode Command Line Tools
  - Install with: `xcode-select --install`

#### Linux-specific Requirements
- Development packages for ALSA and JACK
  - Debian/Ubuntu: `sudo apt-get install libasound2-dev libjack-jackd2-dev`
  - Fedora/RHEL: `sudo dnf install alsa-lib-devel jack-audio-connection-kit-devel`

### Basic Setup

```bash
# Clone the repository
git clone https://github.com/ashp8i/midi-hid-inspektr.git
cd midi-hid-inspektr

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

### Building Application Packages

First, install the build requirements:

```bash
uv pip install -r build-requirements.txt
# or
pip install pyinstaller
```

#### Building on Windows

```bash
# Build standard Windows app
python build_helper.py --platform windows --version 1.0.0 --project-path "C:\path\to\midi-hid-inspektr"

# Build portable Windows executable
python build_helper.py --platform windows --version 1.0.0 --project-path "C:\path\to\midi-hid-inspektr" --portable

# Build Windows installer (requires Inno Setup)
python build_helper.py --platform windows --version 1.0.0 --project-path "C:\path\to\midi-hid-inspektr" --installer

# Build both portable executable and installer
python build_helper.py --platform windows --version 1.0.0 --project-path "C:\path\to\midi-hid-inspektr" --portable --installer
```

#### Windows Troubleshooting

- If you encounter errors installing python-rtmidi:
  - Make sure Visual Studio is installed with the "Python development" workload
  - Try: `uv pip install python-rtmidi --no-binary python-rtmidi`

- If you get "ImportError: DLL load failed" when running the app:
  - Make sure you have the Microsoft Visual C++ Redistributable installed
  - For MIDI functionality, ensure you have an MIDI service like Windows MIDI Services or loopMIDI installed

#### Building on macOS

```bash
python3 build_helper.py --platform macos --version 1.0.0
```

#### Building on Linux

```bash
python3 build_helper.py --platform linux --version 1.0.0
```

### Advanced Packaging Options

The build script supports customizing locations and adding resources. See the extended documentation for more options:

```bash
python build_helper.py --help
```

Disclaimer
USE AT YOUR OWN RISK: This software is provided "as is", without warranty of any kind, express or implied. While the code has been tested to work in various environments, I cannot guarantee its reliability in all situations or accept responsibility for any issues that may arise from its usage.

The software may contain bugs or errors that could potentially affect your system or other software.
Always back up your data before connecting devices or using software that interacts with system hardware.
This tool is designed for educational and diagnostic purposes only.
License
This project is released under the GNU General Public License v3.0 (GPL-3.0), making it free and open-source software. The GPL license ensures that:

You can use, modify, and distribute this software freely
Any modifications or derivative works must also be open-source and GPL-compatible
The complete source code must be made available when distributing the software
For the full license text, please see the LICENSE file in the repository.

Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

Fork the repository
Create your feature branch (git checkout -b feature/amazing-feature)
Commit your changes (git commit -m 'Add some amazing feature')
Push to the branch (git push origin feature/amazing-feature)
Open a Pull Request
Acknowledgments
Thanks to all the contributors who have helped with this project
Built with Python and Qt framework