
import pytest
from order_pipeline.validator import ShoplinkValidator

@pytest.fixture
def validator():
    return ShoplinkValidator(min_qty=1.0, min_price=0.1, min_total=0.1)

def test_valid_record_passes(validator):
    record = {
        "order_id": "ORD001",
        "timestamp": "2025-10-01T10:00:00Z",
        "item": "Mouse",
        "payment_status": "paid",
        "quantity": "2",
        "price": "10",
        "total": "20"
    }
    result = validator.validate_record(record)
    assert result is not None
    assert result.item == "mouse"
    assert result.total == 20.0

def test_missing_required_field_fails(validator):
    record = {
        "timestamp": "2025-10-01T10:00:00Z",
        "item": "Mouse",
        "payment_status": "paid"
    }
    assert validator.validate_record(record) is None

def test_invalid_order_id_format(validator):
    record = {
        "order_id": "123ORD",
        "timestamp": "2025-10-01T10:00:00Z",
        "item": "Mouse",
        "payment_status": "paid",
        "quantity": 1,
        "price": 10,
        "total": 10
    }
    assert validator.validate_record(record) is None

def test_invalid_timestamp_format(validator):
    record = {
        "order_id": "ORD002",
        "timestamp": "01-10-2025 10:00",  # unsupported format
        "item": "Mouse",
        "payment_status": "paid",
        "quantity": 1,
        "price": 10,
        "total": 10
    }
    assert validator.validate_record(record) is None

def test_negative_values_rejected(validator):
    record = {
        "order_id": "ORD003",
        "timestamp": "2025-10-01T10:00:00Z",
        "item": "Mouse",
        "payment_status": "paid",
        "quantity": -1,
        "price": 10,
        "total": -10
    }
    assert validator.validate_record(record) is None

def test_missing_numeric_field_computed(validator):
    record = {
        "order_id": "ORD004",
        "timestamp": "2025-10-01T10:00:00Z",
        "item": "Mouse",
        "payment_status": "paid",
        "quantity": 2,
        "price": 10
        # total missing
    }
    result = validator.validate_record(record)
    assert result.total == 20.0

def test_invalid_payment_status(validator):
    record = {
        "order_id": "ORD005",
        "timestamp": "2025-10-01T10:00:00Z",
        "item": "Mouse",
        "payment_status": "unknown",
        "quantity": 1,
        "price": 10,
        "total": 10
    }
    assert validator.validate_record(record) is None

def test_clean_numeric_string_with_symbols(validator):
    assert validator.clean_numeric("₦1,200.50") == 1200.50
    assert validator.clean_numeric("USD 99.99") == 99.99
    assert validator.clean_numeric("abc") is None

def test_clean_numeric_none_input(validator):
    assert validator.clean_numeric(None) is None
    
def test_clean_numeric_invalid_input(validator):
    assert validator.clean_numeric("5,0000usd") is not 50000
    
def test_validate_data_non_dict(validator):
    assert validator.validate_data(["not", "a", "dict"]) is None

def test_validate_data_missing_required(validator):
    record = {"order_id": "ORD001"}  # missing others
    assert validator.validate_data(record) is None

def test_validate_data_insufficient_numeric(validator):
    record = {"order_id": "ORD001", "timestamp": "2025-10-01", "item": "X", "payment_status": "paid", "quantity": 2}
    assert validator.validate_data(record) is None

def test_validate_data_valid(validator):
    record = {"order_id": "ORD001", "timestamp": "2025-10-01", "item": "X", "payment_status": "paid", "quantity": 2, "price": 3}
    assert validator.validate_data(record) == record


def test_clean_numeric_int_and_float(validator):
    assert validator.clean_numeric(5) == 5.0
    assert validator.clean_numeric(12.3) == 12.3

def test_clean_numeric_unsupported_type(validator):
    assert validator.clean_numeric(["12.5"]) is None


def test_validate_timestamp_various_formats(validator):
    assert validator.validate_timestamp("2025-10-01T10:00:00Z") == "2025-10-01T10:00:00Z"
    assert validator.validate_timestamp("2025-10-01 10:00") == "2025-10-01T10:00:00Z"
    assert validator.validate_timestamp("01/10/2025 10:00 AM") == "2025-10-01T10:00:00Z"
    assert validator.validate_timestamp("2025/10/01T10:00Z") == "2025-10-01T10:00:00Z"
