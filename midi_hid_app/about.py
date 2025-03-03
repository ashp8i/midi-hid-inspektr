# midi_hid_app/about.py
from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
from PySide6.QtGui import QPixmap, QFont
from PySide6.QtCore import Qt
import os

class AboutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("About MIDI/HID Inspektr")
        self.setFixedSize(450, 350)
        
        # Main layout
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # Try to load app icon
        icon_layout = QHBoxLayout()
        icon_label = QLabel()
        
        # Find the icon
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        icon_paths = [
            os.path.join(base_dir, 'resources', 'icons', 'app_icon.png'),
            os.path.join(base_dir, 'resources', 'images', 'logo.png')
        ]
        
        icon_found = False
        for path in icon_paths:
            if os.path.exists(path):
                pixmap = QPixmap(path)
                scaled_pixmap = pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                icon_label.setPixmap(scaled_pixmap)
                icon_found = True
                break
        
        if not icon_found:
            # Create a text-based "logo" if icon not found
            icon_label.setText("MIDI/HID")
            icon_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #0D6EFD;")
        
        icon_layout.addStretch()
        icon_layout.addWidget(icon_label)
        icon_layout.addStretch()
        layout.addLayout(icon_layout)
        
        # App name
        app_name = QLabel("MIDI/HID Inspektr")
        app_name.setAlignment(Qt.AlignCenter)
        app_name.setFont(QFont("Arial", 18, QFont.Bold))
        layout.addWidget(app_name)
        
        # Version
        version = QLabel("Version 1.0.0")
        version.setAlignment(Qt.AlignCenter)
        layout.addWidget(version)
        
        # Description
        desc = QLabel("A tool for monitoring MIDI and HID device activity")
        desc.setWordWrap(True)
        desc.setAlignment(Qt.AlignCenter)
        desc.setContentsMargins(20, 20, 20, 20)
        layout.addWidget(desc)
        
        # Copyright
        copyright = QLabel("© 2025 Ashish Khimani. All rights reserved.")
        copyright.setAlignment(Qt.AlignCenter)
        layout.addWidget(copyright)
        
        # Credits
        credits = QLabel(
            "Built with Python, PySide6, and PyAudio"
        )
        credits.setAlignment(Qt.AlignCenter)
        layout.addWidget(credits)
        
        # Close button
        button_layout = QHBoxLayout()
        close_button = QPushButton("Close")
        close_button.setFixedWidth(100)
        close_button.clicked.connect(self.accept)
        
        button_layout.addStretch()
        button_layout.addWidget(close_button)
        button_layout.addStretch()
        
        layout.addStretch()
        layout.addLayout(button_layout)