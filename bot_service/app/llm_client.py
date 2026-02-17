import os
import openai
from dotenv import load_dotenv

load_dotenv()

YANDEX_API_KEY = os.getenv("YANDEX_API_KEY")
YANDEX_CLOUD_FOLDER = os.getenv("YANDEX_CLOUD_FOLDER")
ASSISTANT_ID = os.getenv("YANDEX_ASSISTANT_ID")

def ask_yandex(prompt: str):

    if not YANDEX_API_KEY:

        raise ValueError("YANDEX_API_KEY not set")

    client = openai.OpenAI(
        api_key=YANDEX_API_KEY,
        base_url="https://ai.api.cloud.yandex.net/v1",
        project=YANDEX_CLOUD_FOLDER
    )

    conv = client.conversations.create()

    response = client.responses.create(
        prompt={"id": ASSISTANT_ID},
        conversation=conv.id,
        input=prompt
    )

    if hasattr(response, 'output_text') and response.output_text:
        return response.output_text

    for item in response.output:
        if item.type == 'message' and item.content:
            return item.content[0].text

    return "[Нет текстового ответа]"

def ask_llm(prompt: str):
    return ask_yandex(prompt)

def summarize_text(provider: str, text: str):
    prompt = f"Сделай краткое резюме диалога:\n{text}"
    return ask_llm(provider, prompt)