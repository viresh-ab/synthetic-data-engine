from openai import OpenAI
client = OpenAI()

def generate_text(prompt, rows):
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt,
        temperature=0.9,
        top_p=0.95,
        presence_penalty=0.6
    )
    return response.output_text.split("\n")[:rows]
