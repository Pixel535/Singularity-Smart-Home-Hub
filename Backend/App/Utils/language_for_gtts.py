
SUPPORTED_GTTS_LANGUAGES = {
    "af", "sq", "ar", "hy", "bn", "bs", "ca", "hr", "cs", "da", "nl", "en", "eo",
    "et", "tl", "fi", "fr", "de", "el", "gu", "hi", "hu", "is", "id", "it", "ja",
    "jw", "kn", "km", "ko", "la", "lv", "lt", "mk", "ml", "mr", "my", "ne", "no",
    "pl", "pt", "pa", "ro", "ru", "sr", "si", "sk", "sl", "es", "su", "sw", "sv",
    "ta", "te", "th", "tr", "uk", "ur", "vi", "cy", "zh"
}

def resolve_gtts_language(lang_code: str) -> str:
    return lang_code.lower() if lang_code and lang_code.lower() in SUPPORTED_GTTS_LANGUAGES else "en"