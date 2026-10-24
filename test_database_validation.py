
from database_validation import validate_database


def test_database_validation_returns_expected_structure():
    result = validate_database()

    assert "valid" in result
    assert "errors" in result
    assert "warnings" in result
    assert "medicine_count" in result
    assert "rule_count" in result

    assert isinstance(result["valid"], bool)
    assert isinstance(result["errors"], list)
    assert isinstance(result["warnings"], list)


def test_current_medicine_database_has_three_demo_records():
    result = validate_database()

    assert result["medicine_count"] == 3


def test_empty_interaction_rules_are_reported_as_warning():
    result = validate_database()

    if result["rule_count"] == 0:
        assert any(
            "interaction rules file is empty" in warning.lower()
            for warning in result["warnings"]
        )


def test_current_database_structure_is_valid():
    result = validate_database()

    assert result["valid"] is True
    assert result["errors"] == []


def test_unverified_data_is_not_claimed_as_clinically_verified():
    result = validate_database()

    assert any(
        "not necessarily clinically verified" in warning.lower()
        for warning in result["warnings"]
    )
