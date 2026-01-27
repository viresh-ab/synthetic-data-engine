import numpy as np
import pandas as pd
from scipy.stats import ks_2samp


def _safe_numeric(series: pd.Series) -> np.ndarray:
    """
    Convert series to clean numeric numpy array:
    - coercion
    - NaN removal
    """
    arr = pd.to_numeric(series, errors="coerce")
    arr = arr.replace([np.inf, -np.inf], np.nan)
    arr = arr.dropna()
    return arr.to_numpy()


def numeric_similarity(real_df: pd.DataFrame, synthetic_df: pd.DataFrame) -> dict:
    """
    KS-based similarity score (1 - KS statistic).
    Safe against NaNs, constants, and small samples.
    """

    scores = {}

    real_numeric_cols = real_df.select_dtypes(include="number").columns

    for col in real_numeric_cols:

        if col not in synthetic_df.columns:
            continue

        real_arr = _safe_numeric(real_df[col])
        synth_arr = _safe_numeric(synthetic_df[col])

        # ---- Guard rails ----
        if len(real_arr) < 10 or len(synth_arr) < 10:
            scores[col] = None
            continue

        if np.unique(real_arr).size < 2 or np.unique(synth_arr).size < 2:
            scores[col] = None
            continue

        try:
            ks = ks_2samp(real_arr, synth_arr).statistic
            scores[col] = round(1.0 - ks, 3)
        except Exception:
            # Never crash the app for metrics
            scores[col] = None

    return scores


def text_diversity(text_series: pd.Series) -> float | None:
    if text_series.empty:
        return None
    return round(text_series.nunique() / len(text_series), 3)


def pii_uniqueness(series: pd.Series) -> float | None:
    if series.empty:
        return None
    return round(series.nunique() / len(series), 3)


def generate_quality_report(
    real_df: pd.DataFrame,
    synthetic_df: pd.DataFrame
) -> dict:
    """
    Generate full quality report without ever crashing.
    """

    report = {
        "numeric_similarity": numeric_similarity(real_df, synthetic_df),
        "text_diversity": {},
        "pii_uniqueness": {}
    }

    # ---- Text columns ----
    for col in synthetic_df.select_dtypes(include="object").columns:
        report["text_diversity"][col] = text_diversity(synthetic_df[col])

    return report
