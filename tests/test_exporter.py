import pytest
import json
import csv
import os
from pathlib import Path
from order_pipeline.exporter import ShoplinkExporter


@pytest.fixture
def sample_data():
    return [
        {"order_id": "ORD001", "item": "Mouse", "price": 10, "quantity": 2, "total": 20},
        {"order_id": "ORD002", "item": "Keyboard", "price": 15, "quantity": 1, "total": 15},
    ]


@pytest.fixture
def tmp_csv_path(tmp_path: Path):
    return tmp_path / "orders.csv"


@pytest.fixture
def tmp_json_path(tmp_path: Path):
    return tmp_path / "orders.json"


def test_export_csv_creates_file_with_expected_content(sample_data, tmp_csv_path):
    fieldnames = ["order_id", "item", "price", "quantity", "total"]
    exporter = ShoplinkExporter(fieldnames, tmp_csv_path, format="csv")

    exporter.export(sample_data)
    assert tmp_csv_path.exists()

    with open(tmp_csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    assert len(rows) == 2
    assert rows[0]["order_id"] == "ORD001"
    assert rows[1]["item"] == "Keyboard"


def test_export_json_creates_file_with_expected_content(sample_data, tmp_json_path):
    fieldnames = ["order_id", "item", "price", "quantity", "total"]
    exporter = ShoplinkExporter(fieldnames, tmp_json_path, format="json")

    exporter.export(sample_data)
    assert tmp_json_path.exists()

    with open(tmp_json_path, encoding="utf-8") as f:
        data = json.load(f)

    assert len(data) == 2
    assert data[0]["order_id"] == "ORD001"


def test_export_empty_data_triggers_warning_and_writes_header(tmp_path, caplog):
    """Covers 'no data' + os.makedirs creation"""
    empty_csv_path = tmp_path / "nested/folder/orders.csv"
    fieldnames = ["order_id", "item", "price", "quantity", "total"]
    exporter = ShoplinkExporter(fieldnames, empty_csv_path, format="csv")

    # Should create nested dirs and log warning
    with caplog.at_level("WARNING"):
        exporter.export([])
    assert "No data to export" in caplog.text

    # Directory should exist now
    assert empty_csv_path.exists()
    with open(empty_csv_path, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        rows = list(reader)
    assert rows[0] == fieldnames


def test_export_with_custom_path_argument(sample_data, tmp_path):
    """Ensure custom_path overrides default output_path."""
    fieldnames = ["order_id", "item"]
    exporter = ShoplinkExporter(fieldnames, tmp_path / "ignored.csv", format="csv")
    custom_path = tmp_path / "custom_output.csv"

    exporter.export(sample_data, custom_path=custom_path)
    assert custom_path.exists()


def test_export_json_with_custom_path(sample_data, tmp_path):
    """Covers JSON export path explicitly passed."""
    fieldnames = ["order_id", "item"]
    exporter = ShoplinkExporter(fieldnames, tmp_path / "default.json", format="json")
    custom_json = tmp_path / "custom.json"

    exporter.export(sample_data, custom_path=custom_json)
    with open(custom_json, encoding="utf-8") as f:
        data = json.load(f)
    assert isinstance(data, list)
    assert data[0]["order_id"] == "ORD001"


def test_export_unsupported_format_raises_error(sample_data, tmp_csv_path):
    fieldnames = ["order_id", "item", "price", "quantity", "total"]
    exporter = ShoplinkExporter(fieldnames, tmp_csv_path, format="xml")

    with pytest.raises(ValueError, match="Unsupported format"):
        exporter.export(sample_data)


def test_json_serialization_error(tmp_json_path):
    fieldnames = ["order_id"]
    exporter = ShoplinkExporter(fieldnames, tmp_json_path, format="json")

    bad_data = [{"order_id": {"ORD001", "ORD002"}}]  # Set not serializable
    with pytest.raises(TypeError):
        exporter.export(bad_data)
