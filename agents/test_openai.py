from openai import OpenAI

client = OpenAI()

response = client.responses.create(
    model="gpt-6.2-astra",
    input="Explain what an AI Business Analyst does in two sentences."
)

print(response.output_text)