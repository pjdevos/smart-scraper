"""
Progress Widget
Dedicated widget for displaying scraping progress
"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QProgressBar, QGroupBox
)
from PyQt6.QtCore import Qt


class ProgressWidget(QWidget):
    """Widget for displaying progress"""

    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        """Setup UI components"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # Group box
        group = QGroupBox("Progress")
        group_layout = QVBoxLayout()

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(True)
        group_layout.addWidget(self.progress_bar)

        # Status label
        self.status_label = QLabel("Ready")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setWordWrap(True)
        group_layout.addWidget(self.status_label)

        # Phase indicator
        self.phase_label = QLabel("")
        self.phase_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.phase_label.setStyleSheet("""
            QLabel {
                color: #888888;
                font-size: 10px;
                font-style: italic;
            }
        """)
        group_layout.addWidget(self.phase_label)

        group.setLayout(group_layout)
        layout.addWidget(group)

    def set_progress(self, percentage: int, message: str = ""):
        """Set progress percentage and message"""
        self.progress_bar.setValue(percentage)

        if message:
            self.status_label.setText(message)

        # Update phase indicator based on percentage
        if percentage == 0:
            self.phase_label.setText("")
        elif percentage < 20:
            self.phase_label.setText("📋 Initializing...")
        elif percentage < 40:
            self.phase_label.setText("🔍 Checking cache...")
        elif percentage < 60:
            self.phase_label.setText("🌐 Fetching HTML...")
        elif percentage < 80:
            self.phase_label.setText("🧠 Analyzing content...")
        elif percentage < 100:
            self.phase_label.setText("💾 Processing data...")
        else:
            self.phase_label.setText("✅ Complete!")

    def set_message(self, message: str):
        """Set status message only"""
        self.status_label.setText(message)

    def set_phase(self, phase: str):
        """Set phase indicator"""
        self.phase_label.setText(phase)

    def set_complete(self):
        """Set to completed state"""
        self.progress_bar.setValue(100)
        self.status_label.setText("✓ Scraping completed successfully!")
        self.phase_label.setText("✅ Complete!")
        self.status_label.setStyleSheet("color: #00ff00; font-weight: bold;")

    def set_error(self, message: str = ""):
        """Set to error state"""
        self.progress_bar.setValue(0)
        error_text = f"✗ Error: {message}" if message else "✗ Scraping failed"
        self.status_label.setText(error_text)
        self.phase_label.setText("❌ Failed")
        self.status_label.setStyleSheet("color: #ff0000; font-weight: bold;")

    def reset(self):
        """Reset to initial state"""
        self.progress_bar.setValue(0)
        self.status_label.setText("Ready")
        self.phase_label.setText("")
        self.status_label.setStyleSheet("")
