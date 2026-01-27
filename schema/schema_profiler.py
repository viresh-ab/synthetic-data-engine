import pandas as pd
import re
from schema.column_types import SemanticType
from schema.pii_detector import detect_pii


DATE_REGEX = re.compile(r"\d{4}[-/]\d{1,2}[-/]\d{1,2}")

# -------- Domain-locked categorical columns --------
FORCED_CATEGORICAL = {
    "city",
    "location",
    "town",
    "gender",
    "sex",
    "state",
    "country"
}


def infer_semantic_type(series: pd.Series) -> SemanticType:
    """
    Infer semantic meaning of a column.
    Domain locks are applied BEFORE statistical inference.
    """

    col_name = series.name.lower().strip()
    non_null = series.dropna()

    # ----------------- 0️⃣ HARD DOMAIN LOCKS -----------------
    if col_name in FORCED_CATEGORICAL:
        return SemanticType.CATEGORICAL

    # ----------------- 1️⃣ PII & IDENTIFIERS -----------------
    if detect_pii(col_name):
        if "email" in col_name:
            return SemanticType.PII_EMAIL

        if "phone" in col_name or "mobile" in col_name:
            return SemanticType.PII_PHONE

        if "id" in col_name:
            return SemanticType.IDENTIFIER

        return SemanticType.PII_NAME

    # ----------------- 2️⃣ Numeric -----------------
    if pd.api.types.is_numeric_dtype(series):
        return SemanticType.NUMERIC_CONTINUOUS

    coerced = pd.to_numeric(series, errors="coerce")
    if coerced.notna().mean() > 0.85:
        return SemanticType.NUMERIC_CONTINUOUS

    # ----------------- 3️⃣ Date -----------------
    if not non_null.empty:
        sample = non_null.astype(str).head(25)
        if sample.str.match(DATE_REGEX).mean() > 0.7:
            return SemanticType.DATE

    # ----------------- 4️⃣ Boolean -----------------
    boolean_values = {True, False, "true", "false", "True", "False", 0, 1}
    if not non_null.empty and non_null.isin(boolean_values).all():
        return SemanticType.BOOLEAN

    # ----------------- 5️⃣ Categorical vs Text -----------------
    avg_len = non_null.astype(str).str.len().mean()
    unique_ratio = non_null.nunique() / max(len(non_null), 1)

    # Low-cardinality, short values → categorical
    if unique_ratio < 0.3 and avg_len < 40:
        return SemanticType.CATEGORICAL

    # ----------------- 6️⃣ Text -----------------
    if avg_len < 80:
        return SemanticType.TEXT_SHORT

    return SemanticType.TEXT_LONG
