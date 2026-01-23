from engines.faker_engine import (
    generate_pii_column,
    generate_identifier
)

def run_pii_pipeline(semantic_map, num_rows):
    pii_data = {}

    for col, sem_type in semantic_map.items():
        if sem_type.name.startswith("PII"):
            pii_data[col] = generate_pii_column(
                sem_type.value,
                num_rows
            )

        if sem_type.name == "IDENTIFIER":
            pii_data[col] = generate_identifier(
                prefix=col[:4].upper(),
                num_rows=num_rows
            )

    return pii_data
