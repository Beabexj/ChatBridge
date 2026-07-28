import time
import keyboard
import pyautogui
import pyperclip
from deep_translator import GoogleTranslator

translator = GoogleTranslator(source="th", target="en")

def translate_chat():
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

        print("Original:", text)

        translated = translator.translate(text)

        print("Translated:", translated)

        # วางข้อความใหม่
        pyperclip.copy(translated)

        pyautogui.hotkey("ctrl", "a")
        time.sleep(0.05)

        pyautogui.hotkey("ctrl", "v")

    except Exception as e:
        print(e)

print("F8 = Translate Thai -> English")
keyboard.add_hotkey("F8", translate_chat)

keyboard.wait()