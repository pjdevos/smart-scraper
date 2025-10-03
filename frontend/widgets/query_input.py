"""
Query Input Widget
Dedicated widget for natural language query input with templates
"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QTextEdit, QComboBox, QPushButton
)
from PyQt6.QtCore import pyqtSignal
import json
from pathlib import Path
from config.settings import DATA_DIR


class QueryInputWidget(QWidget):
    """Widget for natural language query input"""

    # Signal emitted when query changes
    query_changed = pyqtSignal(str)

    # Common query templates
    TEMPLATES = {
        "Custom": "",
        "Product Data": "product name, price, rating, description",
        "Article Content": "article title, author, publish date, content",
        "Contact Info": "email addresses, phone numbers, social media links",
        "Job Listings": "job title, company, location, salary, description",
        "Event Details": "event name, date, time, location, ticket price",
        "Real Estate": "property address, price, bedrooms, bathrooms, square feet",
        "Reviews": "reviewer name, rating, review text, review date"
    }

    def __init__(self):
        super().__init__()
        self.history_file = DATA_DIR / "query_history.json"
        self.query_history = self._load_history()
        self.setup_ui()

    def setup_ui(self):
        """Setup UI components"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # Header with label and template selector
        header_layout = QHBoxLayout()

        label = QLabel("What to extract (natural language):")
        header_layout.addWidget(label)

        header_layout.addStretch()

        # Template selector
        template_label = QLabel("Template:")
        header_layout.addWidget(template_label)

        self.template_combo = QComboBox()
        self.template_combo.addItems(self.TEMPLATES.keys())
        self.template_combo.currentTextChanged.connect(self._on_template_changed)
        header_layout.addWidget(self.template_combo)

        layout.addLayout(header_layout)

        # Query input
        self.query_input = QTextEdit()
        self.query_input.setPlaceholderText(
            "Example: product name, price, and rating\n"
            "Or: email addresses and phone numbers\n"
            "Or: article title, author, and publish date"
        )
        self.query_input.setMaximumHeight(80)
        self.query_input.textChanged.connect(self._on_text_changed)

        layout.addWidget(self.query_input)

        # History dropdown (hidden by default, shows recent queries)
        self.history_combo = QComboBox()
        self.history_combo.setVisible(False)
        if self.query_history:
            self.history_combo.addItems(["Recent queries..."] + self.query_history[-10:])
            self.history_combo.currentTextChanged.connect(self._on_history_selected)
            self.history_combo.setVisible(True)

        layout.addWidget(self.history_combo)

    def _on_template_changed(self, template_name: str):
        """Handle template selection"""
        if template_name != "Custom":
            template_text = self.TEMPLATES[template_name]
            self.query_input.setPlainText(template_text)

    def _on_text_changed(self):
        """Handle text change"""
        self.query_changed.emit(self.get_query())

    def _on_history_selected(self, query: str):
        """Handle history selection"""
        if query and query != "Recent queries...":
            self.query_input.setPlainText(query)
            self.template_combo.setCurrentText("Custom")

    def _load_history(self) -> list:
        """Load query history from file"""
        if self.history_file.exists():
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return []
        return []

    def _save_history(self):
        """Save query history to file"""
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(self.query_history[-50:], f, indent=2)  # Keep last 50
        except:
            pass

    def get_query(self) -> str:
        """Get current query"""
        return self.query_input.toPlainText().strip()

    def set_query(self, query: str):
        """Set query"""
        self.query_input.setPlainText(query)
        self.template_combo.setCurrentText("Custom")

    def add_to_history(self, query: str):
        """Add query to history"""
        if query and query not in self.query_history:
            self.query_history.append(query)
            self._save_history()

            # Update history combo
            self.history_combo.clear()
            self.history_combo.addItems(["Recent queries..."] + self.query_history[-10:])
            self.history_combo.setVisible(True)

    def clear(self):
        """Clear input"""
        self.query_input.clear()
        self.template_combo.setCurrentText("Custom")
