# tests/test_hid.py - Test HID functionality
import sys
import time
from midi_hid_app.simple_hid import SimpleHIDHandler


def main():
    # Create HID handler
    hid_handler = SimpleHIDHandler()

    # List available devices
    devices = hid_handler.get_devices()
    print(f"Found {len(devices)} HID devices:")

    for i, device in enumerate(devices):
        vendor_id = device.get("vendor_id", 0)
        product_id = device.get("product_id", 0)
        manufacturer = device.get("manufacturer_string", "Unknown")
        product = device.get("product_string", "Unknown")

        print(f"{i+1}. {manufacturer} {product} ({vendor_id:04x}:{product_id:04x})")

    if not devices:
        print("No HID devices found. Please connect an HID device and try again.")
        return

    # Ask which device to test
    try:
        if len(devices) > 1:
            selection = int(input(f"Select device (1-{len(devices)}): "))
            device_info = devices[selection - 1]
        else:
            device_info = devices[0]

        # Display selected device
        print(
            f"Selected: {device_info.get('manufacturer_string', '')} {device_info.get('product_string', '')}"
        )

        # Define a simple callback
        def on_hid_message(device_info, data, device_name):
            hex_data = " ".join([f"{b:02X}" for b in data])
            print(f"HID: {hex_data} from {device_name}")

        # Connect signal
        hid_handler.message_received.connect(on_hid_message)

        # Connect to the device
        if hid_handler.connect_device(device_info):
            print("Connected. Please interact with your HID device...")
            print("Listening for 10 seconds...")

            # Wait for some time
            try:
                time.sleep(10)
            except KeyboardInterrupt:
                print("Test interrupted")

            # Disconnect
            path = device_info["path"]
            hid_handler.disconnect_device(path)
            print("Disconnected from device")
        else:
            print("Failed to connect to device")

    except (ValueError, IndexError):
        print("Invalid selection")
    except KeyboardInterrupt:
        print("Test cancelled")


if __name__ == "__main__":
    main()
