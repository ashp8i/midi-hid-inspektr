# MIDI/HID Controller Mapping Documentation Tool

A cross-platform tool for recording, analyzing, and documenting MIDI and HID controller mappings with support for multiple decks and template-based documentation.

## Features

- **Device Detection**: Automatically detects connected MIDI and HID devices
- **Real-time Capture**: Records MIDI/HID messages as you interact with your controller
- **Visual Mapping**: Create visual representations of your controller's layout
- **Template System**: Build reusable templates for common controller sections
- **4-Deck Support**: Full support for 4-deck controllers with deck-specific mappings
- **Comprehensive Documentation**: Generates detailed HTML5 documentation
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
git clone https://github.com/yourusername/midi-doc-tool.git
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