import pandas as pd
import re
from schema.column_types import SemanticType
from schema.pii_detector import detect_pii


DATE_REGEX = re.compile(
    r"\d{4}[-/]\d{1,2}[-/]\d{1,2}"
)


def infer_semantic_type(series: pd.Series) -> SemanticType:
    name = series.name.lower()

    # 1️⃣ PII / Identifier detection
    if detect_pii(name):
        if "id" in name:
            return SemanticType.IDENTIFIER
        return SemanticType.PII_NAME

    # 2️⃣ Numeric detection (even if stored as string)
    if pd.api.types.is_numeric_dtype(series):
        return SemanticType.NUMERIC_CONTINUOUS

    # Try coercing strings to numbers
    coerced = pd.to_numeric(series, errors="coerce")
    if coerced.notna().mean() > 0.8:
        return SemanticType.NUMERIC_CONTINUOUS

    # 3️⃣ Date detection (string-based)
    sample = series.dropna().astype(str).head(10)
    if sample.str.match(DATE_REGEX).mean() > 0.6:
        return SemanticType.DATE

    # 4️⃣ Boolean
    if series.dropna().isin([True, False, "True", "False", 0, 1]).all():
        return SemanticType.BOOLEAN

    # 5️⃣ Categorical vs Text
    avg_len = series.dropna().astype(str).str.len().mean()
    unique_ratio = series.nunique() / max(len(series), 1)

    if unique_ratio < 0.2 and avg_len < 30:
        return SemanticType.CATEGORICAL

    if avg_len < 50:
        return SemanticType.TEXT_SHORT

    return SemanticType.TEXT_LONG
