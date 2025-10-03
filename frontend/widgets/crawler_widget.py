"""
Crawler Widget - UI for web crawler mode
"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QComboBox, QCheckBox, QTextEdit, QGroupBox,
    QListWidget, QListWidgetItem, QProgressBar, QFileDialog,
    QMessageBox
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
from pathlib import Path

from config.settings import EXPORTS_DIR
from frontend.workers.crawler_worker import CrawlerWorker
from utils.helpers import format_currency


class CrawlerWidget(QWidget):
    """Widget for crawler mode with URL discovery"""

    # Signal emitted when user wants to scrape discovered URLs
    start_scraping = pyqtSignal(list, str)  # urls, query

    def __init__(self):
        super().__init__()
        self.worker = None
        self.discovered_urls = []
        self.setup_ui()

    def setup_ui(self):
        """Setup UI components"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # Info box
        info_box = self.create_info_box()
        layout.addWidget(info_box)

        # Start URL (outside group box, like mockup)
        url_label = QLabel("Start URL")
        url_label.setStyleSheet("font-weight: 500; font-size: 14px; color: #2C1338; margin-bottom: 10px;")
        layout.addWidget(url_label)

        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("https://example.com/products")
        layout.addWidget(self.url_input)

        # What to Extract (like mockup)
        extract_label = QLabel("What to Extract (from each found page)")
        extract_label.setStyleSheet("font-weight: 500; font-size: 14px; color: #2C1338; margin-top: 16px; margin-bottom: 10px;")
        layout.addWidget(extract_label)

        self.extract_query = QTextEdit()
        self.extract_query.setPlaceholderText("Describe what to extract from each discovered page...")
        self.extract_query.setMaximumHeight(80)
        layout.addWidget(self.extract_query)

        # Configuration section - Crawler Settings
        config_group = QGroupBox("🔧 Crawler Settings")
        config_group.setStyleSheet("""
            QGroupBox {
                background-color: #FFFBF8;
                border: 2px solid #E8D5D0;
                border-radius: 10px;
                padding: 20px;
                margin-top: 16px;
                font-weight: 600;
                font-size: 15px;
                color: #2C1338;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 10px;
                background-color: #FFFBF8;
            }
        """)
        config_layout = QVBoxLayout()

        # URL Pattern Filter
        pattern_label = QLabel("URL Pattern Filter (regex)")
        pattern_label.setStyleSheet("font-size: 13px; color: #735D78; font-weight: 500;")
        self.pattern_input = QLineEdit()
        self.pattern_input.setPlaceholderText("/product/.*")
        config_layout.addWidget(pattern_label)
        config_layout.addWidget(self.pattern_input)

        help_text = QLabel("Only URLs matching this pattern will be scraped")
        help_text.setStyleSheet("font-size: 12px; color: #735D78; margin-top: 6px; margin-bottom: 16px;")
        config_layout.addWidget(help_text)

        # Max Pages and Max Depth (grid layout like mockup)
        limits_layout = QHBoxLayout()
        limits_layout.setSpacing(16)

        # Max Pages
        max_pages_container = QVBoxLayout()
        max_pages_label = QLabel("Max Pages")
        max_pages_label.setStyleSheet("font-size: 13px; color: #735D78; font-weight: 500;")
        self.max_pages_combo = QComboBox()
        self.max_pages_combo.addItems(["50", "100", "500", "1000", "Unlimited"])
        self.max_pages_combo.setCurrentText("500")
        max_pages_container.addWidget(max_pages_label)
        max_pages_container.addWidget(self.max_pages_combo)

        # Max Depth
        max_depth_container = QVBoxLayout()
        max_depth_label = QLabel("Max Depth")
        max_depth_label.setStyleSheet("font-size: 13px; color: #735D78; font-weight: 500;")
        self.max_depth_combo = QComboBox()
        self.max_depth_combo.addItems(["1", "2", "3", "5", "Unlimited"])
        self.max_depth_combo.setCurrentText("3")
        max_depth_container.addWidget(max_depth_label)
        max_depth_container.addWidget(self.max_depth_combo)

        limits_layout.addLayout(max_pages_container)
        limits_layout.addLayout(max_depth_container)
        config_layout.addLayout(limits_layout)

        # Checkboxes (with spacing)
        checkbox_layout = QVBoxLayout()
        checkbox_layout.setSpacing(10)
        checkbox_layout.setContentsMargins(0, 12, 0, 0)

        self.internal_only_cb = QCheckBox("Follow internal links only")
        self.internal_only_cb.setChecked(True)
        self.respect_robots_cb = QCheckBox("Respect robots.txt")
        self.respect_robots_cb.setChecked(True)
        self.try_sitemap_cb = QCheckBox("Parse sitemap.xml first (faster!)")
        self.try_sitemap_cb.setChecked(True)
        self.follow_pagination_cb = QCheckBox("Follow pagination links")
        self.follow_pagination_cb.setChecked(False)

        checkbox_layout.addWidget(self.internal_only_cb)
        checkbox_layout.addWidget(self.respect_robots_cb)
        checkbox_layout.addWidget(self.try_sitemap_cb)
        checkbox_layout.addWidget(self.follow_pagination_cb)
        config_layout.addLayout(checkbox_layout)

        config_group.setLayout(config_layout)
        layout.addWidget(config_group)

        # Control buttons (mockup style)
        control_layout = QHBoxLayout()
        control_layout.setSpacing(12)
        control_layout.setContentsMargins(0, 24, 0, 0)

        self.start_crawl_btn = QPushButton("🔍 Start Crawling")
        self.start_crawl_btn.clicked.connect(self.start_crawling)
        self.start_crawl_btn.setMinimumHeight(40)
        # Primary button style already in QSS

        self.load_urls_btn = QPushButton("💾 Load URLs")
        self.load_urls_btn.setMinimumHeight(40)
        self.load_urls_btn.setProperty("class", "secondary")

        control_layout.addWidget(self.start_crawl_btn)
        control_layout.addWidget(self.load_urls_btn)
        layout.addLayout(control_layout)

        # Progress section (mockup style)
        progress_group = QGroupBox("")
        progress_group.setStyleSheet("""
            QGroupBox {
                background-color: white;
                border: 2px solid #E8D5D0;
                border-radius: 10px;
                padding: 24px;
                margin-top: 24px;
            }
        """)
        progress_layout = QVBoxLayout()

        # Status label
        self.crawler_status_label = QLabel("🔄 Crawling in progress...")
        self.crawler_status_label.setStyleSheet("""
            font-size: 16px;
            font-weight: 600;
            color: #2C1338;
            margin-bottom: 16px;
        """)
        self.crawler_status_label.setVisible(False)
        progress_layout.addWidget(self.crawler_status_label)

        # Stats row (3 columns like mockup)
        stats_row = QHBoxLayout()
        stats_row.setSpacing(16)

        # Found stat
        found_container = QWidget()
        found_container.setStyleSheet("background-color: #FFFBF8; border-radius: 8px; padding: 12px;")
        found_layout = QVBoxLayout(found_container)
        found_layout.setContentsMargins(12, 12, 12, 12)
        found_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.urls_found_value = QLabel("0")
        self.urls_found_value.setStyleSheet("font-size: 24px; font-weight: 700; color: #E0A6D8;")
        self.urls_found_value.setAlignment(Qt.AlignmentFlag.AlignCenter)
        found_label = QLabel("FOUND")
        found_label.setStyleSheet("font-size: 12px; color: #735D78; margin-top: 4px;")
        found_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        found_layout.addWidget(self.urls_found_value)
        found_layout.addWidget(found_label)

        # Crawled stat
        crawled_container = QWidget()
        crawled_container.setStyleSheet("background-color: #FFFBF8; border-radius: 8px; padding: 12px;")
        crawled_layout = QVBoxLayout(crawled_container)
        crawled_layout.setContentsMargins(12, 12, 12, 12)
        crawled_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.urls_crawled_value = QLabel("0")
        self.urls_crawled_value.setStyleSheet("font-size: 24px; font-weight: 700; color: #E0A6D8;")
        self.urls_crawled_value.setAlignment(Qt.AlignmentFlag.AlignCenter)
        crawled_label = QLabel("CRAWLED")
        crawled_label.setStyleSheet("font-size: 12px; color: #735D78; margin-top: 4px;")
        crawled_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        crawled_layout.addWidget(self.urls_crawled_value)
        crawled_layout.addWidget(crawled_label)

        # Matched stat
        matched_container = QWidget()
        matched_container.setStyleSheet("background-color: #FFFBF8; border-radius: 8px; padding: 12px;")
        matched_layout = QVBoxLayout(matched_container)
        matched_layout.setContentsMargins(12, 12, 12, 12)
        matched_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.urls_matched_value = QLabel("0")
        self.urls_matched_value.setStyleSheet("font-size: 24px; font-weight: 700; color: #E0A6D8;")
        self.urls_matched_value.setAlignment(Qt.AlignmentFlag.AlignCenter)
        matched_label = QLabel("MATCHED")
        matched_label.setStyleSheet("font-size: 12px; color: #735D78; margin-top: 4px;")
        matched_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        matched_layout.addWidget(self.urls_matched_value)
        matched_layout.addWidget(matched_label)

        stats_row.addWidget(found_container)
        stats_row.addWidget(crawled_container)
        stats_row.addWidget(matched_container)
        progress_layout.addLayout(stats_row)

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setMaximumHeight(8)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                background-color: #E8D5D0;
                border: none;
                border-radius: 4px;
                margin-top: 20px;
                margin-bottom: 12px;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                            stop:0 #E0A6D8, stop:1 #D89BCF);
                border-radius: 4px;
            }
        """)
        progress_layout.addWidget(self.progress_bar)

        # Progress text
        self.progress_text = QLabel("")
        self.progress_text.setStyleSheet("font-size: 14px; color: #735D78; text-align: center;")
        self.progress_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        progress_layout.addWidget(self.progress_text)

        # Control buttons
        control_btns_layout = QHBoxLayout()
        control_btns_layout.setSpacing(8)
        control_btns_layout.setContentsMargins(0, 16, 0, 0)

        self.pause_btn = QPushButton("⏸️ Pause")
        self.pause_btn.clicked.connect(self.pause_crawling)
        self.pause_btn.setEnabled(False)
        self.pause_btn.setProperty("class", "control")

        self.stop_btn = QPushButton("⏹️ Stop")
        self.stop_btn.clicked.connect(self.stop_crawling)
        self.stop_btn.setEnabled(False)
        self.stop_btn.setProperty("class", "control")

        view_log_btn = QPushButton("📊 View Log")
        view_log_btn.setProperty("class", "control")

        control_btns_layout.addWidget(self.pause_btn)
        control_btns_layout.addWidget(self.stop_btn)
        control_btns_layout.addWidget(view_log_btn)
        progress_layout.addLayout(control_btns_layout)

        progress_group.setLayout(progress_layout)
        layout.addWidget(progress_group)

        # URL Preview Panel
        preview_group = QGroupBox("🔗 Discovered URLs")
        preview_layout = QVBoxLayout()

        # Search/filter box
        search_layout = QHBoxLayout()
        search_label = QLabel("Filter:")
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search URLs...")
        self.search_input.textChanged.connect(self.filter_urls)
        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_input)
        preview_layout.addLayout(search_layout)

        # URL list
        self.url_list = QListWidget()
        self.url_list.setSelectionMode(QListWidget.SelectionMode.MultiSelection)
        preview_layout.addWidget(self.url_list)

        # Action buttons
        action_layout = QHBoxLayout()
        self.save_urls_btn = QPushButton("💾 Save URL List")
        self.save_urls_btn.clicked.connect(self.save_url_list)
        self.save_urls_btn.setEnabled(False)
        self.save_urls_btn.setProperty("class", "secondary")

        self.select_all_btn = QPushButton("☑️ Select All")
        self.select_all_btn.clicked.connect(self.select_all_urls)
        self.select_all_btn.setEnabled(False)
        self.select_all_btn.setProperty("class", "secondary")

        self.deselect_all_btn = QPushButton("☐ Deselect All")
        self.deselect_all_btn.clicked.connect(self.deselect_all_urls)
        self.deselect_all_btn.setEnabled(False)
        self.deselect_all_btn.setProperty("class", "secondary")

        self.scrape_all_btn = QPushButton("🚀 Start Scraping All")
        self.scrape_all_btn.clicked.connect(self.start_scraping_selected)
        self.scrape_all_btn.setEnabled(False)
        # Uses primary button style from QSS

        action_layout.addWidget(self.save_urls_btn)
        action_layout.addWidget(self.select_all_btn)
        action_layout.addWidget(self.deselect_all_btn)
        action_layout.addWidget(self.scrape_all_btn)
        preview_layout.addLayout(action_layout)

        preview_group.setLayout(preview_layout)
        layout.addWidget(preview_group)

    def create_info_box(self) -> QWidget:
        """Create info box widget (mockup style)"""
        info_box = QWidget()
        info_box.setStyleSheet("""
            QWidget {
                background-color: #FFF9E6;
                border: 2px solid #F4D4A6;
                border-radius: 10px;
                padding: 16px;
            }
        """)
        layout = QHBoxLayout(info_box)
        layout.setSpacing(12)

        icon_label = QLabel("💡")
        icon_label.setStyleSheet("font-size: 20px;")
        icon_label.setAlignment(Qt.AlignmentFlag.AlignTop)

        text_container = QVBoxLayout()
        title_label = QLabel("Crawler Mode")
        title_label.setStyleSheet("font-size: 14px; font-weight: 600; color: #2C1338; margin-bottom: 6px;")

        desc_label = QLabel(
            "Automatically discover URLs by following links. "
            "Perfect for scraping entire product catalogs, blog archives, or listing sites."
        )
        desc_label.setStyleSheet("font-size: 13px; color: #735D78; line-height: 1.5;")
        desc_label.setWordWrap(True)

        text_container.addWidget(title_label)
        text_container.addWidget(desc_label)

        layout.addWidget(icon_label)
        layout.addLayout(text_container, 1)

        return info_box

    def start_crawling(self):
        """Start crawling process"""
        # Validate inputs
        url = self.url_input.text().strip()
        if not url:
            QMessageBox.warning(self, "Invalid URL", "Please enter a start URL")
            return

        # Get settings
        pattern = self.pattern_input.text().strip() or None
        max_pages_text = self.max_pages_combo.currentText()
        max_pages = 999999 if max_pages_text == "Unlimited" else int(max_pages_text)
        max_depth_text = self.max_depth_combo.currentText()
        max_depth = -1 if max_depth_text == "Unlimited" else int(max_depth_text)

        # Update UI
        self.start_crawl_btn.setEnabled(False)
        self.pause_btn.setEnabled(True)
        self.stop_btn.setEnabled(True)
        self.url_list.clear()
        self.discovered_urls.clear()
        self.progress_bar.setValue(0)

        # Create and start worker
        self.worker = CrawlerWorker(
            start_url=url,
            max_pages=max_pages,
            max_depth=max_depth,
            pattern=pattern,
            internal_only=self.internal_only_cb.isChecked(),
            respect_robots=self.respect_robots_cb.isChecked(),
            try_sitemap=self.try_sitemap_cb.isChecked(),
            follow_pagination=self.follow_pagination_cb.isChecked()
        )

        self.worker.progress_update.connect(self.update_progress)
        self.worker.url_found.connect(self.add_url)
        self.worker.finished.connect(self.crawling_finished)
        self.worker.error.connect(self.crawling_error)

        self.worker.start()

    def pause_crawling(self):
        """Pause/resume crawling"""
        if self.worker:
            if self.pause_btn.text() == "⏸️ Pause":
                self.worker.pause()
                self.pause_btn.setText("▶️ Resume")
            else:
                self.worker.resume()
                self.pause_btn.setText("⏸️ Pause")

    def stop_crawling(self):
        """Stop crawling"""
        if self.worker:
            self.worker.stop()
            self.start_crawl_btn.setEnabled(True)
            self.pause_btn.setEnabled(False)
            self.stop_btn.setEnabled(False)
            self.pause_btn.setText("⏸️ Pause")

    def update_progress(self, stats: dict):
        """Update progress display"""
        self.urls_found_value.setText(str(stats.get('found', 0)))
        self.urls_crawled_value.setText(str(stats.get('crawled', 0)))
        self.urls_matched_value.setText(str(stats.get('matched', 0)))

        # Update progress bar
        crawled = stats.get('crawled', 0)
        max_pages_text = self.max_pages_combo.currentText()
        if max_pages_text != "Unlimited":
            max_pages = int(max_pages_text)
            percentage = min(int((crawled / max_pages) * 100), 100)
            self.progress_bar.setValue(percentage)

    def add_url(self, url: str):
        """Add URL to list"""
        if url not in self.discovered_urls:
            self.discovered_urls.append(url)
            item = QListWidgetItem(url)
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            item.setCheckState(Qt.CheckState.Checked)
            self.url_list.addItem(item)

    def crawling_finished(self, urls: list):
        """Handle crawling completion"""
        self.start_crawl_btn.setEnabled(True)
        self.pause_btn.setEnabled(False)
        self.stop_btn.setEnabled(False)
        self.pause_btn.setText("⏸️ Pause")
        self.progress_bar.setValue(100)

        # Enable action buttons
        if urls:
            self.save_urls_btn.setEnabled(True)
            self.select_all_btn.setEnabled(True)
            self.deselect_all_btn.setEnabled(True)
            self.scrape_all_btn.setEnabled(True)

            # Show completion message
            QMessageBox.information(
                self,
                "Crawling Complete",
                f"Found {len(urls)} matching URLs.\n\n"
                f"Review the URLs and click 'Start Scraping Selected' to proceed."
            )

    def crawling_error(self, error_msg: str):
        """Handle crawling error"""
        self.start_crawl_btn.setEnabled(True)
        self.pause_btn.setEnabled(False)
        self.stop_btn.setEnabled(False)
        QMessageBox.critical(self, "Crawling Error", f"An error occurred:\n{error_msg}")

    def filter_urls(self, text: str):
        """Filter URL list based on search text"""
        for i in range(self.url_list.count()):
            item = self.url_list.item(i)
            item.setHidden(text.lower() not in item.text().lower())

    def select_all_urls(self):
        """Select all URLs"""
        for i in range(self.url_list.count()):
            item = self.url_list.item(i)
            if not item.isHidden():
                item.setCheckState(Qt.CheckState.Checked)

    def deselect_all_urls(self):
        """Deselect all URLs"""
        for i in range(self.url_list.count()):
            item = self.url_list.item(i)
            item.setCheckState(Qt.CheckState.Unchecked)

    def save_url_list(self):
        """Save URL list to file"""
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save URL List",
            str(EXPORTS_DIR / "discovered_urls.txt"),
            "Text Files (*.txt)"
        )

        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    for url in self.discovered_urls:
                        f.write(url + '\n')
                QMessageBox.information(self, "Success", f"Saved {len(self.discovered_urls)} URLs to {file_path}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save file: {e}")

    def start_scraping_selected(self):
        """Start scraping selected URLs"""
        # Get selected URLs
        selected_urls = []
        for i in range(self.url_list.count()):
            item = self.url_list.item(i)
            if item.checkState() == Qt.CheckState.Checked:
                selected_urls.append(item.text())

        if not selected_urls:
            QMessageBox.warning(self, "No URLs Selected", "Please select at least one URL to scrape")
            return

        # Get query
        query = self.extract_query.toPlainText().strip()
        if not query:
            QMessageBox.warning(self, "No Query", "Please enter what you want to extract")
            return

        # Emit signal to main window
        self.start_scraping.emit(selected_urls, query)

    def get_selected_urls(self) -> list:
        """Get list of selected URLs"""
        selected = []
        for i in range(self.url_list.count()):
            item = self.url_list.item(i)
            if item.checkState() == Qt.CheckState.Checked:
                selected.append(item.text())
        return selected

    def get_query(self) -> str:
        """Get extraction query"""
        return self.extract_query.toPlainText().strip()
