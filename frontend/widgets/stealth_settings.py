"""
Stealth Settings Widget
"""
from PyQt6.QtWidgets import (
    QGroupBox, QVBoxLayout, QHBoxLayout, QLabel,
    QComboBox, QCheckBox
)
from PyQt6.QtCore import pyqtSignal


class StealthSettingsWidget(QGroupBox):
    """Widget for configuring stealth settings"""

    # Signal emitted when settings change
    settings_changed = pyqtSignal(dict)

    def __init__(self):
        super().__init__("Stealth Settings")
        self.setup_ui()

    def setup_ui(self):
        """Setup UI components"""
        layout = QVBoxLayout()

        # Stealth level selector
        level_layout = QHBoxLayout()
        level_label = QLabel("Stealth Level:")
        self.level_combo = QComboBox()
        self.level_combo.addItems(["Basic", "Medium", "High", "Maximum"])
        self.level_combo.setCurrentText("Medium")
        self.level_combo.currentTextChanged.connect(self._on_settings_changed)

        level_layout.addWidget(level_label)
        level_layout.addWidget(self.level_combo)
        level_layout.addStretch()

        layout.addLayout(level_layout)

        # Description of current level
        self.description_label = QLabel()
        self.description_label.setWordWrap(True)
        self.description_label.setStyleSheet("color: #999; font-size: 9pt;")
        layout.addWidget(self.description_label)

        # Options
        self.use_proxies_checkbox = QCheckBox("Use Proxy Rotation")
        self.use_proxies_checkbox.setToolTip("Rotate through configured proxies")
        self.use_proxies_checkbox.stateChanged.connect(self._on_settings_changed)
        layout.addWidget(self.use_proxies_checkbox)

        self.respect_robots_checkbox = QCheckBox("Respect robots.txt")
        self.respect_robots_checkbox.setChecked(True)
        self.respect_robots_checkbox.setToolTip("Follow website scraping rules")
        self.respect_robots_checkbox.stateChanged.connect(self._on_settings_changed)
        layout.addWidget(self.respect_robots_checkbox)

        self.setLayout(layout)

        # Update description
        self._update_description()

    def _update_description(self):
        """Update description based on selected level"""
        level = self.level_combo.currentText().lower()

        descriptions = {
            "basic": "✓ User-Agent headers, basic delays (2-5s), rate limiting",
            "medium": "✓ Basic + scrolling, cookies, random jitter, gradual loading",
            "high": "✓ Medium + mouse movements, UA rotation, fingerprint masking (5-10s delays)",
            "maximum": "✓ High + proxies, CAPTCHA handling, very slow (1 req/min)"
        }

        self.description_label.setText(descriptions.get(level, ""))

    def _on_settings_changed(self):
        """Emit settings changed signal"""
        self._update_description()
        self.settings_changed.emit(self.get_settings())

    def get_settings(self) -> dict:
        """
        Get current stealth settings.

        Returns:
            Dictionary with settings
        """
        return {
            "stealth_level": self.level_combo.currentText().lower(),
            "use_proxies": self.use_proxies_checkbox.isChecked(),
            "respect_robots": self.respect_robots_checkbox.isChecked()
        }

    def set_settings(self, settings: dict):
        """
        Set stealth settings.

        Args:
            settings: Dictionary with settings
        """
        if "stealth_level" in settings:
            level = settings["stealth_level"].capitalize()
            self.level_combo.setCurrentText(level)

        if "use_proxies" in settings:
            self.use_proxies_checkbox.setChecked(settings["use_proxies"])

        if "respect_robots" in settings:
            self.respect_robots_checkbox.setChecked(settings["respect_robots"])