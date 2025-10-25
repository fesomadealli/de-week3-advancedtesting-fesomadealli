
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(message)s")

class ShoplinkTransformer:
    """ Transform and clean Shoplink order data."""
    
    def __init__(self, unique_fields=("order_id", "timestamp")):
        self.unique_fields = unique_fields

    def transform(self, entries: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        
        duplicate_count = 0
        cache = {}
        for entry in entries:
            # composite_key = tuple(entry.to_dict().get(col) for col in self.unique_fields)   
            composite_key = tuple(getattr(entry, col) for col in self.unique_fields)  # alternative if entry is a dataclass
            if composite_key in cache:
                logger.info(f"Duplicate found for key {composite_key}, overwriting previous entry")
                duplicate_count += 1
            cache[composite_key] = entry  # overwrite duplicates

        cleaned = []
        for data in cache.values():
            order_id = str(data.order_id)
            timestamp = str(data.timestamp)
            product = str(data.item)
            name = product.lower().strip() if isinstance(product, str) else None
            qty = round(float(data.quantity), 2)
            unit_cost = round(float(data.price), 2)
            bill = round(float(data.total), 2)
            payment_status = str(data.payment_status)

            cleaned.append({
                "order_id": order_id,
                "timestamp": timestamp,
                "item": name,
                "quantity": qty,
                "price": unit_cost,
                "total": bill,
                "payment_status": payment_status
            })

        return cleaned
