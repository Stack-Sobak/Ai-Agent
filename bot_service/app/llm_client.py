import requests

def ask_llm(prompt: str):
    response = requests.post(
        "http://llm:11434/api/generate",
        json={
            "model": "llama3",
            "prompt": prompt,
            "stream": False
        }
    )

    return response.json()["response"]


def summarize_text(text: str):
    prompt = f"Сделай краткую выжимку этого диалога:\n{text}"
    return ask_llm(prompt)