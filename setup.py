import os
from setuptools import setup

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

APP = ['main.py']
DATA_FILES = [
    ('resources/icons', [os.path.join(BASE_DIR, 'resources', 'icons', 'app_icon.icns')]),
]
OPTIONS = {
    'argv_emulation': False,
    'plist': {
        'CFBundleName': 'MIDI/HID Inspektr',
        'CFBundleDisplayName': 'MIDI/HID Inspektr',
        'CFBundleIdentifier': 'com.ashp8i.midihidinspektr',
        'CFBundleVersion': '1.0.0',
        'CFBundleIconFile': 'app_icon.icns',
    },
    'packages': ['PySide6'],
    'optimize': 2,  # Add optimization level
    'excludes': ['PySide6.QtWebEngineCore', 'PySide6.QtWebEngine', 'PySide6.QtWebEngineWidgets', 
                'PySide6.QtNetwork', 'PySide6.QtPositioning', 'PySide6.QtLocation',
                'PySide6.QtMultimedia', 'PySide6.QtMultimediaWidgets', 'PySide6.QtPrintSupport'],
    'strip': True  # Strip debug symbols
}

setup(
    app=APP,
    name='midihidinspektr',
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)