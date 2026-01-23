import pandas as pd
import numpy as np
from datetime import timedelta


def run_numeric_pipeline(real_df, semantic_map, num_rows):
    numeric_cols = []
    date_cols = []

    for col, sem in semantic_map.items():
        if sem.name.startswith("NUMERIC") or sem.name == "CATEGORICAL":
            numeric_cols.append(col)
        elif sem.name == "DATE":
            date_cols.append(col)

    synthetic_df = pd.DataFrame(index=range(num_rows))

    # ---- Numeric & categorical ----
    if numeric_cols:
        sampled = real_df[numeric_cols].sample(
            n=num_rows,
            replace=True,
            random_state=42
        ).reset_index(drop=True)
        synthetic_df[numeric_cols] = sampled

    # ---- Date columns ----
    for col in date_cols:
        real_dates = pd.to_datetime(
            real_df[col],
            errors="coerce"
        ).dropna()

        if real_dates.empty:
            continue

        min_date = real_dates.min()
        max_date = real_dates.max()

        random_days = np.random.randint(
            0,
            (max_date - min_date).days + 1,
            size=num_rows
        )

        synthetic_df[col] = [
            (min_date + timedelta(days=int(d))).date()
            for d in random_days
        ]

    return synthetic_df
