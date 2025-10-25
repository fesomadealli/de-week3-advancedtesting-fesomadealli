
from datetime import datetime
from collections import defaultdict, Counter
from typing import List, Dict, Any
from statistics import mean, stdev
import logging

logger = logging.getLogger(__name__)



class ShoplinkAnalyzer:
    def __init__(self):
        pass


    def aggregate_by_item(self, records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        grouped = defaultdict(list)
        for r in records:
            grouped[r["item"]].append(r)

        summary = []
        for item, rows in grouped.items():
            total_qty = sum(r["quantity"] for r in rows)
            total_revenue = sum(r["total"] for r in rows)
            avg_price = mean(r["price"] for r in rows)
            price_std = stdev([r["price"] for r in rows]) if len(rows) > 1 else 0.0

            summary.append({
                "item": item,
                "total_quantity": round(total_qty, 2),
                "total_revenue": round(total_revenue, 2),
                "average_price": round(avg_price, 2),
                "price_std_dev": round(price_std, 2),
                "orders": len(rows)
            })

        logger.info("Aggregated sales by item")
        return sorted(summary, key=lambda x: x["total_revenue"], reverse=True)



    def aggregate_by_status(self, records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        status_group = defaultdict(list)
        for r in records:
            status_group[r["payment_status"]].append(r)

        summary = []
        for status, rows in status_group.items():
            total = sum(r["total"] for r in rows)
            summary.append({
                "payment_status": status,
                "total_orders": len(rows),
                "total_value": round(total, 2)
            })

        logger.info("Aggregated by payment status")
        return summary



    def top_sellers(self, records: List[Dict[str, Any]], by: str = "quantity", top_n: int = 5) -> List[Dict[str, Any]]:
        grouped = defaultdict(lambda: {"quantity": 0.0, "total": 0.0})
        for r in records:
            grouped[r["item"]]["quantity"] += r["quantity"]
            grouped[r["item"]]["total"] += r["total"]

        sorted_items = sorted(grouped.items(), key=lambda x: x[1][by], reverse=True)
        return [
            {
                "item": item,
                "total_quantity": round(data["quantity"], 2),
                "total_revenue": round(data["total"], 2)
            }
            for item, data in sorted_items[:top_n]
        ]



    def detect_price_anomalies(self, records: List[Dict[str, Any]], threshold: float = 0.25) -> List[Dict[str, Any]]:
        grouped = defaultdict(list)
        for r in records:
            grouped[r["item"]].append(r["price"])

        anomalies = []
        for item, prices in grouped.items():
            if len(prices) < 2:
                continue
            _mean = mean(prices)
            _stdev = stdev(prices)
            if _mean > 0 and (_stdev / _mean) > threshold:
                anomalies.append({
                    "item": item,
                    "average_price": round(_mean, 2),
                    "price_std_dev": round(_stdev, 2),
                    "coefficient_of_variation": round(_stdev / _mean, 2),
                    "samples": len(prices)
                })

        logger.info("Detected price anomalies")
        return anomalies



    def sales_by_day(self, records: List[Dict[str, Any]]) -> Dict[str, float]:
        daily_sales = defaultdict(float)
        for r in records:
            try:
                dt = datetime.strptime(r["timestamp"], "%Y-%m-%dT%H:%M:00Z")
                day = dt.strftime("%Y-%m-%d")
                daily_sales[day] += r["total"]
            except Exception:
                continue
        logger.info("Computed sales by day")
        return dict(sorted(daily_sales.items()))



    def sales_by_hour(self, records: List[Dict[str, Any]]) -> Dict[int, float]:
        hourly_sales = defaultdict(float)
        for r in records:
            try:
                dt = datetime.strptime(r["timestamp"], "%Y-%m-%dT%H:%M:00Z")
                hour = dt.hour
                hourly_sales[hour] += r["total"]
            except Exception:
                continue
        logger.info("Computed sales by hour")
        return dict(sorted(hourly_sales.items()))



    def refund_loss(self, records: List[Dict[str, Any]]) -> float:
        loss = sum(r["total"] for r in records if r["payment_status"] == "refunded")
        logger.info("Calculated refund loss")
        return round(loss, 2)



    def conversion_rate(self, records: List[Dict[str, Any]]) -> float:
        paid = sum(1 for r in records if r["payment_status"] == "paid")
        total = len(records)
        rate = (paid / total) * 100 if total > 0 else 0.0
        logger.info("Calculated conversion rate")
        return round(rate, 2)



    def item_frequency(self, records: List[Dict[str, Any]]) -> Dict[str, int]:
        counter = Counter(r["item"] for r in records)
        logger.info("Computed item frequency")
        return dict(counter)



    def average_order_value(self, records: List[Dict[str, Any]]) -> float:
        if not records:
            return 0.0
        avg = mean(r["total"] for r in records)
        logger.info("Calculated average order value")
        return round(avg, 2)



    def high_value_orders(self, records: List[Dict[str, Any]], threshold: float = 100.0) -> List[Dict[str, Any]]:
        high_orders = [r for r in records if r["total"] >= threshold]
        logger.info("Identified high-value orders")
        return high_orders
