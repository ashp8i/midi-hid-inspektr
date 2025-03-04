# midi_hid_app/splash.py
from PySide6.QtWidgets import QSplashScreen
from PySide6.QtGui import QPixmap, QPainter, QColor, QFont
from PySide6.QtCore import Qt, QTimer


class CustomSplash(QSplashScreen):
    def __init__(self, app_name="MIDI/HID Inspektr", version="1.0"):
        # Create a blank pixmap
        pixmap = QPixmap(500, 300)
        pixmap.fill(Qt.transparent)
        super().__init__(pixmap)

        self.app_name = app_name
        self.version = version

        # Draw splash content
        self.draw_splash()

    def draw_splash(self):
        pixmap = self.pixmap()
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)

        # Draw background with rounded corners
        painter.setBrush(QColor(35, 35, 35))
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(0, 0, pixmap.width(), pixmap.height(), 10, 10)

        # Draw title
        title_font = QFont("Arial", 24, QFont.Bold)
        painter.setFont(title_font)
        painter.setPen(QColor(13, 110, 253))  # Blue color
        painter.drawText(pixmap.rect(), Qt.AlignHCenter | Qt.AlignTop, self.app_name)

        # Draw version
        ver_font = QFont("Arial", 12)
        painter.setFont(ver_font)
        painter.setPen(QColor(200, 200, 200))
        painter.drawText(
            pixmap.rect().adjusted(0, 50, 0, 0),
            Qt.AlignHCenter | Qt.AlignTop,
            f"Version {self.version}",
        )

        # Draw status text placeholder
        painter.drawText(
            pixmap.rect().adjusted(0, 250, 0, -10),
            Qt.AlignHCenter | Qt.AlignBottom,
            "Initializing...",
        )

        painter.end()

    def show_with_timer(self, duration=1500):
        """Show splash screen for a specific duration"""
        self.show()
        QTimer.singleShot(duration, self.close)

    def showMessage(
        self, message, alignment=Qt.AlignBottom | Qt.AlignHCenter, color=Qt.white
    ):
        """Update the message on the splash screen"""
        pixmap = self.pixmap()
        painter = QPainter(pixmap)

        # Clear previous message area
        painter.setBrush(QColor(35, 35, 35))
        painter.setPen(Qt.NoPen)
        painter.drawRect(0, pixmap.height() - 40, pixmap.width(), 40)

        # Draw new message
        painter.setPen(QColor(200, 200, 200))
        font = QFont("Arial", 11)
        painter.setFont(font)
        painter.drawText(
            pixmap.rect().adjusted(0, 0, 0, -10),
            Qt.AlignHCenter | Qt.AlignBottom,
            message,
        )

        painter.end()
        self.setPixmap(pixmap)
        self.repaint()
