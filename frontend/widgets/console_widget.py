"""
Console Widget
Real-time log display widget
"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QTextEdit, QGroupBox, QHBoxLayout, QPushButton
)
from PyQt6.QtGui import QTextCursor, QFont
from PyQt6.QtCore import Qt
from datetime import datetime


class ConsoleWidget(QWidget):
    """Widget for displaying console output"""

    def __init__(self):
        super().__init__()
        self.max_lines = 1000  # Maximum lines to keep
        self.setup_ui()

    def setup_ui(self):
        """Setup UI components"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # Group box
        group = QGroupBox("Console Output")
        group_layout = QVBoxLayout()

        # Console text area
        self.console = QTextEdit()
        self.console.setReadOnly(True)
        self.console.setMaximumHeight(200)

        # Use monospace font
        font = QFont("Consolas", 9)
        font.setStyleHint(QFont.StyleHint.Monospace)
        self.console.setFont(font)

        # Dark console style
        self.console.setStyleSheet("""
            QTextEdit {
                background-color: #1a1a1a;
                color: #00ff00;
                border: 1px solid #333333;
                padding: 5px;
            }
        """)

        group_layout.addWidget(self.console)

        # Control buttons
        button_layout = QHBoxLayout()

        self.clear_btn = QPushButton("🗑️ Clear")
        self.clear_btn.clicked.connect(self.clear)
        self.clear_btn.setMaximumWidth(100)
        button_layout.addWidget(self.clear_btn)

        self.autoscroll_btn = QPushButton("📜 Auto-scroll: ON")
        self.autoscroll_btn.setCheckable(True)
        self.autoscroll_btn.setChecked(True)
        self.autoscroll_btn.clicked.connect(self._toggle_autoscroll)
        self.autoscroll_btn.setMaximumWidth(150)
        button_layout.addWidget(self.autoscroll_btn)

        button_layout.addStretch()
        group_layout.addLayout(button_layout)

        group.setLayout(group_layout)
        layout.addWidget(group)

        self.autoscroll = True

    def _toggle_autoscroll(self):
        """Toggle auto-scroll"""
        self.autoscroll = self.autoscroll_btn.isChecked()
        if self.autoscroll:
            self.autoscroll_btn.setText("📜 Auto-scroll: ON")
        else:
            self.autoscroll_btn.setText("📜 Auto-scroll: OFF")

    def log(self, message: str, level: str = "INFO"):
        """
        Log a message to console.

        Args:
            message: Message to log
            level: Log level (INFO, WARNING, ERROR, DEBUG, SUCCESS)
        """
        timestamp = datetime.now().strftime("%H:%M:%S")

        # Color coding based on level
        color = "#00ff00"  # Default green
        if level == "ERROR":
            color = "#ff0000"  # Red
        elif level == "WARNING":
            color = "#ffaa00"  # Orange
        elif level == "DEBUG":
            color = "#888888"  # Gray
        elif level == "SUCCESS":
            color = "#00ffff"  # Cyan

        # Format message
        formatted = f'<span style="color: #888888;">[{timestamp}]</span> '
        formatted += f'<span style="color: {color}; font-weight: bold;">[{level}]</span> '
        formatted += f'<span style="color: #cccccc;">{message}</span>'

        self.console.append(formatted)

        # Auto-scroll to bottom
        if self.autoscroll:
            scrollbar = self.console.verticalScrollBar()
            scrollbar.setValue(scrollbar.maximum())

        # Limit number of lines
        self._limit_lines()

    def log_info(self, message: str):
        """Log info message"""
        self.log(message, "INFO")

    def log_warning(self, message: str):
        """Log warning message"""
        self.log(message, "WARNING")

    def log_error(self, message: str):
        """Log error message"""
        self.log(message, "ERROR")

    def log_debug(self, message: str):
        """Log debug message"""
        self.log(message, "DEBUG")

    def log_success(self, message: str):
        """Log success message"""
        self.log(message, "SUCCESS")

    def _limit_lines(self):
        """Limit console to max_lines"""
        document = self.console.document()
        if document.blockCount() > self.max_lines:
            cursor = QTextCursor(document)
            cursor.movePosition(QTextCursor.MoveOperation.Start)
            cursor.movePosition(
                QTextCursor.MoveOperation.Down,
                QTextCursor.MoveMode.KeepAnchor,
                document.blockCount() - self.max_lines
            )
            cursor.removeSelectedText()

    def clear(self):
        """Clear console"""
        self.console.clear()
        self.log_info("Console cleared")
