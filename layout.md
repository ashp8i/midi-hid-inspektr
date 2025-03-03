midi_hid_poc/
├── main.py              # Main entry point
├── requirements.txt     # Just the essential dependencies 
├── tests/               # Testing directory
│   ├── test_core.py     # Basic dependency tests
│   ├── test_midi.py     # MIDI-specific tests
│   └── test_hid.py      # HID-specific tests
└── midi_hid_app/        # Main app module
    ├── __init__.py      # Make it a proper package
    ├── simple_midi.py   # Simplified MIDI handler
    ├── simple_hid.py    # Simplified HID handler
    └── simple_ui.py     # Minimal Qt UI