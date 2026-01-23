import os
import json
import yaml
import random

from engines.llm_engine import generate_text


def run_text_pipeline(semantic_map, real_df, num_rows):
    base_dir = os.getcwd()

    # Load assets
    personas = json.load(
        open(os.path.join(base_dir, "prompts/fashion_personas.json"))
    )
    column_prompts = yaml.safe_load(
        open(os.path.join(base_dir, "prompts/column_prompts.yaml"))
    )
    base_prompt = open(
        os.path.join(base_dir, "prompts/base_prompt.txt")
    ).read()

    text_data = {}

    for col, sem_type in semantic_map.items():
        if not sem_type.name.startswith("TEXT"):
            continue

        col_cfg = column_prompts.get(col, {})
        instruction = col_cfg.get(
            "instruction",
            f"Write a natural response for {col}"
        )

        column_outputs = []

        for i in range(num_rows):
            persona = random.choice(personas)

            full_prompt = f"""
{base_prompt}

Persona:
- Type: {persona['name']}
- Traits: {', '.join(persona['traits'])}

Task:
{instruction}
"""

            row_text = generate_text(full_prompt, 1)[0]
            column_outputs.append(row_text)

        text_data[col] = column_outputs

    return text_data
