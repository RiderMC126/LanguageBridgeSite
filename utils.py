from deep_translator import GoogleTranslator
import asyncio

async def translate_text(text: str, target_lang: str) -> str:
    """Асинхронный перевод текста"""
    loop = asyncio.get_event_loop()
    try:
        return await loop.run_in_executor(None, lambda: GoogleTranslator(source='auto', target=target_lang).translate(text))
    except Exception as e:
        print(f"Translation error: {e}")
        return text