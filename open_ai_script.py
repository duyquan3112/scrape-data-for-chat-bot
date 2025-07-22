from openai import OpenAI

client = OpenAI(
  api_key="your_api_key_here",  # Replace with your actual API key
)

completion = client.chat.completions.create(
  model="gpt-4o-mini",
  store=True,
  messages=[
    {"role": "user", "content": "write a haiku about ai"}
  ]
)

print(completion.choices[0].message);
