import time
import pyautogui
import pyperclip
from logger import logger

def handle_hotkey(translator):
    """
    Simulate keyboard shortcuts to copy text, translate it, and paste it back.
    """
    try:
        # เลือกข้อความทั้งหมด
        pyautogui.hotkey("ctrl", "a")
        time.sleep(0.05)

        # คัดลอก
        pyautogui.hotkey("ctrl", "c")
        time.sleep(0.1)

        text = pyperclip.paste().strip()

        if not text:
            return

        logger.info(f"Original: {text}")

        translated = translator.translate(text)

        logger.info(f"Translated: {translated}")

        # วางข้อความใหม่
        pyperclip.copy(translated)

        pyautogui.hotkey("ctrl", "a")
        time.sleep(0.05)

        pyautogui.hotkey("ctrl", "v")

    except Exception as e:
        logger.error(f"Error handling hotkey: {e}")
