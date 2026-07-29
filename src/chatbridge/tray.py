import os
import sys
import subprocess
import threading
import platform
import webbrowser

import pystray
from PIL import Image

from chatbridge.logger import logger
from chatbridge.version import __version__
from chatbridge.resources import load_icon, create_icon_image


def _open_file_in_editor(path: str) -> None:
    """Open a file with the default text editor (Notepad on Windows)."""
    abs_path = os.path.abspath(path)
    if not os.path.exists(abs_path):
        # Create file if it doesn't exist yet
        os.makedirs(os.path.dirname(abs_path), exist_ok=True)
        open(abs_path, "a", encoding="utf-8").close()
    if platform.system() == "Windows":
        subprocess.Popen(["notepad.exe", abs_path])
    else:
        subprocess.Popen(["xdg-open", abs_path])


class TrayApp:
    def __init__(self, translator, hotkey_key: str, on_hotkey_changed=None):
        self._translator = translator
        self._hotkey_key = hotkey_key
        self.on_hotkey_changed = on_hotkey_changed
        self._enabled = True  # Translator starts enabled
        self._icon: pystray.Icon | None = None
        self._settings_window_open = False

    # ------------------------------------------------------------------ #
    #  Public API                                                          #
    # ------------------------------------------------------------------ #

    def run(self, hotkey_thread: threading.Thread) -> None:
        """Start the system tray (blocks until Exit is chosen)."""
        self._hotkey_thread = hotkey_thread
        self._icon = pystray.Icon(
            "ChatBridge",
            load_icon(),
            "ChatBridge",
            menu=self._build_menu(),
        )
        self._icon.run()

    # ------------------------------------------------------------------ #
    #  Menu construction                                                   #
    # ------------------------------------------------------------------ #

    def _build_menu(self) -> pystray.Menu:
        return pystray.Menu(
            # Header (read-only title)
            pystray.MenuItem(
                f"ChatBridge v{__version__}",
                action=None,
                enabled=False,
            ),
            pystray.Menu.SEPARATOR,
            # Toggle status
            pystray.MenuItem(
                "Enabled",
                self._toggle_enabled,
                checked=lambda item: self._enabled,
                radio=False,
            ),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Settings...", self._open_settings),
            pystray.MenuItem("Open Logs", self._open_logs),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("About", self._show_about),
            pystray.MenuItem("Exit", self._exit),
        )

    # ------------------------------------------------------------------ #
    #  Menu actions                                                        #
    # ------------------------------------------------------------------ #

    def _toggle_enabled(self, icon, item) -> None:
        self._enabled = not self._enabled
        state = "Enabled" if self._enabled else "Disabled"
        logger.info(f"Translator {state}")
        # Update icon colour to reflect state
        icon.icon = load_icon() if self._enabled else create_icon_image("#ef4444")
        icon.update_menu()

    def _open_settings(self, icon, item) -> None:
        if self._settings_window_open:
            return  # Prevent opening multiple instances
            
        def launch_settings():
            self._settings_window_open = True
            from chatbridge.settings import SettingsWindow
            app = SettingsWindow(on_save_callback=self._on_settings_saved)
            app.run()
            self._settings_window_open = False
            
        threading.Thread(target=launch_settings, daemon=True).start()

    def _on_settings_saved(self, new_config: dict) -> None:
        """Callback fired when user clicks Save in SettingsWindow."""
        # 1. Update translator target language dynamically
        if hasattr(self._translator, "default_target"):
            self._translator.default_target = new_config.get("target_lang", "en")
            
        # 2. Update hotkey if callback provided
        new_hotkey = new_config.get("hotkey", "F8")
        if new_hotkey != self._hotkey_key:
            self._hotkey_key = new_hotkey
            if self.on_hotkey_changed:
                self.on_hotkey_changed(new_hotkey)

    def _open_logs(self, icon, item) -> None:
        from chatbridge.resources import get_app_dir
        log_path = get_app_dir() / "logs" / "app.log"
        _open_file_in_editor(str(log_path))

    def _show_about(self, icon, item) -> None:
        import tkinter as tk
        from tkinter import messagebox
        root = tk.Tk()
        root.withdraw()  # Hide the root window
        
        # ถามผู้ใช้เพื่อให้คลิกปุ่ม OK
        response = messagebox.askokcancel(
            "About ChatBridge",
            f"ChatBridge\nVersion {__version__}\nMIT License\nGitHub: https://github.com/Beabexj/ChatBridge\n\nClick OK to open GitHub page.",
        )
        if response:
            webbrowser.open("https://github.com/Beabexj/ChatBridge")
        root.destroy()

    def _exit(self, icon, item) -> None:
        logger.info("Shutting down ChatBridge...")
        # Stop icon first
        icon.stop()

    # ------------------------------------------------------------------ #
    #  Left-click default action                                           #
    # ------------------------------------------------------------------ #

    def handle_click(self) -> None:
        """Toggle enable/disable when user left-clicks the tray icon."""
        self._enabled = not self._enabled
        state = "Enabled" if self._enabled else "Disabled"
        logger.info(f"Translator {state} (via left-click)")
        if self._icon:
            self._icon.icon = load_icon() if self._enabled else create_icon_image("#ef4444")
            self._icon.update_menu()

    @property
    def is_enabled(self) -> bool:
        return self._enabled
