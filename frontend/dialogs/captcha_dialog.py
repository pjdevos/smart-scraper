"""
CAPTCHA Solver Dialog
Manual CAPTCHA solving interface
"""
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QTextEdit, QGroupBox, QProgressBar
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont
from PyQt6.QtWebEngineWidgets import QWebEngineView
import logging

logger = logging.getLogger(__name__)


class CaptchaSolverDialog(QDialog):
    """Dialog for manual CAPTCHA solving"""

    def __init__(self, url: str, timeout_seconds: int = 300, parent=None):
        """
        Initialize CAPTCHA solver dialog.

        Args:
            url: URL with CAPTCHA
            timeout_seconds: Time limit for solving (default 5 minutes)
            parent: Parent widget
        """
        super().__init__(parent)
        self.url = url
        self.timeout_seconds = timeout_seconds
        self.time_remaining = timeout_seconds
        self.solved = False

        self.setup_ui()
        self.start_timer()

        logger.info(f"CAPTCHA dialog opened for: {url}")

    def setup_ui(self):
        """Setup UI components"""
        self.setWindowTitle("Manual CAPTCHA Solving Required")
        self.setGeometry(100, 100, 900, 700)
        self.setModal(True)

        layout = QVBoxLayout(self)

        # Header
        header = QLabel("🧩 CAPTCHA Detected - Manual Intervention Required")
        header_font = QFont()
        header_font.setPointSize(14)
        header_font.setBold(True)
        header.setFont(header_font)
        layout.addWidget(header)

        # Instructions
        instructions_group = QGroupBox("Instructions")
        instructions_layout = QVBoxLayout()

        instructions_text = QLabel(
            "A CAPTCHA challenge has been detected on this page.\n\n"
            "Please solve the CAPTCHA in the browser below and click 'Done' when completed.\n\n"
            "The scraping process will continue automatically after you solve the CAPTCHA."
        )
        instructions_text.setWordWrap(True)
        instructions_layout.addWidget(instructions_text)

        instructions_group.setLayout(instructions_layout)
        layout.addWidget(instructions_group)

        # Browser view
        browser_group = QGroupBox(f"Browser View - {self.url}")
        browser_layout = QVBoxLayout()

        self.browser = QWebEngineView()
        self.browser.setUrl(self.url)
        browser_layout.addWidget(self.browser)

        browser_group.setLayout(browser_layout)
        layout.addWidget(browser_group, stretch=1)

        # Timer and progress
        timer_layout = QHBoxLayout()

        self.timer_label = QLabel(f"⏱️ Time remaining: {self._format_time(self.time_remaining)}")
        self.timer_label.setStyleSheet("font-size: 12pt; font-weight: bold;")
        timer_layout.addWidget(self.timer_label)

        timer_layout.addStretch()
        layout.addLayout(timer_layout)

        # Progress bar (countdown)
        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximum(self.timeout_seconds)
        self.progress_bar.setValue(self.timeout_seconds)
        self.progress_bar.setFormat("%v seconds remaining")
        layout.addWidget(self.progress_bar)

        # Buttons
        button_layout = QHBoxLayout()

        self.done_btn = QPushButton("✓ Done (CAPTCHA Solved)")
        self.done_btn.clicked.connect(self.on_done)
        self.done_btn.setMinimumHeight(40)
        self.done_btn.setStyleSheet("""
            QPushButton {
                background-color: #00aa00;
                color: white;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #00cc00;
            }
        """)
        button_layout.addWidget(self.done_btn)

        self.cancel_btn = QPushButton("✗ Cancel")
        self.cancel_btn.clicked.connect(self.on_cancel)
        self.cancel_btn.setMinimumHeight(40)
        button_layout.addWidget(self.cancel_btn)

        layout.addLayout(button_layout)

        # Status label
        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet("color: #888888;")
        layout.addWidget(self.status_label)

    def start_timer(self):
        """Start countdown timer"""
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)
        self.timer.start(1000)  # Update every second

    def update_timer(self):
        """Update countdown timer"""
        self.time_remaining -= 1

        # Update labels
        self.timer_label.setText(f"⏱️ Time remaining: {self._format_time(self.time_remaining)}")
        self.progress_bar.setValue(self.time_remaining)

        # Change color when time is running out
        if self.time_remaining <= 30:
            self.timer_label.setStyleSheet("font-size: 12pt; font-weight: bold; color: #ff0000;")
        elif self.time_remaining <= 60:
            self.timer_label.setStyleSheet("font-size: 12pt; font-weight: bold; color: #ffaa00;")

        # Timeout
        if self.time_remaining <= 0:
            self.on_timeout()

    def _format_time(self, seconds: int) -> str:
        """Format seconds as MM:SS"""
        minutes = seconds // 60
        secs = seconds % 60
        return f"{minutes:02d}:{secs:02d}"

    def on_done(self):
        """Handle done button click"""
        self.solved = True
        self.timer.stop()
        logger.info("CAPTCHA marked as solved by user")
        self.accept()

    def on_cancel(self):
        """Handle cancel button click"""
        self.solved = False
        self.timer.stop()
        logger.info("CAPTCHA solving cancelled by user")
        self.reject()

    def on_timeout(self):
        """Handle timeout"""
        self.timer.stop()
        self.status_label.setText("⏱️ Timeout! CAPTCHA not solved in time.")
        self.status_label.setStyleSheet("color: #ff0000; font-weight: bold;")
        self.done_btn.setEnabled(False)
        logger.warning("CAPTCHA solving timed out")

        # Auto-close after 3 seconds
        QTimer.singleShot(3000, self.reject)

    def is_solved(self) -> bool:
        """Check if CAPTCHA was solved"""
        return self.solved

    def get_page_url(self) -> str:
        """Get current page URL (may have changed after CAPTCHA)"""
        return self.browser.url().toString()
