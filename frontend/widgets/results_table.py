"""
Results Table Widget
"""
from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView
from PyQt6.QtCore import Qt
from typing import List, Dict


class ResultsTable(QTableWidget):
    """Table widget for displaying scraped results"""

    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        """Setup table UI"""
        self.setAlternatingRowColors(True)
        self.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.horizontalHeader().setStretchLastSection(True)
        self.verticalHeader().setVisible(False)

    def set_data(self, data: List[Dict[str, str]]):
        """
        Set table data.

        Args:
            data: List of dictionaries containing scraped data
        """
        if not data:
            self.clear()
            self.setRowCount(0)
            self.setColumnCount(0)
            return

        # Get column names from first item
        columns = list(data[0].keys())

        # Setup table
        self.setRowCount(len(data))
        self.setColumnCount(len(columns))
        self.setHorizontalHeaderLabels(columns)

        # Populate data
        for row_idx, row_data in enumerate(data):
            for col_idx, col_name in enumerate(columns):
                value = row_data.get(col_name, "")
                item = QTableWidgetItem(str(value))
                self.setItem(row_idx, col_idx, item)

        # Resize columns to content
        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)

    def get_data(self) -> List[Dict[str, str]]:
        """
        Get current table data.

        Returns:
            List of dictionaries
        """
        if self.rowCount() == 0:
            return []

        # Get column names
        columns = [self.horizontalHeaderItem(i).text() for i in range(self.columnCount())]

        # Extract data
        data = []
        for row in range(self.rowCount()):
            row_data = {}
            for col, col_name in enumerate(columns):
                item = self.item(row, col)
                row_data[col_name] = item.text() if item else ""
            data.append(row_data)

        return data

    def clear_data(self):
        """Clear all data from table"""
        self.clear()
        self.setRowCount(0)
        self.setColumnCount(0)