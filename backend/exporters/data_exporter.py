"""
Data Exporter
Centralized export logic for CSV, JSON, Excel formats
"""
import pandas as pd
import json
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class DataExporter:
    """Handles data export to various formats"""

    def __init__(self, default_dir: Path = None):
        """
        Initialize data exporter.

        Args:
            default_dir: Default directory for exports
        """
        self.default_dir = default_dir or Path("exports")
        self.default_dir.mkdir(exist_ok=True)

    def _generate_filename(self, base_name: str, extension: str) -> str:
        """
        Generate timestamped filename.

        Args:
            base_name: Base name (e.g., "scraped_data")
            extension: File extension (e.g., ".csv")

        Returns:
            Filename with timestamp
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"{base_name}_{timestamp}{extension}"

    def export_csv(
        self,
        data: List[Dict],
        file_path: Optional[Path] = None,
        encoding: str = 'utf-8-sig'
    ) -> Path:
        """
        Export data to CSV.

        Args:
            data: List of dictionaries to export
            file_path: Target file path (generates if None)
            encoding: File encoding (default: utf-8-sig for Excel compatibility)

        Returns:
            Path to exported file
        """
        if not data:
            raise ValueError("No data to export")

        # Generate path if not provided
        if file_path is None:
            filename = self._generate_filename("scraped_data", ".csv")
            file_path = self.default_dir / filename

        # Convert to DataFrame
        df = pd.DataFrame(data)

        # Export
        df.to_csv(file_path, index=False, encoding=encoding)

        logger.info(f"Exported {len(data)} rows to CSV: {file_path}")
        return file_path

    def export_json(
        self,
        data: List[Dict],
        file_path: Optional[Path] = None,
        indent: int = 2,
        ensure_ascii: bool = False
    ) -> Path:
        """
        Export data to JSON.

        Args:
            data: List of dictionaries to export
            file_path: Target file path (generates if None)
            indent: JSON indentation
            ensure_ascii: Force ASCII encoding

        Returns:
            Path to exported file
        """
        if not data:
            raise ValueError("No data to export")

        # Generate path if not provided
        if file_path is None:
            filename = self._generate_filename("scraped_data", ".json")
            file_path = self.default_dir / filename

        # Export
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=indent, ensure_ascii=ensure_ascii)

        logger.info(f"Exported {len(data)} items to JSON: {file_path}")
        return file_path

    def export_excel(
        self,
        data: List[Dict],
        file_path: Optional[Path] = None,
        sheet_name: str = "Scraped Data"
    ) -> Path:
        """
        Export data to Excel.

        Args:
            data: List of dictionaries to export
            file_path: Target file path (generates if None)
            sheet_name: Excel sheet name

        Returns:
            Path to exported file
        """
        if not data:
            raise ValueError("No data to export")

        # Generate path if not provided
        if file_path is None:
            filename = self._generate_filename("scraped_data", ".xlsx")
            file_path = self.default_dir / filename

        # Convert to DataFrame
        df = pd.DataFrame(data)

        # Export
        df.to_excel(file_path, index=False, sheet_name=sheet_name, engine='openpyxl')

        logger.info(f"Exported {len(data)} rows to Excel: {file_path}")
        return file_path

    def export_all(
        self,
        data: List[Dict],
        base_name: str = "scraped_data"
    ) -> Dict[str, Path]:
        """
        Export data to all formats (CSV, JSON, Excel).

        Args:
            data: List of dictionaries to export
            base_name: Base name for files

        Returns:
            Dictionary mapping format to file path
        """
        if not data:
            raise ValueError("No data to export")

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        results = {}

        # CSV
        csv_path = self.default_dir / f"{base_name}_{timestamp}.csv"
        results['csv'] = self.export_csv(data, csv_path)

        # JSON
        json_path = self.default_dir / f"{base_name}_{timestamp}.json"
        results['json'] = self.export_json(data, json_path)

        # Excel
        excel_path = self.default_dir / f"{base_name}_{timestamp}.xlsx"
        results['excel'] = self.export_excel(data, excel_path)

        logger.info(f"Exported to all formats: {len(data)} items")
        return results

    def export_with_metadata(
        self,
        data: List[Dict],
        metadata: Dict,
        file_path: Optional[Path] = None
    ) -> Path:
        """
        Export data with metadata to JSON.

        Args:
            data: List of dictionaries to export
            metadata: Metadata dictionary (e.g., url, query, timestamp, cost)
            file_path: Target file path (generates if None)

        Returns:
            Path to exported file
        """
        if not data:
            raise ValueError("No data to export")

        # Generate path if not provided
        if file_path is None:
            filename = self._generate_filename("scraped_data_with_metadata", ".json")
            file_path = self.default_dir / filename

        # Combine data and metadata
        export_data = {
            "metadata": metadata,
            "data": data,
            "exported_at": datetime.now().isoformat()
        }

        # Export
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)

        logger.info(f"Exported {len(data)} items with metadata to: {file_path}")
        return file_path

    def get_export_formats(self) -> List[str]:
        """Get list of supported export formats"""
        return ['csv', 'json', 'excel']

    def validate_data(self, data: List[Dict]) -> bool:
        """
        Validate data before export.

        Args:
            data: Data to validate

        Returns:
            True if valid

        Raises:
            ValueError if invalid
        """
        if not data:
            raise ValueError("Data is empty")

        if not isinstance(data, list):
            raise ValueError("Data must be a list")

        if not all(isinstance(item, dict) for item in data):
            raise ValueError("All items must be dictionaries")

        return True
