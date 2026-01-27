import pandas as pd


def validate_rules(df: pd.DataFrame, constraints: dict | None = None) -> dict:
    """
    Validate business rules on synthetic data.
    Returns a structured report instead of raising assertions.
    """

    if constraints is None:
        constraints = {}

    report = {
        "violations": [],
        "summary": {
            "rows_checked": len(df),
            "violations_count": 0
        }
    }

    has_age = "Age" in df.columns
    has_spend = "Monthly_Spend" in df.columns
    has_income = "Monthly_Income" in df.columns

    student_max = constraints.get("student_spend_max", 3000)
    professional_min = constraints.get("professional_spend_min", 2000)
    max_ratio = constraints.get("max_spend_ratio", 0.2)

    for idx, row in df.iterrows():

        # -------- Age ↔ Spend --------
        if has_age and has_spend:
            if row["Age"] < 22 and row["Monthly_Spend"] > student_max:
                report["violations"].append({
                    "row": idx,
                    "rule": "student_spend_max",
                    "value": row["Monthly_Spend"]
                })

            if row["Age"] >= 30 and row["Monthly_Spend"] < professional_min:
                report["violations"].append({
                    "row": idx,
                    "rule": "professional_spend_min",
                    "value": row["Monthly_Spend"]
                })

        # -------- Spend vs Income --------
        if has_spend and has_income:
            if row["Monthly_Spend"] > row["Monthly_Income"] * max_ratio:
                report["violations"].append({
                    "row": idx,
                    "rule": "spend_income_ratio",
                    "value": row["Monthly_Spend"]
                })

    report["summary"]["violations_count"] = len(report["violations"])
    return report
