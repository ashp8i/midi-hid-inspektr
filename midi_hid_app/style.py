# midi_hid_app/style.py

def get_pro_dark_theme():
    """Returns a professional dark theme for the app"""
    return """
    /* Main Application */
    QMainWindow {
        background-color: #1E1E1E;
        color: #FFFFFF;
    }
    
    /* Central Widget */
    QWidget {
        background-color: #1E1E1E;
        color: #FFFFFF;
    }
    
    /* Tab Widget */
    QTabWidget::pane {
        border: 1px solid #3F3F3F;
        background-color: #2D2D2D;
        border-radius: 3px;
    }
    
    QTabBar::tab {
        background-color: #3D3D3D;
        color: #BABABA;
        padding: 8px 16px;
        border-top-left-radius: 3px;
        border-top-right-radius: 3px;
        border: 1px solid #3F3F3F;
        margin-right: 2px;
    }
    
    QTabBar::tab:selected {
        background-color: #0D6EFD;
        color: white;
    }
    
    QTabBar::tab:!selected:hover {
        background-color: #4D4D4D;
    }
    
    /* Group Box */
    QGroupBox {
        font-weight: bold;
        border: 1px solid #3F3F3F;
        border-radius: 4px;
        margin-top: 8px;
        padding-top: 8px;
    }
    
    QGroupBox::title {
        subcontrol-origin: margin;
        subcontrol-position: top center;
        padding: 0 5px;
        color: #FFFFFF;
    }
    
    /* Radio Button */
    QRadioButton {
        color: #FFFFFF;
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
        background-color: #2D2D2D;
        border: 2px solid #6B6B6B;
        border-radius: 9px;
    }
    
    /* Buttons */
    QPushButton {
        background-color: #3D3D3D;
        color: #FFFFFF;
        border: 1px solid #3F3F3F;
        border-radius: 4px;
        padding: 6px 12px;
        min-width: 80px;
    }
    
    QPushButton:hover {
        background-color: #4D4D4D;
        border: 1px solid #6B6B6B;
    }
    
    QPushButton:pressed {
        background-color: #333333;
    }
    
    /* Primary Button (like Connect) */
    QPushButton#connectButton, QPushButton#createButton {
        background-color: #0D6EFD;
        color: white;
        border: 1px solid #0B5ED7;
    }
    
    QPushButton#connectButton:hover, QPushButton#createButton:hover {
        background-color: #0B5ED7;
        border: 1px solid #0A58CA;
    }
    
    QPushButton#refreshDevicesButton {
        background-color: #6C757D;
        color: white;
        border: 1px solid #5C636A;
    }
    
    QPushButton#refreshDevicesButton:hover {
        background-color: #5C636A;
        border: 1px solid #565E64;
    }
    
    QPushButton:disabled {
        background-color: #2A2A2A;
        color: #6B6B6B;
        border: 1px solid #3F3F3F;
    }
    
    /* ComboBox (dropdown) */
    QComboBox {
        background-color: #2D2D2D;
        color: #FFFFFF;
        border: 1px solid #3F3F3F;
        border-radius: 4px;
        padding: 5px 10px;
        min-width: 6em;
    }
    
    QComboBox:editable {
        background-color: #2D2D2D;
    }
    
    QComboBox:!editable, QComboBox::drop-down:editable {
        background-color: #2D2D2D;
    }
    
    QComboBox:!editable:hover, QComboBox::drop-down:editable:hover {
        background-color: #3D3D3D;
        border: 1px solid #6B6B6B;
    }
    
    QComboBox::drop-down {
        subcontrol-origin: padding;
        subcontrol-position: top right;
        width: 20px;
        border-left: 1px solid #3F3F3F;
    }
    
    QComboBox::down-arrow {
        image: url(:/images/arrow_down.png);
        width: 12px;
        height: 12px;
    }
    
    QComboBox QAbstractItemView {
        background-color: #2D2D2D;
        color: #FFFFFF;
        selection-background-color: #0D6EFD;
        selection-color: white;
        border: 1px solid #3F3F3F;
    }
    
    /* Line Edit (text input) */
    QLineEdit {
        background-color: #2D2D2D;
        color: #FFFFFF;
        border: 1px solid #3F3F3F;
        border-radius: 4px;
        padding: 5px;
    }
    
    QLineEdit:focus {
        border: 1px solid #0D6EFD;
    }
    
    /* Headers */
    QHeaderView::section {
        background-color: #3D3D3D;
        color: #FFFFFF;
        padding: 5px;
        border: 1px solid #3F3F3F;
    }
    
    /* Scrollbars */
    QScrollBar:vertical {
        background-color: #2D2D2D;
        width: 14px;
        margin: 15px 0 15px 0;
        border: 1px solid #3F3F3F;
        border-radius: 4px;
    }
    
    QScrollBar::handle:vertical {
        background-color: #5D5D5D;
        min-height: 30px;
        border-radius: 2px;
    }
    
    QScrollBar::handle:vertical:hover {
        background-color: #6D6D6D;
    }
    
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
        border: none;
        background: none;
        height: 15px;
    }
    
    QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
        background: none;
    }
    """
