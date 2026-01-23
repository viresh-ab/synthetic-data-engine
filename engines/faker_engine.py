from faker import Faker

FAKER_MAP = {
    "pii_name": "name",
    "pii_email": "email",
    "pii_phone": "phone_number"
}

def generate_pii_column(semantic_type, num_rows, locale="en_IN"):
    fake = Faker(locale)
    Faker.seed()

    generator = getattr(fake, FAKER_MAP[semantic_type])

    return [generator() for _ in range(num_rows)]

def generate_identifier(prefix, num_rows):
    return [
        f"{prefix}{str(i).zfill(6)}"
        for i in range(1, num_rows + 1)
    ]
