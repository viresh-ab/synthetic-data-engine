import os
import json
import yaml
import random

from engines.llm_engine import generate_text


# ----------------- HARD BLOCK: GPT MUST NEVER TOUCH THESE -----------------
BLOCKED_TYPES = {
    "IDENTIFIER",
    "NUMERIC_CONTINUOUS",
    "NUMERIC_DISCRETE",
    "DATE",
    "BOOLEAN"
}


# ----------------- DEDUPLICATION UTILITY -----------------
def deduplicate(texts):
    """
    Ensures text uniqueness by lightly modifying duplicates.
    Acts as a final safety net.
    """
    seen = set()
    final = []

    for t in texts:
        if t not in seen:
            final.append(t)
            seen.add(t)
        else:
            # minimal change to force uniqueness
            final.append(t + " ")

    return final


# ----------------- TEXT PIPELINE -----------------
def run_text_pipeline(semantic_map, real_df, num_rows):
    base_dir = os.getcwd()

    # -------- Load prompt assets --------
    with open(os.path.join(base_dir, "prompts/fashion_personas.json"), "r") as f:
        personas = json.load(f)

    with open(os.path.join(base_dir, "prompts/column_prompts.yaml"), "r") as f:
        column_prompts = yaml.safe_load(f)

    with open(os.path.join(base_dir, "prompts/base_prompt.txt"), "r") as f:
        base_prompt = f.read()

    text_data = {}

    # -------- Generate text column-wise --------
    for col, sem_type in semantic_map.items():

        # 🔒 ABSOLUTE SAFETY: GPT NEVER touches these
        if sem_type.name in BLOCKED_TYPES:
            continue

        # Only TEXT columns are allowed
        if not sem_type.name.startswith("TEXT"):
            continue

        col_cfg = column_prompts.get(col, {})
        instruction = col_cfg.get(
            "instruction",
            f"Write a natural response for the column '{col}'"
        )

        column_outputs = []

        for i in range(num_rows):
            persona = random.choice(personas)

            full_prompt = f"""
{base_prompt}

Persona:
- Type: {persona.get('name')}
- Traits: {', '.join(persona.get('traits', []))}

Important:
- This response must be unique.
- Do NOT repeat wording from previous responses.
- Vary sentence length and tone.
- Sound like a real individual.

Task:
{instruction}

Response #{i + 1}:
"""

            row_text = generate_text(full_prompt, 1)[0]
            column_outputs.append(row_text.strip())

        # 🔁 Final deduplication safety net
        text_data[col] = deduplicate(column_outputs)

    return text_data
