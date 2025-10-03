"""
CAPTCHA Settings Widget
Configuration for CAPTCHA handling
"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QComboBox, QCheckBox, QSpinBox, QLineEdit, QGroupBox, QPushButton
)
from PyQt6.QtCore import pyqtSignal
from config.settings import TWOCAPTCHA_API_KEY, ANTICAPTCHA_API_KEY


class CaptchaSettingsWidget(QWidget):
    """Widget for CAPTCHA settings"""

    # Signal emitted when settings change
    settings_changed = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        """Setup UI components"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # Detection settings
        detection_group = QGroupBox("CAPTCHA Detection")
        detection_layout = QVBoxLayout()

        self.enable_detection = QCheckBox("Enable automatic CAPTCHA detection")
        self.enable_detection.setChecked(True)
        self.enable_detection.toggled.connect(self._on_detection_toggled)
        detection_layout.addWidget(self.enable_detection)

        info_label = QLabel(
            "Automatically detect and handle CAPTCHAs during scraping.\n"
            "Options: Manual solving, API solving, or skip."
        )
        info_label.setStyleSheet("color: #888888; font-size: 10px;")
        info_label.setWordWrap(True)
        detection_layout.addWidget(info_label)

        detection_group.setLayout(detection_layout)
        layout.addWidget(detection_group)

        # Solving method
        method_group = QGroupBox("Solving Method")
        method_layout = QVBoxLayout()

        method_label = QLabel("When CAPTCHA is detected:")
        method_layout.addWidget(method_label)

        self.method_combo = QComboBox()
        self.method_combo.addItems([
            "Manual (pause for user)",
            "API - 2Captcha",
            "API - Anti-Captcha",
            "Skip page"
        ])
        self.method_combo.currentTextChanged.connect(self._on_method_changed)
        method_layout.addWidget(self.method_combo)

        method_group.setLayout(method_layout)
        layout.addWidget(method_group)

        # Manual solving settings
        self.manual_group = QGroupBox("Manual Solving Settings")
        manual_layout = QVBoxLayout()

        timeout_layout = QHBoxLayout()
        timeout_label = QLabel("Timeout (seconds):")
        timeout_layout.addWidget(timeout_label)

        self.manual_timeout = QSpinBox()
        self.manual_timeout.setMinimum(30)
        self.manual_timeout.setMaximum(600)
        self.manual_timeout.setValue(300)
        timeout_layout.addWidget(self.manual_timeout)
        timeout_layout.addStretch()

        manual_layout.addLayout(timeout_layout)

        manual_info = QLabel("Browser window will pause for you to solve the CAPTCHA manually.")
        manual_info.setStyleSheet("color: #888888; font-size: 10px;")
        manual_info.setWordWrap(True)
        manual_layout.addWidget(manual_info)

        self.manual_group.setLayout(manual_layout)
        layout.addWidget(self.manual_group)

        # API settings
        self.api_group = QGroupBox("API Settings")
        api_layout = QVBoxLayout()

        # 2Captcha API key
        twocaptcha_layout = QHBoxLayout()
        twocaptcha_label = QLabel("2Captcha API Key:")
        twocaptcha_layout.addWidget(twocaptcha_label)

        self.twocaptcha_key = QLineEdit()
        self.twocaptcha_key.setPlaceholderText("Enter 2Captcha API key")
        self.twocaptcha_key.setEchoMode(QLineEdit.EchoMode.Password)
        if TWOCAPTCHA_API_KEY:
            self.twocaptcha_key.setText(TWOCAPTCHA_API_KEY)
            self.twocaptcha_key.setEnabled(False)
        twocaptcha_layout.addWidget(self.twocaptcha_key)

        api_layout.addLayout(twocaptcha_layout)

        # Anti-Captcha API key
        anticaptcha_layout = QHBoxLayout()
        anticaptcha_label = QLabel("Anti-Captcha API Key:")
        anticaptcha_layout.addWidget(anticaptcha_label)

        self.anticaptcha_key = QLineEdit()
        self.anticaptcha_key.setPlaceholderText("Enter Anti-Captcha API key")
        self.anticaptcha_key.setEchoMode(QLineEdit.EchoMode.Password)
        if ANTICAPTCHA_API_KEY:
            self.anticaptcha_key.setText(ANTICAPTCHA_API_KEY)
            self.anticaptcha_key.setEnabled(False)
        anticaptcha_layout.addWidget(self.anticaptcha_key)

        api_layout.addLayout(anticaptcha_layout)

        # Test balance button
        self.test_balance_btn = QPushButton("Test Balance")
        self.test_balance_btn.clicked.connect(self._test_balance)
        api_layout.addWidget(self.test_balance_btn)

        api_info = QLabel(
            "API keys should be configured in .env file.\n"
            "2Captcha: ~$2.99/1000 CAPTCHAs\n"
            "Anti-Captcha: ~$2.00/1000 CAPTCHAs"
        )
        api_info.setStyleSheet("color: #888888; font-size: 10px;")
        api_info.setWordWrap(True)
        api_layout.addWidget(api_info)

        self.api_group.setLayout(api_layout)
        self.api_group.setVisible(False)  # Hidden by default
        layout.addWidget(self.api_group)

        layout.addStretch()

        # Initial state
        self._on_method_changed(self.method_combo.currentText())

    def _on_detection_toggled(self, checked: bool):
        """Handle detection toggle"""
        self.method_combo.setEnabled(checked)
        self.settings_changed.emit()

    def _on_method_changed(self, method: str):
        """Handle method change"""
        # Show/hide groups based on method
        self.manual_group.setVisible("Manual" in method)
        self.api_group.setVisible("API" in method)
        self.settings_changed.emit()

    def _test_balance(self):
        """Test API balance"""
        from backend.captcha.api_solvers import get_solver
        from PyQt6.QtWidgets import QMessageBox

        method = self.method_combo.currentText()

        if "2Captcha" in method:
            solver = get_solver("2captcha")
            service = "2Captcha"
        elif "Anti-Captcha" in method:
            solver = get_solver("anticaptcha")
            service = "Anti-Captcha"
        else:
            QMessageBox.warning(self, "No API Selected", "Please select an API method first.")
            return

        if solver:
            balance = solver.get_balance()
            if balance is not None:
                QMessageBox.information(
                    self,
                    f"{service} Balance",
                    f"Current balance: ${balance:.2f}"
                )
            else:
                QMessageBox.warning(
                    self,
                    f"{service} Error",
                    "Failed to retrieve balance. Check your API key."
                )
        else:
            QMessageBox.warning(
                self,
                "API Not Configured",
                f"{service} API key not configured. Add it to your .env file."
            )

    def get_settings(self) -> dict:
        """Get current settings"""
        method = self.method_combo.currentText()

        return {
            "enabled": self.enable_detection.isChecked(),
            "method": method,
            "manual_timeout": self.manual_timeout.value(),
            "twocaptcha_key": self.twocaptcha_key.text() if self.twocaptcha_key.isEnabled() else TWOCAPTCHA_API_KEY,
            "anticaptcha_key": self.anticaptcha_key.text() if self.anticaptcha_key.isEnabled() else ANTICAPTCHA_API_KEY
        }

    def set_method(self, method: str):
        """Set solving method"""
        index = self.method_combo.findText(method)
        if index >= 0:
            self.method_combo.setCurrentIndex(index)
