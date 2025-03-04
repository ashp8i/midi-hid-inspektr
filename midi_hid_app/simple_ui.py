from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                              QLabel, QPushButton, QComboBox, QTextEdit,
                              QGroupBox, QSplitter, QCheckBox, QRadioButton,
                              QButtonGroup, QMessageBox, QTabWidget,
                              QMenuBar, QMenu)  # These are in QtWidgets
from PySide6.QtGui import QAction  # QAction is in QtGui, not QtWidgets
from PySide6.QtCore import Qt, QTimer, Slot
from midi_hid_app.about import AboutDialog  # Import the About dialog

class SimpleMainWindow(QMainWindow):
    """An improved main window that properly handles virtual and physical ports"""
    
    def __init__(self, midi_handler, hid_handler):
        super().__init__()
        self.setWindowTitle("MIDI/HID Inspektr")
        self.resize(900, 700)
        
        self.midi_handler = midi_handler
        self.hid_handler = hid_handler
        
        # Apply platform-specific tweaks
        self.apply_platform_tweaks()
        
        # Set up UI components FIRST
        self.setup_ui()
        
        # THEN create the menu bar
        self.create_menu_bar()
        
        # Connect signals
        self.setup_connections()
        
        # Initial device scan (after a short delay to ensure UI is fully built)
        QTimer.singleShot(100, self.refresh_devices)

    def apply_platform_tweaks(self):
        """Apply platform-specific UI tweaks"""
        import platform
        
        system = platform.system()
        
        if system == 'Darwin':  # macOS
            # Fix for macOS combo boxes
            self.setUnifiedTitleAndToolBarOnMac(True)
            
        elif system == 'Windows':
            # Windows-specific tweaks
            pass
        else:
            # Linux-specific tweaks
            pass
    
    def create_menu_bar(self):
        """Create application menu bar"""
        menu_bar = self.menuBar()
        
        # File menu
        file_menu = menu_bar.addMenu("&File")
        
        # Save Log action
        save_log_action = QAction("Save Log...", self)
        save_log_action.setShortcut("Ctrl+S")
        save_log_action.triggered.connect(self.save_log)
        file_menu.addAction(save_log_action)
        
        file_menu.addSeparator()
        
        # Exit action
        exit_action = QAction("Exit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # View menu
        view_menu = menu_bar.addMenu("&View")
        
        # Refresh action
        refresh_action = QAction("Refresh Devices", self)
        refresh_action.setShortcut("F5")
        refresh_action.triggered.connect(self.refresh_devices)
        view_menu.addAction(refresh_action)
        
        view_menu.addSeparator()
        
        # Display options as checkable menu items
        autoscroll_action = QAction("Auto-scroll", self)
        autoscroll_action.setCheckable(True)
        autoscroll_action.setChecked(True)
        autoscroll_action.toggled.connect(self.autoscroll_check.setChecked)
        view_menu.addAction(autoscroll_action)
        
        timestamp_action = QAction("Show Timestamps", self)
        timestamp_action.setCheckable(True)
        timestamp_action.setChecked(True)
        timestamp_action.toggled.connect(self.timestamp_check.setChecked)
        view_menu.addAction(timestamp_action)
        
        interpret_action = QAction("Interpret MIDI", self)
        interpret_action.setCheckable(True)
        interpret_action.setChecked(True)
        interpret_action.toggled.connect(self.interpret_check.setChecked)
        view_menu.addAction(interpret_action)
        
        view_menu.addSeparator()
        
        clear_action = QAction("Clear Display", self)
        clear_action.triggered.connect(self.clear_display)
        view_menu.addAction(clear_action)
        
        # Tools menu
        tools_menu = menu_bar.addMenu("&Tools")
        
        # Test MIDI note action
        test_note_action = QAction("Send Test Note", self)
        test_note_action.triggered.connect(self.send_test_midi)
        tools_menu.addAction(test_note_action)
        
        # Help menu
        help_menu = menu_bar.addMenu("&Help")
        
        # About action
        about_action = QAction("About MIDI/HID Inspektr", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

    def setup_ui(self):
        # Central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Tabs for different sections
        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)
        
        # === Device Selection Tab ===
        device_tab = QWidget()
        device_layout = QVBoxLayout(device_tab)
        
        # MIDI Devices
        midi_group = QGroupBox("MIDI Devices")
        midi_layout = QVBoxLayout(midi_group)
        
        # MIDI port type selection
        port_type_layout = QHBoxLayout()
        self.port_type_group = QButtonGroup()
        
        self.all_ports_radio = QRadioButton("All Ports")
        self.physical_ports_radio = QRadioButton("Physical Only")
        self.virtual_ports_radio = QRadioButton("Virtual Only")
        self.physical_ports_radio.setChecked(True)  # Default to physical ports
        
        self.port_type_group.addButton(self.all_ports_radio)
        self.port_type_group.addButton(self.physical_ports_radio)
        self.port_type_group.addButton(self.virtual_ports_radio)
        
        port_type_layout.addWidget(self.all_ports_radio)
        port_type_layout.addWidget(self.physical_ports_radio)
        port_type_layout.addWidget(self.virtual_ports_radio)
        midi_layout.addLayout(port_type_layout)
        
        # MIDI port selection
        self.midi_combo = QComboBox()
        self.midi_combo.setMinimumWidth(300)
        midi_layout.addWidget(QLabel("Select MIDI Port:"))
        midi_layout.addWidget(self.midi_combo)
        
        # MIDI connection buttons
        midi_btn_layout = QHBoxLayout()
        self.midi_connect_btn = QPushButton("Connect")
        self.midi_test_btn = QPushButton("Send Test Note")
        self.midi_test_btn.setEnabled(False)
        
        midi_btn_layout.addWidget(self.midi_connect_btn)
        midi_btn_layout.addWidget(self.midi_test_btn)
        midi_layout.addLayout(midi_btn_layout)
        
        device_layout.addWidget(midi_group)
        
        # Virtual port creation (macOS/Linux only)
        if self.is_virtual_port_supported():
            virtual_group = QGroupBox("Create Virtual MIDI Port")
            virtual_layout = QHBoxLayout(virtual_group)
            
            self.virtual_port_name = QComboBox()
            self.virtual_port_name.setEditable(True)
            self.virtual_port_name.addItems(["MIDI Test Port", "My Virtual Device", "Debug Port"])
            self.create_virtual_btn = QPushButton("Create")
            
            virtual_layout.addWidget(QLabel("Name:"))
            virtual_layout.addWidget(self.virtual_port_name)
            virtual_layout.addWidget(self.create_virtual_btn)
            
            device_layout.addWidget(virtual_group)
            
        # HID Devices
        hid_group = QGroupBox("HID Devices")
        hid_layout = QVBoxLayout(hid_group)
        
        self.hid_combo = QComboBox()
        self.hid_combo.setMinimumWidth(300)
        hid_layout.addWidget(QLabel("Select HID Device:"))
        hid_layout.addWidget(self.hid_combo)
        
        self.hid_connect_btn = QPushButton("Connect")
        hid_layout.addWidget(self.hid_connect_btn)
        
        device_layout.addWidget(hid_group)
        
        # Refresh button
        refresh_layout = QHBoxLayout()
        self.refresh_btn = QPushButton("Refresh Devices")
        
        refresh_layout.addWidget(self.refresh_btn)
        refresh_layout.addStretch()
        device_layout.addLayout(refresh_layout)
        
        # Add to tabs
        self.tabs.addTab(device_tab, "Device Selection")
        
        # === Data Monitor Tab ===
        monitor_tab = QWidget()
        monitor_layout = QVBoxLayout(monitor_tab)
        
        # Data display options
        display_options = QHBoxLayout()
        
        self.autoscroll_check = QCheckBox("Auto-scroll")
        self.autoscroll_check.setChecked(True)
        
        self.timestamp_check = QCheckBox("Show Timestamps")
        self.timestamp_check.setChecked(True)
        
        self.interpret_check = QCheckBox("Interpret MIDI")
        self.interpret_check.setChecked(True)
        
        display_options.addWidget(self.autoscroll_check)
        display_options.addWidget(self.timestamp_check)
        display_options.addWidget(self.interpret_check)
        display_options.addStretch()
        
        monitor_layout.addLayout(display_options)
        
        # Data display
        monitor_layout.addWidget(QLabel("MIDI/HID Data:"))
        self.data_display = QTextEdit()
        self.data_display.setReadOnly(True)
        self.data_display.setFontFamily("Monospace")
        self.data_display.setText("Connect to a device to see data...\n")
        monitor_layout.addWidget(self.data_display)
        
        # Clear button
        controls_layout = QHBoxLayout()
        self.clear_btn = QPushButton("Clear Display")
        self.save_btn = QPushButton("Save Log")
        
        controls_layout.addWidget(self.clear_btn)
        controls_layout.addWidget(self.save_btn)
        controls_layout.addStretch()
        monitor_layout.addLayout(controls_layout)
        
        # Add to tabs
        self.tabs.addTab(monitor_tab, "Data Monitor")
    
    def setup_connections(self):
        # Button connections
        self.refresh_btn.clicked.connect(self.refresh_devices)
        self.midi_connect_btn.clicked.connect(self.connect_midi)
        self.hid_connect_btn.clicked.connect(self.connect_hid)
        self.clear_btn.clicked.connect(self.clear_display)
        self.save_btn.clicked.connect(self.save_log)
        self.midi_test_btn.clicked.connect(self.send_test_midi)
        
        # Port type radio buttons
        self.all_ports_radio.toggled.connect(self.update_midi_ports)
        self.physical_ports_radio.toggled.connect(self.update_midi_ports)
        self.virtual_ports_radio.toggled.connect(self.update_midi_ports)
        
        # Virtual port creation (if supported)
        if self.is_virtual_port_supported():
            self.create_virtual_btn.clicked.connect(self.create_virtual_port)
        
        # MIDI/HID data signals
        self.midi_handler.message_received.connect(self.on_midi_data)
        self.hid_handler.message_received.connect(self.on_hid_data)
    
        # Checkbox connections for syncing with menu
        self.autoscroll_check.toggled.connect(self.on_autoscroll_toggled)
        self.timestamp_check.toggled.connect(self.on_timestamp_toggled)
        self.interpret_check.toggled.connect(self.on_interpret_toggled)

    def is_virtual_port_supported(self):
        """Check if virtual MIDI ports are supported on this platform"""
        import platform
        return platform.system() in ('Darwin', 'Linux')
    
    def refresh_devices(self):
        """Refresh the device lists"""
        # Get MIDI ports
        self.update_midi_ports()
        
        # Get HID devices
        self.update_hid_devices()
        
        self.status_message("Devices refreshed")
    
    def update_midi_ports(self):
        """Update the MIDI port dropdown based on selected port type"""
        # Get ports categorized by type
        ports_by_type = self.midi_handler.get_ports_by_type()
        
        # Determine which ports to show
        if self.all_ports_radio.isChecked():
            ports = ports_by_type['all']
            port_type = "all"
        elif self.physical_ports_radio.isChecked():
            ports = ports_by_type['physical']
            port_type = "physical"
        else:  # virtual ports
            ports = ports_by_type['virtual']
            port_type = "virtual"
        
        # Update the combo box
        self.midi_combo.clear()
        
        if not ports:
            self.midi_combo.addItem(f"No {port_type} MIDI ports found")
            self.midi_connect_btn.setEnabled(False)
        else:
            for port in ports:
                # Add a visual indicator for connected ports
                if port in self.midi_handler.connected_ports:
                    self.midi_combo.addItem(f"► {port}")
                else:
                    self.midi_combo.addItem(port)
            self.midi_connect_btn.setEnabled(True)
    
    def update_hid_devices(self):
        """Update the HID device dropdown"""
        # Get HID devices
        hid_devices = self.hid_handler.get_devices()
        self.hid_devices = hid_devices  # Store for later access
        
        # Update the combo box
        self.hid_combo.clear()
        
        if not hid_devices:
            self.hid_combo.addItem("No HID devices found")
            self.hid_connect_btn.setEnabled(False)
        else:
            for i, device in enumerate(hid_devices):
                vendor_id = device.get('vendor_id', 0)
                product_id = device.get('product_id', 0)
                manufacturer = device.get('manufacturer_string', 'Unknown')
                product = device.get('product_string', 'Unknown')
                
                display_name = f"{manufacturer} {product} ({vendor_id:04x}:{product_id:04x})"
                
                # Add a visual indicator for connected devices
                path = device['path']
                if path in self.hid_handler.connected_devices:
                    self.hid_combo.addItem(f"► {display_name}", i)
                else:
                    self.hid_combo.addItem(display_name, i)
            
            self.hid_connect_btn.setEnabled(True)
    
    def connect_midi(self):
        """Connect to or disconnect from the selected MIDI port"""
        # Get the port name (remove the connection indicator if present)
        port_text = self.midi_combo.currentText()
        if port_text.startswith("► "):
            port_name = port_text[2:]  # Remove the indicator
        else:
            port_name = port_text
        
        # Check if "No ports found" message
        if "No" in port_name and "found" in port_name:
            return
        
        # Check if already connected
        if port_name in self.midi_handler.connected_ports:
            # Disconnect
            if self.midi_handler.disconnect_port(port_name):
                self.status_message(f"Disconnected from MIDI port: {port_name}")
                self.midi_connect_btn.setText("Connect")
                self.midi_test_btn.setEnabled(False)
                self.update_midi_ports()  # Refresh the ports list
        else:
            # Connect
            if self.midi_handler.connect_port(port_name):
                self.status_message(f"Connected to MIDI port: {port_name}")
                self.midi_connect_btn.setText("Disconnect")
                
                # Only enable test button for output ports
                out_ports = self.midi_handler.midi_out.get_ports()
                self.midi_test_btn.setEnabled(port_name in out_ports)
                
                self.update_midi_ports()  # Refresh the ports list
                
                # Switch to Data Monitor tab
                self.tabs.setCurrentIndex(1)

                # Enable/disable the test button
                self.midi_test_btn.setEnabled(port_name in out_ports)
                
                # Also update the menu action (new code)
                for action in self.menuBar().findChildren(QAction):
                    if action.text() == "Send Test Note":
                        action.setEnabled(port_name in out_ports)
                        break
                
    def connect_hid(self):
        """Connect to or disconnect from the selected HID device"""
        if self.hid_combo.currentIndex() < 0:
            return
            
        # Get the device info
        index = self.hid_combo.currentData()
        if index is None or "No HID devices found" in self.hid_combo.currentText():
            return
            
        if 0 <= index < len(self.hid_devices):
            device_info = self.hid_devices[index]
            path = device_info['path']
            
            # Format a nice name for display
            manufacturer = device_info.get('manufacturer_string', 'Unknown')
            product = device_info.get('product_string', 'Unknown')
            device_name = f"{manufacturer} {product}"
            
            # Check if already connected
            if path in self.hid_handler.connected_devices:
                # Disconnect
                if self.hid_handler.disconnect_device(path):
                    self.status_message(f"Disconnected from HID device: {device_name}")
                    self.hid_connect_btn.setText("Connect")
                    self.update_hid_devices()  # Refresh the devices list
            else:
                # Connect
                if self.hid_handler.connect_device(device_info):
                    self.status_message(f"Connected to HID device: {device_name}")
                    self.hid_connect_btn.setText("Disconnect")
                    self.update_hid_devices()  # Refresh the devices list
                    
                    # Switch to Data Monitor tab
                    self.tabs.setCurrentIndex(1)
    
    def create_virtual_port(self):
        """Create a virtual MIDI port"""
        if not self.is_virtual_port_supported():
            self.status_message("Virtual MIDI ports are not supported on this platform")
            return
            
        port_name = self.virtual_port_name.currentText().strip()
        if not port_name:
            self.status_message("Please enter a valid port name")
            return
            
        if self.midi_handler.create_virtual_port(port_name):
            self.status_message(f"Created virtual MIDI port: {port_name}")
            self.refresh_devices()
        else:
            self.status_message("Failed to create virtual MIDI port")
    
    def send_test_midi(self):
        """Send a test MIDI note"""
        # Get the port name
        port_text = self.midi_combo.currentText()
        if port_text.startswith("► "):
            port_name = port_text[2:]  # Remove the indicator
        else:
            port_name = port_text
        
        # Send a note on message (channel 1, note 60, velocity 100)
        note_on = [0x90, 60, 100]
        if self.midi_handler.send_midi(port_name, note_on):
            self.status_message(f"Sent test note to {port_name}")
            
            # After a moment, send note off
            def send_note_off():
                note_off = [0x80, 60, 0]
                self.midi_handler.send_midi(port_name, note_off)
            
            # Use a timer to send note off after 300ms
            QTimer.singleShot(300, send_note_off)
        else:
            self.status_message(f"Failed to send test note to {port_name}")
    
    def on_midi_data(self, data, timestamp, port_name):
        """Handle incoming MIDI data"""
        from datetime import datetime
        
        # Format timestamp
        time_str = ""
        if self.timestamp_check.isChecked():
            time_str = f"[{datetime.now().strftime('%H:%M:%S.%f')[:-3]}] "
        
        # Format as hex
        hex_data = " ".join([f"{b:02X}" for b in data])
        
        # Basic MIDI decoding if requested
        description = ""
        if self.interpret_check.isChecked() and data:
            status = data[0]
            message_type = status & 0xF0
            channel = (status & 0x0F) + 1
            
            if message_type == 0x80:
                description = f" - Note Off (Ch: {channel}, Note: {data[1]}, Velocity: {data[2]})"
            elif message_type == 0x90:
                if data[2] == 0:
                    description = f" - Note Off (Ch: {channel}, Note: {data[1]})"
                else:
                    description = f" - Note On (Ch: {channel}, Note: {data[1]}, Velocity: {data[2]})"
            elif message_type == 0xB0:
                description = f" - Control Change (Ch: {channel}, Control: {data[1]}, Value: {data[2]})"
            elif message_type == 0xE0:
                value = (data[2] << 7) | data[1]
                description = f" - Pitch Bend (Ch: {channel}, Value: {value})"
            elif data[0] == 0xF0:
                description = " - SysEx"
        
        # Add to display
        self.data_display.append(f"{time_str}MIDI [{port_name}]: {hex_data}{description}")
        
        # Auto-scroll if enabled
        if self.autoscroll_check.isChecked():
            self.data_display.ensureCursorVisible()
    
    def on_hid_data(self, device_info, data, device_name):
        """Handle incoming HID data"""
        from datetime import datetime
        
        # Format timestamp
        time_str = ""
        if self.timestamp_check.isChecked():
            time_str = f"[{datetime.now().strftime('%H:%M:%S.%f')[:-3]}] "
        
        # Format as hex
        hex_data = " ".join([f"{b:02X}" for b in data])
        
        # Add to display
        self.data_display.append(f"{time_str}HID [{device_name}]: {hex_data}")
        
        # Auto-scroll if enabled
        if self.autoscroll_check.isChecked():
            self.data_display.ensureCursorVisible()
    
    @Slot()
    def show_about(self):
        """Show the About dialog"""
        about_dialog = AboutDialog(self)
        about_dialog.exec()

    @Slot(bool)
    def on_autoscroll_toggled(self, checked):
        """Handle autoscroll checkbox toggle"""
        # Find and update the menu action if it exists
        for action in self.menuBar().findChildren(QAction):
            if action.text() == "Auto-scroll":
                action.setChecked(checked)
                break

    @Slot(bool)
    def on_timestamp_toggled(self, checked):
        """Handle timestamp checkbox toggle"""
        # Find and update the menu action if it exists
        for action in self.menuBar().findChildren(QAction):
            if action.text() == "Show Timestamps":
                action.setChecked(checked)
                break

    @Slot(bool)
    def on_interpret_toggled(self, checked):
        """Handle interpret MIDI checkbox toggle"""
        # Find and update the menu action if it exists
        for action in self.menuBar().findChildren(QAction):
            if action.text() == "Interpret MIDI":
                action.setChecked(checked)
                break

    def clear_display(self):
        """Clear the data display"""
        self.data_display.clear()
        self.data_display.setText("Connect to a device to see data...\n")
    
    def save_log(self):
        """Save the current log to a file"""
        from PySide6.QtWidgets import QFileDialog
        from datetime import datetime
        
        filename, _ = QFileDialog.getSaveFileName(
            self, "Save Log", 
            f"midi_hid_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            "Text Files (*.txt)"
        )
        
        if filename:
            try:
                with open(filename, 'w') as f:
                    f.write(self.data_display.toPlainText())
                self.status_message(f"Log saved to {filename}")
            except Exception as e:
                self.status_message(f"Error saving log: {e}")
    
    def status_message(self, message):
        """Display a status message in the data display"""
        # Add a horizontal line before status messages
        self.data_display.append("----------------------------------------")
        self.data_display.append(f"STATUS: {message}")
        self.data_display.append("----------------------------------------")
        
        # Auto-scroll
        self.data_display.ensureCursorVisible()
    
    def closeEvent(self, event):
        """Handle window close event"""
        # Clean up connections
        self.midi_handler.close_all()
        self.hid_handler.close_all()
        super().closeEvent(event)
