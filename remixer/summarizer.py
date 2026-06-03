import httpx


SYSTEM_PROMPT = """You are a helpful assistant for parents. Given a video transcript, write a concise summary in {lang} covering:
- Main topic and key points
- Any content that may need parental guidance (violence, complex themes, sensitive topics)

Be factual and brief."""


def summarize(
    segments: list[dict],
    target_lang: str = "zh",
    host: str = "http://127.0.0.1:8080",
    model: str = "qwen",
) -> str:
    """Summarize transcript segments via llama.cpp server.

    Returns a summary string in the target language.
    """
    transcript = "\n".join(s["text"] for s in segments)

    response = httpx.post(
        f"{host}/v1/chat/completions",
        json={
            "model": model,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT.format(lang=target_lang)},
                {"role": "user", "content": transcript},
            ],
            "temperature": 0.5,
        },
    )
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"].strip()
