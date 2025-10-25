
import os
import csv
import json
import logging
from typing import List, Dict, Any
from pathlib import Path

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(message)s")


class ShoplinkExporter:
    """ Export Shoplink order summary data to CSV or JSON files. """
    
    def __init__(self, fieldnames: List[str], output_path: Path, format: str = "csv"):
        self.output_path = output_path
        self.format = format.lower()
        self.fieldnames = fieldnames

    def export(self, data: List[Dict[str, Any]], custom_path: Path | None = None) -> None:
        """ Export the summary data to the specified format. """
        
        custom_path = custom_path or self.output_path
        os.makedirs(os.path.dirname(custom_path), exist_ok=True) 
        
        if not data:
            logger.warning("No data to export.")
            with open(custom_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(self.fieldnames)
            return

        if self.format == "csv":
            logger.info("Exporting %d rows to CSV: %s", len(data), custom_path)
            with open(custom_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=self.fieldnames)
                writer.writeheader()
                for row in data:
                    clean_row = {key: row.get(key, "") for key in self.fieldnames}
                    writer.writerow(clean_row)

        elif self.format == "json":
            logger.info("Exporting %d rows to JSON: %s", len(data), custom_path)
            with open(custom_path, "w", encoding="utf-8") as f:
                try:
                    json.dump(data, f, indent=2)
                except TypeError as e:
                    logger.error("Failed to serialize data to JSON: %s", e)
                    raise

        else:
            logger.error("Unsupported export format: %s", self.format)
            raise ValueError("Unsupported format: " + self.format)
