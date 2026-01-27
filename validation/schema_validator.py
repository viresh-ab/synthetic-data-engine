import pandas as pd


def validate_schema(real_df: pd.DataFrame, synthetic_df: pd.DataFrame) -> bool:
    """
    Validate that synthetic data matches the real data schema.
    Checks column presence and order.
    """

    real_cols = list(real_df.columns)
    synth_cols = list(synthetic_df.columns)

    # ----------------- Missing / Extra Columns -----------------
    missing = set(real_cols) - set(synth_cols)
    extra = set(synth_cols) - set(real_cols)

    if missing:
        raise ValueError(
            f"Synthetic data is missing columns: {sorted(missing)}"
        )

    if extra:
        raise ValueError(
            f"Synthetic data has unexpected columns: {sorted(extra)}"
        )

    # ----------------- Column Order -----------------
    if real_cols != synth_cols:
        synthetic_df = synthetic_df[real_cols]

    # ----------------- Row Count -----------------
    if len(synthetic_df) == 0:
        raise ValueError("Synthetic dataset is empty")

    return True
