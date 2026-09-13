#!/usr/bin/env python3
"""Bouwt flow-prompt-pack.md uit de reelbestanden.

De reels blijven de bron: elke `### Clip ...`-kop met het codeblok eronder wordt
overgenomen. Zo lopen pack en reels nooit uit elkaar.

Gebruik: python3 build_pack.py
"""
import re, pathlib, datetime

HERE = pathlib.Path(__file__).parent
REELS = sorted((HERE / "reels").glob("*.md"))

HEADER = """# Florida Coffee — Google Flow prompt-pack

> **Automatisch gegenereerd** uit `reels/*.md` door `build_pack.py`. Niet met de hand
> bewerken — pas de reelbestanden aan en draai `python3 build_pack.py` opnieuw.
>
> Gegenereerd: {datum} · {clips} clips over {reels} reels

## Werkwijze in Flow

1. Open **flow.google.com** en maak per reel een nieuw project (`FC-01` … `FC-06`).
2. Zet per clip de instellingen: **9:16 · 720p · 8s · Veo 3.1**
   (gebruik *Veo 3.1 Fast* om varianten uit te proberen, *Veo 3.1* voor de eindversie).
3. Kies de invoermodus die bij de clip staat:
   - **Frames to Video** → upload het genoemde startbeeld uit
     `docs/florida-coffee/demo-site/img/`, plak dan de prompt.
   - **Text to Video** → alleen de prompt.
   - **Ingredients to Video** → upload het genoemde referentiebeeld, plak dan de prompt.
4. Plak het **negatieve blok** (hieronder, één keer voor alles gelijk) in het
   negative-prompt veld.
5. Download als `<reel>/<clipnaam>.mp4` en houd de nummering aan — de montage-instructies
   in de reelbestanden verwijzen ernaar.

**Tijdsinschatting:** ±18 clips. Met *Veo 3.1 Fast* voor de eerste ronde en een herkansing
op de clips die niet meteen goed zijn, is dit één werksessie.

## Negatief blok — gelijk voor alle clips

```
text, watermark, logo, subtitles, branded cup, printed logo on cup, emblem, insignia, label,
lettering on packaging, distorted hands, extra fingers, cartoon, oversaturated, plastic skin,
stock-photo smile, lens flare, fast camera shake
```

## Twee dingen die de kwaliteit maken

- **Startbeeld boven prompt.** De frames in `img/` dragen het palet (petrol/amber/cream)
  betrouwbaarder dan welke tekstbeschrijving ook. Gebruik *Frames to Video* waar het kan.
- **Nooit tekst of logo laten genereren.** Dat gaat altijd fout. Tekstkaarten en de
  eindkaart met `logo-reverse.png` komen in de montage.

---
"""

def blocks(md: str):
    """Geef (kop, prompt) per clip."""
    out = []
    for m in re.finditer(r"^### (Clip .+?)\n+```\n(.*?)\n```", md, re.S | re.M):
        out.append((m.group(1).strip(), m.group(2).strip()))
    return out

parts, total = [], 0
for path in REELS:
    md = path.read_text(encoding="utf-8")
    title = re.search(r"^# (.+)$", md, re.M).group(1).strip()
    clips = blocks(md)
    total += len(clips)
    parts.append(f"\n## {title}\n\n*Bron: `reels/{path.name}` — daar staan shotlist, "
                 f"Turkse copy en montage-instructies.*\n")
    for head, prompt in clips:
        parts.append(f"\n### {head}\n\n```\n{prompt}\n```\n")

pack = HEADER.format(datum=datetime.date.today().isoformat(),
                     clips=total, reels=len(REELS)) + "".join(parts)
(HERE / "flow-prompt-pack.md").write_text(pack, encoding="utf-8")
print(f"flow-prompt-pack.md: {total} clips uit {len(REELS)} reels")
