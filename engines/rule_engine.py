def apply_numeric_rules(df, constraints):
    for i, row in df.iterrows():
        if row["Age"] < 22:
            df.at[i, "Monthly_Spend"] = min(
                row["Monthly_Spend"],
                constraints["student_spend_max"]
            )

        if row["Age"] > 30:
            df.at[i, "Monthly_Spend"] = max(
                row["Monthly_Spend"],
                constraints["professional_spend_min"]
            )
    return df
