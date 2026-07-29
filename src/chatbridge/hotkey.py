import time
import pyperclip
import keyboard
from chatbridge.logger import logger


def handle_hotkey(translator, tray_app=None) -> None:
    """
    Copy text, translate it, and paste it back.
    Respects the enabled/disabled state from the tray.
    """
    # If tray app exists and is disabled, do nothing
    if tray_app is not None and not tray_app.is_enabled:
        logger.debug("Hotkey fired but translator is disabled. Skipping.")
        return

    try:
        # คัดลอกข้อความที่ถูกลากคลุม (highlighted)
        keyboard.send("ctrl+c")
        time.sleep(0.15)  # รอให้ clipboard อัปเดต

        text = pyperclip.paste().strip()

        if not text:
            return

        logger.info(f"Original: {text}")

        result = translator.translate(text)

        if result.success:
            logger.info(f"Translated: {result.text}")

            # วางข้อความใหม่ทับที่เดิมที่ถูกลากคลุมอยู่
            pyperclip.copy(result.text)
            time.sleep(0.15)  # รอให้ clipboard พร้อม
            keyboard.send("ctrl+v")
            time.sleep(0.05)
            
            # ถ้าตั้งค่า auto_send ให้กด Enter ด้วย
            try:
                from chatbridge.config import load_config
                config = load_config()
                if config.get("auto_send", False):
                    keyboard.send("enter")
            except Exception as e:
                logger.error(f"Error reading auto_send config: {e}")
                
        else:
            logger.error(f"Failed to translate: {result.error}")

    except Exception as e:
        logger.error(f"Error handling hotkey: {e}")

