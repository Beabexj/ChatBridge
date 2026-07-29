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
        t0 = time.perf_counter()
        
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

        t_selection = time.perf_counter()
        selection_ms = (t_selection - t0) * 1000

        if not text:
            # ถ้ายังไม่มีข้อความอีก คืนค่า clipboard เดิม
            if old_clipboard:
                pyperclip.copy(old_clipboard)
            return

        logger.info(f"Original: {text}")

        # --- Translation Phase ---
        result = translator.translate(text)
        t_translate = time.perf_counter()
        translate_ms = (t_translate - t_selection) * 1000

        if result.success:
            logger.info(f"Translated: {result.text}")

            # --- Paste Phase ---
            pyperclip.copy(result.text)
            time.sleep(0.1) 
            
            if replace_all:
                # ถ้าตอนแรกเรา select all ตอนวางก็ต้อง select all อีกรอบเพื่อทับของเดิม
                pyautogui.hotkey("ctrl", "a")
                time.sleep(0.05)
                
            pyautogui.hotkey("ctrl", "v")
            time.sleep(0.05)
            
            t_paste = time.perf_counter()
            paste_ms = (t_paste - t_translate) * 1000
            
            # --- Auto Send Phase ---
            try:
                from chatbridge.config import load_config
                config = load_config()
                if config.get("auto_send", False):
                    pyautogui.press("enter")
            except Exception as e:
                logger.error(f"Error reading auto_send config: {e}")
            
            t_send = time.perf_counter()
            send_ms = (t_send - t_paste) * 1000
            
            total_ms = (t_send - t0) * 1000
            
            # Log performance metrics
            perf_log = (
                f"\n[PERF]\n"
                f"Selection : {selection_ms:.0f} ms\n"
                f"Copy      : (Included in Selection)\n"
                f"Translate : {translate_ms:.0f} ms\n"
                f"Paste     : {paste_ms:.0f} ms\n"
                f"Auto Send : {send_ms:.0f} ms\n"
                f"Total     : {total_ms:.0f} ms"
            )
            logger.info(perf_log)
                
        else:
            logger.error(f"Failed to translate: {result.error}")
            if old_clipboard:
                pyperclip.copy(old_clipboard)

    except Exception as e:
        logger.error(f"Error handling hotkey: {e}")

