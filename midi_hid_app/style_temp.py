# midi_hid_app/style.py

def get_dark_theme():
    """Returns a dark theme stylesheet for the application"""
    return """
    /* Main Application */
    QMainWindow, QDialog {
        background-color: #2D2D2D;
        color: #E0E0E0;
    }
    
    /* Widgets */
    QWidget {
        background-color: #2D2D2D;
        color: #E0E0E0;
    }
    
    /* Group Boxes */
    QGroupBox {
        border: 1px solid #555555;
        border-radius: 5px;
        margin-top: 1ex;
        font-weight: bold;
        color: #E0E0E0;
    }
    
    QGroupBox::title {
        subcontrol-origin: margin;
        subcontrol-position: top center;
        padding: 0 5px;
    }
    
    /* Tabs */
    QTabWidget::pane {
        border: 1px solid #555555;
        border-radius: 3px;
    }
    
    QTabBar::tab {
        background-color: #3D3D3D;
        color: #BBBBBB;
        border: 1px solid #555555;
        border-bottom-color: #555555;
        border-top-left-radius: 3px;
        border-top-right-radius: 3px;
        padding: 8px 16px;
        min-width: 100px;
    }
    
    QTabBar::tab:selected {
        background-color: #0D6EFD;
        color: white;
    }
    
    QTabBar::tab:!selected {
        margin-top: 2px;
    }
    
    /* Buttons */
    QPushButton {
        background-color: #3D3D3D;
        color: #E0E0E0;
        border: 1px solid #555555;
        border-radius: 4px;
        padding: 6px 12px;
        min-width: 80px;
    }
    
    QPushButton:hover {
        background-color: #4D4D4D;
        border: 1px solid #666666;
    }
    
    QPushButton:pressed {
        background-color: #303030;
    }
    
    QPushButton:disabled {
        background-color: #2A2A2A;
        color: #666666;
        border: 1px solid #444444;
    }
    
    /* Special Buttons */
    QPushButton#connectButton {
        background-color: #0D6EFD;
        color: white;
    }
    
    QPushButton#connectButton:hover {
        background-color: #0B5ED7;
    }
    
    QPushButton#disconnectButton {
        background-color: #DC3545;
        color: white;
    }
    
    QPushButton#disconnectButton:hover {
        background-color: #BB2D3B;
    }
    
    QPushButton#testButton {
        background-color: #198754;
        color: white;
    }
    
    QPushButton#testButton:hover {
        background-color: #157347;
    }
    
    /* ComboBox */
    QComboBox {
        background-color: #3D3D3D;
        color: #E0E0E0;
        border: 1px solid #555555;
        border-radius: 4px;
        padding: 5px 10px;
        min-width: 6em;
    }
    
    QComboBox::drop-down {
        subcontrol-origin: padding;
        subcontrol-position: top right;
        width: 20px;
        border-left: 1px solid #555555;
    }
    
    QComboBox QAbstractItemView {
        background-color: #3D3D3D;
        color: #E0E0E0;
        selection-background-color: #0D6EFD;
        selection-color: white;
    }
    
    /* Text Edit / Display */
    QTextEdit {
        background-color: #1D1D1D;
        color: #E0E0E0;
        border: 1px solid #555555;
        border-radius: 4px;
        font-family: Menlo, Monaco, Consolas, "Courier New", monospace;
        selection-background-color: #264F78;
    }
    
    /* Radio Buttons */
    QRadioButton {
        color: #E0E0E0;
        spacing: 5px;
    }
    
    QRadioButton::indicator {
        width: 18px;
        height: 18px;
    }
    
    QRadioButton::indicator:checked {
        background-color: #0D6EFD;
        border: 2px solid #0D6EFD;
        border-radius: 9px;
    }
    
    QRadioButton::indicator:unchecked {
        background-color: #1D1D1D;
        border: 2px solid #555555;
        border-radius: 9px;
    }
    
    /* Checkboxes */
    QCheckBox {
        color: #E0E0E0;
        spacing: 5px;
    }
    
    QCheckBox::indicator {
        width: 18px;
        height: 18px;
    }
    
    QCheckBox::indicator:checked {
        background-color: #0D6EFD;
        border: 2px solid #0D6EFD;
        border-radius: 4px;
    }
    
    QCheckBox::indicator:unchecked {
        background-color: #1D1D1D;
        border: 2px solid #555555;
        border-radius: 4px;
    }
    
    /* Labels */
    QLabel {
        color: #E0E0E0;
    }
    
    /* Splitter */
    QSplitter::handle {
        background-color: #555555;
    }
    
    /* Scrollbars */
    QScrollBar:vertical {
        border: none;
        background-color: #2D2D2D;
        width: 12px;
        margin: 16px 0 16px 0;
    }
    
    QScrollBar::handle:vertical {
        background-color: #4D4D4D;
        min-height: 20px;
        border-radius: 6px;
    }
    
    QScrollBar::handle:vertical:hover {
        background-color: #555555;
    }
    
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
        border: none;
        background: none;
        height: 0px;
    }
    
    QScrollBar:horizontal {
        border: none;
        background-color: #2D2D2D;
        height: 12px;
        margin: 0 16px 0 16px;
    }
    
    QScrollBar::handle:horizontal {
        background-color: #4D4D4D;
        min-width: 20px;
        border-radius: 6px;
    }
    
    QScrollBar::handle:horizontal:hover {
        background-color: #555555;
    }
    
    QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
        border: none;
        background: none;
        width: 0px;
    }
    
    /* Status Bar */
    QStatusBar {
        background-color: #222222;
        color: #E0E0E0;
    }
    """

