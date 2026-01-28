import os
import json
import yaml
import numpy as np
from engines.llm_engine import generate_text
from schema.column_types import SemanticType


# ----------------- BLOCKED TYPES -----------------
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


def _age_bucket(age):
    if age < 22:
        return "young adult"
    if age < 35:
        return "working professional"
    if age < 50:
        return "mid-career adult"
    return "older adult"


def _truncate_to_length(text: str, max_chars: int) -> str:
    if len(text) <= max_chars:
        return text
    return text[:max_chars].rsplit(" ", 1)[0]


def run_text_pipeline(semantic_map, base_df, num_rows, real_df):
    """
    Row-aware + length-controlled text generation.
    - Length learned from REAL data
    - Context taken from SYNTHETIC rows
    """

    base_dir = os.getcwd()

    # -------- Load assets --------
    with open(os.path.join(base_dir, "prompts/base_prompt.txt"), "r") as f:
        base_prompt = f.read()

    with open(os.path.join(base_dir, "prompts/fashion_personas.json"), "r") as f:
        personas = json.load(f)

    with open(os.path.join(base_dir, "prompts/column_prompts.yaml"), "r") as f:
        column_prompts = yaml.safe_load(f)

    text_data = {}

    # -------- Learn length distribution from REAL input --------
    length_profile = {}

    for col, sem in semantic_map.items():
        if sem in (SemanticType.TEXT_SHORT, SemanticType.TEXT_LONG) and col in real_df.columns:
            real_lengths = real_df[col].dropna().astype(str).str.len()
            if not real_lengths.empty:
                length_profile[col] = {
                    "mean": int(real_lengths.mean()),
                    "max": int(real_lengths.quantile(0.9))
                }

    # -------- Generate text columns --------
    for col, sem_type in semantic_map.items():

        if sem_type in BLOCKED_TYPES:
            continue

        if sem_type not in (SemanticType.TEXT_SHORT, SemanticType.TEXT_LONG):
            continue

        col_cfg = column_prompts.get(col, {})
        instruction = col_cfg.get(
            "instruction",
            f"Write a short, realistic response for '{col}'."
        )

        mean_len = length_profile.get(col, {}).get("mean", 120)
        max_len = length_profile.get(col, {}).get("max", mean_len + 30)

        prompts = []

        for i in range(num_rows):
            row = base_df.iloc[i]

            age = row.get("Age", 30)
            gender = row.get("Gender", "Unknown")
            city = row.get("City", "an Indian city")

            persona = personas[i % len(personas)]

            prompts.append(
                f"""
{base_prompt}

Context:
- Age group: {_age_bucket(age)}
- Gender: {gender}
- City: {city}
- Persona: {persona['name']} ({', '.join(persona.get('traits', []))})

STRICT OUTPUT RULES:
- Keep response between {int(mean_len*0.8)} and {int(mean_len*1.2)} characters
- Never exceed {max_len} characters
- Use 1 sentence only
- Survey-style tone (not essay)

Task:
{instruction}
"""
            )

        outputs = generate_text(prompts, n=len(prompts))

        final_texts = []
        for t in outputs:
            t = t.strip()
            t = _truncate_to_length(t, max_len)
            final_texts.append(t)

        text_data[col] = final_texts

    return text_data
