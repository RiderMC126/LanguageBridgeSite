from deep_translator import GoogleTranslator

async def translate_text(text: str, target_lang: str) -> str:
    try:
        translated = GoogleTranslator(source='auto', target=target_lang).translate(text)
        return translated
    except Exception as e:
        print(f"Translation error: {e}")
        return text
