import pytest
from order_pipeline.reader import ShoplinkReader
from pathlib import Path
import json
import csv

#------- how to run ---------
# poetry run pytest tests/test_reader.py -v

@pytest.fixture
def sample_json(tmp_path):
    """Create a temporary JSON file with a single order record."""
    
    data = [
        {"order_id": "ORD001", "timestamp": "2025-10-01T10:00:00Z", "item": "mouse", "payment_status": "paid", "quantity": 2, "price": 10, "total": 20}
    ]
    path = tmp_path / "orders.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f)
    return path


@pytest.fixture
def sample_csv(tmp_path):
    """Create a temporary CSV file with one record."""
    
    path = tmp_path / "orders.csv"
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["order_id", "timestamp", "item", "payment_status", "quantity", "price", "total"]
        )
        writer.writeheader()
        writer.writerow({
            "order_id": "ORD002",
            "timestamp": "2025-10-01T11:00:00Z",
            "item": "keyboard",
            "payment_status": "paid",
            "quantity": 1,
            "price": 15,
            "total": 15
        })
    return path


@pytest.fixture
def empty_csv(tmp_path):
    """Empty CSV with only header."""
    path = tmp_path / "empty.csv"
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["order_id", "timestamp", "item", "payment_status", "quantity", "price", "total"]
        )
        writer.writeheader()
    return path



def test_read_json(sample_json):
    reader = ShoplinkReader(sample_json, format="json")
    records = list(reader.read())
    assert len(records) == 1
    assert records[0]["item"] == "mouse"
    assert "order_id" in records[0]


def test_read_csv(sample_csv):
    reader = ShoplinkReader(sample_csv, format="csv")
    records = list(reader.read())
    assert len(records) == 1
    assert records[0]["item"] == "keyboard"
    assert records[0]["price"] == "15" or records[0]["price"] == 15


def test_empty_csv_returns_nothing(empty_csv):
    """Ensure empty CSVs yield no records."""
    reader = ShoplinkReader(empty_csv, format="csv")
    records = list(reader.read())
    assert records == []


def test_invalid_format_raises_error(tmp_path):
    """Unsupported format should raise ValueError."""
    fake_path = tmp_path / "orders.xml"
    fake_path.write_text("<data></data>")
    reader = ShoplinkReader(fake_path, format="xml")
    with pytest.raises(ValueError):
        list(reader.read())
        

def test_missing_file_raises_error(tmp_path):
    """Non-existent file should raise FileNotFoundError."""
    missing_path = tmp_path / "no_such_file.csv"
    with pytest.raises(FileNotFoundError):
        ShoplinkReader(missing_path, format="csv")
        
        
def test_json_structure_invalid(tmp_path):
    """Invalid JSON should raise JSONDecodeError."""
    bad_json = tmp_path / "bad.json"
    bad_json.write_text("{bad json here}")
    reader = ShoplinkReader(bad_json, format="json")
    with pytest.raises(json.JSONDecodeError):
        list(reader.read())
