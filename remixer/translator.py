import httpx


SYSTEM_PROMPT = "You are a translator. Translate the given text to {lang}. Output only the translated text, no explanations."


def translate(
    segments: list[dict],
    target_lang: str = "zh",
    host: str = "http://127.0.0.1:8080",
    model: str = "qwen",
) -> list[dict]:
    """Translate transcript segments via llama.cpp server.

    Returns segments with an added 'translation' field.
    """
    translated = []
    for segment in segments:
        response = httpx.post(
            f"{host}/v1/chat/completions",
            json={
                "model": model,
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT.format(lang=target_lang)},
                    {"role": "user", "content": segment["text"]},
                ],
                "temperature": 0.3,
            },
        )
        response.raise_for_status()
        translation = response.json()["choices"][0]["message"]["content"].strip()
        translated.append({**segment, "translation": translation})

    return translated
