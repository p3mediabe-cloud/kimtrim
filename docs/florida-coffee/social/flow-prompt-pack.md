# Florida Coffee — Google Flow prompt-pack

> **Automatisch gegenereerd** uit `reels/*.md` door `build_pack.py`. Niet met de hand
> bewerken — pas de reelbestanden aan en draai `python3 build_pack.py` opnieuw.
>
> Gegenereerd: 2026-09-13 · 18 clips over 6 reels

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

## Reel 01 — "Boğaz'da Sabah 7"

*Bron: `reels/01-bogazda-sabah-7.md` — daar staan shotlist, Turkse copy en montage-instructies.*

### Clip 1 — `01-haak` · startbeeld `img/hero.jpg`

```
Static shot with the faintest micro-drift on a cream takeaway cup with a deep teal band,
resting on a weathered wooden terrace rail high above the Bosphorus. Steam curls slowly
upward and catches the low sun. Far below, water glitters; a ferry sits small on the horizon.
A linen napkin lifts slightly in the breeze. Golden hour backlight, warm haze, calm and still.
Brand: Florida Coffee, Istanbul. Palette petrol teal #004854, amber #F09C1C, rust #D44808, cream.
One continuous shot, no cuts, no scene changes, loopable. Photoreal, cinematic, natural light,
shallow depth of field, no text, no logos, no captions, no talking, no people looking at camera.
Compose for 9:16 vertical with the top-left corner kept quiet and free of key detail or moving
highlights — reserved space for a logo composited in post. Every cup, glass, package and surface is
plain and unbranded: no printed marks, emblems, lettering or labels anywhere in frame.
Ambient only: distant ferry horn, soft water, faint gulls — no voices, no music.
```

### Clip 2 — `02-moment` · startbeeld `img/sunset.jpg`

```
Slow lateral dolly to the right along a terrace rail overlooking the Bosphorus at golden hour.
A ferry drifts across the frame in the far distance, its wake catching amber light. The water
surface glitters with thousands of small highlights. Foreground rail stays softly out of focus.
Serene, unhurried, premium.
Brand: Florida Coffee, Istanbul. Palette petrol teal #004854, amber #F09C1C, rust #D44808, cream.
One continuous shot, no cuts, no scene changes, loopable. Photoreal, cinematic, natural light,
shallow depth of field, no text, no logos, no captions, no talking, no people looking at camera.
Compose for 9:16 vertical with the top-left corner kept quiet and free of key detail or moving
highlights — reserved space for a logo composited in post. Every cup, glass, package and surface is
plain and unbranded: no printed marks, emblems, lettering or labels anywhere in frame.
Ambient only: distant ferry horn, soft lapping water — no voices, no music.
```

### Clip 3 — `03-landing` · startbeeld `img/cup.jpg`

```
Static macro shot, shallow depth of field: a hand enters frame from the right and lifts a cream
cup with a teal band off a wooden rail, then leaves frame. Behind it the Bosphorus glows out of
focus in warm amber bokeh. Only the hand and forearm are visible, no face.
Brand: Florida Coffee, Istanbul. Palette petrol teal #004854, amber #F09C1C, rust #D44808, cream.
One continuous shot, no cuts, no scene changes, loopable. Photoreal, cinematic, natural light,
shallow depth of field, no text, no logos, no captions, no talking, no people looking at camera.
Compose for 9:16 vertical with the top-left corner kept quiet and free of key detail or moving
highlights — reserved space for a logo composited in post. Every cup, glass, package and surface is
plain and unbranded: no printed marks, emblems, lettering or labels anywhere in frame.
Ambient only: soft ceramic on wood, distant city murmur — no voices, no music.
```

## Reel 02 — "18 Saat"

*Bron: `reels/02-18-saat-cold-brew.md` — daar staan shotlist, Turkse copy en montage-instructies.*

### Clip 1 — `01-damla` · startbeeld `img/coldbrew.jpg`

```
Extreme macro, static camera: a single dark coffee droplet forms at the tip of a glass cold-brew
tower valve, hangs, then falls and breaks the surface of clear water below, sending one slow
ripple outward. Amber rim light from the left, deep teal tiled wall far out of focus behind.
Very slow, meditative, high detail on the glass and the droplet.
Brand: Florida Coffee, Istanbul. Palette petrol teal #004854, amber #F09C1C, rust #D44808, cream.
One continuous shot, no cuts, no scene changes, loopable. Photoreal, cinematic, natural light,
shallow depth of field, no text, no logos, no captions, no talking, no people looking at camera.
Compose for 9:16 vertical with the top-left corner kept quiet and free of key detail or moving
highlights — reserved space for a logo composited in post. Every cup, glass, package and surface is
plain and unbranded: no printed marks, emblems, lettering or labels anywhere in frame.
Ambient only: a single soft drip, faint room tone — no voices, no music.
```

