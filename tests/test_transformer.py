
from order_pipeline.transformer import ShoplinkTransformer
from order_pipeline.reader import ShoplinkOrder

def test_transform_removes_duplicates():
    transformer = ShoplinkTransformer()
    records = [
        ShoplinkOrder("ORD001", "2025-10-01T10:00:00Z", "mouse", "paid", 2, 10, 20),
        ShoplinkOrder("ORD001", "2025-10-01T10:00:00Z", "mouse", "paid", 2, 10, 20),
        ShoplinkOrder("ORD002", "2025-10-01T11:00:00Z", "keyboard", "paid", 1, 15, 15)
    ]
    result = transformer.transform(records)
    assert len(result) == 2
    assert any(r["item"] == "mouse" for r in result)
    assert any(r["item"] == "keyboard" for r in result)

def test_transform_rounds_values():
    transformer = ShoplinkTransformer()
    records = [
        ShoplinkOrder("ORD003", "2025-10-01T12:00:00Z", "webcam", "paid", 1.234, 29.999, 37.001)
    ]
    result = transformer.transform(records)
    assert result[0]["quantity"] == 1.23
    assert result[0]["price"] == 30.0
    assert result[0]["total"] == 37.0

def test_transform_normalizes_item_name():
    transformer = ShoplinkTransformer()
    records = [
        ShoplinkOrder("ORD004", "2025-10-01T13:00:00Z", "  Mouse Pad  ", "paid", 1, 5, 5)
    ]
    result = transformer.transform(records)
    assert result[0]["item"] == "mouse pad"
