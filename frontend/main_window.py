"""
Main Application Window - Refactored with new widgets
"""
import sys
from pathlib import Path
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QMessageBox, QFileDialog,
    QGroupBox, QSplitter, QTabWidget, QCheckBox, QSpinBox,
    QScrollArea, QApplication
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QScreen

from config.settings import (
    WINDOW_TITLE, WINDOW_WIDTH, WINDOW_HEIGHT,
    WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT,
    WINDOW_MAX_WIDTH, WINDOW_MAX_HEIGHT,
    DEFAULT_DAILY_BUDGET, ANTHROPIC_API_KEY, EXPORTS_DIR
)
from backend.scraper_engine import ScrapingMethod
from backend.exporters import DataExporter
from frontend.widgets import (
    URLInputWidget, QueryInputWidget, MethodSelectorWidget,
    ProgressWidget, ConsoleWidget, ResultsTable,
    StealthSettingsWidget, CacheStatsWidget, SelectorStatsWidget,
    CrawlerWidget
)
from frontend.widgets.captcha_settings import CaptchaSettingsWidget
from frontend.dialogs import CaptchaSolverDialog
from frontend.workers.scraper_worker import ScraperWorker
from utils.helpers import format_currency


class MainWindow(QMainWindow):
    """Main application window with improved layout"""

    def __init__(self):
        super().__init__()
        self.worker = None
        self.current_result = None
        self.data_exporter = DataExporter(EXPORTS_DIR)
        self.setup_ui()
        self.load_stylesheet()

    def setup_ui(self):
        """Setup user interface with splitter layout"""
        self.setWindowTitle(WINDOW_TITLE)

        # Get available screen size (excludes taskbar)
        screen = QApplication.primaryScreen()
        available_geometry = screen.availableGeometry()  # Excludes taskbar
        screen_width = available_geometry.width()
        screen_height = available_geometry.height()

        # Set a more compact default size (1200x800 or 50% of screen, whichever is smaller)
        window_width = min(1200, int(screen_width * 0.50))
        window_height = min(800, int(screen_height * 0.70))

        # Center window on screen
        x = available_geometry.x() + (screen_width - window_width) // 2
        y = available_geometry.y() + (screen_height - window_height) // 2

        self.setGeometry(x, y, window_width, window_height)

        # Set minimum and maximum sizes
        self.setMinimumSize(900, 600)  # Smaller minimum
        self.setMaximumSize(screen_width, screen_height)  # Max = available screen

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main wrapper layout
        wrapper_layout = QVBoxLayout(central_widget)
        wrapper_layout.setContentsMargins(0, 0, 0, 0)
        wrapper_layout.setSpacing(0)

        # Scroll area for entire content
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)  # Disable horizontal scroll
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setFrameShape(QScrollArea.Shape.NoFrame)

        # Content widget inside scroll area
        content_widget = QWidget()
        from PyQt6.QtWidgets import QSizePolicy
        content_widget.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding
        )
        scroll_area.setWidget(content_widget)

        # Content layout
        main_layout = QVBoxLayout(content_widget)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(15)
        main_layout.setSizeConstraint(QVBoxLayout.SizeConstraint.SetMinimumSize)

        # Header
        header = self.create_header()
        main_layout.addWidget(header)

        # Main content - Splitter (left/right panels)
        splitter = QSplitter(Qt.Orientation.Horizontal)

        # Left panel - Input & Settings
        left_panel = self.create_left_panel()
        splitter.addWidget(left_panel)

        # Right panel - Results & Console
        right_panel = self.create_right_panel()
        splitter.addWidget(right_panel)

        # Splitter proportions: 45% left, 55% right (more compact)
        splitter.setStretchFactor(0, 45)
        splitter.setStretchFactor(1, 55)

        main_layout.addWidget(splitter)

        # Add scroll area to wrapper
        wrapper_layout.addWidget(scroll_area)

        # Status bar
        self.statusBar().showMessage("Ready")

    def create_header(self) -> QWidget:
        """Create application header matching mockup design"""
        header = QWidget()
        header.setStyleSheet("""
            QWidget {
                background-color: #FFF5F0;
                border-bottom: 1px solid #E8D5D0;
            }
        """)
        layout = QHBoxLayout(header)
        layout.setContentsMargins(20, 20, 20, 20)

        # Left side - Logo and Title
        left_layout = QHBoxLayout()

        # Logo
        logo = QLabel("🕷️")
        logo_font = QFont()
        logo_font.setPointSize(24)
        logo.setFont(logo_font)
        left_layout.addWidget(logo)

        # Title section
        title_layout = QVBoxLayout()
        title_layout.setSpacing(2)

        title = QLabel("SmartScraper")
        title_font = QFont()
        title_font.setPointSize(20)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setStyleSheet("color: #2C1338;")
        title_layout.addWidget(title)

        subtitle = QLabel("AI-Powered Web Scraping with Built-in Crawler")
        subtitle.setStyleSheet("color: #735D78; font-size: 12px;")
        title_layout.addWidget(subtitle)

        left_layout.addLayout(title_layout)
        left_layout.addSpacing(10)

        layout.addLayout(left_layout)
        layout.addStretch()

        # Right side - Budget and Settings
        right_layout = QHBoxLayout()
        right_layout.setSpacing(12)

        # Budget display
        self.budget_label = QLabel("💰 €0.00")
        self.budget_label.setStyleSheet("""
            QLabel {
                background-color: #E0A6D8;
                color: #2C1338;
                padding: 10px 20px;
                border-radius: 24px;
                font-weight: 600;
                font-size: 15px;
            }
        """)
        right_layout.addWidget(self.budget_label)

        # Settings button
        settings_button = QPushButton("⚙️")
        settings_button.setFixedSize(44, 44)
        settings_button.setStyleSheet("""
            QPushButton {
                background-color: #E0A6D8;
                border-radius: 22px;
                font-size: 20px;
                padding: 0px;
            }
            QPushButton:hover {
                background-color: #D89BCF;
            }
        """)
        settings_button.setCursor(Qt.CursorShape.PointingHandCursor)
        right_layout.addWidget(settings_button)

        layout.addLayout(right_layout)

        return header

    def create_left_panel(self) -> QWidget:
        """Create left panel with mode tabs and settings"""
        from PyQt6.QtWidgets import QSizePolicy
        panel = QWidget()
        panel.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        panel.setMaximumWidth(600)  # Prevent left panel from being too wide
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(0, 0, 0, 0)

        # Mode Tabs (Single URL / URL List / Crawl Site)
        mode_tabs = QTabWidget()

        # Tab 1: Single URL Mode
        single_url_widget = QWidget()
        single_layout = QVBoxLayout(single_url_widget)
        self.url_input = URLInputWidget()
        self.query_input = QueryInputWidget()
        self.method_selector = MethodSelectorWidget()
        
        # Pagination options for single URL
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
        
        single_layout.addWidget(self.url_input)
        single_layout.addWidget(self.query_input)
        single_layout.addWidget(self.method_selector)
        single_layout.addLayout(pagination_layout)
        single_layout.addStretch()
        mode_tabs.addTab(single_url_widget, "📄 Single URL")

        # Tab 2: URL List Mode (placeholder for now)
        url_list_widget = QWidget()
        url_list_layout = QVBoxLayout(url_list_widget)
        url_list_label = QLabel("URL List Mode - Coming Soon")
        url_list_layout.addWidget(url_list_label)
        url_list_layout.addStretch()
        mode_tabs.addTab(url_list_widget, "📋 URL List")

        # Tab 3: Crawler Mode
        self.crawler_widget = CrawlerWidget()
        self.crawler_widget.start_scraping.connect(self.start_scraping_from_crawler)
        mode_tabs.addTab(self.crawler_widget, "🕷️ Crawl Site")

        layout.addWidget(mode_tabs)

        # Settings Tabs
        settings_tabs = QTabWidget()

        # Stealth tab
        self.stealth_settings = StealthSettingsWidget()
        settings_tabs.addTab(self.stealth_settings, "🕵️ Stealth")

        # CAPTCHA tab
        self.captcha_settings = CaptchaSettingsWidget()
        settings_tabs.addTab(self.captcha_settings, "🧩 CAPTCHA")

        # Stats tab
        stats_widget = QWidget()
        stats_layout = QVBoxLayout(stats_widget)
        self.cache_stats = CacheStatsWidget()
        self.selector_stats = SelectorStatsWidget()
        stats_layout.addWidget(self.cache_stats)
        stats_layout.addWidget(self.selector_stats)
        stats_layout.addStretch()
        settings_tabs.addTab(stats_widget, "📊 Stats")

        layout.addWidget(settings_tabs)

        # Control Buttons
        control_layout = QHBoxLayout()

        self.start_button = QPushButton("🚀 Start Scraping")
        self.start_button.clicked.connect(self.start_scraping)
        self.start_button.setMinimumHeight(40)
        self.start_button.setStyleSheet("""
            QPushButton {
                background-color: #0d7377;
                color: white;
                font-size: 14px;
                font-weight: bold;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #14a0a6;
            }
        """)
        control_layout.addWidget(self.start_button)

        self.stop_button = QPushButton("⏹ Stop")
        self.stop_button.setEnabled(False)
        self.stop_button.clicked.connect(self.stop_scraping)
        self.stop_button.setMinimumHeight(40)
        control_layout.addWidget(self.stop_button)

        layout.addLayout(control_layout)

        # Progress Widget
        self.progress_widget = ProgressWidget()
        layout.addWidget(self.progress_widget)

        layout.addStretch()

        return panel

    def create_right_panel(self) -> QWidget:
        """Create right panel with results and console"""
        from PyQt6.QtWidgets import QSizePolicy
        panel = QWidget()
        panel.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(0, 0, 0, 0)

        # Results Section
        results_group = QGroupBox("📊 Results")
        results_layout = QVBoxLayout()

        self.results_table = ResultsTable()
        results_layout.addWidget(self.results_table)

        # Export buttons
        export_layout = QHBoxLayout()

        self.export_csv_button = QPushButton("💾 Export CSV")
        self.export_csv_button.clicked.connect(self.export_csv)
        self.export_csv_button.setEnabled(False)
        export_layout.addWidget(self.export_csv_button)

        self.export_json_button = QPushButton("💾 Export JSON")
        self.export_json_button.clicked.connect(self.export_json)
        self.export_json_button.setEnabled(False)
        export_layout.addWidget(self.export_json_button)

        self.export_excel_button = QPushButton("💾 Export Excel")
        self.export_excel_button.clicked.connect(self.export_excel)
        self.export_excel_button.setEnabled(False)
        export_layout.addWidget(self.export_excel_button)

        export_layout.addStretch()
        results_layout.addLayout(export_layout)

        results_group.setLayout(results_layout)
        layout.addWidget(results_group, stretch=2)

        # Console Widget
        self.console = ConsoleWidget()
        layout.addWidget(self.console, stretch=1)

        return panel

    def load_stylesheet(self):
        """Load light theme stylesheet (mockup design)"""
        stylesheet_path = Path(__file__).parent / "styles" / "light_theme.qss"
        if stylesheet_path.exists():
            with open(stylesheet_path, 'r') as f:
                self.setStyleSheet(f.read())

    def _on_pagination_toggled(self, checked: bool):
        """Enable/disable pagination controls"""
        self.max_pages_spinbox.setEnabled(checked)

    def update_budget_display(self, cost: float):
        """Update the budget display in header"""
        if hasattr(self, 'budget_label'):
            self.budget_label.setText(f"💰 {format_currency(cost)}")

    def start_scraping(self):
        """Start scraping process"""
        self.console.log_info("Starting scraping process...")

        # Validate inputs
        url = self.url_input.get_url()
        query = self.query_input.get_query()

        if not url:
            QMessageBox.warning(self, "Invalid URL", "Please enter a valid URL")
            self.console.log_error("No URL provided")
            return

        if not query:
            QMessageBox.warning(self, "Invalid Query", "Please enter what you want to extract")
            self.console.log_error("No query provided")
            return

        # Get method
        method = self.method_selector.get_selected_method()
        self.console.log_info(f"Using method: {self.method_selector.get_method_name()}")

        # Get stealth settings
        stealth_settings = self.stealth_settings.get_settings()
        self.console.log_info(f"Stealth level: {stealth_settings['stealth_level']}")

        # Get pagination settings
        enable_pagination = self.pagination_checkbox.isChecked()
        max_pages = self.max_pages_spinbox.value()

        if enable_pagination:
            self.console.log_info(f"Pagination enabled: max {max_pages} pages")

        # Check API key
        if not ANTHROPIC_API_KEY:
            QMessageBox.warning(
                self,
                "API Key Missing",
                "Please set your ANTHROPIC_API_KEY in the .env file"
            )
            self.console.log_error("ANTHROPIC_API_KEY not found in environment")
            return

        # Update UI
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        self.progress_widget.reset()
        self.results_table.clear_data()
        self.export_csv_button.setEnabled(False)
        self.export_json_button.setEnabled(False)
        self.export_excel_button.setEnabled(False)

        # Add to history
        self.url_input.add_to_history(url)
        self.query_input.add_to_history(query)

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
        self.console.log_success("Worker thread started")

    def stop_scraping(self):
        """Stop scraping process"""
        if self.worker and self.worker.isRunning():
            self.worker.terminate()
            self.worker.wait()
            self.progress_widget.set_message("Stopped by user")
            self.start_button.setEnabled(True)
            self.stop_button.setEnabled(False)
            self.console.log_warning("Scraping stopped by user")

    def update_progress(self, message: str, percentage: int):
        """Update progress bar and status"""
        self.progress_widget.set_progress(percentage, message)
        self.statusBar().showMessage(message)
        self.console.log_debug(f"Progress: {percentage}% - {message}")

    def scraping_finished(self, result: dict):
        """Handle scraping completion"""
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)

        if result["success"]:
            data = result["data"]
            cost = result.get("cost", result.get("total_cost", 0.0))
            method_used = result["method_used"]
            message = result.get("message", "")
            pages_scraped = result.get("pages_scraped", 1)

            # Display results
            self.results_table.set_data(data)
            self.current_result = data

            # Update budget display
            self.update_budget_display(cost)

            # Enable export buttons
            self.export_csv_button.setEnabled(True)
            self.export_json_button.setEnabled(True)
            self.export_excel_button.setEnabled(True)

            # Update UI
            self.progress_widget.set_complete()
            self.statusBar().showMessage(f"✓ {message}")

            # Console logging
            self.console.log_success(f"Scraping completed: {len(data)} items extracted")
            self.console.log_info(f"Method used: {method_used}")
            self.console.log_info(f"Cost: {format_currency(cost)}")
            if pages_scraped > 1:
                self.console.log_info(f"Pages scraped: {pages_scraped}")

            # Show success message
            dialog_msg = f"Extracted {len(data)} items\nMethod: {method_used}\nCost: {format_currency(cost)}"
            if pages_scraped > 1:
                dialog_msg += f"\nPages scraped: {pages_scraped}"

            QMessageBox.information(self, "Success", dialog_msg)

        else:
            error_msg = result.get("message", "Scraping failed")
            self.progress_widget.set_error(error_msg)
            self.statusBar().showMessage(f"Failed: {error_msg}")
            self.console.log_error(f"Scraping failed: {error_msg}")

            QMessageBox.warning(self, "Scraping Failed", error_msg)

    def scraping_error(self, error_message: str):
        """Handle scraping error"""
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.progress_widget.set_error(error_message)
        self.statusBar().showMessage(f"Error: {error_message}")
        self.console.log_error(f"Scraping error: {error_message}")

        QMessageBox.critical(self, "Error", f"An error occurred:\n{error_message}")

    def export_csv(self):
        """Export results to CSV"""
        if not self.current_result:
            return

        self.console.log_info("Exporting to CSV...")

        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Export CSV",
            str(EXPORTS_DIR / "scraped_data.csv"),
            "CSV Files (*.csv)"
        )

        if file_path:
            try:
                exported_path = self.data_exporter.export_csv(
                    self.current_result,
                    Path(file_path)
                )
                QMessageBox.information(self, "Success", f"Exported to {exported_path}")
                self.console.log_success(f"Exported to CSV: {exported_path}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Export failed: {e}")
                self.console.log_error(f"CSV export failed: {e}")

    def export_json(self):
        """Export results to JSON"""
        if not self.current_result:
            return

        self.console.log_info("Exporting to JSON...")

        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Export JSON",
            str(EXPORTS_DIR / "scraped_data.json"),
            "JSON Files (*.json)"
        )

        if file_path:
            try:
                exported_path = self.data_exporter.export_json(
                    self.current_result,
                    Path(file_path)
                )
                QMessageBox.information(self, "Success", f"Exported to {exported_path}")
                self.console.log_success(f"Exported to JSON: {exported_path}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Export failed: {e}")
                self.console.log_error(f"JSON export failed: {e}")

    def export_excel(self):
        """Export results to Excel"""
        if not self.current_result:
            return

        self.console.log_info("Exporting to Excel...")

        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Export Excel",
            str(EXPORTS_DIR / "scraped_data.xlsx"),
            "Excel Files (*.xlsx)"
        )

        if file_path:
            try:
                exported_path = self.data_exporter.export_excel(
                    self.current_result,
                    Path(file_path)
                )
                QMessageBox.information(self, "Success", f"Exported to {exported_path}")
                self.console.log_success(f"Exported to Excel: {exported_path}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Export failed: {e}")
                self.console.log_error(f"Excel export failed: {e}")

    def start_scraping_from_crawler(self, urls: list, query: str):
        """Start scraping from discovered URLs in crawler mode"""
        if not urls:
            QMessageBox.warning(self, "No URLs", "No URLs selected to scrape")
            return

        if not query:
            QMessageBox.warning(self, "No Query", "Please enter what you want to extract")
            return

        # Check API key
        if not ANTHROPIC_API_KEY:
            QMessageBox.warning(
                self,
                "API Key Missing",
                "Please set your ANTHROPIC_API_KEY in the .env file"
            )
            self.console.log_error("ANTHROPIC_API_KEY not found in environment")
            return

        # Get method and stealth settings
        method = self.method_selector.get_selected_method()
        stealth_settings = self.stealth_settings.get_settings()

        self.console.log_info(f"Starting scraping for {len(urls)} URLs from crawler")
        self.console.log_info(f"Using method: {self.method_selector.get_method_name()}")

        # Update UI
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        self.progress_widget.reset()
        self.results_table.clear_data()
        self.export_csv_button.setEnabled(False)
        self.export_json_button.setEnabled(False)
        self.export_excel_button.setEnabled(False)

        # For now, scrape the first URL as POC
        # TODO: Implement multi-URL scraping with learned selectors
        url = urls[0]
        
        self.console.log_info(f"Scraping first URL: {url}")
        self.console.log_warning("Multi-URL scraping coming soon - using first URL for now")

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
            enable_pagination=False,
            max_pages=1
        )

        self.worker.progress.connect(self.update_progress)
        self.worker.finished.connect(self.scraping_finished)
        self.worker.error.connect(self.scraping_error)

        self.worker.start()
        self.console.log_success("Worker thread started")

