from faker import Faker
from typing import List, Optional
import random


FAKER_MAP = {
    "pii_name": "name",
    "pii_email": "email",
    "pii_phone": "phone_number",
}


def generate_pii_column(
    semantic_type: str,
    num_rows: int,
    locale: str = "en_IN",
    gender_series: Optional[List[str]] = None
) -> List[str]:
    """
    Generate PII columns using Faker.
    - Names are gender-aware if gender_series is provided
    - Email / phone are always safe
    """

    if semantic_type not in FAKER_MAP:
        raise ValueError(
            f"Unsupported PII semantic type: {semantic_type}"
        )

    fake = Faker(locale)
    Faker.seed(42)
    random.seed(42)

    values = []

    for i in range(num_rows):

        gender = None
        if gender_series is not None and i < len(gender_series):
            gender = str(gender_series[i]).strip().lower()

        # ----------------- NAME (GENDER-AWARE) -----------------
        if semantic_type == "pii_name":

            if gender:
                if gender.startswith("m"):
                    values.append(fake.first_name_male())
                    continue

                if gender.startswith("f"):
                    values.append(fake.first_name_female())
                    continue

            # fallback (unknown / other)
            values.append(fake.name())
            continue

        # ----------------- OTHER PII -----------------
        provider = getattr(fake, FAKER_MAP[semantic_type])
        values.append(str(provider()))

    return values


def generate_identifier(prefix: str, num_rows: int) -> List[str]:
    """
    Generate stable, unique identifiers.
    Example: RESP000001
    """

    prefix = prefix.upper()

    return [
        f"{prefix}{str(i).zfill(6)}"
        for i in range(1, num_rows + 1)
    ]
