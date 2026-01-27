import pandas as pd
from sdv.single_table import GaussianCopulaSynthesizer
from sdv.metadata import SingleTableMetadata


def generate_numeric_data(df_numeric: pd.DataFrame, num_rows: int) -> pd.DataFrame:
    """
    Generate synthetic numeric data using SDV Gaussian Copula.
    Handles continuous + discrete numeric columns safely.
    """

    # ----------------- Defensive copy -----------------
    df = df_numeric.copy()

    # ----------------- Ensure numeric types -----------------
    for col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Fill NaNs (SDV requirement)
    df = df.fillna(df.median(numeric_only=True))

    # ----------------- Build metadata -----------------
    metadata = SingleTableMetadata()
    metadata.detect_from_dataframe(df)

    # Force numeric columns as numerical
    for col in df.columns:
        metadata.update_column(
            column_name=col,
            sdtype="numerical"
        )

    # ----------------- Train synthesizer -----------------
    synthesizer = GaussianCopulaSynthesizer(
        metadata=metadata,
        enforce_min_max_values=True,
        enforce_rounding=False
    )

    synthesizer.fit(df)

    # ----------------- Sample synthetic data -----------------
    synthetic_df = synthesizer.sample(num_rows)

    return synthetic_df
