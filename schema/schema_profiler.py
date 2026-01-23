import pandas as pd
from schema.column_types import SemanticType
from schema.pii_detector import detect_pii

def infer_semantic_type(series: pd.Series) -> SemanticType:
    name = series.name.lower()

    # 1️⃣ PII detection
    if detect_pii(name):
        if "email" in name:
            return SemanticType.PII_EMAIL
        if "phone" in name:
            return SemanticType.PII_PHONE
        return SemanticType.PII_NAME

    # 2️⃣ Numeric types
    if pd.api.types.is_numeric_dtype(series):
        unique_ratio = series.nunique() / len(series)
        if unique_ratio > 0.7:
            return SemanticType.NUMERIC_CONTINUOUS
        return SemanticType.NUMERIC_DISCRETE

    # 3️⃣ Boolean
    if series.dropna().isin([True, False]).all():
        return SemanticType.BOOLEAN

    # 4️⃣ Text vs categorical
    avg_len = series.dropna().astype(str).str.len().mean()

    if avg_len < 30 and series.nunique() < 20:
        return SemanticType.CATEGORICAL

    if avg_len < 50:
        return SemanticType.TEXT_SHORT

    return SemanticType.TEXT_LONG
