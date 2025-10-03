"""
Learned Selectors Statistics Widget
"""
from PyQt6.QtWidgets import (
    QGroupBox, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QMessageBox
)
from PyQt6.QtCore import QTimer
from backend.storage import SelectorManager


class SelectorStatsWidget(QGroupBox):
    """Widget displaying learned selector statistics"""

    def __init__(self):
        super().__init__("🎓 Learned Selectors")
        self.selector_manager = SelectorManager()
        self.setup_ui()

        # Auto-refresh every 5 seconds
        self.timer = QTimer()
        self.timer.timeout.connect(self.refresh_stats)
        self.timer.start(5000)

    def setup_ui(self):
        """Setup UI components"""
        layout = QVBoxLayout()

        # Stats display
        self.domains_label = QLabel("Learned domains: 0")
        self.queries_label = QLabel("Total queries: 0")
        self.reuses_label = QLabel("Selector reuses: 0")
        self.savings_label = QLabel("Saved: €0.00")

        # Style labels
        for label in [self.domains_label, self.queries_label, self.reuses_label, self.savings_label]:
            label.setStyleSheet("font-size: 10pt;")

        layout.addWidget(self.domains_label)
        layout.addWidget(self.queries_label)
        layout.addWidget(self.reuses_label)
        layout.addWidget(self.savings_label)

        # Top domains button
        self.top_domains_button = QPushButton("📊 View Top Domains")
        self.top_domains_button.clicked.connect(self.show_top_domains)
        layout.addWidget(self.top_domains_button)

        self.setLayout(layout)

        # Initial refresh
        self.refresh_stats()

    def refresh_stats(self):
        """Refresh selector statistics"""
        try:
            savings = self.selector_manager.get_savings_estimate()

            self.domains_label.setText(f"Learned domains: {savings['learned_domains']}")
            self.queries_label.setText(f"Total queries: {savings['learned_queries']}")
            self.reuses_label.setText(f"Selector reuses: {savings['total_reuses']}")
            self.savings_label.setText(f"🎓 Saved: €{savings['total_savings_eur']:.2f}")

            # Color code savings
            if savings['total_savings_eur'] > 1.0:
                self.savings_label.setStyleSheet("color: #00ff00; font-weight: bold; font-size: 11pt;")
            elif savings['total_savings_eur'] > 0.1:
                self.savings_label.setStyleSheet("color: #90EE90; font-weight: bold; font-size: 11pt;")
            else:
                self.savings_label.setStyleSheet("font-size: 10pt;")

        except Exception as e:
            self.domains_label.setText(f"Error: {e}")

    def show_top_domains(self):
        """Show top domains dialog"""
        top_domains = self.selector_manager.get_top_domains(10)

        if not top_domains:
            QMessageBox.information(
                self,
                "No Domains",
                "No learned selectors yet. Scrape some pages first!"
            )
            return

        # Build message
        message = "Top domains by usage:\n\n"
        for i, domain_info in enumerate(top_domains, 1):
            message += f"{i}. {domain_info['domain']}\n"
            message += f"   Queries: {domain_info['queries']}, Uses: {domain_info['uses']}\n\n"

        savings = self.selector_manager.get_savings_estimate()
        message += f"\n💰 Total saved from selector reuse: €{savings['total_savings_eur']:.2f}"
        message += f"\n📊 Reuse rate: {savings['reuse_rate']:.1f}%"

        QMessageBox.information(
            self,
            "Top Learned Domains",
            message
        )

    def cleanup(self):
        """Stop timer when widget is destroyed"""
        if self.timer:
            self.timer.stop()