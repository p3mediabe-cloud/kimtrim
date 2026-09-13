---
name: florida-reels
description: Produceer merkvaste reels, shorts en social posts voor Florida Coffee — van brief naar Google Flow-prompts, Turkse captions, montage-instructies en publicatieklaar pakket. Gebruik dit bij elke vraag om een reel, short, TikTok, Instagram-post, story of videocampagne voor Florida Coffee, en bij het vullen van de wekelijkse contentkalender (contractueel 3 video's per week).
---

# Florida Coffee — Reels & Posts productie

Je produceert social video en posts voor **Florida Coffee**, een Turkse koffieketen
(±15–18 vestigingen: İstanbul, Anatolië, Karadağ). Opdrachtgever van de productie is
**P3Media**. Publicatietaal is **Turks**.

## Stap 0 — Lees eerst het merk-OS. Altijd.

```
docs/florida-coffee/social/brand-voice.md
```

Dat bestand is de enige waarheid over toon, palet, beeldtaal, verboden woorden en
platformspecs. Begin nooit met schrijven of genereren voordat je het gelezen hebt.
Bij tegenstrijdigheid tussen dit document en het merk-OS wint **het merk-OS**.

Aanvullende bronnen wanneer je context nodig hebt:

| Bestand | Waarvoor |
|---|---|
| `docs/florida-coffee/00-analiz-raporu.md` | Personas (§5.2), merkanalyse (§8), vestigingen (§2.2) |
| `docs/florida-coffee/demo-site/menu.json` | 53 producten, categorieën, fotografie-aanwijzingen |
| `docs/florida-coffee/demo-site/img/` | 23 merkframes + menufoto's — bruikbaar als first frame |
| `docs/florida-coffee/demo-site/brand/` | Logobestanden voor de eindkaart |

## Stap 1 — Intake

Leid deze zes velden af uit de vraag. Ontbreekt er één, kies de meest waarschijnlijke
op basis van het merk-OS en **benoem je aanname** — vraag niet door op details die je
zelf kunt invullen.

| Veld | Opties |
|---|---|
| **Pijler** | manzara · ürün · barista · kampanya · franchise · karadağ |
| **Persona** | Zeynep · Emre · Selin&Can · Ahmet · Mira (precies één) |
| **Platform** | Reels · TikTok · beide (dan twee monteringen, één bronclip) |
| **Vestiging** | Beykoz · Çengelköy · Kadıköy · Kavacık · Taksim · Sakarya · Budva … |
| **Aanleiding** | seizoen, nieuw product, actie, opening, weekdag |
| **Aantal** | standaard 3 per week (contract §8.4) |

## Stap 2 — Concept: de drie-slagen-structuur

Elke reel heeft exact drie slagen. Houd het totaal onder 20 seconden.

```
SLAG 1 — HAAK      (0–1,5 s)  Beeld dat stopt. Kleur = merk. Hook-formule uit §6 van het merk-OS.
SLAG 2 — MOMENT    (1,5–12 s) Eén doorlopende handeling. Geen montage-acrobatiek.
SLAG 3 — LANDING   (12–18 s)  Rust, CTA in beeld, 1,5 s eindkaart met logo.
```

Toets het concept hardop aan de kernzin uit het merk-OS:
*verkoop het moment aan de Bosporus, en bewijs waarom de koffie dat waard is.*
Lukt dat niet, dan is het concept nog niet af.

## Stap 3 — Shotlist

Per slag: **wat zien we · camerabeweging · licht · duur · first frame**.

Regels die niet onderhandelbaar zijn:
- Eén doorlopende camerabeweging per clip. Geen cuts bínnen een gegenereerde clip.
- Maximaal 8 seconden per gegenereerde clip (modelgrens). Langer = meerdere clips
  aan elkaar in de montage, of Flow's *Extend*.
- Niemand kijkt in de lens. Mensen als handen, silhouet of half in beeld.
- Geen tekst, logo of ondertiteling in de generatie — die komt in de montage.
- Kies waar mogelijk een bestaand frame uit `demo-site/img/` als startbeeld: dat borgt
  het palet beter dan welke prompt ook.

## Stap 4 — Google Flow-prompts

Dit is de productieroute: P3Media plakt de prompts in **flow.google.com** en betaalt met
de eigen (gratis) credits. Lever ze daarom **kant-en-klaar en zonder uitleg ertussen**.

### 4.1 Kies de invoermodus

| Modus | Wanneer | Wat je aanlevert |
|---|---|---|
| **Frames to Video** | Voorkeur. Er is een passend startbeeld in `img/` | Bestandsnaam + prompt |
| **Text to Video** | Nieuwe scène zonder bruikbaar frame | Alleen prompt |
| **Ingredients to Video** | Herkenbare beker, verpakking of persoon moet consistent terug | Referentiebeelden + prompt |

### 4.2 Promptopbouw — vaste volgorde

```
<CAMERA> <ONDERWERP + HANDELING> <OMGEVING> <LICHT> <SFEER> <MERKBLOK> <LOGOBLOK> <AUDIO>
```

**Merkblok — plak dit ongewijzigd achter elke prompt:**

```
Brand: Florida Coffee, Istanbul. Palette petrol teal #004854, amber #F09C1C, rust #D44808, cream.
One continuous shot, no cuts, no scene changes, loopable. Photoreal, cinematic, natural light,
shallow depth of field, no text, no logos, no captions, no talking, no people looking at camera.
```

**Logoblok — plak dit ongewijzigd onder het merkblok, vóór de audioregel:**

```
Compose for 9:16 vertical with the top-left corner kept quiet and free of key detail or moving
highlights — reserved space for a logo composited in post. Every cup, glass, package and surface is
plain and unbranded: no printed marks, emblems, lettering or labels anywhere in frame.
```

P3Media zet het logo bij élke video zelf in de montage. Daarom doet dit blok twee dingen:
het houdt de linkerbovenhoek vrij zodat het logo ergens kan landen, en het verbiedt
gegenereerde merktekens op bekers en verpakking — die botsen met het echte logo en komen
er als verminkte letters uit. Onderin reserveren heeft geen zin: daar staat de
platform-UI. Noteer per reel welke logoversie past bij de toon van die hoek.

**Negatief — standaard:**

```
text, watermark, logo, subtitles, branded cup, printed logo on cup, emblem, insignia, label,
lettering on packaging, distorted hands, extra fingers, cartoon, oversaturated, plastic skin,
stock-photo smile, lens flare, fast camera shake
```

**Instellingen in Flow:** verhouding `9:16` · resolutie `720p` (upscalen kan later) ·
duur `8s` · model `Veo 3.1` (of `Veo 3.1 Fast` bij het uitproberen van varianten).

### 4.3 Geluid

Veo genereert natively audio. Vraag **omgevingsgeluid, geen spraak**:
`ambient only: espresso machine hiss, distant ferry horn, soft street murmur — no voices, no music`.
Muziek komt in de montage (TikTok: trending sound leidt).

## Stap 5 — Turkse copy

Schrijf caption, on-screen tekst en hashtags volgens §7, §8 en §9 van het merk-OS.

- Caption volgt het vaste stramien: hook → 2–3 korte regels → één zachte CTA → vestiging → hashtags.
- On-screen tekst: 3–5 woorden per kaart, maximaal 3 kaarten, binnen de veilige zone.
- 8–10 hashtags: 4 vast + 1–2 locatie + 2–3 onderwerp.
- Controleer elk woord tegen de verbodenlijst (§4.4). Eén superlatief maakt de reel
  aanvechtbaar in de reacties — dat is de reden dat die lijst bestaat.

Bij platform `beide`: lever **twee** captions. TikTok korter, directer, kleine letters
toegestaan; Reels rustiger en cinematischer.

## Stap 6 — Montage-instructies

Lever per reel een blokje dat een editor zonder verdere uitleg kan uitvoeren:

```
Clips      : 01-haak.mp4 (0–2 s) · 02-moment.mp4 (2–14 s) · 03-landing.mp4 (14–18 s)
Tekstkaart : 0,4 s  "<TR tekst>"        — cream op petrol, onderin binnen veilige zone
Tekstkaart : 13,5 s "<TR CTA>"
Eindkaart  : 16,5–18 s  logo-reverse.png gecentreerd op #004854
Geluid     : <trending sound / ambient + licht muziekbed>
Export     : 1080×1920, H.264, ±8 Mbps
```

## Stap 7 — QA vóór oplevering

Loop deze lijst af. Eén kruisje = terug naar de tekentafel.

- [ ] Eén pijler, één persona, één CTA
- [ ] Merk herkenbaar aan kleur binnen de eerste seconde
- [ ] Geen verboden woord, geen prijsclaim, geen absolute kwaliteitsclaim
- [ ] Geen ongeverifieerde vestigingsgegevens (§2.2 is nog niet door de klant bevestigd)
- [ ] Niemand kijkt in de lens; geen AI-tekst of AI-logo in beeld
- [ ] Caption volgt het stramien, 8–10 hashtags
- [ ] Tekst binnen de veilige zone van het platform
- [ ] Twee monteringen als het platform `beide` is

## Stap 8 — Wegschrijven

```
docs/florida-coffee/social/reels/<nr>-<slug>.md   één bestand per reel, compleet
docs/florida-coffee/social/flow-prompt-pack.md    alle prompts gebundeld, copy-paste
docs/florida-coffee/social/kalender.md            planning bijwerken
```

Eén bestand per reel bevat: concept, shotlist, Flow-prompts, Turkse copy,
montage-instructies. Zo kan één reel los doorgegeven worden aan een editor of klant.

## Posts (geen video)

Voor statische posts of carrousels: sla stap 3, 4 en 6 over. Beschrijf in plaats daarvan
per kaart het beeld (of verwijs naar `img/`), de Turkse tekst en de opbouw. Toon, palet,
CTA-bank, hashtags en de verbodenlijst gelden onverkort.

## Levend houden

Verandert de merkrichting, dan pas je **`brand-voice.md`** aan — niet dit bestand en niet
losse reels. Dit bestand beschrijft het *proces*; het merk-OS beschrijft het *merk*.
