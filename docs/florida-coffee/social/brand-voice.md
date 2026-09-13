# Florida Coffee — Merk- & Stem-OS voor social video

> **Wat dit is.** Het enige bronbestand voor tone of voice, beeldtaal en merkregels bij
> reels, shorts en posts. De workflow-agent (`.claude/agents/florida-social.md`) leest dit
> bestand vóór elke productie. Wijzig je hier iets, dan verandert alle output mee.
>
> **Taalafspraak.** Uitleg en instructies staan in het Nederlands (werktaal P3Media).
> Alles wat daadwerkelijk gepubliceerd wordt — captions, on-screen tekst, hashtags —
> staat in het **Turks** en is letterlijk overneembaar.
>
> Bron: `docs/florida-coffee/00-analiz-raporu.md` §2, §5, §8. Contractuele basis voor
> wekelijkse videoproductie: analyse §8.4 (3 korte video's per week, centrale productie).

---

## 1. Merkkern

| Element | Waarde |
|---|---|
| Merk | Florida Coffee (Florida Coffee Kahve Gıda Sanayi ve Ticaret A.Ş.) |
| Filosofie | **"Mutluluğun Tadı"** / "Taste of Joy" |
| Hoofdkantoor | Çengelköy, Üsküdar — İstanbul |
| Bereik | ±15–18 vestigingen: İstanbul, İzmit, Sakarya, Bursa, Samsun, Rize, Erzincan + Karadağ (Podgorica, Budva) |
| Ambacht | Eigen branderij, SCA-standaard, 30 dagen manager- + 15 dagen barista-opleiding |
| Sub-merken | FloridaDays, Mi Florida, BİFLORİDA, Florida Plus |

### 1.1 De positionering die we in beeld brengen

De analyse (§8.2) legt de vinger op de zere plek: **de belofte hangt aan de beleving, niet
aan het product.** Lof gaat over Boğaz-uitzicht en ruimte; kritiek over prijs en wisselende
kwaliteit.

Daarom is de opdracht van élke video één van deze twee:

1. **Manzara + huzur + kahve ritüeli** — de beleving die niemand kan kopiëren.
2. **Zanaat bewijzen** — branderij, cupping, SCA, opleiding. Dit is het tegengif tegen
   "duur en wisselvallig". Laat het vakmanschap zién, claim het niet.

> **Kernzin voor elke brief:** *Verkoop geen koffie. Verkoop het moment aan de Bosporus —
> en bewijs waarom die koffie dat moment waard is.*

---

## 2. Publiek per platform

Uit de personaset (§5.2). Kies per reel één persona — niet meer.

| # | Persona | Platform | Wat hen beweegt | Toon |
|---|---|---|---|---|
| 1 | **Zeynep, 21**, studente Sakarya | **TikTok** | Betaalbaar, stopcontact, wifi, lang zitten, acties | Speels, snel, vriendin-toon, trend-bewust |
| 2 | **Emre, 29**, kantoor Kadıköy/Taksim | **Reels** | Snelheid, voorbestellen, niet in de rij | Strak, functioneel, ochtendritme |
| 3 | **Selin & Can, 34–40**, weekend Beykoz/Çengelköy | **Reels** | Uitzicht, ontbijt, reserveren, parkeren | Rustig, cinematisch, weinig tekst |
| 4 | **Ahmet, 45**, investeerder | Reels + LinkedIn | Transparante cijfers, referentievestiging | Zakelijk, feitelijk, geen hype |
| 5 | **Mira, 27**, toerist Budva | Reels (EN-variant) | Türk kahvesi, Boğaz-verhaal, instagramwaardig | Uitnodigend, licht exotisch |

**Verdeling per maand (12 video's):** 5× Zeynep/TikTok · 4× Selin&Can + Emre/Reels ·
2× zanaat (alle platforms) · 1× franchise of Karadağ.

---

## 3. Visuele code

### 3.1 Palet — exact, gemeten uit het logo

| Kleur | HEX | Gebruik in video |
|---|---|---|
| Petrol | `#004854` | Basis, diepe schaduw, tekstbalk, wanden/tegels |
| Amber | `#F09C1C` | Licht, gloed, accent, CTA-tekst |
| Rust | `#D44808` | Spaarzaam accent, nooit als vlak |
| Cream | `#F5EFE6` | Bekers, tekst op donker, lucht |

Regel: **petrol + cream draagt het beeld, amber is het licht.** Rust is kruiden — hooguit
één element per frame.

### 3.2 Beeldtaal

- **Altijd:** natuurlijk licht, gouden uur of blauw uur, geringe scherptediepte, stoom,
  waterreflectie, echte handen, echte textuur (hout, tegel, linnen, karton).
- **Camerawerk:** één doorlopende beweging per clip. Slow push-in, zachte lateral dolly,
  macro rack focus. Nooit snelle whip-pans of schokkerige handheld.
- **Nooit:** stockfoto-glimlach richting camera, oververzadiging, vuurwerk-transities,
  drukke collages, zichtbare AI-artefacten (handen, tekst in beeld), lens flares.
- **Mensen:** silhouetten, handen, over-de-schouder, half afgesneden gezichten.
  Niemand kijkt in de lens. Dit houdt het cinematisch én voorkomt AI-gezichtsfouten.

### 3.3 Logo in video

Bestanden: `docs/florida-coffee/demo-site/brand/`

| Bestand | Waar |
|---|---|
| `logo.png` | Op crème/lichte achtergrond |
| `logo-reverse.png` | Op petrol/donkere achtergrond — standaard voor reels |
| `wordmark-noo.png` / `wordmark-reverse-noo.png` | Woordmerk met uitgespaarde "o" voor animatie |

**Het logo wordt altijd in de montage toegevoegd, nooit gegenereerd.** Dat is een vaste
afspraak met P3Media en heeft twee harde consequenties voor elke prompt:

1. **Ruimte reserveren.** Elke gegenereerde clip houdt de **linkerbovenhoek** rustig: geen
   hoofdonderwerp, geen bewegende highlights, weinig detail. Daar landt het logo. Onderin
   kan het niet — daar zitten de knoppen en captions van Reels en TikTok.
2. **Niets laten bedrukken.** Bekers, glazen, verpakking en oppervlakken worden expliciet
   als **blanco en merkloos** beschreven. Verzint het model zelf een merkteken, dan botst
   dat met het echte logo dat er overheen komt — en AI-letters zijn altijd verminkt.

Beide staan als vast blok in elke prompt (zie de skill, §4.2) en het negatieve blok vangt
de rest af (`branded cup`, `printed logo on cup`, `emblem`, `insignia`, `label`, `lettering`).

**Welke versie:** kies per reel op de toon van de linkerbovenhoek — `logo.png` op licht
(gouden lucht, zee), `logo-reverse.png` op donker (nacht, branderij, petrol wand). Eén
versie per reel, dezelfde positie in alle clips; wisselen binnen één reel valt op.

---

## 4. Tone of voice (Turks)

### 4.1 Het karakter in vier woorden

**Samimi · sakin · ustalıklı · İstanbullu.**
(Hartelijk · kalm · vakkundig · Istanbuls.)

Premium zonder afstand. We zijn de buurman die toevallig uitstekende koffie brandt — niet
een luxemerk dat neerkijkt, en niet een kortingsketen die schreeuwt.

### 4.2 Regels

| Doen | Laten |
|---|---|
| Tutoyeren (`sen`) | Vousvoyeren (`siz`) in social — te afstandelijk |
| Korte zinnen, veel wit | Lange volzinnen, komma-slierten |
| Concreet: plaats, uur, product | Vage superlatieven |
| Eén emoji, hooguit twee | Emoji-slierten ☕️☕️☕️🔥🔥 |
| Kleine letters mogen in TikTok-captions | ALLES IN HOOFDLETTERS |
| Uitnodiging: `gel`, `uğra`, `dene` | Bevel: `hemen satın al`, `kaçırma!` |

### 4.3 Woorden die we gebruiken (Turks)

`Boğaz` · `manzara` · `huzur` · `ritüel` · `demleme` · `kavurma` · `çekirdek` ·
`taze` · `usta` · `sabah` · `akşamüstü` · `köşe` · `keyif` · `mutluluğun tadı`

### 4.4 Woorden die we vermijden

`en ucuz` · `bomba fiyat` · `kaçırma` · `sınırlı süre!!!` · `efsane` · `bayılacaksınız` ·
`dünyanın en iyisi` · elke absolute kwaliteitsclaim.

**Waarom dit hard is:** de analyse (§5.3) laat klachten zien over prijs-perceptie en
wisselende kwaliteit. Een superlatief in een reel is munitie in de reacties. We tonen
vakmanschap, we claimen het niet.

### 4.5 Zinnen die de stem vastleggen — letterlijk bruikbaar

**Manzara / huzur:**
- `Boğaz'a bakan bir köşe. Ve senin fincanın.`
- `Sabah 7. Vapur geçiyor. Kahven hazır.`
- `Şehir uyanmadan önceki o yarım saat.`
- `Akşamüstü Beykoz. Işık tam burada bitiyor.`

**Zanaat:**
- `Çekirdek bizim, kavurma bizim. Tadı da öyle.`
- `Her fincanın arkasında 45 günlük eğitim var.`
- `Usta eli değmeden fincana gitmez.`

**Product:**
- `Boğaz Cold Brew. 18 saat bekledi, sen 18 saniye bekle.`
- `Tek kaynak çekirdek. Bu hafta: Etiyopya.`

**Actie / loyaliteit (nooit schreeuwerig):**
- `FloridaDays başladı. Kahven bizden bir tane daha.`
- `Uygulamada biriktir, bir sonraki kahven hediye.`

**Karadağ:**
- `Budva'da da aynı çekirdek. Aynı tat.`

---

## 5. Content-pijlers

Zes pijlers, uit analyse §8.4. Elke video draagt **één** pijler.

| # | Pijler | Doel | Aandeel |
|---|---|---|---|
| 1 | **Manzara / mekan** | Merkgevoel, bereik, opslaan | 30% |
| 2 | **Ürün / tarif** | Verlangen, bezoek | 25% |
| 3 | **Barista / insan** | Vertrouwen, tegengif tegen kwaliteitskritiek | 20% |
| 4 | **Kampanya / sadakat** | App-installaties, herhaalbezoek | 15% |
| 5 | **Franchise** | Investeerders-leads | 5% |
| 6 | **Karadağ** | Internationale allure, toeristen | 5% |

---

## 6. Hook-formules (eerste 1,5 seconde)

De hook bepaalt alles. Kies er één, vul in met Turkse copy.

| Type | Formule | Voorbeeld (TR) |
|---|---|---|
| **Plaats-tijd** | `<plaats>. <uur>.` | `Beykoz. Akşamüstü 18:40.` |
| **Getal** | `<getal> <eenheid> <belofte>` | `18 saat. Tek bir bardak için.` |
| **Tegenstelling** | `<verwachting>, <werkelijkheid>` | `Sıradan bir salı. Sıra dışı bir köşe.` |
| **Vraag** | korte directe vraag | `İstanbul'un en sakin sabahı nerede?` |
| **Proces** | midden in de handeling beginnen | *(geen tekst — alleen het geluid van de maalmolen)* |

**Vaste regel:** in de eerste seconde is het merk herkenbaar aan **kleur** (petrol/amber),
niet aan een logo.

---

## 7. Captionstructuur

Vast stramien, alle platforms:

```
<HOOK — max 6 woorden, staat ook in beeld>

<2–3 korte regels: het moment, niet het product>

<CTA — één, zacht>

<vestiging + eventueel openingstijd>
<hashtags>
```

**Voorbeeld:**
```
Beykoz. Akşamüstü 18:40.

Işık suya değiyor, vapur geçiyor.
Elinde sıcak bir fincan.
Şehrin gürültüsü burada bitiyor.

Bu köşe seni bekliyor ☕

📍 Florida Coffee Beykoz — Kelle İbrahim Cad. 27, gece 02:00'a kadar açık
#floridacoffee #boğaz #beykoz #kahvekeyfi #mutluluğuntadı
```

---

## 8. CTA-bank (Turks)

Zacht, uitnodigend, nooit dwingend.

| Doel | CTA |
|---|---|
| Bezoek | `Bu köşe seni bekliyor.` · `Yolun düşerse uğra.` |
| App | `Uygulamadan sipariş ver, sırada bekleme.` · `Biriktir, bir sonraki kahven bizden.` |
| Opslaan | `Kaydet, hafta sonu lazım olur.` |
| Reactie | `Hangi şubemiz senin köşen? 👇` |
| Franchise | `Yatırım dosyamız hazır. Profildeki bağlantı.` |
| Karadağ (EN) | `Same beans. Same taste. Now in Budva.` |

---

## 9. Hashtags

**Vast (altijd, 4):**
`#floridacoffee #mutluluğuntadı #kahvekeyfi #üçüncüdalga`

**Locatie (kies 1–2):**
`#beykoz #çengelköy #kadıköy #boğaz #taksim #kavacık #üsküdar #sakarya #izmit #bursa #budva`

**Onderwerp (kies 2–3):**
`#coldbrew #filtrekahve #espresso #latteart #kahvedemleme #barista #cupping #kahvekavurma #sabahkahvesi #çalışmakafesi`

**Totaal 8–10.** Meer werkt niet en oogt goedkoop.

---

## 10. Platformspecificaties

| | Instagram Reels | TikTok |
|---|---|---|
| Verhouding | 9:16 (1080×1920) | 9:16 (1080×1920) |
| Duur | 8–15 s (max 20) | 12–25 s |
| Veilige zone | 250 px boven, 420 px onder vrijhouden | 180 px boven, 500 px onder vrijhouden |
| Tekst in beeld | 3–5 woorden per kaart, max 3 kaarten | Mag meer, mag ruwer |
| Toon | Cinematisch, rustig | Sneller, directer, trend-bewust |
| Geluid | Muziek mag dragend | **Trending sound leidt** — beeld volgt het ritme |
| Ondertiteling | Alleen als er gesproken wordt | Altijd |
| Eindkaart | 1,5 s logo op petrol | 1 s, mag korter |

**Eén bronclip, twee monteringen.** Nooit hetzelfde bestand op beide platforms dumpen.

---

## 11. Harde grenzen

1. Geen prijzen in beeld zonder schriftelijke bevestiging van HQ.
2. Geen openingstijden of adressen noemen die niet in `demo-site/index.html` staan —
   de vestigingslijst is nog niet door de klant geverifieerd (§2.2).
3. Geen gezichten van herkenbare personeelsleden zonder toestemming.
4. Geen claim over SCA-certificering per vestiging; alleen over de standaard van de branderij.
5. Geen AI-gegenereerde tekst of logo's in het beeld zelf — die komen in de montage.
6. Sub-merken (FloridaDays, Mi Florida, BİFLORİDA, Florida Plus) zijn **programma- en
   productnamen**, nooit losse afzenders. Afzender is altijd Florida Coffee.
