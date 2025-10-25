
from dataclasses import dataclass, asdict
from typing import Dict, Any, Iterable
import csv
import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(message)s")


@dataclass
class ShoplinkOrder:
    """ Dataclass for Shoplink order record. """
    
    order_id: str
    timestamp: str 
    item: str
    payment_status: str
    quantity: float
    price: float
    total: float

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
    
    
    
class ShoplinkReader:
    """ Read Shoplink order data from CSV or JSON files. """
    
    def __init__(self, path: Path, format: str = "csv"):
        self.path = path
        self.format = format

        if self.path.exists():
            valid_ext = {"csv": ".csv", "json": ".json"}
            expected_ext = valid_ext.get(self.format)
            
            if expected_ext and self.path.suffix.lower() != expected_ext:
                raise ValueError(f"File extension mismatch: expected {expected_ext}, got {self.path.suffix}")
        else:
            raise FileNotFoundError(f"File not found: {self.path}")


    def read(self) -> Iterable[Dict[str, Any]]:
        """ Read records from the specified file format. """
        
        if self.format == "csv":
            with open(self.path, newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                     yield dict(row)

        elif self.format == "json":
            try:
                with open(self.path, "r", encoding="utf-8") as f:
                 data = json.load(f)
            except json.JSONDecodeError as e:
                logger.error("Failed to decode JSON file: %s", e)
                raise 
            
            for row in data:
                yield row
        else:
            raise ValueError("Unsupported format: " + str(self.format))