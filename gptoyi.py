from openai import OpenAI

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",  # ✅ this is required for OpenRouter
    api_key="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",   # 🔒 put your OpenRouter key here
)

response = client.chat.completions.create(
    model="openrouter/openai/gpt-3.5-turbo",  # ✅ or any other supported model
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Check if you're working properly."}
    ]
)

print(response.choices[0].message.content)
