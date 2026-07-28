import keyboard
from config import load_config
from translator import ChatTranslator
from hotkey import handle_hotkey
from logger import logger

def main():
    # โหลด config
    config = load_config()
    source_lang = config.get("source_lang", "th")
    target_lang = config.get("target_lang", "en")
    hotkey_key = config.get("hotkey", "F8")
    
    # สร้างตัวแปลภาษา
    translator = ChatTranslator(source=source_lang, target=target_lang)
    
    logger.info("ChatBridge Initialized")
    logger.info(f"[{hotkey_key}] = Translate {source_lang} -> {target_lang}")
    
    # ผูกปุ่มลัดเข้ากับฟังก์ชัน handle_hotkey
    keyboard.add_hotkey(hotkey_key, lambda: handle_hotkey(translator))
    
    logger.info("Press CTRL+C to exit.")
    keyboard.wait()

if __name__ == "__main__":
    main()