from enum import Enum

class SemanticType(Enum):
    PII_NAME = "pii_name"
    PII_EMAIL = "pii_email"
    PII_PHONE = "pii_phone"
    IDENTIFIER = "identifier"

    NUMERIC_CONTINUOUS = "numeric_continuous"
    NUMERIC_DISCRETE = "numeric_discrete"

    CATEGORICAL = "categorical"
    ORDINAL = "ordinal"

    TEXT_SHORT = "text_short"
    TEXT_LONG = "text_long"

    DATE = "date"
    BOOLEAN = "boolean"
