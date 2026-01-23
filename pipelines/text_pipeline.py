import os
import json
import yaml
import random

from engines.llm_engine import generate_text


def run_text_pipeline(semantic_map, real_df, num_rows):
    """
    Generates synthetic text columns using LLMs.
    It loads personas + column prompts internally.
    """

    # Paths
    base_dir = os.path.join(os.getcwd(), "")

    # Load personas
    with open(os.path.join(base_dir, "prompts/fashion_personas.json"), "r") as f:
        personas = json.load(f)

    # Load column prompts
    with open(os.path.join(base_dir, "prompts/column_prompts.yaml"), "r") as f:
        column_prompts = yaml.safe_load(f)

    # Load base prompt
    with open(os.path.join(base_dir, "prompts/base_prompt.txt"), "r") as f:
        base_prompt = f.read()

    text_data = {}

    for col, sem_type in semantic_map.items():
        # Only generate text for LONG or SHORT text types
        if not sem_type.name.startswith("TEXT"):
            continue

        # Pick a random persona each time
        persona = random.choice(personas)

        # Prompt config (fallback if no custom config for this column)
        col_cfg = column_prompts.get(col, {})
        instruction = col_cfg.get(
            "instruction",
            f"Write a natural response for the column '{col}'"
        )

        # Build the actual prompt text
        full_prompt = f"""
{base_prompt}

Persona: {persona.get('name')}
Traits: {', '.join(persona.get('traits', []))}

Task:
{instruction}
"""

        # Generate text
        text_data[col] = generate_text(full_prompt, num_rows)

    return text_data
