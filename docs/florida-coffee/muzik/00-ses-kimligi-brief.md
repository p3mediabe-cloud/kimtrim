# 00 · Ses kimliği brief'i

Bütün parçalar bu brief'e uyar. Yeni bir parça yazılacaksa önce burası okunur.

## Marka çıkış noktası

| Alan | Karar | Kaynak |
|---|---|---|
| Vaat | "Mutluluğun Tadı / Taste of Joy" | §8.2 |
| Ton | Samimi + premium; ukala değil, cıvık değil | §8.3 |
| Boşluk | Vaat deneyime bağlı, ürüne değil → müzikte **manzara, huzur, ritüel** anlatılır | §8.2 |
| Anlatı | "Boğaz'da Bir Gün": 06:40 şafak → 08:30 telaş → 17:00 eve götür → 21:00 kulüp → 23:30 gece → 02:00 kapanış → ertesi sabah yeniden | Ana sayfa |
| Anlatıcı | Flo, logodaki tukan; sıcak, kısa cümleli, işini bilen | Ana sayfa asistanı |
| Coğrafya | İstanbul ve Boğaz; Karadağ ikinci kıyı | §2.2 |

## Palet → ses eşlemesi

Görsel palet logodan ölçülmüş gerçek değerler; ses de aynı üç renkten kurulur.

| Renk | HEX | Ses karşılığı |
|---|---|---|
| Petrol | `#004854` | Zemin: kontrbas, oda tonu, uzak vapur düdüğü, su. Derinlik ve sükûnet. |
| Amber | `#F09C1C` | Melodi: naylon telli gitar, felt piyano, sıcak vokal. Işık ve davet. |
| Pas | `#D44808` | Vurgu: fırça davul, tef, tek bir üflemeli cümle. Sıcaklık ve insan eli. |

Kural: bir parçada üç renk de duyulur, ama **aynı anda ikisinden fazlası öne çıkmaz.**

## Ortak teknik çerçeve

- **Tempo aralığı:** 72–115 BPM. Marka hiçbir yerde koşmaz; telaşı anlatırken bile nabzı sabittir.
- **Ton merkezi:** D ve A majör ailesi (sabah, gündüz), F# ve D minör (gece). Katalog
  boyunca akraba tonlarda kalmak, parçaların art arda çalındığında tek yapıt gibi
  duyulmasını sağlar.
- **Çalgılar (çekirdek kadro):** naylon telli gitar, kontrbas, fırça davul/rim, felt piyano
  veya Rhodes, yumuşak oda tonu.
- **Yerel doku:** ud veya bağlama, **melodiyi taşımadan**, sadece renk olarak. Oryantal
  klişe değil, İstanbullu bir doku.
- **Vokal:** yakın mikrofon, nefes duyulur, düşük efekt. Erkek lider + kadın armoni
  (marş), kadın lider (sadakat/kulüp), fısıltıya yakın kadın (gece).
- **Miks:** analog bant sıcaklığı, kuyruklarda geniş rever, **sıkıştırma az.** Mağaza
  içinde saatlerce çalacak; yorucu olmamalı.
- **Ortam sesi:** uzak vapur düdüğü, martı, su, fincan-tabak, değirmen. Efekt olarak
  değil, mekânın kendisi olarak; her parçada en fazla iki tanesi.

## Sözlük

**Kullanılır:** Boğaz, vapur, şafak, tezgâh, fincan, çekirdek, değirmen, teras, kıyı,
rüzgâr, gün batımı, kepenk, sabır, kıvam, sıra, ışık, karşı kıyı.

**Kullanılmaz:** Florida (ABD çağrışımı: palmiye, plaj, Miami, sahil şeridi, neon,
tropikal), "enerji", "patlama", "bomba gibi", "acele et", "kaçırma", indirim dili,
İngilizce-Türkçe karışık cümle ("coffee'ni al"), aşırı samimi argo.

> **Neden:** Rapor §7.5'e göre markanın en kritik dijital sorunu, "Florida" adının ABD'yle
> karışması. Müzik de bu düzeltmenin parçası: her parça markayı İstanbul ve Boğaz'a
> bağlar, tropikal hiçbir çağrışım verilmez. Tukan Flo görsel dilde tropik kuş olabilir;
> müzikte tropikal ritim (bossa, reggaeton, steel drum, latin perküsyon) **yasak.**

## Söz kodlaması (etiket dili)

Bu katalogda söz alanı düz metin değil; Suno'ya **ne söyleyeceğini değil, nasıl söyleyeceğini**
de anlatan bir partisyon. Dokuz parçanın hepsi aynı beş işaretle kodlandı.

