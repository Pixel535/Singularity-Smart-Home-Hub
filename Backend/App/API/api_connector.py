from deep_translator import GoogleTranslator, MyMemoryTranslator, PonsTranslator, LingueeTranslator, MicrosoftTranslator
from deep_translator.exceptions import NotValidPayload, TranslationNotFound, TooManyRequests


def api_translate_text(text: str, target_lang: str) -> str:
    translators = [
        lambda: GoogleTranslator(source='en', target=target_lang).translate(text),
        lambda: MyMemoryTranslator(source='en', target=target_lang).translate(text),
        lambda: MicrosoftTranslator(source='en', target=target_lang).translate(text),
        lambda: PonsTranslator(source='en', target=target_lang).translate(text),
        lambda: LingueeTranslator(source='en', target=target_lang).translate(text),
    ]

    for translate in translators:
        try:
            return translate()
        except (NotValidPayload, TranslationNotFound, TooManyRequests, Exception):
            continue

    return text
