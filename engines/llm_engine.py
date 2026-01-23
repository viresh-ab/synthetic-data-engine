from openai import OpenAI

client = OpenAI()


def generate_text(prompt: str, num_rows: int):
    """
    Generate synthetic text using OpenAI Responses API.
    Returns a list of strings (length = num_rows).
    """

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt,
        temperature=0.9
    )

    # Extract text safely
    output_text = response.output_text

    if not output_text:
        return [""] * num_rows

    # Split lines into rows
    lines = [line.strip() for line in output_text.split("\n") if line.strip()]

    # Ensure correct length
    if len(lines) < num_rows:
        lines.extend([lines[-1]] * (num_rows - len(lines)))
    else:
        lines = lines[:num_rows]

    return lines
