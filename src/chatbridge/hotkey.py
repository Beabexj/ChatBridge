import time
import pyperclip
import pyautogui
from chatbridge.logger import logger

# ป้องกันโปรแกรมแครชถ้าวางเมาส์ไว้มุมจอใน VM
pyautogui.FAILSAFE = False

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
        # 1. แบ็คอัปข้อความใน clipboard เดิม
        old_clipboard = pyperclip.paste()
        
        # 2. ล้าง clipboard เพื่อเช็คว่ามีการคลุมดำข้อความไว้หรือไม่
        pyperclip.copy('')
        time.sleep(0.05)

        # 3. ลองก๊อปปี้สิ่งที่คลุมดำอยู่
        pyautogui.hotkey("ctrl", "c")
        time.sleep(0.1)

        text = pyperclip.paste().strip()
        replace_all = False

        # 4. ถ้าไม่มีข้อความเข้ามา แปลว่าผู้ใช้ไม่ได้คลุมดำไว้ -> ทำการ Select All (Ctrl+A) ให้เอง
        if not text:
            logger.debug("No text highlighted. Falling back to select all (ctrl+a).")
            pyautogui.hotkey("ctrl", "a")
            time.sleep(0.05)
            pyautogui.hotkey("ctrl", "c")
            time.sleep(0.1)
            
            text = pyperclip.paste().strip()
            replace_all = True # จดจำไว้ว่าตอนวางต้องคลุมดำทั้งหมดเพื่อวางทับ

        if not text:
            # ถ้ายังไม่มีข้อความอีก คืนค่า clipboard เดิม
            if old_clipboard:
                pyperclip.copy(old_clipboard)
            return

        logger.info(f"Original: {text}")

        result = translator.translate(text)

        if result.success:
            logger.info(f"Translated: {result.text}")

            # วางข้อความใหม่
            pyperclip.copy(result.text)
            time.sleep(0.1) 
            
            if replace_all:
                # ถ้าตอนแรกเรา select all ตอนวางก็ต้อง select all อีกรอบเพื่อทับของเดิม
                pyautogui.hotkey("ctrl", "a")
                time.sleep(0.05)
                
            pyautogui.hotkey("ctrl", "v")
            time.sleep(0.05)
            
            # ถ้าตั้งค่า auto_send ให้กด Enter ด้วย
            try:
                from chatbridge.config import load_config
                config = load_config()
                if config.get("auto_send", False):
                    pyautogui.press("enter")
            except Exception as e:
                logger.error(f"Error reading auto_send config: {e}")
                
        else:
            logger.error(f"Failed to translate: {result.error}")
            if old_clipboard:
                pyperclip.copy(old_clipboard)

    except Exception as e:
        logger.error(f"Error handling hotkey: {e}")

