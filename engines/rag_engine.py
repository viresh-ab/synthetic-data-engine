def fetch_constraints(context):
    """
    In production: vector DB + embeddings
    For now: static retrieval
    """
    rules = {
        "student_spend_max": 3000,
        "professional_spend_min": 2000,
        "max_spend_ratio": 0.2
    }
    return rules
