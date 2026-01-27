import pandas as pd


def apply_numeric_rules(df: pd.DataFrame, constraints: dict) -> pd.DataFrame:
    """
    Apply business and sanity rules to numeric synthetic data.
    Rules are corrective (clip/adjust), never destructive.
    """

    df = df.copy()

    # ----------------- Column presence checks -----------------
    has_age = "Age" in df.columns
    has_spend = "Monthly_Spend" in df.columns
    has_income = "Monthly_Income" in df.columns

    # ----------------- AGE BOUNDS -----------------
    if has_age:
        min_age = constraints.get("min_age", 15)
        max_age = constraints.get("max_age", 65)

        df["Age"] = df["Age"].clip(lower=min_age, upper=max_age)

    # ----------------- AGE ↔ SPEND RULES -----------------
    if has_age and has_spend:
        student_max = constraints.get("student_spend_max", 3000)
        professional_min = constraints.get("professional_spend_min", 2000)

        # Students / young users
        young_mask = df["Age"] < 22
        df.loc[young_mask, "Monthly_Spend"] = (
            df.loc[young_mask, "Monthly_Spend"]
            .clip(upper=student_max)
        )

        # Working professionals
        professional_mask = df["Age"] >= 30
        df.loc[professional_mask, "Monthly_Spend"] = (
            df.loc[professional_mask, "Monthly_Spend"]
            .clip(lower=professional_min)
        )

    # ----------------- SPEND VS INCOME -----------------
    if has_spend and has_income:
        ratio = constraints.get("max_spend_ratio", 0.2)

        max_allowed_spend = df["Monthly_Income"] * ratio

        df["Monthly_Spend"] = df[
            ["Monthly_Spend", max_allowed_spend]
        ].min(axis=1)

    # ----------------- NON-NEGATIVE SAFETY -----------------
    for col in df.select_dtypes(include="number").columns:
        df[col] = df[col].clip(lower=0)

    return df
