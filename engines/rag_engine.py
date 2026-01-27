import os
import re


def _parse_numeric_constraints(md_text: str) -> dict:
    """
    Very lightweight parser for numeric_constraints.md
    Extracts hard limits used by rule_engine.
    """

    constraints = {}

    # Age limits
    age_min = re.search(r"Minimum age:\s*(\d+)", md_text)
    age_max = re.search(r"Maximum age:\s*(\d+)", md_text)

    if age_min:
        constraints["min_age"] = int(age_min.group(1))
    if age_max:
        constraints["max_age"] = int(age_max.group(1))

    # Spend caps
    student_max = re.search(r"Students.*₹([\d,]+)", md_text)
    professional_min = re.search(r"Mid professionals.*₹([\d,]+)", md_text)

    if student_max:
        constraints["student_spend_max"] = int(
            student_max.group(1).replace(",", "")
        )

    if professional_min:
        constraints["professional_spend_min"] = int(
            professional_min.group(1).replace(",", "")
        )

    # Spend vs income
    if "20%" in md_text:
        constraints["max_spend_ratio"] = 0.20

    return constraints


def fetch_constraints(context=None) -> dict:
    """
    RAG entry point.
    Currently performs static grounding from markdown knowledge.
    """

    base_dir = os.getcwd()
    constraints_path = os.path.join(
        base_dir,
        "data/knowledge/numeric_constraints.md"
    )

    if not os.path.exists(constraints_path):
        # Safe fallback (never crash)
        return {
            "student_spend_max": 3000,
            "professional_spend_min": 2000,
            "max_spend_ratio": 0.2,
        }

    with open(constraints_path, "r", encoding="utf-8") as f:
        md_text = f.read()

    constraints = _parse_numeric_constraints(md_text)

    # Final safety defaults
    constraints.setdefault("student_spend_max", 3000)
    constraints.setdefault("professional_spend_min", 2000)
    constraints.setdefault("max_spend_ratio", 0.2)

    return constraints
