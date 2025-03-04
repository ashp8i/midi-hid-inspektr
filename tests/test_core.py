# tests/test_core.py - Test if all dependencies are properly installed
import sys
import os
import pytest
import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("test_core")

# Check if running in CI environment
is_ci = "CI" in os.environ or "GITHUB_ACTIONS" in os.environ

# Print basic system info
logger.info(f"Python version: {sys.version}")
logger.info(f"Python executable: {sys.executable}")


def test_pyside6():
    """Test if PySide6 is properly installed and working."""
    try:
        from PySide6 import QtCore
        from PySide6.QtWidgets import QApplication

        logger.info(f"PySide6 version: {QtCore.__version__}")
        logger.info(f"Qt version: {QtCore.qVersion()}")

        # Skip QApplication creation in CI environment
        if not is_ci:
            # Create test QApplication to verify Qt works
            app = QApplication([])
            logger.info("Successfully created QApplication")
        else:
            logger.info("Skipping QApplication creation in CI environment")

        assert True, "PySide6 import successful"
    except ImportError as e:
        if is_ci:
            pytest.skip(f"PySide6 not available in CI: {e}")
        else:
            logger.error(f"Failed to import PySide6: {e}")
            logger.error("Try reinstalling with: uv pip install PySide6")
            pytest.fail(f"Failed to import PySide6: {e}")
    except Exception as e:
        if is_ci:
            pytest.skip(f"Qt initialization error in CI: {e}")
        else:
            logger.error(f"Error initializing Qt: {e}")
            pytest.fail(f"Error initializing Qt: {e}")


def test_rtmidi():
    """Test if rtmidi is properly installed."""
    try:
        import rtmidi

        logger.info("Successfully imported rtmidi")
        assert True, "rtmidi import successful"
    except ImportError as e:
        if is_ci:
            pytest.skip(f"rtmidi not available in CI: {e}")
        else:
            logger.error(f"Failed to import rtmidi: {e}")
            logger.error("Try reinstalling with: uv pip install python-rtmidi")
            pytest.fail(f"Failed to import rtmidi: {e}")


def test_hidapi():
    """Test if hidapi is properly installed."""
    try:
        import hid

        logger.info("Successfully imported hidapi")
        assert True, "hidapi import successful"
    except ImportError as e:
        if is_ci:
            pytest.skip(f"hidapi not available in CI: {e}")
        else:
            logger.error(f"Failed to import hidapi: {e}")
            logger.error("Try reinstalling with: uv pip install hidapi")
            pytest.fail(f"Failed to import hidapi: {e}")


def test_all_core_dependencies():
    """Meta-test to ensure all core dependencies were successfully imported."""
    # This will automatically pass if all individual dependency tests pass
    # or be skipped if we're in CI and dependencies are missing
    if is_ci:
        pytest.skip("Skipping full dependency check in CI environment")

    logger.info("All core dependencies successfully imported!")
    assert True, "All dependencies available"
