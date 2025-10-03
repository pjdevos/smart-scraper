"""
Cache Statistics Widget - Shows cache savings
"""
from PyQt6.QtWidgets import (
    QGroupBox, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
)
from PyQt6.QtCore import Qt, QTimer
from backend.storage import CacheManager
from utils.helpers import format_currency


class CacheStatsWidget(QGroupBox):
    """Widget displaying cache statistics and savings"""

    def __init__(self):
        super().__init__("💰 Cache Statistics")
        self.cache_manager = CacheManager()
        self.setup_ui()

        # Auto-refresh every 5 seconds
        self.timer = QTimer()
        self.timer.timeout.connect(self.refresh_stats)
        self.timer.start(5000)

    def setup_ui(self):
        """Setup UI components"""
        layout = QVBoxLayout()

        # Stats display
        self.entries_label = QLabel("Cached entries: 0")
        self.hits_label = QLabel("Cache hits: 0")
        self.savings_label = QLabel("Total saved: €0.00")
        self.hit_rate_label = QLabel("Hit rate: 0%")

        # Style labels
        for label in [self.entries_label, self.hits_label, self.savings_label, self.hit_rate_label]:
            label.setStyleSheet("font-size: 10pt;")

        layout.addWidget(self.entries_label)
        layout.addWidget(self.hits_label)
        layout.addWidget(self.savings_label)
        layout.addWidget(self.hit_rate_label)

        # Buttons
        button_layout = QHBoxLayout()

        self.refresh_button = QPushButton("↻ Refresh")
        self.refresh_button.clicked.connect(self.refresh_stats)
        self.refresh_button.setMaximumWidth(100)

        self.clear_button = QPushButton("Clear Cache")
        self.clear_button.clicked.connect(self.clear_cache)
        self.clear_button.setMaximumWidth(100)

        button_layout.addWidget(self.refresh_button)
        button_layout.addWidget(self.clear_button)
        button_layout.addStretch()

        layout.addLayout(button_layout)

        self.setLayout(layout)

        # Initial refresh
        self.refresh_stats()

    def refresh_stats(self):
        """Refresh cache statistics"""
        try:
            # Get basic stats
            stats = self.cache_manager.get_stats()

            # Get savings estimate
            savings = self.cache_manager.get_savings_estimate()

            # Update labels
            self.entries_label.setText(f"Cached entries: {stats['valid_entries']}")
            self.hits_label.setText(f"Cache hits: {savings['total_cache_hits']}")
            self.savings_label.setText(f"💰 Total saved: €{savings['total_savings_eur']:.2f}")
            self.hit_rate_label.setText(f"Hit rate: {savings['average_hit_rate']:.1f}%")

            # Color code savings
            if savings['total_savings_eur'] > 1.0:
                self.savings_label.setStyleSheet("color: #00ff00; font-weight: bold; font-size: 11pt;")
            elif savings['total_savings_eur'] > 0.1:
                self.savings_label.setStyleSheet("color: #90EE90; font-weight: bold; font-size: 11pt;")
            else:
                self.savings_label.setStyleSheet("font-size: 10pt;")

        except Exception as e:
            self.entries_label.setText(f"Error loading stats: {e}")

    def clear_cache(self):
        """Clear all cache"""
        from PyQt6.QtWidgets import QMessageBox

        reply = QMessageBox.question(
            self,
            'Clear Cache',
            'Are you sure you want to clear all cached data?\n\nThis will reset cost savings tracking.',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            self.cache_manager.clear_all()
            self.refresh_stats()
            QMessageBox.information(self, "Success", "Cache cleared successfully!")

    def cleanup(self):
        """Stop timer when widget is destroyed"""
        if self.timer:
            self.timer.stop()