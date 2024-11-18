import requests
import os

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def process_with_llm(prompt, context):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "prompt": prompt.format(context=context),
        "max_tokens": 100
    }
    response = requests.post("https://api.groq.com/v1/completions", json=data, headers=headers)
    if response.status_code == 200:
        return response.json()["choices"][0]["text"].strip()
    else:
        raise Exception(f"Error with Groq API: {response.status_code}")
