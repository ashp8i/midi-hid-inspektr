# midi_hid_app/style.py

def apply_platform_fixes(app):
    """Apply platform-specific style fixes while keeping native look"""
    import platform
    import sys
    from PySide6.QtCore import QByteArray, QSettings
    
    system = platform.system()
    
    # Platform-specific tweaks that preserve native look
    if system == 'Darwin':  # macOS
        # Fix for combo box dropdown visibility on macOS
        fix_style = """
        QComboBox::drop-down {
            border: 0px;
            width: 24px;
        }
        QComboBox::down-arrow {
            width: 14px;
            height: 14px;
        }
        """
        app.setStyleSheet(fix_style)
        
        # Enable dark mode detection
        QSettings.setDefaultFormat(QSettings.NativeFormat)
        
    elif system == 'Windows':
        # Windows-specific fixes if needed
        pass
    else:
        # Linux-specific fixes if needed
        pass
        
    return app

def is_dark_mode():
    """Detect if system is using dark mode"""
    import platform
    import sys
    from PySide6.QtGui import QPalette, QColor
    
    system = platform.system()
    
    if system == 'Darwin':  # macOS
        # Get color scheme from app palette
        app = QApplication.instance()
        bg_color = app.palette().color(QPalette.Window)
        # Calculate luminance - lower value = darker
        luminance = (0.299 * bg_color.red() + 0.587 * bg_color.green() + 0.114 * bg_color.blue()) / 255
        return luminance < 0.5
    
    elif system == 'Windows':
        # Windows 10+ dark mode detection
        try:
            import winreg
            registry = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
            key = winreg.OpenKey(registry, r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize")
            value, _ = winreg.QueryValueEx(key, "AppsUseLightTheme")
            return value == 0
        except:
            return False
    
    else:  # Linux
        # For Linux, check desktop environment variable
        desktop_env = os.environ.get('XDG_CURRENT_DESKTOP', '').lower()
        if 'gnome' in desktop_env:
            try:
                import subprocess
                result = subprocess.run(['gsettings', 'get', 'org.gnome.desktop.interface', 'color-scheme'], 
                                        capture_output=True, text=True)
                return 'dark' in result.stdout.lower()
            except:
                pass
        
        # Fallback to palette detection
        app = QApplication.instance()
        bg_color = app.palette().color(QPalette.Window)
        luminance = (0.299 * bg_color.red() + 0.587 * bg_color.green() + 0.114 * bg_color.blue()) / 255
        return luminance < 0.5