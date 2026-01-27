from faker import Faker
from typing import List


# Mapping between semantic types and Faker providers
FAKER_MAP = {
    "pii_name": "name",
    "pii_email": "email",
    "pii_phone": "phone_number",
}


def generate_pii_column(
    semantic_type: str,
    num_rows: int,
    locale: str = "en_IN"
) -> List[str]:
    """
    Generate a list of PII-safe synthetic values using Faker.
    """

    if semantic_type not in FAKER_MAP:
        raise ValueError(
            f"Unsupported PII semantic type: {semantic_type}"
        )

    fake = Faker(locale)
    Faker.seed(42)  # deterministic but safe

    provider_name = FAKER_MAP[semantic_type]
    provider = getattr(fake, provider_name)

    values = []

    for _ in range(num_rows):
        val = provider()

        # Ensure string output
        if val is None:
            val = ""

        values.append(str(val))

    return values


def generate_identifier(prefix: str, num_rows: int) -> List[str]:
    """
    Generate stable, unique identifiers (no collisions).
    Example: USER000001
    """

    prefix = prefix.upper()

    return [
        f"{prefix}{str(i).zfill(6)}"
        for i in range(1, num_rows + 1)
    ]
