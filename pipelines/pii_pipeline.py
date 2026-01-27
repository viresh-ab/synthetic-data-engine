from engines.faker_engine import (
    generate_pii_column,
    generate_identifier
)
from schema.column_types import SemanticType


def run_pii_pipeline(semantic_map, num_rows, base_df=None):
    """
    Generate PII and identifier columns.
    - Names are generated using Gender if available
    """

    pii_data = {}

    # ----------------- Extract Gender column (if exists) -----------------
    gender_series = None
    if base_df is not None:
        for col, sem in semantic_map.items():
            if col.lower() == "gender" and sem == SemanticType.CATEGORICAL:
                gender_series = base_df[col].tolist()
                break

    # ----------------- Generate PII -----------------
    for col, sem_type in semantic_map.items():

        # -------- IDENTIFIERS --------
        if sem_type == SemanticType.IDENTIFIER:
            pii_data[col] = generate_identifier(
                prefix=col[:4].upper(),
                num_rows=num_rows
            )

        # -------- NAMES (GENDER-AWARE) --------
        elif sem_type == SemanticType.PII_NAME:
            pii_data[col] = generate_pii_column(
                semantic_type=sem_type.value,
                num_rows=num_rows,
                gender_series=gender_series
            )

        # -------- OTHER PII --------
        elif sem_type in (
            SemanticType.PII_EMAIL,
            SemanticType.PII_PHONE,
        ):
            pii_data[col] = generate_pii_column(
                semantic_type=sem_type.value,
                num_rows=num_rows
            )

    return pii_data