### Clip 2 — `02-ekstraksiyon` · startbeeld `img/coldbrew.jpg`

```
Slow push-in on a tall glass vessel: dark coffee tendrils curl and bloom downward through clear
cold water like ink in slow motion, forming soft brown veils. Backlit by warm amber light, deep
teal background. Mesmerising, unhurried, laboratory-clean.
Brand: Florida Coffee, Istanbul. Palette petrol teal #004854, amber #F09C1C, rust #D44808, cream.
One continuous shot, no cuts, no scene changes, loopable. Photoreal, cinematic, natural light,
shallow depth of field, no text, no logos, no captions, no talking, no people looking at camera.
Compose for 9:16 vertical with the top-left corner kept quiet and free of key detail or moving
highlights — reserved space for a logo composited in post. Every cup, glass, package and surface is
plain and unbranded: no printed marks, emblems, lettering or labels anywhere in frame.
Ambient only: faint liquid movement, quiet room tone — no voices, no music.
```

### Clip 3 — `03-servis` · startbeeld `img/menu/bogaz-cold-brew.jpg`

```
Slow tilt up along a tall glass filled with clear ice as dark cold brew is poured in from above,
swirling between the cubes. Condensation beads and runs down the outside of the glass. A hand
holds the carafe, only fingers visible. Warm amber light, deep teal tiled wall softly blurred.
Brand: Florida Coffee, Istanbul. Palette petrol teal #004854, amber #F09C1C, rust #D44808, cream.
One continuous shot, no cuts, no scene changes, loopable. Photoreal, cinematic, natural light,
shallow depth of field, no text, no logos, no captions, no talking, no people looking at camera.
Compose for 9:16 vertical with the top-left corner kept quiet and free of key detail or moving
highlights — reserved space for a logo composited in post. Every cup, glass, package and surface is
plain and unbranded: no printed marks, emblems, lettering or labels anywhere in frame.
Ambient only: ice clinking, liquid pouring — no voices, no music.
```

## Reel 03 — "Usta Eli"

*Bron: `reels/03-usta-eli.md` — daar staan shotlist, Turkse copy en montage-instructies.*

### Clip 1 — `01-cekirdek` · startbeeld `img/hasat.jpg`

```
Extreme macro, static camera, shallow depth of field: pale green raw coffee beans pour slowly
through an open weathered hand and fall out of frame. Only hand and forearm visible, no face.
Warm directional side light from the left, deep shadow behind. Skin texture and bean detail sharp.
Brand: Florida Coffee, Istanbul. Palette petrol teal #004854, amber #F09C1C, rust #D44808, cream.
One continuous shot, no cuts, no scene changes, loopable. Photoreal, cinematic, natural light,
shallow depth of field, no text, no logos, no captions, no talking, no people looking at camera.
Compose for 9:16 vertical with the top-left corner kept quiet and free of key detail or moving
highlights — reserved space for a logo composited in post. Every cup, glass, package and surface is
plain and unbranded: no printed marks, emblems, lettering or labels anywhere in frame.
Ambient only: beans rattling, low roaster drum hum — no voices, no music.
```

### Clip 2 — `02-kavurma` · startbeeld `img/kavurma.jpg`

```
Slow push-in toward the glass port of a rotating coffee roaster drum. Inside, beans tumble and
glow, shifting from pale to deep amber, thin smoke drifting. Intense warm amber light spills out
of the drum onto a dark workshop. Industrial, warm, controlled.
Brand: Florida Coffee, Istanbul. Palette petrol teal #004854, amber #F09C1C, rust #D44808, cream.
One continuous shot, no cuts, no scene changes, loopable. Photoreal, cinematic, natural light,
shallow depth of field, no text, no logos, no captions, no talking, no people looking at camera.
Compose for 9:16 vertical with the top-left corner kept quiet and free of key detail or moving
highlights — reserved space for a logo composited in post. Every cup, glass, package and surface is
plain and unbranded: no printed marks, emblems, lettering or labels anywhere in frame.
Ambient only: roaster drum rumble, first crack pops — no voices, no music.
```

### Clip 3 — `03-shot` · startbeeld `img/pour.jpg`

```
Static extreme macro with a gentle rack focus: espresso streams from a polished portafilter into
a small cream cup, thick tiger-striped crema forming and swirling, tiny bubbles catching the light.
Warm amber light, deep teal tiled wall softly out of focus behind.
Brand: Florida Coffee, Istanbul. Palette petrol teal #004854, amber #F09C1C, rust #D44808, cream.
One continuous shot, no cuts, no scene changes, loopable. Photoreal, cinematic, natural light,
shallow depth of field, no text, no logos, no captions, no talking, no people looking at camera.
Compose for 9:16 vertical with the top-left corner kept quiet and free of key detail or moving
highlights — reserved space for a logo composited in post. Every cup, glass, package and surface is
plain and unbranded: no printed marks, emblems, lettering or labels anywhere in frame.
Ambient only: espresso machine hiss, liquid into ceramic — no voices, no music.
```

