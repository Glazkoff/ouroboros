import os
from openai import OpenAI

client = OpenAI(
    api_key="aa0f869575cb45dea3d108c3b14d360c.HFmeMIsoOi9YX8EQ", base_url="https://api.z.ai/api/coding/paas/v4"
)
response = client.chat.completions.create(
    model="glm-4.7",
    messages=[
        {"role": "system", "content": "you are a helpful assistant"},
        {"role": "user", "content": "what is the revolution of llm?"},
    ],
    stream=True,
    extra_body={
        "thinking": {
            "type": "enabled",
        },
    },
)
for chunk in response:
    if chunk.choices[0].delta.reasoning_content:
        print(chunk.choices[0].delta.reasoning_content, end="")
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="")
