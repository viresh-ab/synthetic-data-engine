import json
import yaml
import os
import random

from engines.llm_engine import generate_text


def run_text_pipeline(semantic_map, real_df, num_rows):
    """
    Generates text columns using GPT LLM with personas
    and column-specific prompts.
    """

    base_dir = os.path.dirname(os.path.dirname(__file__))

    # Load personas
    with open(os.path.join(base_dir, "prompts/fashion_personas.json")) as f:
        personas = json.load(f)

    # Load column prompts
    with open(os.path.join(base_dir, "prompts/column_prompts.yaml")) as f:
        column_prompts = yaml.safe_load(f)

    # Load base prompt
    with open(os.path.join(base_dir, "prompts/base_prompt.txt")) as f:
        base_prompt = f.read()

    text_data = {}

    for col, sem_type in semantic_map.items():
        if not sem_type.name.startswith("TEXT"):
            continue

        persona = random.choice(personas)
        prompt_cfg = column_prompts.get(col, {})

        instruction = prompt_cfg.get(
            "instruction",
            f"Write a natural response for {col}"
        )

        full_prompt = f"""
{base_prompt}

Persona: {persona['name']}
Traits: {', '.join(persona['traits'])}

Task:
{instruction}
"""

        text_data[col] = generate_text(full_prompt, num_rows)

    return text_data
