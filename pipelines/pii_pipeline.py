from engines.faker_engine import (
    generate_pii_column,
    generate_identifier
)
from schema.column_types import SemanticType


def run_pii_pipeline(semantic_map, num_rows):
    """
    Generate privacy-safe PII and identifier columns using Faker.
    Only columns explicitly marked as PII / IDENTIFIER are generated.
    """

    pii_data = {}

    for col, sem_type in semantic_map.items():

        # ----------------- IDENTIFIERS -----------------
        if sem_type == SemanticType.IDENTIFIER:
            pii_data[col] = generate_identifier(
                prefix=col[:4].upper(),
                num_rows=num_rows
            )

        # ----------------- PII FIELDS -----------------
        elif sem_type in (
            SemanticType.PII_NAME,
            SemanticType.PII_EMAIL,
            SemanticType.PII_PHONE
        ):
            pii_data[col] = generate_pii_column(
                semantic_type=sem_type.value,
                num_rows=num_rows
            )

    return pii_data