def get_light_theme():
    """Returns a light theme stylesheet for the application"""
    return """
    /* Main Application */
    QMainWindow, QDialog {
        background-color: #F8F9FA;
        color: #212529;
    }
    
    /* Widgets */
    QWidget {
        background-color: #F8F9FA;
        color: #212529;
    }
    
    /* Group Boxes */
    QGroupBox {
        border: 1px solid #DFE0E1;
        border-radius: 5px;
        margin-top: 1ex;
        font-weight: bold;
        color: #212529;
    }
    
    QGroupBox::title {
        subcontrol-origin: margin;
        subcontrol-position: top center;
        padding: 0 5px;
    }
    
    /* Tabs */
    QTabWidget::pane {
        border: 1px solid #DFE0E1;
        border-radius: 3px;
    }
    
    QTabBar::tab {
        background-color: #E9ECEF;
        color: #495057;
        border: 1px solid #DFE0E1;
        border-bottom-color: #DFE0E1;
        border-top-left-radius: 3px;
        border-top-right-radius: 3px;
        padding: 8px 16px;
        min-width: 100px;
    }
    
    QTabBar::tab:selected {
        background-color: #0D6EFD;
        color: white;
    }
    
    QTabBar::tab:!selected {
        margin-top: 2px;
    }
    
    /* Buttons */
    QPushButton {
        background-color: #E9ECEF;
        color: #212529;
        border: 1px solid #CED4DA;
        border-radius: 4px;
        padding: 6px 12px;
        min-width: 80px;
    }
    
    QPushButton:hover {
        background-color: #DEE2E6;
        border: 1px solid #CED4DA;
    }
    
    QPushButton:pressed {
        background-color: #CED4DA;
    }
    
    QPushButton:disabled {
        background-color: #F8F9FA;
        color: #ADB5BD;
        border: 1px solid #E9ECEF;
    }
    
    /* Special Buttons */
    QPushButton#connectButton {
        background-color: #0D6EFD;
        color: white;
    }
    
    QPushButton#connectButton:hover {
        background-color: #0B5ED7;
    }
    
    QPushButton#disconnectButton {
        background-color: #DC3545;
        color: white;
    }
    
    QPushButton#disconnectButton:hover {
        background-color: #BB2D3B;
    }
    
    QPushButton#testButton {
        background-color: #198754;
        color: white;
    }
    
    QPushButton#testButton:hover {
        background-color: #157347;
    }
    
    /* More light theme styles would go here */
    """