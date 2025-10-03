"""
Method Selector Widget
Dedicated widget for scraping method selection with descriptions
"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox
)
from PyQt6.QtCore import pyqtSignal
from backend.scraper_engine import ScrapingMethod


class MethodSelectorWidget(QWidget):
    """Widget for scraping method selection"""

    # Signal emitted when method changes
    method_changed = pyqtSignal(str)

    # Method descriptions
    DESCRIPTIONS = {
        "Auto": "Automatically selects best method (recommended)",
        "Requests": "Fast for static HTML pages",
        "Selenium": "For JavaScript-heavy sites (slower)",
        "Playwright": "Modern, faster than Selenium",
        "Stealth": "Maximum anti-detection, slowest"
    }

    # Speed indicators
    SPEEDS = {
        "Auto": "⚡ Adaptive",
        "Requests": "⚡⚡⚡ Very Fast",
        "Selenium": "⚡ Slow",
        "Playwright": "⚡⚡ Fast",
        "Stealth": "🐌 Very Slow"
    }

    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        """Setup UI components"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # Header
        header_layout = QHBoxLayout()
        label = QLabel("Scraping Method:")
        header_layout.addWidget(label)
        header_layout.addStretch()
        layout.addLayout(header_layout)

        # Method selector
        self.method_combo = QComboBox()
        self.method_combo.addItems(["Auto", "Requests", "Selenium", "Playwright", "Stealth"])
        self.method_combo.setCurrentText("Auto")
        self.method_combo.currentTextChanged.connect(self._on_method_changed)
        layout.addWidget(self.method_combo)

        # Description label
        self.description_label = QLabel()
        self.description_label.setWordWrap(True)
        self.description_label.setStyleSheet("""
            QLabel {
                color: #888888;
                font-size: 11px;
                padding: 5px;
                background-color: rgba(255, 255, 255, 0.05);
                border-radius: 3px;
            }
        """)
        layout.addWidget(self.description_label)

        # Speed indicator
        self.speed_label = QLabel()
        self.speed_label.setStyleSheet("""
            QLabel {
                color: #00ff00;
                font-size: 10px;
                font-weight: bold;
            }
        """)
        layout.addWidget(self.speed_label)

        # Update initial description
        self._update_description("Auto")

    def _on_method_changed(self, method: str):
        """Handle method change"""
        self._update_description(method)
        self.method_changed.emit(method)

    def _update_description(self, method: str):
        """Update description and speed indicator"""
        description = self.DESCRIPTIONS.get(method, "")
        speed = self.SPEEDS.get(method, "")

        self.description_label.setText(description)
        self.speed_label.setText(f"Speed: {speed}")

    def get_selected_method(self) -> ScrapingMethod:
        """Get selected scraping method as enum"""
        method_text = self.method_combo.currentText().lower()
        return ScrapingMethod[method_text.upper()]

    def set_method(self, method: str):
        """Set selected method"""
        self.method_combo.setCurrentText(method)

    def get_method_name(self) -> str:
        """Get selected method name as string"""
        return self.method_combo.currentText()
