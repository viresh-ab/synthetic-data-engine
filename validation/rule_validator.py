def validate_rules(df):
    for _, row in df.iterrows():
        if row["Age"] < 18:
            assert row["Monthly_Spend"] <= 3000

        if row["Age"] > 35:
            assert row["Monthly_Spend"] >= 2000
