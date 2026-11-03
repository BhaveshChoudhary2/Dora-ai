"""Question-answering module for Dora, using OpenRouter's chat completions API."""
import json
import os
import urllib.request

URL = "https://openrouter.ai/api/v1/chat/completions"


def ask(question):
    # Read at call time so a key added after startup is also picked up.
    key = os.environ.get("OPENROUTER_API_KEY") or os.environ.get("OPENAI_API_KEY")
    if not key:
        return "AI answers ke liye OPENROUTER_API_KEY environment variable set karo."
    payload = json.dumps({
        "model": "openai/gpt-4o-mini",
        "messages": [
            {"role": "system", "content": "You are Dora, a helpful assistant. Keep answers concise; Hinglish is okay."},
            {"role": "user", "content": question},
        ],
    }).encode("utf-8")
    request = urllib.request.Request(URL, data=payload, headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {key}",
    })
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            result = json.load(response)
        return result["choices"][0]["message"]["content"].strip()
    except Exception:
        return "AI se jawab nahi mil paya. API key, internet, ya OpenRouter status check karo."


if __name__ == "__main__":
    print(ask("India ki rajdhani kya hai?"))
