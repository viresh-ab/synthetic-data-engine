import random
from engines.llm_engine import generate_text

def run_text_pipeline(
    semantic_map,
    real_df,
    num_rows,
    personas,
    column_prompts
):
    text_data = {}

    for col, sem_type in semantic_map.items():
        if sem_type.name.startswith("TEXT"):
            persona = random.choice(personas)
            col_prompt = column_prompts[col]

            full_prompt = f"""
            {open("prompts/base_prompt.txt").read()}

            Persona: {persona['name']}
            Traits: {', '.join(persona['traits'])}

            Task:
            {col_prompt['instruction']}
            """

            text_data[col] = generate_text(
                full_prompt,
                num_rows
            )

    return text_data
