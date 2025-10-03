"""
URL Input Widget
Dedicated widget for URL input with validation and history
"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QCompleter
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QValidator
import json
from pathlib import Path
from config.settings import DATA_DIR


class URLValidator(QValidator):
    """Custom validator for URLs"""

    def validate(self, text: str, pos: int):
        """Validate URL as user types"""
        if not text:
            return QValidator.State.Intermediate, text, pos

        # Basic URL validation
        if text.startswith('http://') or text.startswith('https://'):
            return QValidator.State.Acceptable, text, pos
        elif 'http' in text[:10]:
            return QValidator.State.Intermediate, text, pos
        else:
            return QValidator.State.Intermediate, text, pos


class URLInputWidget(QWidget):
    """Widget for URL input with validation and history"""

    # Signal emitted when URL changes
    url_changed = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.history_file = DATA_DIR / "url_history.json"
        self.url_history = self._load_history()
        self.setup_ui()

    def setup_ui(self):
        """Setup UI components"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # Label
        label = QLabel("URL:")
        layout.addWidget(label)

        # URL input with autocomplete
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("https://example.com")
        self.url_input.setValidator(URLValidator())

        # Setup autocomplete from history
        if self.url_history:
            completer = QCompleter(self.url_history)
            completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
            self.url_input.setCompleter(completer)

        # Connect signal
        self.url_input.textChanged.connect(self.url_changed.emit)

        layout.addWidget(self.url_input)

    def _load_history(self) -> list:
        """Load URL history from file"""
        if self.history_file.exists():
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return []
        return []

    def _save_history(self):
        """Save URL history to file"""
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(self.url_history[-50:], f, indent=2)  # Keep last 50
        except:
            pass

    def get_url(self) -> str:
        """Get current URL"""
        return self.url_input.text().strip()

    def set_url(self, url: str):
        """Set URL"""
        self.url_input.setText(url)

    def add_to_history(self, url: str):
        """Add URL to history"""
        if url and url not in self.url_history:
            self.url_history.append(url)
            self._save_history()

            # Update autocomplete
            completer = QCompleter(self.url_history)
            completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
            self.url_input.setCompleter(completer)

    def clear(self):
        """Clear input"""
        self.url_input.clear()
