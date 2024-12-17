from openai import OpenAI
import os
from dotenv import load_dotenv

client = OpenAI(
  base_url = "https://integrate.api.nvidia.com/v1",
  api_key = "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"
)

completion = client.chat.completions.create(
  model="meta/llama-3.1-70b-instruct",
  messages=[{"role":"user","content":"What is RAG in Gen AI?"}],
  temperature=0.2,
  top_p=0.7,
  max_tokens=1024,
  stream=True
)

for chunk in completion:
  if chunk.choices[0].delta.content is not None:
    print(chunk.choices[0].delta.content, end="")

