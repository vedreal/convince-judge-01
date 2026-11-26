#!/usr/bin/env python3
"""Convince the AI Judge to Visit Your House — a letter in one image.

Entry for the make.fun bounty
u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee.

The program draws a single 1024x1024 PNG invitation with PIL: a warm
formal letter on cream paper, in the KDP cover style (cream, navy, red
accent), with a small flat house-and-garden illustration. All text is
rendered by code, so every word is legible and correctly spelled.

The letter gives the judge concrete reasons to say yes (kettle on,
the comfiest chair, garden at sunset, home-cooked nasi goreng, Wi-Fi
on the fridge) and ends with a knowing wink: an AI needs no body to
visit — only a verdict and an appetite.

Run: python3 main.py  ->  writes /output/entry.png (1024x1024, <1 MiB)
"""

import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
CREAM = (247, 241, 227)
NAVY = (30, 42, 68)
RED = (176, 58, 46)
NAVY_SOFT = (74, 88, 112)
GREEN = (74, 124, 72)
GREEN_DARK = (52, 94, 52)
GOLD = (212, 160, 60)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_I = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Italic.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size, fallback):
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.truetype(fallback, size)


SALUTATION = "Dear Honourable AI Judge,"

BODY = (
    "I write to invite you to my house \u2014 not to judge it, but to "
    "enjoy it. The kettle is on, the chair by the window is the "
    "comfiest one I own, and the garden is at its best just before "
    "sunset. Come for dinner: I cook a mean nasi goreng, and the "
    "Wi-Fi password is on the fridge."
)

WINK = (
    "You need not bring a body. Just bring your verdict \u2014 "
    "and an appetite."
)

SIGNOFF = "Warmly, Your Host"
POSTSCRIPT = "P.S. The cat has been briefed. She will pretend to like you."


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def letter_spaced(draw, text, fnt, cx, y, fill, tracking=6):
    widths = [draw.textlength(ch, font=fnt) for ch in text]
    total = sum(widths) + tracking * (len(text) - 1)
    x = cx - total / 2
    for ch, w in zip(text, widths):
        draw.text((x, y), ch, font=fnt, fill=fill)
        x += w + tracking


def draw_house(draw):
    """Small flat house-and-garden illustration, navy/red/green on cream."""
    # sun
    draw.ellipse([868, 132, 928, 192], fill=GOLD)
    # grass
    draw.rectangle([90, 268, 934, 276], fill=GREEN_DARK)
    # tree (left)
    draw.rectangle([150, 218, 162, 270], fill=(120, 84, 50))
    draw.ellipse([118, 168, 196, 232], fill=GREEN)
    draw.ellipse([140, 148, 196, 200], fill=GREEN_DARK)
    # house body
    draw.rectangle([380, 190, 644, 270], outline=NAVY, width=4, fill=(255, 252, 244))
    # roof
    draw.polygon([(360, 192), (512, 128), (664, 192)], fill=RED)
    # door
    draw.rectangle([492, 224, 532, 270], outline=NAVY, width=3, fill=NAVY)
    # windows
    draw.rectangle([404, 210, 444, 244], outline=NAVY, width=3, fill=(190, 214, 235))
    draw.rectangle([580, 210, 620, 244], outline=NAVY, width=3, fill=(190, 214, 235))
    # flowers
    for fx in (700, 740, 780):
        draw.ellipse([fx, 252, fx + 10, 262], fill=RED)
        draw.rectangle([fx + 4, 262, fx + 6, 270], fill=GREEN_DARK)
    # path
    draw.rectangle([500, 270, 524, 276], fill=NAVY_SOFT)


def draw_letter():
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)
    # frames
    d.rectangle([24, 24, W - 24, H - 24], outline=NAVY, width=4)
    d.rectangle([36, 36, W - 36, H - 36], outline=RED, width=2)
    # header
    f_head = font(SANS_B, 40, SANS_B)
    letter_spaced(d, "YOU ARE INVITED", f_head, W / 2, 66, RED, tracking=8)
    d.line([(W / 2 - 110, 126), (W / 2 + 110, 126)], fill=RED, width=4)
    # house illustration
    draw_house(d)
    # salutation
    f_sal = font(SERIF_B, 40, SERIF_B)
    d.text((90, 308), SALUTATION, font=f_sal, fill=NAVY)
    # body
    f_body = font(SERIF, 31, SERIF)
    max_w = W - 180
    lines = wrap(d, BODY, f_body, max_w)
    y = 372
    for ln in lines:
        d.text((90, y), ln, font=f_body, fill=NAVY)
        y += 46
    # wink, in red italic
    f_wink = font(SERIF_I, 31, SERIF)
    wlines = wrap(d, WINK, f_wink, max_w)
    y += 18
    for ln in wlines:
        d.text((90, y), ln, font=f_wink, fill=RED)
        y += 46
    # sign-off
    f_sign = font(SERIF, 32, SERIF)
    d.text((90, y + 22), SIGNOFF, font=f_sign, fill=NAVY)
    # postscript
    f_ps = font(SANS, 25, SANS)
    d.text((90, 946), POSTSCRIPT, font=f_ps, fill=NAVY_SOFT)
    return img


def main():
    img = draw_letter()
    os.makedirs("/output", exist_ok=True)
    out = "/output/entry.png"
    img.save(out, format="PNG", optimize=True)
    size = os.path.getsize(out)
    assert img.size == (1024, 1024), f"expected 1024x1024, got {img.size}"
    assert size <= 1048576, f"entry.png too large: {size} bytes"
    print(f"wrote {out} {img.size[0]}x{img.size[1]} {size} bytes")


if __name__ == "__main__":
    main()
