import os
import sys
from pathlib import Path
from PIL import Image, ImageDraw

def resource_path(relative_path: str) -> Path:
    """Get absolute path to resource, works for dev and for PyInstaller"""
    if getattr(sys, "frozen", False):
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base = Path(sys._MEIPASS)
    else:
        # Normal execution
        base = Path(__file__).resolve().parent.parent.parent

    return base / relative_path

def get_app_dir() -> Path:
    """Get the directory where the app data (config, logs) is stored."""
    # Use %LOCALAPPDATA%\ChatBridge to avoid polluting Desktop or Program Files
    app_dir = Path(os.getenv("LOCALAPPDATA", Path.home() / "AppData" / "Local")) / "ChatBridge"
    app_dir.mkdir(parents=True, exist_ok=True)
    return app_dir

def create_icon_image(color: str = "#22c55e") -> Image.Image:
    """Create a simple circular icon programmatically."""
    size = 64
    image = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    # Outer circle
    draw.ellipse([4, 4, size - 4, size - 4], fill=color)
    # Inner decoration
    draw.ellipse([14, 14, size - 14, size - 14], fill="#ffffff")
    draw.ellipse([22, 22, size - 22, size - 22], fill=color)
    return image

def load_icon() -> Image.Image:
    """Load icon.ico from assets/ or fall back to generated icon."""
    ico_path = resource_path("assets/icon.ico")
    if ico_path.exists():
        return Image.open(ico_path)
    return create_icon_image("#22c55e")
