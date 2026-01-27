from openai import OpenAI

client = OpenAI()


def generate_text(prompt, n: int):
    """
    Supports:
    - single prompt (str)
    - list of prompts (List[str])
    """

    if isinstance(prompt, list):
        outputs = []
        for p in prompt:
            response = client.responses.create(
                model="gpt-4.1-mini",
                input=p,
                temperature=0.9
            )
            outputs.append(response.output_text.strip())
        return outputs

    # fallback (single prompt)
    outputs = []
    for _ in range(n):
        response = client.responses.create(
            model="gpt-4.1-mini",
            input=prompt,
            temperature=0.9
        )
        outputs.append(response.output_text.strip())

    return outputs
