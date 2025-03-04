# tests/test_midi.py - Test MIDI functionality
import sys
import time
from midi_hid_app.simple_midi import SimpleMIDIHandler


def main():
    # Create MIDI handler
    midi = SimpleMIDIHandler()

    # List available ports
    ports = midi.get_ports()
    print(f"Available MIDI ports: {ports}")

    if not ports:
        print("No MIDI ports available. Please connect a MIDI device and try again.")
        return

    # Select the first port
    port_name = ports[0]
    print(f"Using port: {port_name}")

    # Define a simple callback
    def on_midi_message(data, timestamp, port):
        hex_data = " ".join([f"{b:02X}" for b in data])
        print(f"MIDI: {hex_data} from {port} at {timestamp:.3f}")

    # Connect signal
    midi.message_received.connect(on_midi_message)

    # Connect to the port
    if midi.connect_port(port_name):
        print(f"Connected to {port_name}. Please interact with your MIDI device...")
        print("Listening for 10 seconds...")

        # Wait for some time
        try:
            time.sleep(10)
        except KeyboardInterrupt:
            print("Test interrupted")

        # Disconnect
        midi.disconnect_port(port_name)
        print(f"Disconnected from {port_name}")
    else:
        print(f"Failed to connect to {port_name}")


if __name__ == "__main__":
    main()
