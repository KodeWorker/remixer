import httpx
from tqdm import tqdm


SYSTEM_PROMPT = (
    "You are a translator. Translate each numbered line to {lang}. "
    "Return only the numbered translations in the exact same format. "
    "Do not merge or split lines. No explanations. /no_think"
)


def _translate_batch(
    texts: list[str],
    target_lang: str,
    host: str,
    model: str,
    timeout: int,
) -> list[str]:
    numbered = "\n".join(f"{i + 1}. {t}" for i, t in enumerate(texts))
    response = httpx.post(
        f"{host}/v1/chat/completions",
        timeout=timeout,
        json={
            "model": model,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT.format(lang=target_lang)},
                {"role": "user", "content": numbered},
            ],
            "temperature": 0.3,
        },
    )
    response.raise_for_status()
    raw = response.json()["choices"][0]["message"]["content"].strip()

    translations = []
    for line in raw.splitlines():
        line = line.strip()
        if line and line[0].isdigit() and ". " in line:
            translations.append(line.split(". ", 1)[1])

    if len(translations) != len(texts):
        raise ValueError(
            f"Expected {len(texts)} translations, got {len(translations)}. "
            f"Response:\n{raw}"
        )
    return translations


def translate(
    segments: list[dict],
    target_lang: str = "zh-TW",
    host: str = "http://127.0.0.1:8080",
    model: str = "qwen",
    timeout: int = 120,
    batch_size: int = 20,
) -> list[dict]:
    """Translate transcript segments via llama.cpp server.

    Returns segments with an added 'translation' field.
    """
    translated = []
    batches = [segments[i:i + batch_size] for i in range(0, len(segments), batch_size)]

    with tqdm(total=len(segments), desc="Translating", unit="seg") as bar:
        for batch in batches:
            bar.set_postfix(status="requesting...")
            texts = [s["text"] for s in batch]
            translations = _translate_batch(texts, target_lang, host, model, timeout)
            for segment, translation in zip(batch, translations):
                translated.append({**segment, "translation": translation})
            bar.update(len(batch))
            bar.set_postfix(status="done")

    return translated
