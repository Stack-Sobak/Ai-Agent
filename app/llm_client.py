import openai

from .config import settings


def ask_yandex(prompt: str):
    client = openai.OpenAI(
        api_key=settings.yandex_api_key,
        base_url="https://ai.api.cloud.yandex.net/v1",
        project=settings.yandex_cloud_folder
    )

    conv = client.conversations.create()

    response = client.responses.create(
        prompt={"id": settings.assistant_id},
        conversation=conv.id,
        input=prompt
    )

    if hasattr(response, 'output_text') and response.output_text:
        return response.output_text

    for item in response.output:
        if item.type == 'message' and item.content:
            return item.content[0].text

    return "[Нет текстового ответа]"

def summarize_text(provider: str, text: str):
    prompt = f"Сделай краткое резюме диалога:\n{text}"
    return ask_yandex(provider, prompt)