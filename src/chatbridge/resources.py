import os
from PIL import Image, ImageDraw

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
    ico_path = os.path.join(
        os.path.dirname(__file__), "..", "..", "assets", "icon.ico"
    )
    if os.path.exists(ico_path):
        return Image.open(ico_path)
    return create_icon_image("#22c55e")
