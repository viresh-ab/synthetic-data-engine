import pandas as pd


def apply_numeric_rules(df: pd.DataFrame, constraints: dict) -> pd.DataFrame:
    """
    Apply business, sanity, and schema rules to numeric synthetic data.
    This function is corrective (never drops rows).
    """

    df = df.copy()

    # ----------------- Column existence -----------------
    has_age = "Age" in df.columns
    has_spend = "Spend_Per_Month" in df.columns or "Monthly_Spend" in df.columns
    has_income = "Monthly_Income" in df.columns

    spend_col = "Monthly_Spend" if "Monthly_Spend" in df.columns else "Spend_Per_Month"

    # ----------------- AGE RULES -----------------
    if has_age:
        min_age = constraints.get("min_age", 15)
        max_age = constraints.get("max_age", 65)

        # Clip and force integer
        df["Age"] = (
            df["Age"]
            .clip(lower=min_age, upper=max_age)
            .round()
            .astype(int)
        )

    # ----------------- AGE ↔ SPEND RULES -----------------
    if has_age and has_spend:
        student_max = constraints.get("student_spend_max", 3000)
        professional_min = constraints.get("professional_spend_min", 2000)

        # Young users
        young_mask = df["Age"] < 22
        df.loc[young_mask, spend_col] = (
            df.loc[young_mask, spend_col]
            .clip(upper=student_max)
        )

        # Professionals
        prof_mask = df["Age"] >= 30
        df.loc[prof_mask, spend_col] = (
            df.loc[prof_mask, spend_col]
            .clip(lower=professional_min)
        )

    # ----------------- SPEND VS INCOME -----------------
    if has_spend and has_income:
        ratio = constraints.get("max_spend_ratio", 0.2)

        max_allowed = df["Monthly_Income"] * ratio
        df[spend_col] = df[[spend_col, max_allowed]].min(axis=1)

    # ----------------- FORCE INTEGER COLUMNS -----------------
    INTEGER_COLUMNS = {
        "Age",
        "Satisfaction_Score",
        "Spend_Per_Month",
        "Monthly_Spend",
        "Purchase_Frequency",
    }

    for col in INTEGER_COLUMNS:
        if col in df.columns:
            df[col] = (
                df[col]
                .round()
                .fillna(0)
                .astype(int)
            )

    # ----------------- NON-NEGATIVE SAFETY -----------------
    for col in df.select_dtypes(include="number").columns:
        df[col] = df[col].clip(lower=0)

    return df
