# Florida Coffee — Suno v6 müzik paketi

Marka için üretilecek 9 parçanın **şarkı sözü** ve **stil tarifi** dosyaları. Her dosya
Suno'nun Custom (Özel) moduna doğrudan yapıştırılacak biçimde hazırlandı: stil alanı,
hariç tutulacaklar ve sözler ayrı kod bloklarında.

Kaynak: `00-analiz-raporu.md` §8 (marka vaadi, ton), `demo-site/index.html` ana sayfa
hikâyesi (06:40 → 02:00 gün akışı) ve `06-teklif-plani.md` içerik üretimi kalemi.

## Parçalar

| # | Parça | Dil | Kullanım | Süre hedefi |
|---|---|---|---|---|
| 01 | [Boğaz'da Bir Gün](01-bogazda-bir-gun.md) | TR | Marka marşı; hero videosu, mağaza içi, yıllık film | 2:30–3:00 |
| 02 | [Taste of Joy](02-taste-of-joy.md) | EN | Karadağ (Budva, Podgorica), EN site, turist içeriği | 2:15–2:45 |
| 03 | [Sıra Beklemek Yok](03-sira-beklemek-yok.md) | TR | Uygulama + ön sipariş kampanyası; 30/15/6 sn kesitler | 1:45–2:15 |
| 04 | [FloridaDays](04-floridadays.md) | TR | Sadakat kulübü; Reels/TikTok, push kampanyası | 1:30–2:00 |
| 05 | [Gece · Beykoz 02:00](05-gece-beykoz.md) | TR (az sözlü) | Gece içeriği, mağaza içi 22:00 sonrası liste | 3:00–4:00 |
| 06 | [Perşembe Akustik](06-persembe-akustik.md) | TR | Kavacık terası etkinlik duyuruları, etkinlik sayfası | 2:00–2:30 |
| 07 | [Sonbahar Harmanı](07-sonbahar-harmani.md) | TR | Sezonluk ürün lansmanı (çekirdek/ev espresso seti) | 1:45–2:15 |
| 08 | [Kurumsal Yatak](08-kurumsal-yatak.md) | — | Enstrümantal; franchise/kurumsal deste videoları, seslendirme altı | 2:00–3:00 |
| 09 | [Ses Logosu](09-ses-logosu.md) | — | 3–5 sn marka imzası; her videonun kapanışı, uygulama sesi | 3–5 sn |

Ses kimliğinin bütünü (palet–ses eşlemesi, sözlük, yasaklar): [00-ses-kimligi-brief.md](00-ses-kimligi-brief.md).

## Suno v6'da üretim akışı

1. **Create → Custom** (Özel). "Instrumental" yalnızca 08 ve 09'da açık.
2. **Styles** alanına dosyadaki *kısa stil* satırını yapıştır. Alan uzun metni kabul
   ediyorsa *uzun stil* bloğunu kullan; kabul etmiyorsa kısa sürümle devam et — her
   dosyada iki sürüm de var, kısa sürüm 200 karakterin altında tutuldu.
3. **Exclude styles** alanına dosyadaki hariç tutma satırını gir.
4. **Lyrics** alanına söz bloğunu köşeli parantezli etiketleriyle birlikte yapıştır.
   Etiketleri silme; bölüm geçişlerini onlar kuruyor.
5. Parça başına **4–6 varyasyon** üret, en iyisini seç.
6. **Tutarlılık:** 01 numaralı marşın onaylanan kaydından bir *Persona* oluştur ve 02–07'yi
   o Persona ile üret. Katalogun tek marka gibi duymasını sağlayan tek adım budur.
7. Kesitler için **stem** ayrıştırmasını kullan: 30/15/6 sn reklam kesitlerinde vokali
   koru, enstrümantali seslendirme altına yatır. Yeniden üretmek yerine kes.

### Stil alanı neden İngilizce?

Suno stil yönergelerini İngilizce daha isabetli yorumluyor; sözler Türkçe kalır. Bu
ayrım bilinçli: **stil = İngilizce, söz = Türkçe.**

### Türkçe telaffuz

Model Türkçe sözcükleri genelde doğru okur, ancak özel adlarda kayabilir. Kayarsa sözü
değiştirmeden **fonetik yazımla** yeniden dene:

| Yazım | Fonetik yedek |
|---|---|
| Boğaz | Boaz |
| Çengelköy | Chengelkoy |
| Kadıköy | Kadikoy |
| Beykoz | Beykoz (sorun çıkmıyor) |
| Kavacık | Kavajik |

Fonetik yedeği yalnızca üretim girdisinde kullan; yayımlanan söz metninde doğru yazım kalır.

## Dosya adlandırma (dışa aktarım)

```
florida-coffee_<parça-no>-<slug>_<sürüm>_<süre>.mp3
örn. florida-coffee_01-bogazda-bir-gun_v3_2m47s.mp3
```

Onaylanan kayıt `demo-site/audio/` altına, seçilmeyen varyasyonlar depoya girmez.

## Yayından önce kapatılacaklar

Sözlerde geçen marka bilgileri rapordaki **doğrulanmamış** verilerden geliyor. Müşteriyle
teyit edilmeden yayına alınmamalı:

- **"On yedi şube, iki ülke"** — rapor §2.2 şube sayısını 15–18 aralığında tahmin ediyor,
  liste müşteriden alınacak. Teyide kadar sayısız alternatif dizeler her dosyanın
  *Notlar* bölümünde duruyor.
- **"18–23 saniye" espresso standardı** — barista el kitabından geliyor, güncelliği teyit edilmeli.
- **Sadakat mekaniği** (çekirdek biriktirme, "beşincisi bizden") — 04 ve 03'te geçiyor;
  program kuralları netleşmeden mekaniği söyleyen dizeler yerine alternatifleri kullanılmalı.
- **FloridaDays** alt markasının rolü (§8.1) müşteriyle netleşmeden 04 numaralı parça
  kampanya adıyla yayımlanmamalı.

## Kullanım hakları

Suno'da üretilen kayıtların ticari kullanımı ücretli plana bağlı ve şartlar dönem dönem
değişiyor. Reklam yayını, mağaza içi çalma ve sosyal medya kullanımından önce:

1. Üretim P3Media'nın ticari kullanıma açık hesabından yapılmalı, kişisel hesaptan değil.
2. Suno'nun güncel kullanım şartları teklif tarihinde kontrol edilip müşteri sözleşmesine
   ek olarak konmalı.
3. Mağaza içi çalma ayrıca **MESAM/MÜ-YAP** kapsamına girebilir; yapay zekâ üretimi
   kayıtların durumu için hukuk danışmanına sorulmalı.
4. Teslimde müşteriye WAV + MP3, stem'ler ve bu dizindeki söz/stil dosyaları birlikte verilir.
