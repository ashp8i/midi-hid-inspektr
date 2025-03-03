#!/usr/bin/env python3
import sys
import os
import argparse
from PySide6.QtGui import QIcon
import time
# Add the parent directory to sys.path if needed
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from PySide6.QtWidgets import QApplication
from midi_hid_app.splash import CustomSplash
from midi_hid_app.simple_midi import SimpleMIDIHandler
from midi_hid_app.simple_hid import SimpleHIDHandler
from midi_hid_app.simple_ui import SimpleMainWindow
from midi_hid_app.style import get_pro_dark_theme
# Mac-specific icon fix
if sys.platform == 'darwin':
    # Get absolute path to icon file
    base_dir = os.path.dirname(os.path.abspath(__file__))
    icon_path = os.path.join(base_dir, 'resources', 'icons', 'app_icon.icns')
    
    # If ICNS doesn't exist but PNG does, use PNG instead
    if not os.path.exists(icon_path):
        icon_path = os.path.join(base_dir, 'resources', 'icons', 'app_icon.png')
    
    if os.path.exists(icon_path):
        # This forces macOS to show the icon in the dock
        import ctypes
        ctypes.CDLL('/System/Library/Frameworks/AppKit.framework/AppKit').NSApplicationLoad()

# Set application icon
def set_app_icon(app):
    """Set the application icon based on platform"""
    import os
    from PySide6.QtGui import QIcon
    
    # Get the base directory
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # List of icon paths to try (in order of preference)
    icon_paths = [
        os.path.join(base_dir, 'resources', 'icons', 'app_icon.icns'),
        os.path.join(base_dir, 'resources', 'icons', 'app_icon.ico'),
        os.path.join(base_dir, 'resources', 'icons', 'app_icon.png')
    ]
    
    # Try each path and use the first one that exists
    for path in icon_paths:
        if os.path.exists(path):
            print(f"Loading icon from: {path}")
            app.setWindowIcon(QIcon(path))
            
            # For macOS dock icon, we need to set it separately
            if sys.platform == 'darwin':
                import objc
                from AppKit import NSImage
                try:
                    image = NSImage.alloc().initWithContentsOfFile_(path)
                    objc.lookUpClass('NSApplication').sharedApplication().setApplicationIconImage_(image)
                    print("Set macOS dock icon")
                except Exception as e:
                    print(f"Error setting macOS dock icon: {e}")
            return
    
    print("No application icon found")

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='MIDI/HID Test Application')
    parser.add_argument('--scan', action='store_true', help='Scan for devices and exit')
    parser.add_argument('--create-virtual', help='Create a virtual MIDI port with the specified name')
    args = parser.parse_args()
    
    # Create handlers
    midi_handler = SimpleMIDIHandler()
    hid_handler = SimpleHIDHandler()
    
    # Handle scan mode
    if args.scan:
        # Get MIDI ports
        midi_ports = midi_handler.get_ports_by_type()
        print("\n=== MIDI Ports ===")
        print(f"Physical ports ({len(midi_ports['physical'])}):")
        for port in midi_ports['physical']:
            print(f"  - {port}")
        
        print(f"\nVirtual ports ({len(midi_ports['virtual'])}):")
        for port in midi_ports['virtual']:
            print(f"  - {port}")
        
        # Get HID devices
        hid_devices = hid_handler.get_devices()
        print(f"\n=== HID Devices ({len(hid_devices)}) ===")
        for device in hid_devices:
            vendor_id = device.get('vendor_id', 0)
            product_id = device.get('product_id', 0)
            manufacturer = device.get('manufacturer_string', 'Unknown')
            product = device.get('product_string', 'Unknown')
            
            print(f"  - {manufacturer} {product} ({vendor_id:04x}:{product_id:04x})")
        
        print("")
        return 0
    
    # Handle virtual port creation
    if args.create_virtual:
        import platform
        if platform.system() in ('Darwin', 'Linux'):
            if midi_handler.create_virtual_port(args.create_virtual):
                print(f"Created virtual MIDI port: {args.create_virtual}")
                return 0
            else:
                print("Failed to create virtual MIDI port")
                return 1
        else:
            print("Virtual MIDI ports are not supported on this platform")
            return 1
    
    # Create application
    app = QApplication(sys.argv)
    app.setApplicationName("MIDI/HID Inspektr")
    
    # Set app icon
    set_app_icon(app)
    
    # # Apply the dark theme
    # app.setStyleSheet(get_dark_theme())

    # In your main function
    app.setStyleSheet(get_pro_dark_theme())
    
    # Show splash screen
    try:
        splash = CustomSplash("MIDI/HID Inspektr", "1.0.0")
        splash.show()
        app.processEvents()
    except Exception as e:
        print(f"Error creating splash screen: {e}")
        splash = None
    
    # Create handlers
    print("Initializing MIDI subsystem...")
    midi_handler = SimpleMIDIHandler()
    
    print("Initializing HID subsystem...")
    hid_handler = SimpleHIDHandler()
    
    print("Loading main interface...")
    
    # Create main window
    window = SimpleMainWindow(midi_handler, hid_handler)
    
    # Show main window and close splash if it exists
    window.show()
    if splash:
        splash.finish(window)
    
    # Run event loop
    return app.exec()

if __name__ == "__main__":
    sys.exit(main())