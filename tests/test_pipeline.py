from order_pipeline.pipeline import ShoplinkETL
from pathlib import Path
import json

def test_etl_pipeline(tmp_path):
    # --- Prepare input data ---
    input_data = [
        {"order_id": "ORD001", "timestamp": "2025-10-01T10:00:00Z",
         "item": "mouse", "payment_status": "paid", "quantity": 2,
         "price": 10, "total": 20},
        {"order_id": "ORD002", "timestamp": "2025-10-01T11:00:00Z",
         "item": "keyboard", "payment_status": "refunded", "quantity": 1,
         "price": 15, "total": 15}
    ]

    input_path = tmp_path / "orders.json"
    output_dir = tmp_path / "outputs"

    # Write input JSON
    with open(input_path, "w", encoding="utf-8") as f:
        json.dump(input_data, f)

    # --- Run JSON ETL ---
    etl_json = ShoplinkETL(input_path=input_path,
                            output_dir=output_dir,
                            input_format="json",
                            export_format="json")
    result_json = etl_json.run()

    # Check counts
    assert result_json["raw"] == 2
    assert result_json["valid"] == 2
    assert result_json["unique"] == 2

    # Check that files are created
    expected_files = ["summary.json", "top_items.json", "anomalies.json"]
    for fname in expected_files:
        assert (output_dir / fname).exists()

    # --- Run CSV ETL ---
    etl_csv = ShoplinkETL(input_path=input_path,
                           output_dir=output_dir,
                           input_format="json",
                           export_format="csv")
    result_csv = etl_csv.run()

    # Check counts
    assert result_csv["raw"] == 2
    assert result_csv["valid"] == 2
    assert result_csv["unique"] == 2

    # Check that CSV files are created
    expected_csv_files = ["summary.csv", "top_items.csv", "anomalies.csv"]
    for fname in expected_csv_files:
        assert (output_dir / fname).exists()
