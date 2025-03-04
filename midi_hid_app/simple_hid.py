# midi_hid_app/simple_hid.py - Simple HID handling class
import hid
import threading
from PySide6.QtCore import QObject, Signal


class SimpleHIDHandler(QObject):
    """A minimal HID handler that emits signals when HID data is received"""

    # Signal emitted when HID data is received: device_info, data, device_name
    message_received = Signal(dict, bytes, str)

    def __init__(self):
        super().__init__()
        self.connected_devices = {}  # path -> (device, thread, stop_event)

    def get_devices(self):
        """Get list of available HID devices"""
        try:
            return hid.enumerate()
        except Exception as e:
            print(f"Error enumerating HID devices: {e}")
            return []

    def connect_device(self, device_info):
        """Connect to an HID device using its info dict"""
        try:
            path = device_info["path"]
            if path in self.connected_devices:
                return True  # Already connected

            # Create a friendly name for the device
            vendor_id = device_info.get("vendor_id", 0)
            product_id = device_info.get("product_id", 0)
            manufacturer = device_info.get("manufacturer_string", "Unknown")
            product = device_info.get("product_string", "Unknown")

            device_name = f"{manufacturer} {product} ({vendor_id:04x}:{product_id:04x})"

            # Open the device
            device = hid.device()
            device.open_path(path)

            # Set up a stop event for the thread
            stop_event = threading.Event()

            # Create and start a thread to read from the device
            thread = threading.Thread(
                target=self._read_device_thread,
                args=(device, device_info, device_name, stop_event),
                daemon=True,
            )
            thread.start()

            # Store references
            self.connected_devices[path] = (device, thread, stop_event)
            return True

        except Exception as e:
            print(f"Error connecting to HID device: {e}")
            return False

    def _read_device_thread(self, device, device_info, device_name, stop_event):
        """Thread function to continuously read from the device"""
        try:
            while not stop_event.is_set():
                try:
                    # Non-blocking read with timeout (100ms)
                    data = device.read(64, timeout_ms=100)
                    if data:
                        # Use bytes() to ensure we have a proper bytes object
                        self.message_received.emit(
                            device_info, bytes(data), device_name
                        )
                except IOError:
                    # Device disconnected or read error
                    break
        except Exception as e:
            print(f"Error reading from HID device: {e}")
        finally:
            try:
                device.close()
            except:
                pass

    def disconnect_device(self, device_path):
        """Disconnect from an HID device"""
        if device_path not in self.connected_devices:
            return False

        try:
            device, thread, stop_event = self.connected_devices[device_path]

            # Signal thread to stop
            stop_event.set()

            # Close device
            try:
                device.close()
            except:
                pass

            # Wait for thread with timeout
            thread.join(1.0)

            # Remove from connected devices
            del self.connected_devices[device_path]
            return True

        except Exception as e:
            print(f"Error disconnecting HID device: {e}")
            return False

    def close_all(self):
        """Disconnect all devices"""
        for path in list(self.connected_devices.keys()):
            self.disconnect_device(path)
