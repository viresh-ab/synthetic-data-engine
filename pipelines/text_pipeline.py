import os
import json
import yaml
import random

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


# ----------------- DEDUPLICATION -----------------
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


# ----------------- TEXT PIPELINE -----------------
def run_text_pipeline(semantic_map, real_df, num_rows):
    """
    Generates synthetic text columns using GPT in BATCH mode.
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

    # -------- Generate text column-wise --------
    for col, sem_type in semantic_map.items():

        # 🚫 Hard block
        if sem_type in BLOCKED_TYPES:
            continue

        # Only TEXT columns allowed
        if sem_type not in (
            SemanticType.TEXT_SHORT,
            SemanticType.TEXT_LONG,
        ):
            continue

        col_cfg = column_prompts.get(col, {})
        instruction = col_cfg.get(
            "instruction",
            f"Write a realistic response for the column '{col}'."
        )

        # -------- Persona mixing --------
        persona_block = "\n".join(
            [
                f"- {p['name']}: {', '.join(p.get('traits', []))}"
                for p in personas
            ]
        )

        # -------- Single batched prompt --------
        full_prompt = f"""
{base_prompt}

Personas:
{persona_block}

Instructions:
- Generate {num_rows} UNIQUE responses
- Each response must sound like a different person
- Avoid repetition in tone, structure, and wording
- Keep answers realistic and grounded
- DO NOT number the responses

Task:
{instruction}
"""

        # -------- Batched generation --------
        try:
            outputs = generate_text(
                prompt=full_prompt,
                n=num_rows
            )
        except Exception as e:
            raise RuntimeError(
                f"LLM generation failed for column '{col}': {e}"
            )

        if len(outputs) != num_rows:
            raise ValueError(
                f"Expected {num_rows} texts for '{col}', got {len(outputs)}"
            )

        text_data[col] = deduplicate(
            [t.strip() for t in outputs]
        )

    return text_data
