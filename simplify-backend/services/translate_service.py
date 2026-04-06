import re
from deep_translator import GoogleTranslator


def translate_text(text, source="en", target="th"):
    if not text:
        return None

    try:
        translated = GoogleTranslator(
            source=source,
            target=target
        ).translate(text)

        return translated

    except Exception as e:
        print("Translate error:", e)
        return None


def clean_thai(text: str):
    if not text:
        return text

    text = re.sub(r'\s+', ' ', text)

    text = re.sub(r'\s*,\s*', ', ', text)

    text = re.sub(r'\s*[.!?]+\s*', ' ', text)

    text = re.sub(r'(?<=[ก-๙])\s+(?=[ก-๙])', '', text)

    return text.strip()


def translate_sentence(text: str):
    translated = translate_text(text)
    return clean_thai(translated)