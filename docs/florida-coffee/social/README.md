# Florida Coffee — Social video systeem

Een productiesysteem voor reels, shorts en posts dat **altijd** op merk blijft: één
merkbron, één agent die die bron leest, en kant-en-klare Google Flow-prompts als output.

## Waarom dit bestaat

De analyse legt P3Media contractueel vast op **3 korte video's per week** voor Florida
Coffee (§8.4). Dat is 12 per maand, 144 per jaar. Handmatig blijft dat nooit consistent
in toon, kleur en risico-grenzen. Dit systeem maakt van merkconsistentie een
eigenschap van het proces in plaats van een kwestie van oplettendheid.

## Hoe het in elkaar zit

```
brand-voice.md              ← het merk. Toon, palet, pijlers, verbodenlijst.
     │                        Eén bron. Wijzig hier, en alle output verandert mee.
     ▼
.claude/skills/florida-reels/SKILL.md   ← het proces. Brief → concept → shotlist →
     │                                     Flow-prompts → Turkse copy → montage → QA.
     ▼
.claude/agents/florida-social.md        ← de agent. Leest beide, levert compleet af.
     │
     ▼
reels/<nr>-<slug>.md        ← één bestand per reel, volledig, los overdraagbaar
flow-prompt-pack.md         ← alle 18 clips gebundeld, copy-paste naar flow.google.com
kalender.md                 ← 12 video's per maand, verdeeld over de pijlers
```

## Gebruik

**Nieuwe reels laten maken:**

```
Gebruik de florida-social agent: maak 3 reels voor week 3,
pijlers ürün / barista / manzara, vestiging Kadıköy, aanleiding herfstblend.
```

De agent leest het merk-OS, kiest persona en platform, schrijft de reelbestanden,
werkt de kalender bij en levert de Flow-prompts.

**Prompt-pack opnieuw bouwen** na een wijziging in een reel:

```
cd docs/florida-coffee/social && python3 build_pack.py
```

**Merkkoers bijsturen:** pas uitsluitend `brand-voice.md` aan. Niet de losse reels,
niet de skill. Dat is het hele punt van de opzet.

## Video's genereren

Productieroute is **Google Flow** (flow.google.com) met de eigen credits van P3Media.
Flow is een browsertool zonder API — de prompts worden dus aangeleverd om te plakken,
niet automatisch ingeschoten. `flow-prompt-pack.md` staat in de volgorde van het werk.

De 23 bestaande merkframes in `../demo-site/img/` zijn de startbeelden. Die dragen het
palet betrouwbaarder dan welke prompt ook — gebruik *Frames to Video* waar het kan.

> **Automatiseren later?** `../demo-site/gen_video.py` genereert al met Veo 3.1 via de
> Gemini API en kan in CI draaien. Let op: die API rekent **apart** af en raakt de gratis
> Flow-credits niet aan. Alleen zinvol als het volume de handmatige route voorbijgroeit.

## De eerste batch

| # | Reel | Pijler | Persona | Platform |
|---|---|---|---|---|
| 01 | Boğaz'da Sabah 7 | Manzara | Selin & Can | Reels |
| 02 | 18 Saat (cold brew) | Ürün | Zeynep | Beide |
| 03 | Usta Eli (zanaat) | Barista | Alle | Beide |
| 04 | Çalışma Köşesi | Kampanya | Zeynep | TikTok |
| 05 | Şehir Uyurken | Manzara | Selin & Can | Reels |
| 06 | Aynı Çekirdek (Budva) | Karadağ | Mira | Reels |

Samen dekken ze vijf van de zes pijlers en vier van de vijf personas. Franchise staat
in de kalender voor week 4, omdat die reel cijfers van HQ nodig heeft.

## Openstaand bij de klant

Deze punten staan per reel genoteerd en moeten vóór publicatie bevestigd worden.
Het zijn geen details: het zijn precies de dingen waar reacties op aanslaan.

| Punt | Reel | Waarom |
|---|---|---|
| Vestigingslijst, adressen, openingstijden | 01, 04, 05 | §2.2 is via websearch samengesteld, niet geverifieerd |
| Extractietijd cold brew (18 uur?) | 02 | Een fout getal maakt de reel onbruikbaar |
| Landelijke beschikbaarheid cold brew | 02 | Anders `Seçili şubelerde` |
| Voorwaarden loyaliteitsprogramma | 04 | `İkincisi bizden` is een toezegging |
| Sluitingsuur Beykoz (02:00?) | 05 | Zou de reel sterker maken — mits juist |
| Levert de branderij Karadağ? | 06 | Draagt de hele claim `aynı çekirdek` |
| Merkkleuren in officieel kleurprofiel | alle | Palet is nu gemeten uit het logo (§8.3) |
