from deep_translator import GoogleTranslator
from logger import logger

class TranslationResult:
    def __init__(self, success: bool, text: str = "", error: str = ""):
        self.success = success
        self.text = text
        self.error = error

class ChatTranslator:
    def __init__(self, source="th", target="en"):
        self.translator = GoogleTranslator(source=source, target=target)
        
    def translate(self, text) -> TranslationResult:
        """Translates the given text using Google Translator."""
        try:
            translated = self.translator.translate(text)
            return TranslationResult(success=True, text=translated)
        except Exception as e:
            logger.error(f"Translation failed: {e}")
            return TranslationResult(success=False, error=str(e))
