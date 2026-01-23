import pandas as pd

def apply_numeric_rules(df, constraints):
    df = df.copy()

    if "Age" not in df.columns:
        # Dataset has no age → skip age-based rules safely
        return df

    for i, row in df.iterrows():
        age = row.get("Age")

        if pd.isna(age):
            continue

        if age < 22 and "Monthly_Spend" in df.columns:
            df.at[i, "Monthly_Spend"] = min(
                row["Monthly_Spend"],
                constraints.get("student_spend_max", row["Monthly_Spend"])
            )

        if age > 30 and "Monthly_Spend" in df.columns:
            df.at[i, "Monthly_Spend"] = max(
                row["Monthly_Spend"],
                constraints.get("professional_spend_min", row["Monthly_Spend"])
            )

    return df
