from deep_translator import GoogleTranslator

class ChatTranslator:
    def __init__(self, source="th", target="en"):
        self.translator = GoogleTranslator(source=source, target=target)
        
    def translate(self, text):
        """Translates the given text using Google Translator."""
        return self.translator.translate(text)
