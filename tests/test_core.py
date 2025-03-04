# tests/test_core.py - Test if all dependencies are properly installed
import sys
import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("test_core")

# Print basic system info
logger.info(f"Python version: {sys.version}")
logger.info(f"Python executable: {sys.executable}")

# Test PySide6
try:
    from PySide6 import QtCore
    from PySide6.QtWidgets import QApplication

    logger.info(f"PySide6 version: {QtCore.__version__}")
    logger.info(f"Qt version: {QtCore.qVersion()}")

    # Create test QApplication to verify Qt works
    app = QApplication([])
    logger.info("Successfully created QApplication")
except ImportError as e:
    logger.error(f"Failed to import PySide6: {e}")
    logger.error("Try reinstalling with: uv pip install PySide6")
    sys.exit(1)
except Exception as e:
    logger.error(f"Error initializing Qt: {e}")
    sys.exit(1)

# Test rtmidi
try:
    import rtmidi

    logger.info("Successfully imported rtmidi")
except ImportError as e:
    logger.error(f"Failed to import rtmidi: {e}")
    logger.error("Try reinstalling with: uv pip install python-rtmidi")
    sys.exit(1)

# Test hidapi
try:
    import hid

    logger.info("Successfully imported hidapi")
except ImportError as e:
    logger.error(f"Failed to import hidapi: {e}")
    logger.error("Try reinstalling with: uv pip install hidapi")
    sys.exit(1)

logger.info("All core dependencies successfully imported!")
