import io
from typing import Tuple
from PIL import Image, ImageDraw, ImageFont

BG = (12, 14, 23)     # #0C0E17
BG2 = (36, 30, 78)    # #241E4E
TEXT = (234, 232, 227)  # #EAE8E3
ACCENT = (156, 140, 242)  # #9C8CF2

def _load_font(size: int):
    for path in [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    ]:
        try:
            return ImageFont.truetype(path, size=size)
        except Exception:
            continue
    return ImageFont.load_default()

def _gradient_background(w: int, h: int):
    base = Image.new("RGB", (w, h), BG)
    top = Image.new("RGB", (w, h), BG2)
    mask = Image.linear_gradient("L").resize((w, h))
    return Image.composite(top, base, mask)

def _wrap(draw, text, font, max_width):
    words = text.split()
    line, lines = "", []
    for w in words:
        test = (line + " " + w).strip()
        if draw.textlength(test, font=font) <= max_width:
            line = test
        else:
            lines.append(line)
            line = w
    if line:
        lines.append(line)
    return lines

def make_share_card(text: str, size: Tuple[int, int]=(1080, 1350)) -> bytes:
    w, h = size
    img = _gradient_background(w, h)
    draw = ImageDraw.Draw(img)

    title_font = _load_font(52)
    body_font = _load_font(44)
    tag_font = _load_font(28)

    margin = 90
    draw.text((margin, 70), "MuseMate Daily Spark", font=title_font, fill=TEXT)

    lines = _wrap(draw, text.strip() or "Your spark goes here.", body_font, w - 2*margin)
    y = 220
    for ln in lines:
        draw.text((margin, y), ln, font=body_font, fill=TEXT)
        y += 60

    footer = "MuseMate Lite • Fellowship Edition"
    draw.text((margin, h - 120), footer, font=tag_font, fill=ACCENT)

    bio = io.BytesIO()
    img.save(bio, format="PNG")
    bio.seek(0)
    return bio.getvalue()
