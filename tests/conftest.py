# tests/conftest.py
import pytest


# This will be imported by all test modules
def pytest_configure(config):
    """Register markers."""
    config.addinivalue_line(
        "markers", "requires_pyside: mark test as requiring PySide6"
    )


# A helper function to check if PySide6 is available
def is_pyside6_available():
    try:
        import PySide6

        return True
    except ImportError:
        return False