## Reel 04 — "Çalışma Köşesi"

*Bron: `reels/04-calisma-kosesi.md` — daar staan shotlist, Turkse copy en montage-instructies.*

### Clip 1 — `01-priz` · startbeeld `img/workspace.jpg`

```
Static macro shot, shallow depth of field: a hand enters frame and pushes a laptop charger plug
into a wall socket set in a deep teal painted wall with a warm wooden shelf edge above. Only hand
and forearm visible, no face. Soft daylight from the left, calm and domestic.
Brand: Florida Coffee, Istanbul. Palette petrol teal #004854, amber #F09C1C, rust #D44808, cream.
One continuous shot, no cuts, no scene changes, loopable. Photoreal, cinematic, natural light,
shallow depth of field, no text, no logos, no captions, no talking, no people looking at camera.
Compose for 9:16 vertical with the top-left corner kept quiet and free of key detail or moving
highlights — reserved space for a logo composited in post. Every cup, glass, package and surface is
plain and unbranded: no printed marks, emblems, lettering or labels anywhere in frame.
Ambient only: soft click of the plug, distant cafe murmur — no voices, no music.
```

### Clip 2 — `02-kose` · startbeeld `img/workspace.jpg`

```
Slow diagonal push-in over a cafe study corner seen from above: an open laptop, a handwritten
notebook, a cream cup with a teal band, a pair of glasses on a warm wooden table. A soft patch of
afternoon sun moves slowly across the surface. Dust motes drift in the light. No people in frame.
Brand: Florida Coffee, Istanbul. Palette petrol teal #004854, amber #F09C1C, rust #D44808, cream.
One continuous shot, no cuts, no scene changes, loopable. Photoreal, cinematic, natural light,
shallow depth of field, no text, no logos, no captions, no talking, no people looking at camera.
Compose for 9:16 vertical with the top-left corner kept quiet and free of key detail or moving
highlights — reserved space for a logo composited in post. Every cup, glass, package and surface is
plain and unbranded: no printed marks, emblems, lettering or labels anywhere in frame.
Ambient only: pages turning, faint keyboard, soft cafe murmur — no voices, no music.
```

### Clip 3 — `03-ikinci` · startbeeld `img/sakarya.jpg`

```
Static shot, shallow depth of field: a hand sets a second full cream cup with a teal band down on
a warm wooden table next to an empty first cup, then withdraws. Only hand and forearm visible.
Warm late-afternoon light from a window, deep teal wall softly out of focus behind.
Brand: Florida Coffee, Istanbul. Palette petrol teal #004854, amber #F09C1C, rust #D44808, cream.
One continuous shot, no cuts, no scene changes, loopable. Photoreal, cinematic, natural light,
shallow depth of field, no text, no logos, no captions, no talking, no people looking at camera.
Compose for 9:16 vertical with the top-left corner kept quiet and free of key detail or moving
highlights — reserved space for a logo composited in post. Every cup, glass, package and surface is
plain and unbranded: no printed marks, emblems, lettering or labels anywhere in frame.
Ambient only: ceramic on wood, soft cafe murmur — no voices, no music.
```

## Reel 05 — "Şehir Uyurken"

*Bron: `reels/05-gece-0200.md` — daar staan shotlist, Turkse copy en montage-instructies.*

### Clip 1 — `01-vitrin` · startbeeld `img/night.jpg`

```
Static shot with the faintest drift: a cafe window glows warm amber at night on a quiet street
near the water. Rain-wet pavement in the foreground mirrors the light in long vertical streaks.
Deep teal and near-black surroundings, a few warm highlights. Calm, cinematic, nobody in frame yet.
Brand: Florida Coffee, Istanbul. Palette petrol teal #004854, amber #F09C1C, rust #D44808, cream.
One continuous shot, no cuts, no scene changes, loopable. Photoreal, cinematic, natural light,
shallow depth of field, no text, no logos, no captions, no talking, no people looking at camera.
Compose for 9:16 vertical with the top-left corner kept quiet and free of key detail or moving
highlights — reserved space for a logo composited in post. Every cup, glass, package and surface is
plain and unbranded: no printed marks, emblems, lettering or labels anywhere in frame.
Ambient only: light rain, distant traffic, faint water — no voices, no music.
```

### Clip 2 — `02-gecen` · startbeeld `img/night.jpg`

