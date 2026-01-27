import pandas as pd
import re
from schema.column_types import SemanticType
from schema.pii_detector import detect_pii


DATE_REGEX = re.compile(r"\d{4}[-/]\d{1,2}[-/]\d{1,2}")


def infer_semantic_type(series: pd.Series) -> SemanticType:
    """
    Infer semantic meaning of a column using name + values.
    This function is CRITICAL for correct pipeline routing.
    """

    col_name = series.name.lower()
    series_non_null = series.dropna()

    # ----------------- 1️⃣ PII & IDENTIFIERS -----------------
    if detect_pii(col_name):
        if "email" in col_name:
            return SemanticType.PII_EMAIL

        if "phone" in col_name or "mobile" in col_name:
            return SemanticType.PII_PHONE

        if "id" in col_name:
            return SemanticType.IDENTIFIER

        # Default PII fallback
        return SemanticType.PII_NAME

    # ----------------- 2️⃣ Numeric (strict) -----------------
    if pd.api.types.is_numeric_dtype(series):
        return SemanticType.NUMERIC_CONTINUOUS

    # Try coercion (string numbers)
    coerced = pd.to_numeric(series, errors="coerce")
    if coerced.notna().mean() > 0.85:
        return SemanticType.NUMERIC_CONTINUOUS

    # ----------------- 3️⃣ Date -----------------
    if not series_non_null.empty:
        sample = series_non_null.astype(str).head(20)
        if sample.str.match(DATE_REGEX).mean() > 0.7:
            return SemanticType.DATE

    # ----------------- 4️⃣ Boolean -----------------
    boolean_values = {True, False, "true", "false", "True", "False", 0, 1}
    if series_non_null.isin(boolean_values).all():
        return SemanticType.BOOLEAN

    # ----------------- 5️⃣ Categorical vs Text -----------------
    avg_len = series_non_null.astype(str).str.len().mean()
    unique_ratio = series_non_null.nunique() / max(len(series_non_null), 1)

    # Low cardinality, short → categorical
    if unique_ratio < 0.25 and avg_len < 30:
        return SemanticType.CATEGORICAL

    # ----------------- 6️⃣ Text -----------------
    if avg_len < 60:
        return SemanticType.TEXT_SHORT

    return SemanticType.TEXT_LONG
