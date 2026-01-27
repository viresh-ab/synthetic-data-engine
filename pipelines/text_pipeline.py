import os
import json
import yaml
from engines.llm_engine import generate_text
from schema.column_types import SemanticType


# ----------------- GPT MUST NEVER TOUCH THESE -----------------
BLOCKED_TYPES = {
    SemanticType.IDENTIFIER,
    SemanticType.NUMERIC_CONTINUOUS,
    SemanticType.NUMERIC_DISCRETE,
    SemanticType.DATE,
    SemanticType.BOOLEAN,
    SemanticType.PII_NAME,
    SemanticType.PII_EMAIL,
    SemanticType.PII_PHONE,
}


def deduplicate(texts):
    seen = set()
    final = []
    for t in texts:
        if t not in seen:
            final.append(t)
            seen.add(t)
        else:
            final.append(t + " ")
    return final


def _age_bucket(age):
    if age < 22:
        return "young adult / student"
    if age < 35:
        return "working professional"
    if age < 50:
        return "mid-career adult"
    return "senior consumer"


def run_text_pipeline(semantic_map, base_df, num_rows):
    """
    Row-aware text generation.
    Each response is conditioned on Age, Gender, and City.
    """

    base_dir = os.getcwd()

    # -------- Load prompt assets --------
    with open(os.path.join(base_dir, "prompts/base_prompt.txt"), "r") as f:
        base_prompt = f.read()

    with open(os.path.join(base_dir, "prompts/fashion_personas.json"), "r") as f:
        personas = json.load(f)

    with open(os.path.join(base_dir, "prompts/column_prompts.yaml"), "r") as f:
        column_prompts = yaml.safe_load(f)

    text_data = {}

    # -------- Generate text columns --------
    for col, sem_type in semantic_map.items():

        if sem_type in BLOCKED_TYPES:
            continue

        if sem_type not in (SemanticType.TEXT_SHORT, SemanticType.TEXT_LONG):
            continue

        col_cfg = column_prompts.get(col, {})
        instruction = col_cfg.get(
            "instruction",
            f"Write a realistic response for '{col}'."
        )

        prompts = []

        # -------- Build row-aware prompts --------
        for i in range(num_rows):
            row = base_df.iloc[i]

            age = row.get("Age", None)
            gender = row.get("Gender", "Unknown")
            city = row.get("City", "an Indian city")

            age_desc = _age_bucket(age) if age is not None else "adult"

            persona = personas[i % len(personas)]

            row_prompt = f"""
{base_prompt}

Context:
- Age group: {age_desc}
- Gender: {gender}
- City: {city}
- Lifestyle persona: {persona['name']} ({', '.join(persona.get('traits', []))})

Rules:
- Response must align with the context above
- Use culturally appropriate references
- Do not mention the city explicitly unless natural
- Sound like a real individual, not a survey

Task:
{instruction}
"""
            prompts.append(row_prompt)

        # -------- Batched generation --------
        outputs = generate_text(prompts, n=len(prompts))

        text_data[col] = deduplicate(
            [o.strip() for o in outputs]
        )

    return text_data
