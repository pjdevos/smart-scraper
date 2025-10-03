"""
Main Application Window
"""
import sys
from pathlib import Path
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QTextEdit, QComboBox, QPushButton,
    QProgressBar, QGroupBox, QMessageBox, QFileDialog, QScrollArea,
    QCheckBox, QSpinBox
)
from PyQt6.QtCore import Qt, QThread
from PyQt6.QtGui import QFont

from config.settings import (
    WINDOW_TITLE, WINDOW_WIDTH, WINDOW_HEIGHT,
    DEFAULT_DAILY_BUDGET, ANTHROPIC_API_KEY, EXPORTS_DIR
)
from utils.validators import validate_url, validate_query
from utils.helpers import format_currency
from backend.scraper_engine import ScrapingMethod
from frontend.widgets.results_table import ResultsTable
from frontend.widgets.stealth_settings import StealthSettingsWidget
from frontend.widgets.cache_stats_widget import CacheStatsWidget
from frontend.widgets.selector_stats_widget import SelectorStatsWidget
from frontend.workers.scraper_worker import ScraperWorker

import pandas as pd
import json


class MainWindow(QMainWindow):
    """Main application window"""

    def __init__(self):
        super().__init__()
        self.worker = None
        self.current_result = None
        self.setup_ui()
        self.load_stylesheet()

    def setup_ui(self):
        """Setup user interface"""
        self.setWindowTitle(WINDOW_TITLE)
        self.setGeometry(100, 100, WINDOW_WIDTH, WINDOW_HEIGHT)

        # Central widget with scroll area
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main layout for scroll area
        wrapper_layout = QVBoxLayout(central_widget)
        wrapper_layout.setContentsMargins(0, 0, 0, 0)

        # Create scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

        # Content widget inside scroll area
        content_widget = QWidget()
        scroll_area.setWidget(content_widget)
        wrapper_layout.addWidget(scroll_area)

        # Main layout for content
        main_layout = QVBoxLayout(content_widget)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # Title
        title_label = QLabel("SmartScraper")
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title_label.setFont(title_font)
        main_layout.addWidget(title_label)

        subtitle_label = QLabel("AI-Powered Web Scraping Tool")
        main_layout.addWidget(subtitle_label)

        # Input section
        input_group = QGroupBox("Input")
        input_layout = QVBoxLayout()

        # URL input
        url_label = QLabel("URL:")
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("https://example.com")
        input_layout.addWidget(url_label)
        input_layout.addWidget(self.url_input)

        # Query input
        query_label = QLabel("What to extract (natural language):")
        self.query_input = QTextEdit()
        self.query_input.setPlaceholderText("Example: product name, price, and rating")
        self.query_input.setMaximumHeight(80)
        input_layout.addWidget(query_label)
        input_layout.addWidget(self.query_input)

        # Method selector
        method_layout = QHBoxLayout()
        method_label = QLabel("Scraping Method:")
        self.method_combo = QComboBox()
        self.method_combo.addItems(["Auto", "Requests", "Selenium", "Playwright", "Stealth"])
        self.method_combo.setCurrentText("Auto")
        method_layout.addWidget(method_label)
        method_layout.addWidget(self.method_combo)
        method_layout.addStretch()
        input_layout.addLayout(method_layout)

        # Pagination options
        pagination_layout = QHBoxLayout()
        self.pagination_checkbox = QCheckBox("Enable Pagination")
        self.pagination_checkbox.setChecked(False)
        self.pagination_checkbox.toggled.connect(self._on_pagination_toggled)

        self.max_pages_label = QLabel("Max Pages:")
        self.max_pages_spinbox = QSpinBox()
        self.max_pages_spinbox.setMinimum(1)
        self.max_pages_spinbox.setMaximum(100)
        self.max_pages_spinbox.setValue(5)
        self.max_pages_spinbox.setEnabled(False)

        pagination_layout.addWidget(self.pagination_checkbox)
        pagination_layout.addWidget(self.max_pages_label)
        pagination_layout.addWidget(self.max_pages_spinbox)
        pagination_layout.addStretch()
        input_layout.addLayout(pagination_layout)

        input_group.setLayout(input_layout)
        main_layout.addWidget(input_group)

        # Stealth settings and Stats in horizontal layout
        settings_layout = QHBoxLayout()
        self.stealth_settings = StealthSettingsWidget()
        settings_layout.addWidget(self.stealth_settings, 2)

        # Stats layout (Cache + Selectors)
        stats_layout = QVBoxLayout()
        self.cache_stats = CacheStatsWidget()
        self.selector_stats = SelectorStatsWidget()
        stats_layout.addWidget(self.cache_stats)
        stats_layout.addWidget(self.selector_stats)

        settings_layout.addLayout(stats_layout, 1)
        main_layout.addLayout(settings_layout)

        # Control buttons
        button_layout = QHBoxLayout()
        self.start_button = QPushButton("Start Scraping")
        self.start_button.clicked.connect(self.start_scraping)
        self.stop_button = QPushButton("Stop")
        self.stop_button.setEnabled(False)
        self.stop_button.clicked.connect(self.stop_scraping)
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.stop_button)
        button_layout.addStretch()
        main_layout.addLayout(button_layout)

        # Progress section
        progress_group = QGroupBox("Progress")
        progress_layout = QVBoxLayout()

        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        progress_layout.addWidget(self.progress_bar)

        self.status_label = QLabel("Ready")
        progress_layout.addWidget(self.status_label)

        progress_group.setLayout(progress_layout)
        main_layout.addWidget(progress_group)

        # Results section
        results_group = QGroupBox("Results")
        results_layout = QVBoxLayout()

        self.results_table = ResultsTable()
        results_layout.addWidget(self.results_table)

        # Export buttons
        export_layout = QHBoxLayout()
        self.export_csv_button = QPushButton("Export CSV")
        self.export_csv_button.clicked.connect(self.export_csv)
        self.export_csv_button.setEnabled(False)

        self.export_json_button = QPushButton("Export JSON")
        self.export_json_button.clicked.connect(self.export_json)
        self.export_json_button.setEnabled(False)

        self.export_excel_button = QPushButton("Export Excel")
        self.export_excel_button.clicked.connect(self.export_excel)
        self.export_excel_button.setEnabled(False)

        export_layout.addWidget(self.export_csv_button)
        export_layout.addWidget(self.export_json_button)
        export_layout.addWidget(self.export_excel_button)
        export_layout.addStretch()
        results_layout.addLayout(export_layout)

        results_group.setLayout(results_layout)
        main_layout.addWidget(results_group)

        # Status bar
        self.statusBar().showMessage("Ready")

    def _on_pagination_toggled(self, checked: bool):
        """Enable/disable pagination controls"""
        self.max_pages_spinbox.setEnabled(checked)

    def load_stylesheet(self):
        """Load dark theme stylesheet"""
        stylesheet_path = Path(__file__).parent / "styles" / "dark_theme.qss"
        if stylesheet_path.exists():
            with open(stylesheet_path, 'r') as f:
                self.setStyleSheet(f.read())

    def start_scraping(self):
        """Start scraping process"""
        # Validate inputs
        url = self.url_input.text().strip()
        query = self.query_input.toPlainText().strip()

        is_valid, result = validate_url(url)
        if not is_valid:
            QMessageBox.warning(self, "Invalid URL", result)
            return

        url = result  # Use normalized URL

        is_valid, error = validate_query(query)
        if not is_valid:
            QMessageBox.warning(self, "Invalid Query", error)
            return

        # Get method
        method_text = self.method_combo.currentText().lower()
        method = ScrapingMethod[method_text.upper()]

        # Get stealth settings
        stealth_settings = self.stealth_settings.get_settings()

        # Check API key
        if not ANTHROPIC_API_KEY:
            QMessageBox.warning(
                self,
                "API Key Missing",
                "Please set your ANTHROPIC_API_KEY in the .env file"
            )
            return

        # Update UI
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        self.progress_bar.setValue(0)
        self.status_label.setText("Starting...")
        self.results_table.clear_data()
        self.export_csv_button.setEnabled(False)
        self.export_json_button.setEnabled(False)
        self.export_excel_button.setEnabled(False)

        # Get pagination settings
        enable_pagination = self.pagination_checkbox.isChecked()
        max_pages = self.max_pages_spinbox.value()

        # Create and start worker
        self.worker = ScraperWorker(
            url=url,
            query=query,
            method=method,
            api_key=ANTHROPIC_API_KEY,
            daily_budget=DEFAULT_DAILY_BUDGET,
            stealth_level=stealth_settings["stealth_level"],
            use_proxies=stealth_settings["use_proxies"],
            respect_robots=stealth_settings["respect_robots"],
            enable_pagination=enable_pagination,
            max_pages=max_pages
        )

        self.worker.progress.connect(self.update_progress)
        self.worker.finished.connect(self.scraping_finished)
        self.worker.error.connect(self.scraping_error)

        self.worker.start()

    def stop_scraping(self):
        """Stop scraping process"""
        if self.worker and self.worker.isRunning():
            self.worker.terminate()
            self.worker.wait()
            self.status_label.setText("Stopped by user")
            self.start_button.setEnabled(True)
            self.stop_button.setEnabled(False)

    def update_progress(self, message: str, percentage: int):
        """Update progress bar and status"""
        self.progress_bar.setValue(percentage)
        self.status_label.setText(message)
        self.statusBar().showMessage(message)

    def scraping_finished(self, result: dict):
        """Handle scraping completion"""
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.progress_bar.setValue(100)

        if result["success"]:
            data = result["data"]
            cost = result.get("cost", result.get("total_cost", 0.0))
            method_used = result["method_used"]
            message = result.get("message", "")
            pages_scraped = result.get("pages_scraped", 1)

            # Display results
            self.results_table.set_data(data)
            self.current_result = data

            # Enable export buttons
            self.export_csv_button.setEnabled(True)
            self.export_json_button.setEnabled(True)
            self.export_excel_button.setEnabled(True)

            # Show success message
            status_msg = f"✓ {message}"
            self.status_label.setText(status_msg)
            self.statusBar().showMessage(status_msg)

            # Build dialog message
            dialog_msg = f"Extracted {len(data)} items\nMethod: {method_used}\nCost: {format_currency(cost)}"
            if pages_scraped > 1:
                dialog_msg += f"\nPages scraped: {pages_scraped}"

            QMessageBox.information(
                self,
                "Success",
                dialog_msg
            )

        else:
            error_msg = result.get("message", "Scraping failed")
            self.status_label.setText(f"✗ {error_msg}")
            self.statusBar().showMessage(f"Failed: {error_msg}")

            QMessageBox.warning(
                self,
                "Scraping Failed",
                error_msg
            )

    def scraping_error(self, error_message: str):
        """Handle scraping error"""
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.progress_bar.setValue(0)
        self.status_label.setText(f"Error: {error_message}")
        self.statusBar().showMessage(f"Error: {error_message}")

        QMessageBox.critical(
            self,
            "Error",
            f"An error occurred:\n{error_message}"
        )

    def export_csv(self):
        """Export results to CSV"""
        if not self.current_result:
            return

        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Export CSV",
            str(EXPORTS_DIR / "scraped_data.csv"),
            "CSV Files (*.csv)"
        )

        if file_path:
            try:
                df = pd.DataFrame(self.current_result)
                df.to_csv(file_path, index=False, encoding='utf-8-sig')
                QMessageBox.information(self, "Success", f"Exported to {file_path}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Export failed: {e}")

    def export_json(self):
        """Export results to JSON"""
        if not self.current_result:
            return

        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Export JSON",
            str(EXPORTS_DIR / "scraped_data.json"),
            "JSON Files (*.json)"
        )

        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(self.current_result, f, indent=2, ensure_ascii=False)
                QMessageBox.information(self, "Success", f"Exported to {file_path}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Export failed: {e}")

    def export_excel(self):
        """Export results to Excel"""
        if not self.current_result:
            return

        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Export Excel",
            str(EXPORTS_DIR / "scraped_data.xlsx"),
            "Excel Files (*.xlsx)"
        )

        if file_path:
            try:
                df = pd.DataFrame(self.current_result)
                df.to_excel(file_path, index=False, engine='openpyxl')
                QMessageBox.information(self, "Success", f"Exported to {file_path}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Export failed: {e}")