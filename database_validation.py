
from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).resolve().parent

MEDICINE_COLUMNS = {
    "brand_name",
    "aliases",
    "active_ingredients",
    "review_status",
    "source",
}

INTERACTION_COLUMNS = {
    "ingredient_a",
    "ingredient_b",
    "severity",
    "explanation",
    "source",
    "review_status",
}

ALLOWED_STATUSES = {"verified", "unverified"}


def validate_database():
    """Validate CSV structure and basic data quality."""
    errors = []
    warnings = []

    medicine_path = BASE_DIR / "medicines.csv"
    rules_path = BASE_DIR / "interaction_rules.csv"

    # Validate medicine database
    try:
        medicines = pd.read_csv(medicine_path, keep_default_na=False)
    except Exception as error:
        return {
            "valid": False,
            "errors": [f"Could not read medicines.csv: {error}"],
            "warnings": [],
            "medicine_count": 0,
            "rule_count": 0,
        }

    missing_columns = MEDICINE_COLUMNS - set(medicines.columns)

    if missing_columns:
        errors.append(
            "medicines.csv is missing columns: "
            + ", ".join(sorted(missing_columns))
        )

    else:
        for column in [
            "brand_name",
            "active_ingredients",
            "review_status",
            "source",
        ]:
            empty_rows = medicines[
                medicines[column].astype(str).str.strip() == ""
            ]

            if not empty_rows.empty:
                errors.append(
                    f"medicines.csv has empty values in '{column}'."
                )

        statuses = {
            str(value).strip().casefold()
            for value in medicines["review_status"]
        }

        invalid_statuses = statuses - ALLOWED_STATUSES

        if invalid_statuses:
            errors.append(
                "Invalid medicine review_status values: "
                + ", ".join(sorted(invalid_statuses))
            )

        brand_names = [
            str(value).strip().casefold()
            for value in medicines["brand_name"]
            if str(value).strip()
        ]

        if len(brand_names) != len(set(brand_names)):
            errors.append(
                "medicines.csv contains duplicate brand names."
            )

        if not medicines.empty:
            warnings.append(
                "A structurally valid record is not necessarily "
                "clinically verified."
            )

        if not any(
            str(value).strip().casefold() == "verified"
            for value in medicines["review_status"]
        ):
            warnings.append(
                "No medicine records are marked verified."
            )

    # Validate interaction rules database
    rule_count = 0

    try:
        rules = pd.read_csv(rules_path, keep_default_na=False)
    except Exception as error:
        errors.append(f"Could not read interaction_rules.csv: {error}")
        rules = pd.DataFrame()

    missing_rule_columns = (
        INTERACTION_COLUMNS - set(rules.columns)
    )

    if missing_rule_columns:
        errors.append(
            "interaction_rules.csv is missing columns: "
            + ", ".join(sorted(missing_rule_columns))
        )

    else:
        rule_count = len(rules)

        if not rules.empty:
            required_rule_fields = [
                "ingredient_a",
                "ingredient_b",
                "severity",
                "explanation",
                "source",
                "review_status",
            ]

            for column in required_rule_fields:
                empty_rows = rules[
                    rules[column].astype(str).str.strip() == ""
                ]

                if not empty_rows.empty:
                    errors.append(
                        f"interaction_rules.csv has empty values "
                        f"in '{column}'."
                    )

            statuses = {
                str(value).strip().casefold()
                for value in rules["review_status"]
            }

            invalid_statuses = statuses - ALLOWED_STATUSES

            if invalid_statuses:
                errors.append(
                    "Invalid interaction review_status values: "
                    + ", ".join(sorted(invalid_statuses))
                )

            if not any(
                str(value).strip().casefold() == "verified"
                for value in rules["review_status"]
            ):
                warnings.append(
                    "No interaction rules are marked verified. "
                    "No verified interaction rules can currently "
                    "produce an alert."
                )

        else:
            warnings.append(
                "The interaction rules file is empty. "
                "No interaction alerts can currently be generated."
            )

    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings,
        "medicine_count": len(medicines),
        "rule_count": rule_count,
    }
