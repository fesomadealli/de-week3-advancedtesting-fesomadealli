
import pytest
from order_pipeline.analyzer import ShoplinkAnalyzer

@pytest.fixture
def sample_records():
    return [
        {"item": "mouse", "quantity": 2, "price": 10, "total": 20, "timestamp": "2025-10-01T10:00:00Z", "payment_status": "paid"},
        {"item": "mouse", "quantity": 2, "price": 12, "total": 24, "timestamp": "2025-10-01T11:00:00Z", "payment_status": "paid"},
        {"item": "keyboard", "quantity": 1, "price": 15, "total": 15, "timestamp": "2025-10-01T12:00:00Z", "payment_status": "refunded"},
        {"item": "mouse", "quantity": -1, "price": 10, "total": -10, "timestamp": "2025-10-01T13:00:00Z", "payment_status": "paid"},  # negative entry
    ]

def test_aggregate_by_item(sample_records):
    analyzer = ShoplinkAnalyzer()
    result = analyzer.aggregate_by_item(sample_records)
    assert len(result) == 2
    assert result[0]["item"] == "mouse"
    assert result[0]["orders"] == 3  # includes negative entry
    assert result[0]["total_quantity"] == 3.0  # 2 + 2 - 1
    assert result[0]["total_revenue"] == 34.0  # 20 + 24 - 10

def test_detect_price_anomalies(sample_records):
    analyzer = ShoplinkAnalyzer()
    anomalies = analyzer.detect_price_anomalies(sample_records, threshold=0.1)
    assert any(a["item"] == "mouse" for a in anomalies)

def test_sales_by_day(sample_records):
    analyzer = ShoplinkAnalyzer()
    daily = analyzer.sales_by_day(sample_records)
    assert "2025-10-01" in daily
    assert daily["2025-10-01"] == 49.0  # 20 + 24 + 15 - 10

def test_refund_loss(sample_records):
    analyzer = ShoplinkAnalyzer()
    loss = analyzer.refund_loss(sample_records)
    assert loss == 15.0

def test_conversion_rate(sample_records):
    analyzer = ShoplinkAnalyzer()
    rate = analyzer.conversion_rate(sample_records)
    assert rate == 75.0  # 3 paid out of 4

def test_high_value_orders(sample_records):
    analyzer = ShoplinkAnalyzer()
    high_orders = analyzer.high_value_orders(sample_records, threshold=20)
    assert len(high_orders) == 2

