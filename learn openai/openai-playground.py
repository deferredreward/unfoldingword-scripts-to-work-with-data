# openai-playground.py
from openai import OpenAI

client = OpenAI()

completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "user", "content": "write a sonnet about a monster truck"}
    ]
)

print(completion.choices[0].message)