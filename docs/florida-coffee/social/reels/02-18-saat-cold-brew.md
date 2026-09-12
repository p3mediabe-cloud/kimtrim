# Reel 02 — "18 Saat"

| | |
|---|---|
| **Pijler** | Ürün / tarif |
| **Persona** | Zeynep (21, studente) — secundair Emre |
| **Platform** | TikTok (primair) · Reels |
| **Product** | Boğaz Cold Brew |
| **Duur** | 15 s |
| **Doel** | Verlangen + bezoek. Vakmanschap tonen via geduld, niet via claims. |

## Concept

Het getal draagt de reel. **18 uur koud extraheren** is het bewijs van zorg — precies het
tegengif tegen "duur en wisselvallig" uit §5.3. Geen woord over kwaliteit; alleen de tijd
laten spreken.

```
SLAG 1 — HAAK    0–1,5 s   Druppel valt in glas. Harde stop op het getal.
SLAG 2 — MOMENT  1,5–11 s  Koude extractie: druppeltoren, donkere sliert in helder water.
SLAG 3 — LANDING 11–15 s   IJs, gieten, condens. CTA. Eindkaart.
```

## Shotlist

| # | Beeld | Camera | Licht | Duur | First frame |
|---|---|---|---|---|---|
| 1 | Macro: één druppel valt in glazen kolf | Statisch macro | Amber zijlicht, petrol achtergrond | 8 s | `img/coldbrew.jpg` |
| 2 | Donkere koffiesliert kringelt door helder water | Trage push-in | Amber tegenlicht | 8 s | `img/coldbrew.jpg` |
| 3 | Cold brew over ijs, condens loopt langs glas | Trage tilt omhoog | Amber, petrol tegelwand | 8 s | `img/menu/bogaz-cold-brew.jpg` |

## Google Flow — prompts

**Instellingen:** 9:16 · 720p · 8s · Veo 3.1 · modus **Frames to Video**

### Clip 1 — `01-damla` · startbeeld `img/coldbrew.jpg`
```
Extreme macro, static camera: a single dark coffee droplet forms at the tip of a glass cold-brew
tower valve, hangs, then falls and breaks the surface of clear water below, sending one slow
ripple outward. Amber rim light from the left, deep teal tiled wall far out of focus behind.
Very slow, meditative, high detail on the glass and the droplet.
Brand: Florida Coffee, Istanbul. Palette petrol teal #004854, amber #F09C1C, rust #D44808, cream.
One continuous shot, no cuts, no scene changes, loopable. Photoreal, cinematic, natural light,
shallow depth of field, no text, no logos, no captions, no talking, no people looking at camera.
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
Ambient only: ice clinking, liquid pouring — no voices, no music.
```

**Negatief (alle clips):**
```
text, watermark, logo, subtitles, distorted hands, extra fingers, cartoon, oversaturated,
plastic skin, stock-photo smile, lens flare, fast camera shake
```

## Turkse copy

**On-screen (3 kaarten):**
| Tijd | Tekst |
|---|---|
| 0,5 s | `18 saat.` |
| 4,0 s | `Tek bir bardak için.` |
| 12,0 s | `Boğaz Cold Brew` |

**Caption — TikTok:**
```
18 saat. tek bir bardak için.

soğuk demleme acele kaldırmıyor.
18 saat bekledi, sen 18 saniye bekle ☕

boğaz cold brew, tüm şubelerde
#floridacoffee #coldbrew #mutluluğuntadı #kahvekeyfi #üçüncüdalga #soğukkahve #kahvedemleme #boğaz
```

**Caption — Reels:**
```
18 saat. Tek bir bardak için.

Soğuk demleme acele kaldırmaz.
Ne ısı, ne baskı — sadece zaman.
18 saat bekledi; senin 18 saniyen var.

Boğaz Cold Brew, tüm şubelerimizde ☕

#floridacoffee #mutluluğuntadı #kahvekeyfi #üçüncüdalga #coldbrew #soğukkahve #kahvedemleme
```

## Montage

```
Clips      : 01-damla.mp4 (0–2 s) · 02-ekstraksiyon.mp4 (2–11 s) · 03-servis.mp4 (11–15 s)
Tekstkaart : 0,5 s  "18 saat."            — groot, cream op transparant, midden
Tekstkaart : 4,0 s  "Tek bir bardak için."
Tekstkaart : 12,0 s "Boğaz Cold Brew"     — amber, onderin veilige zone
Eindkaart  : 13,5–15 s  logo-reverse.png op #004854
Geluid     : TikTok → trending sound, beeld op de beat geknipt · Reels → ambient + ambient bed
Export     : 1080×1920, H.264, ±8 Mbps
```

## Aannames & te verifiëren

- "18 saat" is de gangbare cold brew-extractietijd en staat als zodanig in de reel.
  **Laat HQ de werkelijke extractietijd bevestigen** — een afwijkend getal maakt de
  reel onbruikbaar en is precies het soort detail waar de reacties op aanslaan.
- "Tüm şubelerimizde" veronderstelt landelijke beschikbaarheid. Niet bevestigd →
  vervang door `Seçili şubelerde` als HQ dat niet bevestigt.