```
Slow lateral dolly to the left past the glowing facade of a night cafe. A person in a long coat
walks through frame carrying a cream cup, seen from behind and in silhouette, never facing camera.
Car headlights pass in the background as soft bokeh. Rain-wet pavement reflects amber light.
Brand: Florida Coffee, Istanbul. Palette petrol teal #004854, amber #F09C1C, rust #D44808, cream.
One continuous shot, no cuts, no scene changes, loopable. Photoreal, cinematic, natural light,
shallow depth of field, no text, no logos, no captions, no talking, no people looking at camera.
Compose for 9:16 vertical with the top-left corner kept quiet and free of key detail or moving
highlights — reserved space for a logo composited in post. Every cup, glass, package and surface is
plain and unbranded: no printed marks, emblems, lettering or labels anywhere in frame.
Ambient only: footsteps on wet pavement, passing car, light rain — no voices, no music.
```

### Clip 3 — `03-filtre` · startbeeld `img/gecefiltre.jpg`

```
Slow push-in on a glass pour-over carafe on a wooden counter at night: dark coffee drips steadily
from the filter cone, steam rising. Behind it, a large window shows the dark water and scattered
distant city lights out of focus. Warm amber lamp above, cool blue night outside. Quiet, intimate.
Brand: Florida Coffee, Istanbul. Palette petrol teal #004854, amber #F09C1C, rust #D44808, cream.
One continuous shot, no cuts, no scene changes, loopable. Photoreal, cinematic, natural light,
shallow depth of field, no text, no logos, no captions, no talking, no people looking at camera.
Compose for 9:16 vertical with the top-left corner kept quiet and free of key detail or moving
highlights — reserved space for a logo composited in post. Every cup, glass, package and surface is
plain and unbranded: no printed marks, emblems, lettering or labels anywhere in frame.
Ambient only: slow dripping, faint room tone — no voices, no music.
```

## Reel 06 — "Aynı Çekirdek"

*Bron: `reels/06-budvada-ayni-cekirdek.md` — daar staan shotlist, Turkse copy en montage-instructies.*

### Clip 1 — `01-istanbul` · modus **Frames to Video** · startbeeld `img/hero.jpg`

```
Static shot with the faintest micro-drift: a cream takeaway cup with a deep teal band on a
weathered wooden terrace rail high above the Bosphorus. A ferry crosses in the far distance,
water glittering in golden hour light. Warm haze, calm, premium.
Brand: Florida Coffee, Istanbul. Palette petrol teal #004854, amber #F09C1C, rust #D44808, cream.
One continuous shot, no cuts, no scene changes, loopable. Photoreal, cinematic, natural light,
shallow depth of field, no text, no logos, no captions, no talking, no people looking at camera.
Compose for 9:16 vertical with the top-left corner kept quiet and free of key detail or moving
highlights — reserved space for a logo composited in post. Every cup, glass, package and surface is
plain and unbranded: no printed marks, emblems, lettering or labels anywhere in frame.
Ambient only: distant ferry horn, gulls, soft water — no voices, no music.
```

### Clip 2 — `02-budva` · modus **Text to Video** (geen bestaand frame)

```
Slow push-in on a cream takeaway cup with a deep teal band resting on an old pale stone wall
above the Adriatic Sea. Clear turquoise water below, a small stone harbour and terracotta roofs
softly out of focus in the background. Bright Mediterranean midday sun, crisp shadows, light
sea breeze. Photoreal, cinematic.
Brand: Florida Coffee, Istanbul. Palette petrol teal #004854, amber #F09C1C, rust #D44808, cream.
One continuous shot, no cuts, no scene changes, loopable. Photoreal, cinematic, natural light,
shallow depth of field, no text, no logos, no captions, no talking, no people looking at camera.
Compose for 9:16 vertical with the top-left corner kept quiet and free of key detail or moving
highlights — reserved space for a logo composited in post. Every cup, glass, package and surface is
plain and unbranded: no printed marks, emblems, lettering or labels anywhere in frame.
Ambient only: waves on stone, distant gulls, light wind — no voices, no music.
```

### Clip 3 — `03-ayni` · modus **Frames to Video** · startbeeld `img/cup.jpg`

```
Slow tilt up along a cream cup with a deep teal band held in a hand, steam rising, with the
out-of-focus blue sea filling the background. Only hand and forearm visible, no face. Warm hard
Mediterranean light, strong rim highlight on the steam.
Brand: Florida Coffee, Istanbul. Palette petrol teal #004854, amber #F09C1C, rust #D44808, cream.
One continuous shot, no cuts, no scene changes, loopable. Photoreal, cinematic, natural light,
shallow depth of field, no text, no logos, no captions, no talking, no people looking at camera.
Compose for 9:16 vertical with the top-left corner kept quiet and free of key detail or moving
highlights — reserved space for a logo composited in post. Every cup, glass, package and surface is
plain and unbranded: no printed marks, emblems, lettering or labels anywhere in frame.
Ambient only: waves, light wind — no voices, no music.
```