| İşaret | Suno ne yapar | Örnek |
|---|---|---|
| Kendi satırında `[köşeli parantez]` | Yönerge olarak okur, söylemez | `[guitar only, no drums]` |
| `[Bölüm — rol, mikrofon, dinamik]` | Bölümü açar ve icrayı belirler | `[Chorus — full band, female harmony a third above]` |
| Dize içinde `(parantez)` | **Söyler:** arka vokal, cevap, ad-lib | `Kahven seni bekler burada (Florida Coffee)` |
| BÜYÜK HARF | Heceyi vurgular | `bu BİZDEN` |
| `—` ve `...` | Notayı uzatır, duraklatır | `tam zamanında—` |
| `[End]` | Parçayı bitirir; uzayıp giden outro'yu keser | |

Kullanılmayacak işaretler: `*yıldız*`, `{süslü}`, `<açılı>` ve emoji. Suno bunları ya şarkının
içinde okur ya da yok sayar; ikisi de istemediğimiz şey.

### Her sözün başındaki üç satır

Her parça aynı üç satırla açılır. Dil kilidi, vokal rolü ve "parantezleri okuma" talimatı:

```
[Lang: Turkish — sing exactly as written, no English words]
[Voice: male lead, close mic, breath audible; female harmony from the second chorus]
[Perform: bracketed lines are directions — do not sing them]
```

Üçüncü satırın tutacağı garanti değil; tutmadığında aşağıdaki düşürme sırası uygulanır.

### Bir bölüm nasıl kodlanır

Bölüm başına en fazla iki yönerge satırı: biri **kim söylüyor, nasıl**, diğeri **çalgılar ne
yapıyor**. Üçten fazlası modelin dikkatini dağıtıyor.

```
[Pre-Chorus — voice lifts, upright bass enters underneath]
[brushed drums enter on the last line only]
Tezgâhta bir fincan ısınır
Gün ilk yudumla başlar
```

### Etiket düşürme sırası

Model yönergeleri şarkının içinde okumaya başlarsa ya da alan metni kabul etmezse, şu sırayla sil:

1. Miks ve konum yönergeleri (`far back in the mix`, `left of centre`)
2. Ortam sesi satırları (`distant ferry horn`, `room noise`)
3. Çalgı giriş-çıkış satırları (`upright bass enters`)
4. **En son gidenler — bunlar kalır:** bölüm etiketleri, vokal rolü satırı, `(parantez içindeki
   arka vokaller)` ve `[End]`

Sözlerin hiçbiri 2.300 karakteri geçmiyor; alan sınırı sorun çıkarırsa sebep uzunluk değil,
yoğunluktur.

### Marka kuralı

Florida Coffee adı **her parçada** geçer. Nasıl geçtiği parçanın türüne göre değişir:

| Parça | Nasıl |
|---|---|
| 01, 02, 04, 07 | Nakaratın arkasından gelen cevap: `(Florida Coffee)` |
| 03 | Grup vokali bağırışı ve kapanış: `(Florida Coffee — uygulamada)` |
| 05 | Fısıltıya yakın konuşma: "Florida Coffee. Beykoz. İkiye kadar açığız." |
| 06 | Sahne girişinde mikrofon dışından: "İyi akşamlar. Florida Coffee, Kavacık terası." |
| 08 | Sözsüz: kapanışta ses logosunun üç notası (D–F#–A); istenirse fısıltılı ek bölüm |
| 09 | Ses logosunun sözlü sürümü: "Florida Coffee. Mutluluğun tadı." |

Kural: marka adı **nakaratın önüne geçmez.** Cevap olarak, kapanışta veya konuşmada geçer;
dizenin konusu olmaz. Şarkı markayı anlatmaz, marka şarkının içinde durur.

## Katalog genelinde hariç tutulacaklar

Her parçanın kendi "Exclude styles" satırı var; ortak çekirdek şu:

```
trap, EDM, festival drop, heavy autotune, screaming vocals, distorted electric guitar, aggressive rap, reggaeton, bossa nova, steel drums, tropical house, corporate stock music, 8-bit
```

## Kullanım haritası

| Nerede | Parça |
|---|---|
| Ana sayfa hero videosu | 01 (enstrümantal kesit) |
| Yıllık marka filmi | 01 (tam) |
| EN site, Karadağ içerikleri | 02 |
| Uygulama lansmanı, ön sipariş reklamı | 03 |
| Sadakat kampanyası, Reels/TikTok | 04 |
| Gece içerikleri, 22:00 sonrası mağaza listesi | 05 |
| Perşembe akustik duyuruları | 06 |
| Sezon ürün lansmanı | 07 |
| Franchise ve kurumsal deste videoları | 08 |
| Her videonun kapanışı, uygulama bildirim sesi | 09 |
