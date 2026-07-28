import os
import sys
import subprocess
import threading
import platform

import pystray
from PIL import Image, ImageDraw

from chatbridge.logger import logger
from chatbridge.version import __version__


def _create_icon_image(color: str = "#22c55e") -> Image.Image:
    """Create a simple circular icon programmatically."""
    size = 64
    image = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    # Outer circle (colored fill)
    draw.ellipse([4, 4, size - 4, size - 4], fill=color)
    # Inner "C" shape hint: a white ring
    draw.ellipse([14, 14, size - 14, size - 14], fill="#ffffff")
    draw.ellipse([22, 22, size - 22, size - 22], fill=color)
    return image


def _load_icon() -> Image.Image:
    """Load icon.ico from assets/ or fall back to generated icon."""
    ico_path = os.path.join(
        os.path.dirname(__file__), "..", "..", "assets", "icon.ico"
    )
    if os.path.exists(ico_path):
        return Image.open(ico_path)
    return _create_icon_image("#22c55e")


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
    def __init__(self, translator, hotkey_key: str):
        self._translator = translator
        self._hotkey_key = hotkey_key
        self._enabled = True  # Translator starts enabled
        self._icon: pystray.Icon | None = None

    # ------------------------------------------------------------------ #
    #  Public API                                                          #
    # ------------------------------------------------------------------ #

    def run(self, hotkey_thread: threading.Thread) -> None:
        """Start the system tray (blocks until Exit is chosen)."""
        self._hotkey_thread = hotkey_thread
        self._icon = pystray.Icon(
            "ChatBridge",
            _load_icon(),
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
                f"ChatBridge  v{__version__}",
                action=None,
                enabled=False,
            ),
            pystray.Menu.SEPARATOR,
            # Toggle status
            pystray.MenuItem(
                "Status",
                pystray.Menu(
                    pystray.MenuItem(
                        "Enabled",
                        self._toggle_enabled,
                        checked=lambda item: self._enabled,
                        radio=False,
                    )
                ),
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
        icon.icon = _load_icon() if self._enabled else _create_icon_image("#ef4444")
        icon.update_menu()

    def _open_settings(self, icon, item) -> None:
        _open_file_in_editor("config.json")

    def _open_logs(self, icon, item) -> None:
        _open_file_in_editor(os.path.join("logs", "app.log"))

    def _show_about(self, icon, item) -> None:
        import tkinter as tk
        from tkinter import messagebox
        root = tk.Tk()
        root.withdraw()  # Hide the root window
        messagebox.showinfo(
            "About ChatBridge",
            f"ChatBridge  v{__version__}\n\nTranslate game chat with one hotkey.\n\nPython {sys.version.split()[0]}",
        )
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
            self._icon.icon = _load_icon() if self._enabled else _create_icon_image("#ef4444")
            self._icon.update_menu()

    @property
    def is_enabled(self) -> bool:
        return self._enabled
