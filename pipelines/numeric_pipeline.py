import pandas as pd
import numpy as np
from datetime import timedelta

from engines.sdv_engine import generate_numeric_data
from engines.rag_engine import fetch_constraints
from engines.rule_engine import apply_numeric_rules
from schema.column_types import SemanticType


def run_numeric_pipeline(real_df, semantic_map, num_rows):
    """
    Generates synthetic numeric, categorical, and date data.
    - Numeric → SDV
    - Categorical → sampled ONLY from real values
    - Date → uniform sampling within real range
    """

    numeric_cols = []
    categorical_cols = []
    date_cols = []

    # ----------------- Column routing -----------------
    for col, sem in semantic_map.items():

        if sem in (
            SemanticType.NUMERIC_CONTINUOUS,
            SemanticType.NUMERIC_DISCRETE,
        ):
            numeric_cols.append(col)

        elif sem == SemanticType.CATEGORICAL:
            categorical_cols.append(col)

        elif sem == SemanticType.DATE:
            date_cols.append(col)

    synthetic_df = pd.DataFrame(index=range(num_rows))

    # ----------------- NUMERIC (SDV) -----------------
    if numeric_cols:
        numeric_real = real_df[numeric_cols].copy()

        # SDV safety
        numeric_real = numeric_real.apply(
            pd.to_numeric, errors="coerce"
        )
        numeric_real = numeric_real.fillna(
            numeric_real.median(numeric_only=True)
        )

        synthetic_numeric = generate_numeric_data(
            df_numeric=numeric_real,
            num_rows=num_rows
        )

        synthetic_df[numeric_cols] = synthetic_numeric[numeric_cols]

    # ----------------- CATEGORICAL (STRICT DOMAIN) -----------------
    for col in categorical_cols:
        values = real_df[col].dropna()

        if values.empty:
            synthetic_df[col] = None
            continue

        probs = values.value_counts(normalize=True)

        synthetic_df[col] = np.random.choice(
            probs.index.tolist(),
            size=num_rows,
            p=probs.values
        )

    # ----------------- DATE -----------------
    for col in date_cols:
        real_dates = pd.to_datetime(
            real_df[col],
            errors="coerce"
        ).dropna()

        if real_dates.empty:
            synthetic_df[col] = None
            continue

        min_date = real_dates.min()
        max_date = real_dates.max()
        delta_days = (max_date - min_date).days

        synthetic_df[col] = [
            (min_date + timedelta(days=int(d))).date()
            for d in np.random.randint(0, delta_days + 1, size=num_rows)
        ]

    # ----------------- APPLY BUSINESS RULES -----------------
    constraints = fetch_constraints()
    synthetic_df = apply_numeric_rules(synthetic_df, constraints)

    return synthetic_df
