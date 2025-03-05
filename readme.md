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

```
uv pip install -r build-requirements.txt
# or
pip install pyinstaller
```

## Building on Windows
To build the application on Windows, you have several options:

# Option 1: Build from the current directory
If you're already in the project directory, you can simply run:

```# Navigate to the project directory first
cd C:\path\to\midi-hid-inspektr

# Build using the current directory
python build_helper.py --platform windows --version 1.0.0 

# For a portable executable
python build_helper.py --platform windows --version 1.0.0 --portable

# For an installer (requires Inno Setup)
python build_helper.py --platform windows --version 1.0.0 --installer```

Option 2: Build from any location (specifying the project path)
If you want to build from another location, specify the correct path to your project:

```# Replace this with YOUR ACTUAL PATH to the project
python build_helper.py --platform windows --version 1.0.0 --project-path "C:\Users\YourUsername\Downloads\midi-hid-inspektr"

# For a portable executable 
python build_helper.py --platform windows --version 1.0.0 --project-path "C:\Users\YourUsername\Downloads\midi-hid-inspektr" --portable

# For an installer (requires Inno Setup)
python build_helper.py --platform windows --version 1.0.0 --project-path "C:\Users\YourUsername\Downloads\midi-hid-inspektr" --installer
```
Important: Make sure to replace C:\Users\YourUsername\Downloads\midi-hid-inspektr with the actual path where you cloned the repository.

## Windows Troubleshooting
Path not found error: Make sure you're using your actual project path, not the example placeholder
Build fails with missing files: Ensure you're in the project directory or providing the correct --project-path
Python-rtmidi installation issues: Make sure Visual Studio is installed with the "Python development" workload

## Building on macOS and Linux
The build process for macOS and Linux is similar:

```
# macOS
python3 build_helper.py --platform macos --version 1.0.0

# Linux
python3 build_helper.py --platform linux --version 1.0.0
```

### Advanced Packaging Options

The build script supports customizing locations and adding resources. See the extended documentation for more options:

```bash
python build_helper.py --help
```

## Disclaimer

**USE AT YOUR OWN RISK**: This software is provided "as is", without warranty of any kind, express or implied. While the code has been tested to work in various environments, I cannot guarantee its reliability in all situations or accept responsibility for any issues that may arise from its usage.

- The software may contain bugs or errors that could potentially affect your system or other software.
- Always back up your data before connecting devices or using software that interacts with system hardware.
- This tool is designed for educational and diagnostic purposes only.

## License

This project is released under the GNU General Public License v3.0 (GPL-3.0), making it free and open-source software. The GPL license ensures that:

- You can use, modify, and distribute this software freely
- Any modifications or derivative works must also be open-source and GPL-compatible
- The complete source code must be made available when distributing the software

For the full license text, please see the LICENSE file in the repository.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Acknowledgments

- Thanks to all the contributors who have helped with this project
- Built with Python and Qt framework
