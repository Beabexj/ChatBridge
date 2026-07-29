import sys
import threading
import keyboard

from chatbridge.config import load_config
from chatbridge.translator import ChatTranslator
from chatbridge.hotkey import handle_hotkey
from chatbridge.logger import logger
from chatbridge.version import __version__
from chatbridge.tray import TrayApp


def _start_hotkey_listener(hotkey_key: str, translator, tray_app: TrayApp) -> None:
    """Register the global hotkey and block until keyboard library exits."""
    keyboard.add_hotkey(
        hotkey_key,
        lambda: handle_hotkey(translator, tray_app),
    )
    keyboard.wait()  # Blocks this thread


def reload_hotkey(new_hotkey: str, translator, tray_app: TrayApp):
    """Update the hotkey dynamically."""
    logger.info(f"Changing hotkey to: {new_hotkey}")
    try:
        keyboard.unhook_all()
        keyboard.add_hotkey(
            new_hotkey,
            lambda: handle_hotkey(translator, tray_app),
        )
        logger.info("Hotkey updated successfully.")
    except Exception as e:
        logger.error(f"Failed to update hotkey: {e}")


def main() -> None:
    # โหลด config
    config = load_config()
    source_lang = config.get("source_lang", "th")
    target_lang = config.get("target_lang", "en")
    hotkey_key = config.get("hotkey", "F8")

    # สร้างตัวแปลภาษา
    translator = ChatTranslator(default_source=source_lang, default_target=target_lang)

    logger.info(f"ChatBridge v{__version__} Initialized")
    logger.info(f"[{hotkey_key}] = Auto-Translate (Thai<->Eng/Jap->Eng)")

    # สร้าง TrayApp พร้อมรับ callback เมื่อ hotkey เปลี่ยน
    tray_app = TrayApp(
        translator=translator, 
        hotkey_key=hotkey_key,
        on_hotkey_changed=lambda new_key: reload_hotkey(new_key, translator, tray_app)
    )

    # รัน Hotkey Listener บน Background Thread
    hotkey_thread = threading.Thread(
        target=_start_hotkey_listener,
        args=(hotkey_key, translator, tray_app),
        daemon=True,  # Thread will die when main thread exits
        name="HotkeyListener",
    )
    hotkey_thread.start()
    logger.info("Hotkey listener started on background thread.")

    # รัน System Tray บน Main Thread (pystray ต้องการ Main Thread)
    logger.info("Starting system tray...")
    tray_app.run(hotkey_thread)

    # เมื่อ tray ปิด (Exit ถูกกด) -> cleanup keyboard และ exit
    keyboard.unhook_all()
    logger.info("ChatBridge exited cleanly.")
    sys.exit(0)


if __name__ == "__main__":
    main()