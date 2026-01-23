from openai import OpenAI
import random

client = OpenAI()


def generate_text(prompt: str, n: int):
    """
    Generate n unique responses using batched LLM calls.
    """

    outputs = []

    for i in range(n):
        varied_prompt = f"""
{prompt}

Important:
- This response must be unique.
- Do NOT reuse wording from previous responses.
- Vary sentence length and tone.
- Answer as a different individual.

Response #{i+1}:
"""

        response = client.responses.create(
            model="gpt-4.1-mini",
            input=varied_prompt,
            temperature=0.95
        )

        text = response.output_text.strip()
        outputs.append(text)

    return outputs
