
from safety_engine import (
    load_medicines,
    find_medicine,
    check_duplicate_ingredients,
)


def test_database_loads():
    medicines = load_medicines()
    assert len(medicines) >= 1


def test_known_brand_is_found():
    medicines = load_medicines()
    result = find_medicine("DemoBrandA", medicines)

    assert result is not None
    assert result["brand_name"] == "DemoBrandA"


def test_unknown_brand_is_not_found():
    medicines = load_medicines()
    result = find_medicine("unknown_brand", medicines)

    assert result is None


def test_unverified_demo_data_does_not_create_alert():
    result = check_duplicate_ingredients(
        ["DemoBrandA", "DemoBrandB"]
    )

    assert result["duplicates"] == {}


def test_unknown_medicine_is_reported():
    result = check_duplicate_ingredients(
        ["unknown_brand"]
    )

    assert result["unknown_medicines"] == ["unknown_brand"]
