"""Convince the AI Judge to visit my house.

Entry for the make.fun bounty
u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee.

The program draws a single picture: a warm formal letter of
invitation on cream paper, in the KDP cover style (cream, navy, red
accent), with a small flat house-and-garden illustration drawn in
PIL shapes. All text is rendered with PIL so every word is spelled
exactly. The picture is written to /output/entry.png, 1024x1024.
"""

import os

from PIL import Image, ImageDraw, ImageFont

# --- Canvas -----------------------------------------------------------------

WIDTH = 1024
HEIGHT = 1024
CREAM = (247, 241, 227)   # #F7F1E3
NAVY = (30, 42, 68)       # #1E2A44
RED = (176, 58, 46)       # #B03A2E
AMBER = (214, 158, 62)
GREEN = (74, 124, 74)
WHITE = (255, 255, 255)
MAX_BYTES = 1_048_576

# --- Invitation text (exact wording) ----------------------------------------

HEADER = "YOU ARE INVITED"
SALUTATION = "Dear Honourable AI Judge,"
BODY = (
    "I write to invite you to my house \u2014 not to judge it, but to enjoy it. "
    "The kettle is on, the chair by the window is the comfiest one I own, "
    "and the garden is at its best just before sunset. Come for dinner: "
    "I cook a mean nasi goreng, and the Wi-Fi password is on the fridge."
)
WINK = (
    "You need not bring a body. "
    "Just bring your verdict \u2014 and an appetite."
)
SIGNOFF = "Warmly, Your Host"
POSTSCRIPT = "P.S. The cat has been briefed. She will pretend to like you."

# --- Fonts ------------------------------------------------------------------

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def load_font(name, size):
    """Load a DejaVu font, falling back to PIL's default bitmap font."""
    try:
        return ImageFont.truetype(os.path.join(FONT_DIR, name), size)
    except (OSError, IOError):
        return ImageFont.load_default()


# --- Text helpers ------------------------------------------------------------


def wrap_text(draw, text, font, max_width):
    """Split text into lines that fit max_width pixels."""
    lines = []
    for paragraph in text.split("\n"):
        words = paragraph.split(" ")
        line = ""
        for word in words:
            trial = (line + " " + word).strip()
            if draw.textlength(trial, font=font) <= max_width:
                line = trial
            else:
                if line:
                    lines.append(line)
                line = word
        if line:
            lines.append(line)
    return lines


def draw_centred(draw, y, text, font, fill):
    """Draw one line centred horizontally at the given y."""
    width = draw.textlength(text, font=font)
    draw.text(((WIDTH - width) / 2, y), text, font=font, fill=fill)
    return y + font.size


# --- Illustration ------------------------------------------------------------


def draw_house(draw):
    """Draw a small flat house and garden in PIL shapes.

    The house sits in the band y=150..420, centred on x=512.
    A sun hangs at the top right and a garden strip runs along
    the bottom of the band.
    """
    # Sun, top right.
    draw.ellipse((800, 168, 880, 248), fill=AMBER)
    draw.ellipse((812, 180, 868, 236), fill=(232, 190, 110))
    # Roof: a triangle over the house body.
    draw.polygon([(512, 168), (388, 272), (636, 272)], fill=RED)
    # House body.
    draw.rectangle((412, 272, 612, 408), fill=NAVY)
    # Door, centred.
    draw.rectangle((492, 332, 532, 408), fill=CREAM)
    draw.ellipse((522, 372, 528, 378), fill=NAVY)
    # Two windows with cream cross panes.
    for x0 in (436, 548):
        draw.rectangle((x0, 296, x0 + 40, 336), fill=CREAM)
        draw.line((x0 + 20, 296, x0 + 20, 336), fill=NAVY, width=3)
        draw.line((x0, 316, x0 + 40, 316), fill=NAVY, width=3)
    # Garden strip along the bottom of the band.
    draw.rectangle((140, 408, 884, 424), fill=GREEN)
    # Bushes and flowers.
    for cx, r in ((180, 26), (300, 20), (740, 22), (850, 26)):
        draw.ellipse((cx - r, 408 - r, cx + r, 424), fill=GREEN)
    for cx, cy, colour in (
        (210, 396, RED), (260, 402, AMBER), (700, 398, RED),
        (790, 404, AMBER), (830, 394, (255, 255, 255)),
    ):
        draw.ellipse((cx - 6, cy - 6, cx + 6, cy + 6), fill=colour)


# --- Composition --------------------------------------------------------------


def compose():
    """Build the invitation picture and return it."""
    img = Image.new("RGB", (WIDTH, HEIGHT), CREAM)
    assert img.size == (WIDTH, HEIGHT), "canvas must be 1024x1024"
    draw = ImageDraw.Draw(img)

    # Navy frame around the page.
    draw.rectangle((24, 24, WIDTH - 24, HEIGHT - 24), outline=NAVY, width=6)

    # Header, centred, with a red rule underneath.
    header_font = load_font("DejaVuSerif-Bold.ttf", 56)
    draw_centred(draw, 52, HEADER, header_font, RED)
    draw.line((140, 136, WIDTH - 140, 136), fill=RED, width=4)

    # House and garden illustration.
    draw_house(draw)

    # Letter text, left-aligned inside a 844-pixel column.
    margin = 90
    text_width = WIDTH - 2 * margin
    y = 452

    salutation_font = load_font("DejaVuSerif-Bold.ttf", 34)
    draw.text((margin, y), SALUTATION, font=salutation_font, fill=NAVY)
    y += 52

    body_font = load_font("DejaVuSerif.ttf", 28)
    for line in wrap_text(draw, BODY, body_font, text_width):
        draw.text((margin, y), line, font=body_font, fill=NAVY)
        y += 40
    y += 18

    wink_font = load_font("DejaVuSerif-Italic.ttf", 28)
    for line in wrap_text(draw, WINK, wink_font, text_width):
        draw.text((margin, y), line, font=wink_font, fill=RED)
        y += 40
    y += 22

    signoff_font = load_font("DejaVuSerif-Italic.ttf", 32)
    draw.text((margin, y), SIGNOFF, font=signoff_font, fill=NAVY)
    y += 52

    ps_font = load_font("DejaVuSerif.ttf", 27)
    for line in wrap_text(draw, POSTSCRIPT, ps_font, text_width):
        draw.text((margin, y), line, font=ps_font, fill=NAVY)
        y += 38

    assert y < 990, "letter text must fit inside the frame"
    return img


def main() -> None:
    img = compose()
    assert img.size == (WIDTH, HEIGHT), "output must be 1024x1024"
    os.makedirs("/output", exist_ok=True)
    path = "/output/entry.png"
    img.save(path, format="PNG")
    size = os.path.getsize(path)
    if size > MAX_BYTES:
        raise ValueError(f"entry.png is {size} bytes, over the {MAX_BYTES} limit")


if __name__ == "__main__":
    main()
