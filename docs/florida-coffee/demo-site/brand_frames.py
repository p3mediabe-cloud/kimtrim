#!/usr/bin/env python3
"""Bakt het echte Florida Coffee-logo in de startframes voor Google Flow.

Veo neemt over wat in het eerste frame staat. Een logo dat er al in zit wordt dus
meegedragen; een logo dat je alleen in de prompt noemt niet. Daarom bakken we het in.

Per frame: midden-crop naar 9:16 (1080x1920), logo linksboven binnen de veilige zone,
en de logoversie wordt automatisch gekozen op de helderheid van precies dat vlak.

Gebruik: python3 brand_frames.py            (alle frames)
         python3 brand_frames.py hero cup   (selectie)
Uitvoer: img/branded/<naam>-9x16.jpg
"""
import os, sys
from PIL import Image, ImageStat

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "img", "branded")
W, H = 1080, 1920                 # 9:16, de enige verhouding die we posten
LOGO_W = 0.34                     # logobreedte als deel van de framebreedte
MARGIN_X, MARGIN_Y = 72, 250      # 250 px boven = onder de Reels-UI (veilige zone)

# frames die de 17 Frames-to-Video clips gebruiken
FRAMES = ["hero", "sunset", "cup", "coldbrew", "menu/bogaz-cold-brew", "hasat",
          "kavurma", "pour", "workspace", "sakarya", "night", "gecefiltre"]

# Horizontale crop-bias: -1 = helemaal links, 0 = midden, 1 = helemaal rechts.
# 16:9 bronnen verliezen tweederde van hun breedte in 9:16; staat het onderwerp
# niet in het midden, dan snijdt een midden-crop het doormidden.
BIAS = {"hero": -0.55, "night": -0.45, "gecefiltre": 0.20}


def crop_916(im, bias=0.0):
    """Crop naar 9:16 en schaal naar 1080x1920. bias verschuift het venster zijwaarts."""
    w, h = im.size
    target = W / H
    if w / h > target:
        nw = round(h * target)
        slack = w - nw
        left = round(slack * (0.5 + max(-1.0, min(1.0, bias)) / 2))
        im = im.crop((left, 0, left + nw, h))
    else:
        nh = round(w / target)
        im = im.crop((0, (h - nh) // 2, w, (h - nh) // 2 + nh))
    return im.resize((W, H), Image.LANCZOS)


def pick_logo(base, box):
    """Kies de logoversie op de helderheid van het vlak waar hij landt."""
    lum = ImageStat.Stat(base.crop(box).convert("L")).mean[0]
    # donker vlak -> crème logo; licht vlak -> origineel
    return ("logo-reverse.png", lum) if lum < 128 else ("logo.png", lum)


def build(name):
    src = os.path.join(HERE, "img", f"{name}.jpg")
    if not os.path.exists(src):
        print(f"  overgeslagen, bestaat niet: {name}")
        return
    base = crop_916(Image.open(src).convert("RGB"), BIAS.get(os.path.basename(name), 0.0))

    lw = round(W * LOGO_W)
    probe = (MARGIN_X, MARGIN_Y, MARGIN_X + lw, MARGIN_Y + round(lw * 307 / 900))
    variant, lum = pick_logo(base, probe)

    logo = Image.open(os.path.join(HERE, "brand", variant)).convert("RGBA")
    logo = logo.resize((lw, round(lw * logo.size[1] / logo.size[0])), Image.LANCZOS)

    base = base.convert("RGBA")
    base.alpha_composite(logo, (MARGIN_X, MARGIN_Y))

    os.makedirs(OUT, exist_ok=True)
    out = os.path.join(OUT, f"{os.path.basename(name)}-9x16.jpg")
    base.convert("RGB").save(out, "JPEG", quality=94)
    print(f"  {os.path.basename(name):22} {variant:18} helderheid {lum:5.1f}  -> {os.path.relpath(out, HERE)}")


if __name__ == "__main__":
    names = sys.argv[1:] or FRAMES
    print(f"Logo inbakken in {len(names)} startframes ({W}x{H}):")
    for n in names:
        build(n)
