
from pathlib import Path

from itertools import combinations

import pandas as pd

BASE_DIR = Path(__file__).resolve().parent


def normalize_name(name: str) -> str:
    """Normalize text for basic name matching."""
    return " ".join(str(name).strip().casefold().split())


def load_medicines() -> pd.DataFrame:
    """Load the local medicine database."""
    path = BASE_DIR / "medicines.csv"
    return pd.read_csv(path).fillna("")


def load_interaction_rules() -> pd.DataFrame:
    """Load the local interaction rules database."""
    path = BASE_DIR / "interaction_rules.csv"
    return pd.read_csv(path).fillna("")


def find_medicine(name: str, medicines: pd.DataFrame):
    """Find a medicine by its brand name or pipe-separated aliases."""
    target = normalize_name(name)

    for _, row in medicines.iterrows():
        candidates = [row["brand_name"]]
        candidates.extend(str(row["aliases"]).split("|"))

        if any(normalize_name(item) == target for item in candidates):
            return row

    return None


def check_duplicate_ingredients(medicine_names: list[str]) -> dict:
    """Check for duplicate ingredients using verified medicine records."""
    medicines = load_medicines()
    matched = []
    unknown = []

    for name in medicine_names:
        row = find_medicine(name, medicines)

        if row is None:
            unknown.append(name)
        else:
            matched.append(row)

    ingredient_to_brands = {}

    for row in matched:
        if normalize_name(row["review_status"]) != "verified":
            continue

        ingredients = [
            item.strip()
            for item in str(row["active_ingredients"]).split("|")
            if item.strip()
        ]

        for ingredient in ingredients:
            ingredient_to_brands.setdefault(
                normalize_name(ingredient), []
            ).append(row["brand_name"])

    duplicates = {
        ingredient: brands
        for ingredient, brands in ingredient_to_brands.items()
        if len(brands) > 1
    }

    return {
        "duplicates": duplicates,
        "unknown_medicines": unknown,
        "matched_medicines": [
            row["brand_name"] for row in matched
        ],
        "note": (
            "Educational prototype only. This result is not a clinical "
            "clearance or a substitute for professional review."
        ),
    }


def check_drug_interactions(medicine_names: list[str]) -> dict:
    """
    Check ingredient pairs against explicitly verified local rules.

    Only verified medicine records and verified interaction rules
    are considered. No match does not mean the prescription is safe.
    """
    medicines = load_medicines()
    rules = load_interaction_rules()

    matched = []
    unknown = []
    unverified = []

    for name in medicine_names:
        row = find_medicine(name, medicines)

        if row is None:
            unknown.append(name)
        elif normalize_name(row["review_status"]) != "verified":
            unverified.append(name)
        else:
            matched.append({
                "entered_name": name,
                "brand_name": row["brand_name"],
                "ingredients": [
                    normalize_name(item)
                    for item in str(row["active_ingredients"]).split("|")
                    if item.strip()
                ],
            })

    verified_rules = rules[
        rules["review_status"].apply(normalize_name) == "verified"
    ]

    # Build lookup keys that work regardless of ingredient order.
    rule_lookup = {}

    for _, rule in verified_rules.iterrows():
        ingredient_a = normalize_name(rule["ingredient_a"])
        ingredient_b = normalize_name(rule["ingredient_b"])

        if not ingredient_a or not ingredient_b:
            continue

        pair_key = tuple(sorted((ingredient_a, ingredient_b)))
        rule_lookup.setdefault(pair_key, []).append({
            "severity": rule["severity"],
            "explanation": rule["explanation"],
            "source": rule["source"],
        })

    interactions = []

    # Compare ingredients belonging to different submitted medicines.
    for medicine_a, medicine_b in combinations(matched, 2):
        for ingredient_a in medicine_a["ingredients"]:
            for ingredient_b in medicine_b["ingredients"]:
                pair_key = tuple(sorted((ingredient_a, ingredient_b)))

                for rule in rule_lookup.get(pair_key, []):
                    interactions.append({
                        "medicine_1": medicine_a["brand_name"],
                        "medicine_2": medicine_b["brand_name"],
                        "ingredient_1": ingredient_a,
                        "ingredient_2": ingredient_b,
                        "severity": rule["severity"],
                        "explanation": rule["explanation"],
                        "source": rule["source"],
                    })

    return {
        "interactions": interactions,
        "unknown_medicines": unknown,
        "unverified_medicines": unverified,
        "verified_medicines": [
            item["brand_name"] for item in matched
        ],
        "note": (
            "Only configured, verified rules were checked. An empty "
            "result does not establish that a prescription is safe "
            "or that no drug interactions exist."
        ),
    }
