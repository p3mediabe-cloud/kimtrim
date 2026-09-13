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
import os, sys, math
from PIL import Image, ImageStat, ImageEnhance

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

# Logo op de beker. Per kader een lijst plaatsingen, gemeten als percentage van
# het 1080x1920 kader: (midden-x, midden-y, breedte, rotatie, variant).
# De bekers dragen al een losse toekan; de plaatsing valt daar bovenop, zodat er
# één merkteken staat met de naam erbij in plaats van alleen een icoon.
# Kaders zonder plaatsing (hasat, kavurma, workspace, sakarya, bogaz-cold-brew)
# hebben een te kleine, half verdekte of al door de toekan gevulde beker; een
# woordmerk wordt daar pap of botst met wat er staat.
CUPS = {
  # kader:            [(midden-x%, midden-y%, breedte%, rotatie, variant)]
  "hero":            [(59.5, 57.5, 40.0, 0.0, "logo.png")],
  "cup":             [(54.0, 68.5, 48.0, 0.0, "logo-reverse.png")],
  "coldbrew":        [(85.0, 79.5, 18.0, 0.0, "logo-reverse.png")],
  "pour":            [(60.0, 76.5, 32.0, 0.0, "logo.png")],
  "night":           [(64.0, 84.5, 24.0, 0.0, "logo-reverse.png")],
  "gecefiltre":      [(63.0, 76.0, 16.0, 0.0, "logo-reverse.png")],
  "sunset":          [(39.5, 66.5, 11.0, 0.0, "logo.png"),
                      (69.5, 66.5, 11.0, 0.0, "logo.png")],
}
CYL_THETA = 0.62   # halve wikkelhoek: hoever het logo om de beker loopt
CYL_BOW   = 0.05   # hoeveel de randen meezakken met de welving


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


def cylinder(logo, theta=CYL_THETA, bow=CYL_BOW):
    """Buigt het logo om een denkbeeldige cilinder, zodat het op de beker gedrukt
    lijkt in plaats van erop geplakt. Randen lopen samen en zakken iets weg."""
    w, h = logo.size
    out = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    st, ct = math.sin(theta), math.cos(theta)
    for x in range(w):
        u = (x / (w - 1) - 0.5) * 2
        phi = math.asin(max(-1.0, min(1.0, u * st)))
        sx = min(w - 1, max(0, int(round(((phi / theta) / 2 + 0.5) * (w - 1)))))
        k = math.cos(phi)                       # 1 in het midden, kleiner aan de rand
        nh = max(1, int(round(h * (0.93 + 0.07 * k))))
        col = logo.crop((sx, 0, sx + 1, h)).resize((1, nh), Image.LANCZOS)
        dy = int(round((h - nh) / 2 + bow * h * (1 - k) / max(1e-6, 1 - ct)))
        out.paste(col, (x, dy))
    return out


def stamp_cups(base, name):
    """Drukt het logo op de bekers, met de schaduw van de beker eroverheen."""
    for cx, cy, cw, rot, variant in CUPS.get(name, []):
        lw = round(W * cw / 100)
        logo = Image.open(os.path.join(HERE, "brand", variant)).convert("RGBA")
        logo = logo.resize((lw, round(lw * logo.size[1] / logo.size[0])), Image.LANCZOS)
        logo = cylinder(logo)
        if rot:
            logo = logo.rotate(rot, resample=Image.BICUBIC, expand=True)

        lh = logo.size[1]
        px, py = round(W * cx / 100 - lw / 2), round(H * cy / 100 - lh / 2)

        # licht van de beker overnemen: waar de beker donkerder is, dempt het logo mee
        patch = base.crop((px, py, px + lw, py + lh)).convert("L")
        mean = ImageStat.Stat(patch).mean[0] or 1
        logo = ImageEnhance.Brightness(logo).enhance(min(1.12, max(0.72, mean / 190 + 0.28)))

        a = logo.split()[3].point(lambda v: int(v * 0.94))
        logo.putalpha(a)
        base.alpha_composite(logo, (px, py))
    return base


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
    base = stamp_cups(base, os.path.basename(name))

    os.makedirs(OUT, exist_ok=True)
    out = os.path.join(OUT, f"{os.path.basename(name)}-9x16.jpg")
    base.convert("RGB").save(out, "JPEG", quality=94)
    print(f"  {os.path.basename(name):22} {variant:18} helderheid {lum:5.1f}  -> {os.path.relpath(out, HERE)}")


if __name__ == "__main__":
    names = sys.argv[1:] or FRAMES
    print(f"Logo inbakken in {len(names)} startframes ({W}x{H}):")
    for n in names:
        build(n)
