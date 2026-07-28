import re
from deep_translator import GoogleTranslator
from logger import logger

class TranslationResult:
    def __init__(self, success: bool, text: str = "", error: str = ""):
        self.success = success
        self.text = text
        self.error = error

class ChatTranslator:
    def __init__(self, default_source="th", default_target="en"):
        self.default_source = default_source
        self.default_target = default_target
        
    def _detect_target_language(self, text: str) -> str:
        """
        Detect language based on characters and return the appropriate target language.
        """
        clean_text = re.sub(r'\W+', '', text)
        if not clean_text:
            return self.default_target
            
        thai_pattern = re.compile(r'[\u0e00-\u0e7f]')
        japanese_pattern = re.compile(r'[\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff]')
        english_pattern = re.compile(r'[a-zA-Z]')
        
        thai_count = len(thai_pattern.findall(clean_text))
        japanese_count = len(japanese_pattern.findall(clean_text))
        english_count = len(english_pattern.findall(clean_text))
        
        max_count = max(thai_count, japanese_count, english_count)
        
        if max_count == 0:
            return self.default_target
            
        if max_count == thai_count:
            return "en" # Thai -> English
        elif max_count == japanese_count:
            return "en" # Japanese -> English
        elif max_count == english_count:
            return "th" # English -> Thai
            
        return self.default_target
        
    def translate(self, text) -> TranslationResult:
        """Translates the given text using Google Translator with auto-detection."""
        try:
            target_lang = self._detect_target_language(text)
            logger.info(f"Auto-detect: Routing translation to target language '{target_lang}'")
            
            translator = GoogleTranslator(source="auto", target=target_lang)
            translated = translator.translate(text)
            return TranslationResult(success=True, text=translated)
        except Exception as e:
            logger.error(f"Translation failed: {e}")
            return TranslationResult(success=False, error=str(e))
