# run_tests.py
import sys
from tests.test_core import main as test_core
from tests.test_midi import main as test_midi
from tests.test_hid import main as test_hid

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python run_tests.py [core|midi|hid|all]")
        sys.exit(1)
    
    test_type = sys.argv[1].lower()
    
    if test_type == "core" or test_type == "all":
        print("=== Running Core Tests ===")
        test_core()
    
    if test_type == "midi" or test_type == "all":
        print("\n=== Running MIDI Tests ===")
        test_midi()
    
    if test_type == "hid" or test_type == "all":
        print("\n=== Running HID Tests ===")
        test_hid()