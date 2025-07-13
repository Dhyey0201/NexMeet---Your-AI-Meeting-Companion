import requests

def extract_action_items(transcript: str) -> str:
    prompt = f"""Extract key action items from the following meeting transcript:

{transcript}

List them clearly using bullet points.
"""

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "mistral", "prompt": prompt, "stream": False}
        )
        if response.status_code == 200:
            return response.json()["response"].strip()
        else:
            return f"⚠️ Ollama error: {response.status_code}"
    except Exception as e:
        return f"❌ Failed to contact Ollama: {e}"
