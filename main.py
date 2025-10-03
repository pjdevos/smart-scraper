"""
SmartScraper - AI-Powered Web Scraping Tool
Main Entry Point
"""
import sys
from PyQt6.QtWidgets import QApplication
from frontend.main_window import MainWindow
from utils.logger import get_logger

logger = get_logger(__name__)


def main():
    """Main application entry point"""
    logger.info("Starting SmartScraper application")

    try:
        app = QApplication(sys.argv)
        app.setApplicationName("SmartScraper")
        app.setOrganizationName("SmartScraper")

        window = MainWindow()
        window.show()

        logger.info("Application window shown")

        sys.exit(app.exec())

    except Exception as e:
        logger.error(f"Application error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()