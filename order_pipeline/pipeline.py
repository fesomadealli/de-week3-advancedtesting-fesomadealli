from typing import Dict, List
from pathlib import Path
import logging
from order_pipeline.reader import ShoplinkReader
from order_pipeline.validator import ShoplinkValidator
from order_pipeline.transformer import ShoplinkTransformer
from order_pipeline.analyzer import ShoplinkAnalyzer
from order_pipeline.exporter import ShoplinkExporter

logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(message)s")
logger = logging.getLogger(__name__)

class ShoplinkETL:
    """ETL pipeline for Shoplink order data."""

    DEFAULT_FIELDNAMES: List[str] = ["item", "total_quantity", "total_revenue", "average_price", "orders"]

    def __init__(self, 
                 input_path: Path, 
                 output_dir: Path, 
                 input_format: str = "json", 
                 export_format: str = "json", 
                 fieldnames=None):
        
        self.FIELDNAMES = fieldnames or self.DEFAULT_FIELDNAMES.copy()
        self.reader = ShoplinkReader(input_path, format=input_format)
        self.validator = ShoplinkValidator()
        self.transformer = ShoplinkTransformer()
        self.analyzer = ShoplinkAnalyzer()
        self.exporter = ShoplinkExporter(fieldnames=self.FIELDNAMES, output_path=output_dir, format=export_format)

    def run(self) -> Dict[str, int]:
        logger.info("Starting ETL pipeline")

        raw = list(self.reader.read())
        logger.info("Read %d raw records", len(raw))

        valid = [self.validator.validate_record(r) for r in raw if self.validator.validate_record(r)]
        logger.info("Validated %d records", len(valid))

        transformed = self.transformer.transform(valid)
        logger.info("Transformed into %d unique records", len(transformed))

        summary = self.analyzer.aggregate_by_item(transformed)
        top_items = self.analyzer.top_sellers(transformed)
        anomalies = self.analyzer.detect_price_anomalies(transformed)

        export_items = {
            "summary": summary,
            "top_items": top_items,
            "anomalies": anomalies,
            "transformed": transformed
        }

        for name, data in export_items.items():
            output_file = self.exporter.output_path / f"{name}.{self.exporter.format}"
            self.exporter.export(data, custom_path=output_file)
            logger.info(f"Exported {name} → {output_file}")

        return {"raw": len(raw), "valid": len(valid), "unique": len(transformed)}


if __name__ == "__main__":
    
    ROOT_DIR = Path(__file__).resolve().parent.parent
    input_json = ROOT_DIR / "example.json"
    input_csv = ROOT_DIR / "example.csv"
    output_dir_csv = ROOT_DIR / "insights" / "csv"
    output_dir_json = ROOT_DIR / "insights" / "json"

    etl_json = ShoplinkETL(input_path=input_json, output_dir=output_dir_json, input_format="json", export_format="json")
    etl_csv = ShoplinkETL(input_path=input_csv, output_dir=output_dir_csv, input_format="csv", export_format="csv")

    result_json = etl_json.run()
    result_csv = etl_csv.run()

    print("JSON ETL Result:", result_json)
    print("CSV ETL Result:", result_csv)
