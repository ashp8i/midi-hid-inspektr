# midi_hid_app/simple_midi.py
import rtmidi
import re
import platform
from PySide6.QtCore import QObject, Signal

class SimpleMIDIHandler(QObject):
    """A more robust MIDI handler that can detect physical vs. virtual ports"""
    
    # Signal emitted when MIDI data is received: data, timestamp, port_name
    message_received = Signal(list, float, str)
    
    def __init__(self):
        super().__init__()
        self.midi_in = rtmidi.MidiIn()
        self.midi_out = rtmidi.MidiOut()
        self.connected_ports = {}  # port_name -> midi_in object
        
        # Common virtual port identifiers
        self.virtual_port_patterns = [
            r'(?i)virtual',    # Any port with "virtual" in the name
            r'(?i)neyrinck',   # Neyrinck V-Control
            r'(?i)IAC',        # macOS Inter-Application Communication
            r'(?i)LoopBe',     # LoopBe Internal MIDI
            r'(?i)LoopMIDI',   # LoopMIDI
            r'(?i)Microsoft GS', # Microsoft GS Wavetable Synth
            r'(?i)VMPK',       # Virtual MIDI Piano Keyboard
            r'(?i)rtpMIDI',    # Network MIDI
            r'(?i)MIDI Yoke',  # MIDI Yoke
            r'(?i)Midi Through'# MIDI Through port
        ]
    
    def get_ports(self):
        """Get list of all available MIDI ports"""
        return self.midi_in.get_ports()
    
    def get_ports_by_type(self):
        """Get MIDI ports categorized as physical or virtual"""
        all_ports = self.get_ports()
        physical_ports = []
        virtual_ports = []
        
        for port in all_ports:
            if self._is_likely_virtual_port(port):
                virtual_ports.append(port)
            else:
                physical_ports.append(port)
        
        return {
            'all': all_ports,
            'physical': physical_ports,
            'virtual': virtual_ports
        }
    
    def _is_likely_virtual_port(self, port_name):
        """Determine if a port is likely a virtual port based on its name"""
        for pattern in self.virtual_port_patterns:
            if re.search(pattern, port_name):
                return True
        return False
    
    def create_virtual_port(self, name="MIDI Test Virtual Port"):
        """Create a virtual MIDI port for testing"""
        try:
            # Different behavior based on platform
            if platform.system() == 'Darwin':  # macOS
                self.midi_in.open_virtual_port(name + " Input")
                self.midi_out.open_virtual_port(name + " Output")
                return True
            elif platform.system() == 'Linux':
                self.midi_in.open_virtual_port(name + " Input")
                self.midi_out.open_virtual_port(name + " Output")
                return True
            else:  # Windows doesn't properly support virtual ports in rtmidi
                return False
        except Exception as e:
            print(f"Error creating virtual port: {e}")
            return False
    
    def connect_port(self, port_name):
        """Connect to a specific MIDI port by name"""
        if port_name in self.connected_ports:
            return True  # Already connected
        
        try:
            ports = self.get_ports()
            if port_name not in ports:
                print(f"Port '{port_name}' not found")
                return False
            
            port_index = ports.index(port_name)
            
            # Create a new MidiIn instance for this port
            midi_in = rtmidi.MidiIn()
            midi_in.open_port(port_index)
            
            # Create closure to capture port name
            def callback(message, time_stamp):
                self.message_received.emit(message[0], time_stamp, port_name)
            
            midi_in.set_callback(callback)
            self.connected_ports[port_name] = midi_in
            return True
            
        except Exception as e:
            print(f"Error connecting to MIDI port '{port_name}': {e}")
            return False
    
    def send_midi(self, port_name, midi_data):
        """Send MIDI data to a port"""
        try:
            ports = self.midi_out.get_ports()
            if port_name not in ports:
                print(f"Output port '{port_name}' not found")
                return False
            
            port_index = ports.index(port_name)
            
            # Open port, send message, and close
            midi_out = rtmidi.MidiOut()
            midi_out.open_port(port_index)
            midi_out.send_message(midi_data)
            midi_out.close_port()
            return True
            
        except Exception as e:
            print(f"Error sending MIDI to port '{port_name}': {e}")
            return False
    
    def disconnect_port(self, port_name):
        """Disconnect from a MIDI port"""
        if port_name not in self.connected_ports:
            return False
        
        try:
            midi_in = self.connected_ports[port_name]
            midi_in.cancel_callback()
            midi_in.close_port()
            del self.connected_ports[port_name]
            return True
        except Exception as e:
            print(f"Error disconnecting from MIDI port '{port_name}': {e}")
            return False
    
    def close_all(self):
        """Disconnect all ports"""
        for port_name in list(self.connected_ports.keys()):
            self.disconnect_port(port_name)