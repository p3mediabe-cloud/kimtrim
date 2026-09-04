# Florida Coffee — Web Sitesi ve Mobil Uygulama Ön Analiz Raporu

**Hazırlayan:** P3Media
**Tarih:** 4 Eylül 2026
**Müşteri:** Florida Coffee Kahve Gıda San. ve Tic. A.Ş. (Çengelköy, Üsküdar / İstanbul)
**Amaç:** Web sitesi + mobil uygulama teklifi öncesi; pazar, rakip, kitle, anahtar kelime, SEO, marka, kullanıcı, site yapısı, yapay zeka ve veri katmanı analizleri. Demo ve sunum bu rapora dayanacaktır.

---

## 0. Yönetici Özeti (2 dakikada)

1. **Florida Coffee dijitalde görünmez durumda.** Semrush Türkiye veritabanında site 208.967. sırada, yalnızca 33 organik anahtar kelimede listeleniyor ve ilk 10'da **sıfır** kelimesi var. Tahmini aylık organik trafik 287 ziyaret. Aynı ölçekteki rakip Espressolab 143.611, Kahve Dünyası 426.933 aylık organik ziyaret alıyor.
2. **Marka adı "Florida" coğrafi bir isim.** Google ve arama motorları markayı ABD'deki Florida kahvecileriyle karıştırıyor (bu raporda yaptığımız 40'tan fazla aramada sonuçların yarısı ABD sitelerine gitti). Bu, sözleşmenin 3.4 maddesinde de kabul edilen yapısal bir sorun ve **varlık (entity) SEO'su** ile çözülmesi gereken en kritik iş.
3. **Franchise sözleşmesi dijitali merkezileştiriyor.** Madde 7.2: franchise alan kendi web sitesi/sosyal medya hesabı açamaz (ceza 100.000 TL). Madde 7.4: önce fiziksel sadakat kartı, sonra mobil uygulama. Madde 6.32: mobil uygulama, yazılım, e-posta, e-fatura franchise alanın aylık gider kalemi. Bu, **tek merkezden yönetilen çok şubeli bir platform** (web + app + franchisee paneli) için doğrudan ticari gerekçe demek. Platform, HQ'ya ürün değil **gelir kalemi** olarak satılabilir.
4. **Şube hesapları dağınık.** Ana Instagram 4.046 takipçi; Kavacık, Yahyakaptan (1.176), Bahçeşehir gibi şube hesapları ayrı; Facebook 32 beğeni; Yandex Haritalar Çengelköy merkez şubesini "artık faal değil" olarak gösteriyor. Bu, sözleşme 7.2'nin bugün fiilen uygulanmadığını ve **NAP/işletme profili hijyeninin** acil olduğunu gösteriyor.
5. **Mevcut bir mobil uygulama var** (iOS id6504341925, Android `com.floridacoffeemobile`) ama görünürlüğü ve incelemesi yok denecek kadar az. Sıfırdan değil, "yeniden lansman ve sadakat + sipariş katmanı" olarak konumlandırılmalı.
6. **Pazar patlama halinde.** Türkiye kahve pazarı 2025'te 15 milyar TL (+%35), kişi başı tüketim 2026'da 2,2–2,5 kg'a gidiyor, 28.000+ kafe var, Starbucks boykotu yerli zincirlere talep kaydırdı. Doğru dijital altyapı ile Florida Coffee bu dalgayı franchise büyümesine çevirebilir.
7. **Kazanma stratejisi:** (a) Marka varlığını Google'da "Florida Coffee Türkiye" olarak sabitle, (b) her şube için yerel SEO sayfası + Google İşletme Profili disiplini, (c) tek uygulamada sadakat + ön sipariş + cüzdan, (d) franchise yatırımcısı için dönüşüm hunisi, (e) HQ'nun zaten topladığı otomasyon verisini (madde 6.23) yapay zeka ile talep tahmini ve kişiselleştirmeye çevir.

---

## 1. Metodoloji ve Veri Kısıtları

| Kaynak | Kullanım | Durum |
|---|---|---|
| Franchise sözleşmesi özet sunumları (2 PDF, 15 sayfa) | Marka yapısı, alt markalar, dijital yükümlülükler, gider kalemleri | Tam okundu |
| Semrush (TR veritabanı) | Domain sıralaması, organik kelime sayısı, trafik, SERP özellikleri | floridacoffee.com.tr, espressolab.com, kahvedunyasi.com çekildi; sonrasında **API birim bakiyesi sıfırlandı** (bkz. §1.1) |
| Web araması (45+ sorgu) | Şube listesi, sosyal medya, yorumlar, rakip uygulamalar, pazar verileri | Tamamlandı |
| Doğrudan site tarama | floridacoffee.com.tr, App Store, Google Play, Şikayetvar, Ekşi Sözlük, Yandex | **Ağ politikası nedeniyle engellendi** (egress proxy). İçerik, arama motoru özetleri üzerinden derlendi |

### 1.1 Eksik kalan ve teklif öncesi tamamlanması gereken veriler

- Semrush birimleri dolunca alınamayan raporlar: Florida Coffee'nin 33 organik kelimesinin listesi, backlink profili, rakip kelime boşluğu (keyword gap), Türkçe anahtar kelime hacimleri ve zorluk skorları. **Aksiyon:** Semrush hesabına birim yüklenince §6'daki 90 kelimelik liste tek çağrıyla doğrulanabilir; rapordaki hacimler bu nedenle "öncelik" olarak verildi, sayı olarak değil.
- Site teknik denetimi (Core Web Vitals, şema, hreflang, sitemap) yapılamadı; demo öncesi Lighthouse + Screaming Frog ile 1 saatte kapatılır.
- Google İşletme Profili yorum sayıları ve puanları şube bazında doğrulanmalı (Yandex verileri bulundu, Google verileri kısmen).
- Uygulama mağazası puanı ve indirme sayısı görülemedi; AppFigures/Sensor Tower ile alınmalı.

---

## 2. Kurum ve Marka Profili

### 2.1 Tüzel yapı (sözleşmeden)

| Alan | Bilgi |
|---|---|
| Ticari unvan | Florida Coffee Kahve Gıda Sanayi ve Ticaret A.Ş. |
| Sicil / Mersis | İstanbul 1007745 / 0388184298400001 |
| Merkez | Çengelköy Mah. Görgeç Sok. Mado No:6, Üsküdar / İstanbul |
| Tebligat e-posta | korhan@floridacoffee.com.tr (karar verici muhtemelen Korhan Bey) |
| Marka sınıfları | 30, 35, 43 (SMK tescilli) |
| Alt markalar | Florida Coffee, FloridaDays, Mi Florida, BİFLORİDA, Florida Plus |
| Çalışan sayısı | 50–74 (sayfa.istanbul / Kariyer.net) |
| Grup şirketleri | Yummy Cheese Pasta ("Türkiye'nin en büyük taze makarna fast food markası", 4 ülke 10 şehir), Amanos Döner (Kariyer.net ilanı) |
| Felsefe | "Mutluluğun Tadı" / "Taste of Joy" |
| Franchise modeli | 10 yıl, 3 km bölge koruması, aylık ciro %5 + KDV royalty, merkezi tedarik, 30 gün yönetici + 15 gün barista eğitimi |

### 2.2 Şube ağı (web araması ile derlenen; doğrulanmalı)

**İstanbul:** Çengelköy (merkez), Taksim Talimhane, Taksim Meydan, Kadıköy, Bahçeşehir, Beykoz (Kelle İbrahim Cad. 27, Boğaz manzaralı, 02:00'a kadar açık), Kavacık (FSM Cad. 42A), Ümraniye, Esenyurt
**Anadolu:** İzmit Yahyakaptan, Sakarya/Adapazarı Çark Caddesi (Cadde54 Florida Coffee Ltd. Şti. – SATSO kayıtlı), Bursa, Samsun (Marina/Atakum bölgesi Yummy ile ortak), Rize, Erzincan
**Yurt dışı:** Karadağ – Podgorica, Budva
**Yeni:** Sakarya Cumhuriyet Mah. Şal Sk. 20A (sözleşme konusu, Çark Caddesi şubesine ek/yenileme)

Toplam tahmini 15–18 nokta. Bu ölçek, Türkiye'de "orta boy yerli zincir" segmentine giriyor (Coffy'nin 3 yıl önceki ölçeği).

### 2.3 Mevcut dijital varlıklar

| Varlık | Durum | Not |
|---|---|---|
| floridacoffee.com.tr | Aktif; bilinen sayfalar: `/` ("Ana Sayfa"), `/about`, `/stores` ("Mağazalarımız") | İngilizce slug + Türkçe içerik; menü, franchise, blog, kariyer sayfası indekste görünmüyor |
| floridacoffee.com | Var (proxy nedeniyle doğrulanamadı) | .com/.com.tr tek kanonik domain'e yönlendirilmeli |
| iOS uygulaması | App Store id6504341925, geliştirici: Florida Coffee Kahve Gıda A.Ş. | Açıklama: "Birkaç dokunuşla favori kahvelerinizi ve atıştırmalıklarınızı sipariş edin" |
| Android uygulaması | `com.floridacoffeemobile` | Aynı açıklama; puan/indirme görülemedi |
| Instagram @floridacoffeetr | 4.046 takipçi, 137 gönderi, bio "Taste of Joy" | Rakipler: Espressolab 191K, Kahve Dünyası 327K, Coffy 20K |
| Şube Instagram hesapları | @floridacoffeekavacik, @floridayahyakaptan (1.176), @florida.bahcesehir | Sözleşme 7.2 ile çelişiyor; merkezi yönetime alınmalı |
| TikTok @floridacoffee_ | Aktif; şube listesi videoları | Takipçi sayısı görülemedi |
| Facebook /floridacoffeetr | 32 beğeni, 8 check-in | Fiilen ölü |
| LinkedIn "Florida Coffee Co." | Var | İşveren markası için kullanılmıyor |
| Yemeksepeti | En az 4 restoran kaydı (İstanbul x3, Kocaeli), min. sepet 300 TL | Getir/Trendyol Go kaydı bulunamadı |
| Şikayetvar | Sayfa var; 2025 sonu–2026 başı şikayetler | Marka yanıt vermiyor görünüyor |
| Yandex Haritalar | Beykoz 3,7 (9 oy), Kavacık 5,0 (13 oy), **Çengelköy "artık faal değil"** | Veri hijyeni sorunu |
| Ekşi Sözlük | Başlık var (#7826154) | İçerik görülemedi |

### 2.4 Sözleşmeden çıkan dijital gereksinimler (teklifin omurgası)

| Madde | Hüküm | Platform gereksinimi |
|---|---|---|
| 3.5 | Yazılım, reklam ajansı merkezden yönlendirilir | HQ onaylı tek tedarikçi = P3Media |
| 4 | Alan adları ve sosyal medya hesapları Franchise Veren'e aittir | Tüm dijital varlıklar HQ hesabında; şube kullanıcıları rol bazlı |
| 6.23 / 9.5 | Online otomasyon ile satış, ciro, stok, muhasebe HQ'ya açık | POS/otomasyon entegrasyonu; HQ dashboard; şube raporlama |
| 6.32 | Aylık: reklam ajansı, yazılım+sunucu, e-posta, e-fatura, **mobil uygulama** ücreti | SaaS abonelik modeli: şube başına aylık lisans |
| 7.1 | Ulusal reklam bütçesi ciro %1 | Kampanya yönetim modülü, ölçümleme |
| 7.2 | Franchise alan web/sosyal açamaz | Şube sayfaları merkezi sitede; sosyal içerik merkezi takvim |
| 7.3 | Ajans ile düzenli sosyal medya ve baskılı görsel | İçerik üretim + AI video (P3Media hizmeti) |
| 7.4 | Fiziksel sadakat kartı → mobil uygulama | Sadakat motoru, kart→app geçiş kampanyası |
| 8 | 30+15 gün eğitim | LMS / eğitim portalı (faz 2) |
| 9.3 | Gizli müşteri denetimi 900 TL/ay | Denetim raporu modülü, AI özetleme |
| 12.3 | Ciro eşiği altında kalma fesih sebebi | Şube performans erken uyarı sistemi |
| 13.2 | Belge iadesi, know-how gizliliği | Franchisee portalında erişim iptali, belge yönetimi |

---

## 3. Pazar Analizi

### 3.1 Büyüklük ve ivme

| Gösterge | Değer | Kaynak |
|---|---|---|
| Türkiye kahve pazarı (2025) | ~15 milyar TL, yıllık +%35 | Marketing Türkiye / Dünya |
| Kişi başı tüketim | 2010: 350–400 g → 2025: ~1,5 kg → 2026 tahmini 2,2–2,5 kg | Karar, Dünya |
| Kahve ithalatı (2025) | 125 bin ton, 909,2 milyon USD (+%82,9 değer) | Gıdatarım |
| Kafe sayısı | 28.000+ (2026) | Accio |
| Kahve zinciri sayısı | 130+ | DergiPark |
| Büyüme motoru | Zincir mağazalaşma, ev dışı tüketim, Z kuşağı, 3. dalga | Gıda Bülteni |

### 3.2 Zincir sıralaması (şube sayısı)

| Marka | Şube (ZAM Haber, 2026) | Şube (Gıda Bülteni, Nis 2025) | Konum |
|---|---|---|---|
| Starbucks | 755 | — | Boykot etkisiyle şube kapatıyor |
| Espressolab | 305 | 338 (Kas 2024: 229) | En hızlı büyüyen, 1M app kullanıcısı |
| Kahve Dünyası | 302 | 343 (Kas 2024: 268) | En güçlü e-ticaret + perakende |
| Gloria Jean's | 206 | 240+ | 50+ il, kendi kavurma tesisi |
| Arabica Coffee | 183 | — | — |
| Mackbear | 182 | — | Anadolu ağırlıklı, "Stay Wild" |
| Coffy | 131 | 200 (2026 hedefi 350) | Tek fiyat, dijital-öncelikli |
| Caffè Nero | 104 | — | Yoyo Wallet app |
| **Florida Coffee** | **~15–18** | — | Boğaz/İstanbul + Marmara + Karadağ |

### 3.3 Fırsat pencereleri

1. **Starbucks boykotu:** Şehir merkezi mağazaları kapanıyor; yerli algısı güçlü markalara talep kayıyor. Florida Coffee "İstanbul doğumlu, Boğaz manzaralı, yerli" hikayesini sahiplenebilir.
2. **Franchise talebi:** 2026'da 17 kahve zinciri 253 girişimci arıyor (Ekonomist); "kahve franchise" aramaları yatırımcı niyetli ve rakipler bu sayfalarda güçlü (Espressolab, Coffy başvuru formları). Florida Coffee'nin franchise sayfası indekste yok.
3. **Sakarya:** Espressolab'ın Sakarya'da 7 şubesi var; Kahve Dünyası Ada AVM, Serdivan AVM, Agora'da; Starbucks Serdivan AVM'de. Çark Caddesi cadde formatında zincir boşluğu var; Sakarya Üniversitesi (60.000+ öğrenci) yakın.
4. **Karadağ:** Türk zinciri olarak Adriyatik'te erken hareket; İngilizce/Karadağca site katmanı ve turist kitlesi.

---

## 4. Rakip Analizi

### 4.1 Dijital güç karşılaştırması (Semrush TR, Eylül 2026)

| Domain | Semrush Rank | Organik kelime | Aylık organik trafik | Trafik değeri (USD) | Top 3 kelime | 4–10 kelime |
|---|---|---|---|---|---|---|
| kahvedunyasi.com | 1.124 | 10.864 | 426.933 | 40.331 | 1.788 | 1.643 |
| espressolab.com | 2.708 | 3.141 | 143.611 | 13.036 | 214 | 422 |
| **floridacoffee.com.tr** | **208.967** | **33** | **287** | **0** | **0** | **0** |

Florida Coffee için ek SERP verisi: 14 kelimede yerel paket (local pack) tetikleniyor, 4 kelimede AI Overview çıkıyor, 4 kelime 11–20 arasında. Yani Google markayı **yerel işletme** olarak tanıyor ama site otorite üretmiyor. Coffy, Starbucks TR, Gloria Jean's, Caffè Nero, Mackbear, Arabica, Petra, Kocatepe verileri Semrush birim limiti nedeniyle alınamadı.

### 4.2 Ürün ve uygulama karşılaştırması

| Marka | Uygulama | Sadakat mekaniği | Ön sipariş | Cüzdan | E-ticaret | Franchise sayfası | Instagram |
|---|---|---|---|---|---|---|---|
| Espressolab | iOS+Android, 1M+ kullanıcı | O-Club 3 seviye (LabClassic/Plus/Premium), LabCoin, 15 coin = 12 oz kahve | "Gel Al" + "Bana Gönder" | Eslab Wallet (kredi/banka/yemek kartı) + QR ödeme | Çekirdek, Türk kahvesi, merch | Var, form | 191K |
| Kahve Dünyası | "Çekirdek Kazan" | Çekirdek puan, 1 puan = 1 TL | "Hazır Al" (Türkiye'de ilk uzaktan sipariş) | Var | Güçlü (çikolata, kahve, hediye) + atölye bileti | Var | 327K |
| Coffy | "Kahve Siparişi" | 5 kahveye 1 kahve, CoffyClub | "Gel Al" + "Ben Geldim" butonu | Hepsipay kampanyaları | Yok | Var, ayrı subdomain | 20K |
| Starbucks TR | Starbucks Türkiye | 15 yıldız = Tall içecek, hoş geldin içeceği, arkadaş davet 5 yıldız | Yok (TR) | Bakiye + QR "telefonu salla" | Yok | Yok | — |
| Gloria Jean's | Var | Öde/damga/kazan | — | — | Trendyol mağazası | Var | 62K |
| Caffè Nero | Yoyo Wallet tabanlı | Damga | — | Var | — | — | — |
| **Florida Coffee** | **Var, görünmez** | **Fiziksel kart planlı (7.4)** | **Belirsiz** | **Yok** | **Yok** | **Yok** | **4K** |

### 4.3 Rakip site yapıları (arama sonuçlarından derlenen)

- **Espressolab:** /kurumsal (kahve ve biz, franchising, kampanyalar), /commercial (ürünler, kullanıcı sözleşmesi), EN dil, Asia Pacific ayrı site. Güçlü yanı: kurumsal + ticaret ayrımı, hikâye anlatımı ("Topraktan Fincana").
- **Kahve Dünyası:** Tam e-ticaret (kategori sayfaları /kahve-c-40), blog (/blog/hazir-al…), SSS sayfası, uygulama tanıtımı, Romanya sitesi. Güçlü yanı: içerik derinliği ve kategori SEO'su (10.864 kelime).
- **Coffy:** Ana site + franchisefirsatlari.coffy.com.tr yatırımcı subdomain'i + /coffy-sana-gelsin app landing. Güçlü yanı: net dönüşüm hunileri.
- **Ortak zayıflık:** Hiçbiri şube bazlı zengin yerel sayfalar (menü, saat, manzara, park, çalışma alanı, etkinlik) üretmiyor; şube sayfaları genelde harita listesi. **Florida Coffee'nin fark yaratabileceği alan bu.**

### 4.4 Yerel rakipler (Sakarya / Çark Caddesi)

| Mekan | Tür | Not |
|---|---|---|
| Espressolab (7 şube: SEAH, Kampüs, Hendek, Akyazı, Karasu, Geyve, Kırkpınar) | Zincir | Üniversite ve ilçe kapsaması |
| Kahve Dünyası (Ada AVM, Serdivan AVM, Agora) | Zincir | AVM odaklı |
| Starbucks (Serdivan AVM) | Zincir | AVM |
| Safir Cafe (Çark Cad.) | Bağımsız | Foursquare 8.0, Türk kahvesi ve personel övgüsü |
| Saklı Bahçe (Çark Cad. 58) | Bağımsız | Bahçe konsepti |
| Kontrbus, Truck City 54 (Serdivan) | Bağımsız/konsept | Sosyal medya viral |

Sonuç: Çark Caddesi'nde "cadde tipi premium kahve zinciri" pozisyonu boş. Yerel SEO'da "çark caddesi cafe", "adapazarı kahveci", "sakarya çalışılacak kafe" kelimeleri düşük rekabetli.

### 4.5 Konumlandırma haritası

```
                 Premium / deneyim
                        ▲
     Petra, Kronotrop   │   Starbucks, Caffè Nero
     (3. dalga butik)   │   (global premium)
                        │
   ◄────────────────────┼────────────────────►
   Butik / az şube      │      Kitlesel / çok şube
                        │
     FLORIDA COFFEE     │   Espressolab, Kahve Dünyası
     (hedef: Boğaz      │   Gloria Jean's
      manzaralı,        │
      yerli premium)    │   Coffy, Mackbear
                        ▼   (uygun fiyat / tek fiyat)
                 Uygun fiyat / hız
```

Florida Coffee'nin savunulabilir konumu: **"İstanbul'un manzaralı köşelerinden doğan, SCA standardında kendi kavurduğu kahveyi ulaşılabilir premium fiyatla sunan yerli zincir."** Bu konum Espressolab ile Petra arasında ve rakipsiz.

---

## 5. Kitle ve Kullanıcı Analizi

### 5.1 Tüketici verileri

- Markalı kahve tüketiminde öncü gruplar: **kadınlar, 18–24 yaş, öğrenciler, orta-üst gelir** (Ipsos hane paneli / DergiPark).
- Kafe tercih faktörleri sırasıyla: **tat ve sunum → makul fiyat → servis kalitesi ve hızı → çeşitlilik → hijyen** (Antalya araştırması); İstanbul araştırmasında **menüde diğer içecekler, hijyen, çeşitlilik, personel kalitesi**.
- Ziyaret sıklığı: ayda birkaç kez; tercih edilen zincirler ağırlıklı **yerli**.
- Büyüyen segmentler: **içime hazır soğuk kahve**, çekirdek/kapsül kahve (evde tüketim), üçüncü dalga.

### 5.2 Persona seti

| # | Persona | Profil | Aradığı şey | Dijital tetikleyici | Öncelikli kanal |
|---|---|---|---|---|---|
| 1 | **Zeynep, 21, SAÜ öğrencisi (Sakarya)** | Günde 1 kahve, bütçe hassas, arkadaşlarıyla çalışır | Uygun fiyat, priz/Wi-Fi, uzun oturma, kampanya | "sakarya çalışılacak kafe", Instagram reels, 5'e 1 kampanya | App sadakat + TikTok |
| 2 | **Emre, 29, plaza çalışanı (Kadıköy/Taksim)** | Sabah ve öğle, hız ister | Ön sipariş, sıra beklememe, cüzdan | "yakınımdaki kahveci", app push | App ön sipariş |
| 3 | **Selin & Can, 34–40, hafta sonu çifti (Beykoz/Çengelköy)** | Manzara, kahvaltı, tatlı | Rezervasyon, manzara fotoğrafı, park bilgisi | "boğaz manzaralı cafe beykoz", Google Haritalar | Web şube sayfası + GBP |
| 4 | **Ahmet, 45, yatırımcı** | Franchise arıyor, 2–5 M TL bütçe | Şeffaf yatırım tablosu, geri dönüş süresi, referans şube | "kahve franchise", "bayilik veren kahve markaları", LinkedIn | Web franchise hunisi + CRM |
| 5 | **Mira, 27, turist (Budva)** | Türk kahvesi ve Boğaz hikayesi merak eder | EN menü, Google Maps, Instagram-able | "coffee Budva", TripAdvisor | EN site + GBP |
| 6 | **Deniz, 24, şube müdürü (iç kullanıcı)** | HQ raporlaması, eğitim, sipariş | Tek panel, mobil uyumlu | Sözleşme 6.23, 8, 9 | Franchisee portalı |
| 7 | **Korhan Bey, HQ yönetimi** | Ciro, royalty, denetim, marka kontrolü | Gerçek zamanlı dashboard, uyarı | Sözleşme 12.3 (ciro eşiği) | HQ admin |

### 5.3 Şikayetlerden çıkan kullanıcı içgörüleri (Şikayetvar, 2025–2026)

| Şikayet | Kök neden | Dijital çözüm |
|---|---|---|
| Soğuk istenen kahve sıcak bardakta geldi | Sipariş modifikasyonu kaybı | App'te zorunlu "sıcak/soğuk/buz" seçici, POS'a yapısal aktarım |
| Laktozsuz süt isteği uygulanmadı | Özel istek takibi yok | Alerjen/süt tercihi profilde kayıtlı; barista ekranında vurgulu |
| Sulu/dengesiz tat, 215 TL ice white mocha'da parçacık (İzmit) | Standart dışı hazırlık, denetim boşluğu | Gizli müşteri + yorum sentimentini AI ile şube skoruna bağla |
| Kağıt bardak ıslanıp yırtıldı | Tedarik kalitesi | Merkezi tedarik geri bildirim modülü |
| Fiyat yüksek algısı (Beykoz) | Değer iletişimi zayıf | Sadakat, kampanya, manzara/deneyim vurgusu |
| Marka yanıt vermiyor | Yorum yönetimi yok | Tüm platform yorumlarını tek gelen kutusunda topla, AI taslak yanıt |

### 5.4 İşler (Jobs-to-be-Done)

1. "Sabah işe giderken sıra beklemeden kahvemi alayım" → ön sipariş + cüzdan.
2. "Yakınımdaki en iyi manzaralı kafeyi bulayım" → şube sayfası + GBP + fotoğraf.
3. "Her kahvede biriktirip bedava kahve kazanayım" → sadakat.
4. "Evde de aynı kahveyi içeyim" → çekirdek e-ticareti (faz 2).
5. "Bu markanın franchise'ını alabilir miyim?" → yatırımcı hunisi.
6. "Şubemi HQ'ya raporlayayım, eğitimi tamamlayayım" → franchisee portalı.

---

## 6. Anahtar Kelime Analizi

> Hacim ve zorluk skorları Semrush birim limiti nedeniyle çekilemedi. Aşağıdaki liste niyet, hedef sayfa ve öncelik olarak verildi; birim yüklenince `phrase_these` raporu ile tek seferde doğrulanır. Öncelik: **A** = ilk 90 gün, **B** = 3–6 ay, **C** = 6–12 ay.

### 6.1 Marka ve varlık kümesi (A)

| Kelime | Niyet | Hedef sayfa | Not |
|---|---|---|---|
| florida coffee | Navigasyonel | Ana sayfa | ABD sonuçlarıyla karışıyor; entity SEO şart |
| florida coffee türkiye | Navigasyonel | Ana sayfa | Marka adı standardı bu olmalı |
| florida coffee menü / fiyat | Ticari | /menu | Şu an rakip site yok, hızlı kazanım |
| florida coffee şubeleri | Navigasyonel | /subeler | |
| florida coffee çengelköy / beykoz / kadıköy / taksim / kavacık / bahçeşehir / ümraniye / esenyurt / izmit / sakarya / adapazarı / bursa / samsun / rize / erzincan | Yerel | /subeler/{sube} | 15+ sayfa |
| florida coffee franchise / bayilik | Ticari (B2B) | /franchise | |
| florida coffee uygulama / app | Navigasyonel | /uygulama | |
| florida coffee kavacık boğaz manzara | Yerel | /subeler/kavacik | |
| floridadays / mi florida / biflorida / florida plus | Navigasyonel | Alt marka sayfaları | Marka mimarisi kararına bağlı |

### 6.2 Yerel keşif kümesi (A)

| Kelime | Niyet | Hedef sayfa |
|---|---|---|
| yakınımdaki kahveci / en yakın kahveci / yakınımdaki cafe | Yerel | GBP + /subeler |
| çengelköy cafe, çengelköy kahvaltı, çengelköy kahve | Yerel | /subeler/cengelkoy |
| beykoz cafe, boğaz manzaralı cafe beykoz, kavacık cafe, gece açık cafe beykoz | Yerel | /subeler/beykoz, /subeler/kavacik |
| kadıköy kahveci, kadıköy çalışılacak kafe, moda cafe | Yerel | /subeler/kadikoy |
| taksim cafe, talimhane cafe, taksim kahve | Yerel | /subeler/taksim-* |
| bahçeşehir cafe, esenyurt cafe, ümraniye cafe | Yerel | ilgili şube |
| adapazarı cafe, sakarya cafe, çark caddesi cafe, sakarya çalışılacak kafe, adapazarı kahveci, serdivan cafe | Yerel | /subeler/sakarya-cark |
| izmit cafe, yahyakaptan cafe, kocaeli kahveci | Yerel | /subeler/izmit |
| bursa cafe, samsun cafe, atakum cafe, rize cafe, erzincan cafe | Yerel | ilgili şube |
| coffee shop Budva, kafić Podgorica, turkish coffee Montenegro | Yerel (EN/ME) | /en/stores/* |

### 6.3 Ürün kümesi (A/B)

| Kelime | Niyet | Hedef sayfa |
|---|---|---|
| filtre kahve, latte, cappuccino, americano, flat white, espresso, cortado | Ticari/bilgi | /menu/{urun} |
| cold brew, soğuk kahve, buzlu kahve, iced latte, frappe | Ticari | /menu/soguk-kahveler |
| türk kahvesi, dibek kahvesi, menengiç | Ticari | /menu/turk-kahvesi |
| matcha latte, chai latte, sıcak çikolata, limonata | Ticari | /menu/kahve-disi |
| kahve yanına tatlı, cheesecake, san sebastian, kruvasan | Ticari | /menu/tatlilar |
| laktozsuz süt kahve, bitkisel süt latte, yulaf sütlü latte | Ticari (niş) | /menu (filtre) |
| kalori latte, kahvede kafein miktarı | Bilgi | Ürün sayfası besin tablosu |

### 6.4 Franchise / B2B kümesi (A)

| Kelime | Niyet |
|---|---|
| kahve franchise, kahve bayilik, kahve bayiliği veren firmalar, coffee shop franchise |
| kahve dükkanı açmak, kahve dükkanı açmak maliyeti, kafe açmak ne kadar |
| en karlı kahve franchise, kahve franchise karşılaştırma 2026 |
| franchise veren kahve markaları, yerli kahve zinciri franchise |
| espressolab franchise bedeli, coffy franchise, kahve dünyası franchise bedeli (karşılaştırma içerikleri) |
| sakarya franchise, bursa franchise, samsun franchise fırsatları (bölgesel) |

### 6.5 Bilgi / blog kümesi (B/C)

| Konu | Örnek kelimeler |
|---|---|
| Demleme | v60 nasıl yapılır, chemex, aeropress, french press oranı, cold brew nasıl yapılır |
| Çekirdek | arabica robusta farkı, kahve çekirdeği nasıl saklanır, single origin nedir, kavurma dereceleri |
| Kültür | türk kahvesi tarihi, kahve falı, dünya kahve günü |
| Sağlık | kahve kafein miktarı, hamilelikte kahve, kahve ve uyku |
| Yaşam | çalışılacak kafeler istanbul, boğaz manzaralı kafeler, kahvaltı mekanları çengelköy |
| Kariyer | barista nasıl olunur, barista maaşları, sca sertifikası |

### 6.6 Uygulama kümesi (B)

kahve sipariş uygulaması, kahve sadakat uygulaması, bedava kahve uygulaması, ön sipariş kahve, kahve cüzdan uygulaması, kahve puan biriktirme.

### 6.7 Sorgu niyet dağılımı (öneri)

- %35 yerel, %25 ürün, %15 marka, %15 franchise, %10 bilgi. Franchise kümesi düşük hacim ama en yüksek ticari değer (1 dönüşüm = 10 yıllık royalty).

---

## 7. SEO Analizi ve Strateji

### 7.1 Mevcut durum teşhisi

| Alan | Bulgu | Etki |
|---|---|---|
| Otorite | Semrush Rank 208.967; organik trafik değeri 0 USD | Google için "önemsiz site" |
| İndeks kapsamı | 3 sayfa bilinir (ana, about, stores); menü/franchise/blog yok | Ürün ve B2B niyetlerinde hiç görünmüyor |
| Başlıklar | "Florida Coffee \| Ana Sayfa", "Florida Coffee \| Mağazalarımız" | Anahtar kelime ve konum sinyali yok |
| URL | İngilizce slug (/about, /stores) + Türkçe içerik | Dil tutarsızlığı; hreflang yok |
| Yerel | 14 kelimede local pack | GBP çalışıyor, site desteklemiyor |
| AI Overview | 4 kelimede | GEO fırsatı var |
| Varlık karışıklığı | "Florida coffee" sorguları ABD'ye gidiyor | Marka aramalarında bile kayıp |
| Yorum yönetimi | Şikayetvar yanıt yok; Yandex'te merkez "kapalı" | Güven ve yerel sıralama kaybı |
| Domain | .com ve .com.tr; kanonik belirsiz | Otorite bölünmesi |
| Backlink | Alınamadı (tahmin: çok düşük) | Otorite inşası gerek |

### 7.2 Teknik SEO hedefleri (yeni site)

| Metrik | Hedef | Gerekçe |
|---|---|---|
| LCP | < 2,0 s (mobil) | Google 2026 "iyi" eşiği 2,0 s'ye indi |
| INP | < 200 ms | 200 ms üstü sıralama kaybı |
| CLS | < 0,1 | Menü görselleri için sabit boyut |
| Lighthouse mobil | ≥ 90 | Restoran siteleri için 2026 standardı |
| Render | SSR/SSG (Next.js) | Menü ve şube sayfaları indekslenebilir HTML |
| Görsel | AVIF/WebP, CDN, lazy | Menü fotoğrafları ağır |
| Sitemap | Ürün, şube, blog, EN ayrı sitemap index | |
| hreflang | tr-TR, en, sr-ME (Karadağ) | |
| Kanonik | floridacoffee.com.tr ana; .com 301 | Yurt dışı büyürse .com'a geçiş planı |

### 7.3 Yapılandırılmış veri planı

| Şema | Sayfa | Alanlar |
|---|---|---|
| Organization + Brand | Ana | sameAs (IG, TikTok, LinkedIn, App Store, Play, Wikidata), logo, founder, foundingLocation |
| CafeOrCoffeeShop (LocalBusiness) | Her şube | address, geo, openingHoursSpecification, telephone, hasMenu, servesCuisine, amenityFeature (Wi-Fi, manzara, otopark, priz), priceRange, aggregateRating |
| Menu / MenuSection / MenuItem | /menu | nutrition, suitableForDiet (laktozsuz, vegan), offers.price |
| MobileApplication | /uygulama | operatingSystem, aggregateRating, downloadUrl |
| FAQPage | Franchise, SSS | GEO ve AI Overview için |
| JobPosting | Kariyer | Google İşler |
| Event | Şube etkinlik (dans grubu performansı, madde 7.3) | |
| BreadcrumbList | Tüm | |
| Article + Person (yazar) | Blog | E-E-A-T |

### 7.4 Yerel SEO ve işletme profili disiplini

1. **NAP tek kaynak:** Site şube sayfası = GBP = Yandex = Apple Maps = Yemeksepeti = Foursquare. Merkezden yönetilen "şube veri kaydı" (bkz. §12).
2. **Yandex Çengelköy "faal değil" düzeltmesi** ilk hafta.
3. Her şube için GBP: birincil kategori "Kafe", ikincil "Kahve dükkanı", "Kahvaltı restoranı"; ürün kataloğu; haftalık gönderi; Q&A tohumlama; fotoğraf standardı (manzara, iç mekan, menü, ekip).
4. Yorum toplama: fiş QR + app push ile "yorum bırak" (Google, Yandex, TripAdvisor Budva için); 24 saat içinde yanıt.
5. Yerel atıflar: Sakarya için medyabar, sakaryaburada; İstanbul için beykozguncel, timeout; franchise portalları (bayilikariyorum, bayilikyatirim, franchiseborsasi, bayimolurmusun) — hem backlink hem lead.

### 7.5 Varlık (entity) SEO: "Florida" sorunu

- Tüm dijital varlıklarda tutarlı ad: **"Florida Coffee Türkiye"** (İngilizce: "Florida Coffee Turkey/Türkiye").
- Wikidata öğesi oluştur (kahve zinciri, kuruluş İstanbul, kurucu, alt markalar) → Google Knowledge Panel.
- Site başlıkları ve Organization şemasında `alternateName`: "Florida Coffee Co.", "Florida Kahve".
- Basın: Marketing Türkiye, Food in Life, Gıda Bülteni, Franchise Market'te "İstanbul doğumlu Florida Coffee Karadağ'a açıldı" gibi haberler; her biri entity sinyali ve backlink.
- Sosyal profillerin biyografilerinde "İstanbul, Türkiye" konumu ve site linki.

### 7.6 GEO (Generative Engine Optimization)

- 2026'da Google aramalarının yaklaşık yarısı AI Overview tetikliyor; Florida Coffee 4 kelimede zaten görünüyor.
- Her şube sayfasında "Soru-cevap" bloğu ("Beykoz Florida Coffee kaça kadar açık?", "Otopark var mı?", "Laktozsuz süt var mı?") + FAQPage şeması.
- Menü sayfalarında tablo formatında besin/fiyat (LLM'ler tablo sever).
- "Hakkımızda" metni doğrudan cevaplar içermeli: kuruluş yılı, şube sayısı, kavurma, SCA.
- llms.txt ve açık, kısa özet paragraflar.

### 7.7 İçerik takvimi (ilk 6 ay)

| Ay | Çıktı |
|---|---|
| 1 | 15 şube sayfası, menü (40+ ürün sayfası), franchise hunisi, uygulama sayfası |
| 2 | 8 blog (demleme + yaşam), SSS, kariyer |
| 3 | "İstanbul'un en manzaralı kahve durakları" rehberi, Sakarya rehberi, franchise karşılaştırma yazısı |
| 4–6 | Ayda 6 blog, sezonluk menü sayfaları (yaz soğuk kahve, kış sıcak çikolata), EN/ME sayfalar |

### 7.8 Hedef KPI (12 ay)

| KPI | Bugün | 6 ay | 12 ay |
|---|---|---|---|
| Organik kelime (TR) | 33 | 600 | 2.000 |
| Top 10 kelime | 0 | 120 | 400 |
| Aylık organik ziyaret | 287 | 8.000 | 30.000 |
| Semrush Rank | 208.967 | < 60.000 | < 20.000 |
| Şube GBP ort. puan | ~4,2 | 4,5 | 4,6 |
| Franchise formu / ay | 0 (ölçülmüyor) | 15 | 40 |
| App aktif kullanıcı | ? | 15.000 | 60.000 |

---

## 8. Kurumsal Kimlik ve Marka Analizi

### 8.1 Marka mimarisi

| Marka | Muhtemel rol | Öneri |
|---|---|---|
| Florida Coffee | Ana marka, kafe | Master brand; tüm dijital "Florida Coffee Türkiye" |
| FloridaDays | Kampanya/etkinlik veya sadakat günü? | Sadakat programının adı olarak kullanılabilir ("FloridaDays Club") |
| Mi Florida | Perakende ürün (çekirdek/kapsül) veya kişisel sadakat? | E-ticaret ve "benim Florida'm" kişiselleştirme katmanı |
| BİFLORİDA | Tek fiyat / hızlı format? | Coffy tarzı ekonomik alt format olabilir |
| Florida Plus | Premium seviye / üyelik? | Sadakat üst seviyesi (Espressolab LabPremium karşılığı) |

Bu roller müşteriyle netleştirilmeli (keşif sorusu). Öneri: **Master brand + endorsed alt markalar**; alt markalar sitede `/floridadays`, `/mi-florida` gibi sayfa değil, **program/ürün adı** olarak yaşamalı ki otorite bölünmesin.

### 8.2 Marka vaadi ve boşluk

- Vaat: "Mutluluğun Tadı / Taste of Joy", "İstanbul'un en keyifli köşeleri", SCA standardı, kendi kavurma.
- Algı: Boğaz manzarası ve ferah mekan övgüsü (Beykoz, Kadıköy), ama fiyat yüksek ve kalite tutarsız şikayetleri.
- Boşluk: **Vaat deneyime bağlı, ürüne değil.** Dijitalde "manzara + huzur + kahve ritüeli" hikayesi anlatılmalı; standardizasyon şikayetleri operasyon ve app doğruluğu ile kapatılmalı.

### 8.3 Kurumsal kimlik denetim listesi (demo öncesi müşteriden istenecek)

- Logo dosyaları (SVG), yatay/dikey/monogram, negatif kullanım
- Renk paleti (HEX/Pantone), tipografi (lisans durumu)
- Fotoğraf dili (manzara, ürün, insan)
- Bardak/ambalaj tasarımları (madde 6.5 merkezi ambalaj)
- Kurumsal kimlik kılavuzu (madde 2'de "Franchise Alan ne alır" içinde geçiyor; var demek)
- Ton: samimi/premium; TR/EN karşılıkları

### 8.4 Sosyal medya değerlendirmesi

- Takipçi ölçeği rakiplerin 1/50'si; ancak şube ağı dağınık hesaplarla bölünmüş.
- Öneri: Tek marka hesabı + şube etiketli içerik + "konum" (Instagram Locations) sahipliği; şube hesapları kapatılmaz, **"Florida Coffee | Kavacık" formatıyla merkezi yönetime** alınır (madde 4: hesaplar Franchise Veren'e ait).
- İçerik pillar: Manzara/mekan, ürün/tarif, barista/insan, kampanya/sadakat, franchise başarı hikayesi, Karadağ.
- P3Media AI video: haftalık 3 kısa video (ürün, mekan, kampanya) merkezi üretim, şube adaptasyonu otomatik (madde 7.3 ajans yükümlülüğü).

---

## 9. Site Yapısı (Bilgi Mimarisi)

### 9.1 Site haritası

```
floridacoffee.com.tr
├── / (Ana sayfa: manzara hero, "en yakın Florida", menü öne çıkanlar, app CTA, franchise CTA)
├── /menu
│   ├── /menu/sicak-kahveler        (espresso bazlı, filtre, türk kahvesi)
│   ├── /menu/soguk-kahveler        (cold brew, iced, frappe)
│   ├── /menu/kahve-disi            (matcha, çay, sıcak çikolata, limonata)
│   ├── /menu/yiyecekler            (kahvaltı, sandviç, tatlı)
│   ├── /menu/sezon                 (yaz/kış)
│   └── /menu/{urun-slug}           (ürün detay: fotoğraf, boy/fiyat, besin, alerjen, süt seçenekleri, "app'te sipariş et")
├── /subeler                         (harita + liste + filtre: manzara, gece açık, otopark, çalışma alanı)
│   └── /subeler/{sehir}/{sube}      (NAP, saat, fotoğraf, özellikler, menü özeti, yorumlar, SSS, yol tarifi, "ön sipariş ver")
├── /uygulama                        (özellikler, sadakat mekaniği, mağaza linkleri, QR, kart→app geçiş)
├── /sadakat (FloridaDays Club)      (seviye, kazanım, SSS)
├── /kampanyalar                     (aktif kampanyalar; şube filtreli)
├── /kahvemiz                        (kavurma, çekirdek kaynağı, SCA, barista eğitimi, sürdürülebilirlik)
├── /hikayemiz                       (kuruluş, Çengelköy, ekip, Karadağ)
├── /franchise
│   ├── /franchise/neden-florida     (rakamlar, destekler: 3 km koruma, eğitim, merkezi tedarik)
│   ├── /franchise/yatirim           (yatırım aralığı, süre, süreç adımları, SSS)
│   ├── /franchise/basari-hikayeleri (şube röportajları)
│   └── /franchise/basvuru           (çok adımlı form → CRM)
├── /kurumsal                        (kurumsal satış, etkinlik, catering, hediye kartı)
├── /blog
│   ├── /blog/demleme, /blog/kahve-kulturu, /blog/mekan-rehberi, /blog/haberler
│   └── /blog/{yazi}
├── /kariyer                         (JobPosting şeması, barista/müdür ilanları)
├── /sss
├── /iletisim
├── /yasal (KVKK, çerez, mesafeli satış, kullanıcı sözleşmesi)
├── /en/... (EN yansıması; menü, stores, franchise, story)
└── /me/... (Karadağ: Podgorica, Budva; sr-ME/EN)

Gizli/uygulama alanları:
├── portal.floridacoffee.com.tr      (Franchisee portalı)
├── admin.floridacoffee.com.tr       (HQ yönetim)
└── api.floridacoffee.com.tr         (Headless API: web + app + POS)
```

### 9.2 Ana sayfa bölüm sırası (dönüşüm odaklı)

1. Hero: Boğaz manzaralı video/AI video, "Mutluluğun Tadı, en yakın Florida'da" + konum izni ile en yakın şube kartı
2. Hızlı aksiyon: "Ön sipariş ver" / "Menüyü gör" / "Uygulamayı indir"
3. Öne çıkan ürünler (sezon)
4. Şube vitrini (manzara filtreli)
5. Sadakat teaser (ilk kahve hediye)
6. Kahvemiz (SCA, kavurma) + sosyal kanıt (Google puanı, yorum sayısı)
7. Franchise CTA ("17 şube, 2 ülke, siz de katılın")
8. Blog/İçerik
9. Footer: NAP, sosyal, app, yasal, dil

### 9.3 Şube sayfası şablonu (fark yaratan sayfa)

- H1: "Florida Coffee Kavacık — Boğaz Manzaralı Kahve, Beykoz"
- Özellik rozetleri: manzara, gece 02:00, Wi-Fi, priz, otopark, evcil dostu, çalışma alanı, çocuk alanı
- Fotoğraf galerisi (sabah/gün batımı)
- Menü özeti + şubeye özel ürünler
- Canlı: bugünkü saatler, yoğunluk (POS verisinden "şu an sakin/yoğun")
- Yorumlar (Google+Yandex çekilmiş, şema ile)
- SSS (5 soru)
- Harita + "Yol tarifi al" + "Bu şubeden ön sipariş ver"
- Yakın şubeler
- Etkinlik takvimi (madde 7.3 dans performansı vb.)

---

## 10. Mobil Uygulama Analizi ve Özellik Seti

### 10.1 Mevcut uygulama değerlendirmesi

Mağaza açıklaması "birkaç dokunuşla sipariş" diyor ama sadakat, cüzdan, kampanya vurgusu yok; arama sonuçlarında puan/inceleme görünmüyor; site uygulamaya link vermiyor. Sözleşme 7.4 "önce fiziksel kart" diyor, yani sadakat henüz app'te değil. **Karar: mevcut uygulamayı "v2 relaunch" olarak konumlandırmak** (aynı mağaza kaydı, indirme geçmişi korunur).

### 10.2 MVP (lansman) özellikleri

| Modül | Özellik | Rakip referans |
|---|---|---|
| Kimlik | Telefon OTP, Apple/Google ile giriş, KVKK onayı | Tümü |
| Sadakat | Puan (1 TL = 1 çekirdek), 10 kahveye 1 kahve, doğum günü içeceği, fiziksel kart QR ile bakiye aktarma | KD "Çekirdek", Espressolab LabCoin |
| Seviye | FloridaDays Club: Classic / Plus / Premium (6 aylık harcama) | Espressolab O-Club |
| Cüzdan | Bakiye yükleme (kredi/banka/yemek kartı: Multinet, Sodexo, Setcard), yüklemede bonus, QR ödeme | Eslab Wallet |
| Ön sipariş | Şube seç → menü → modifikasyon (boy, süt, şurup, sıcak/soğuk, şeker) → ödeme → "Geldim" butonu | Coffy "Ben Geldim", KD "Hazır Al" |
| Şubeler | Harita, filtre, saat, yoğunluk, favori şube | |
| Kampanyalar | Şube/segment hedefli, push, kupon | |
| Favoriler | "Her zamanki" tek dokunuş sipariş | |
| Bildirim | Push (sipariş hazır, kampanya, seviye), SMS yedek | |
| Hediye | Arkadaşa kahve gönder, hediye kartı | KD |
| Geri bildirim | Sipariş sonrası 1 dokunuş puan + yorum yönlendirme | |

### 10.3 V2 (3–6 ay)

- "Bana Gönder" teslimat (Yemeksepeti/Getir API veya kendi kurye)
- E-ticaret: çekirdek, kapsül, merch (Mi Florida)
- AI barista önerisi (bkz. §11)
- Abonelik (aylık sınırsız filtre kahve; Panera/Pret modeli)
- Sosyal: "kafede kim var" (Eslab Finder) — opsiyonel
- Karadağ: EUR, EN/ME dil, yerel ödeme

### 10.4 Teknoloji önerisi

| Katman | Seçim | Gerekçe |
|---|---|---|
| Mobil | Flutter veya React Native (tek kod, iOS+Android) | Hız, maliyet; mevcut mağaza kayıtları korunur |
| Web | Next.js (SSR/ISR), Tailwind | SEO + hız |
| CMS | Headless (Strapi/Payload veya Sanity) | Menü/şube/kampanya tek kaynak; web+app+kiosk |
| Backend | Node/NestJS veya Supabase (Postgres, Auth, Edge Functions) | Hızlı MVP; RLS ile şube izolasyonu |
| Ödeme | iyzico veya PayTR + yemek kartı entegrasyonları + Hepsipay kampanya | TR uyumlu |
| POS | Adisyo / Menulux / Simpra / robotPOS API (HQ'nun mevcut "online otomasyon"u belirlenmeli) | Madde 6.23 |
| E-fatura | Paraşüt / Logo / entegratör | Madde 6.32 |
| Bildirim | Firebase, OneSignal | |
| Analitik | GA4 + server-side tagging, Mixpanel/PostHog (app) | |
| Harita | Google Maps + Yandex (TR kullanıcı alışkanlığı) | |
| Altyapı | Vercel + Supabase/AWS eu-central; KVKK için TR veri lokasyonu değerlendirilmeli | |
| AI | Claude API (öneri, içerik, sentiment, sohbet) | §11 |

### 10.5 Franchisee portalı ve HQ admin (sözleşme yükümlülükleri)

| Sözleşme | Portal modülü |
|---|---|
| 6.23 aylık ciro bildirimi | Otomatik POS çekimi + onay; manuel form yedek |
| 6.32 aylık giderler | Fatura/abonelik görünümü |
| 7.1 reklam bütçesi %1 | Kampanya katkı hesaplaması |
| 8 eğitim | Video LMS, sınav, sertifika |
| 9 denetim | Denetim raporu, eksik listesi, kapatma süresi sayacı |
| 9.3 gizli müşteri | Rapor yükleme, AI özet, şube skoru |
| 12.3 ciro eşiği | Erken uyarı (3 ay trend) |
| 6.4 tedarik | Merkezi sipariş formu, 40 gün vade takibi |
| 13.2 belge iadesi | Belge kütüphanesi, erişim iptali |
| HQ | Tüm şube dashboard: ciro, royalty, sadakat, yorum puanı, kampanya ROI, franchise lead pipeline |

Bu portal, sözleşmede "yazılım ve sunucu (yıllık)" ve "mobil uygulama" kalemleri olarak zaten franchise alana faturalanıyor. **Teklif: şube başına aylık SaaS lisansı** + HQ kurulum bedeli.

---

## 11. Yapay Zeka Entegrasyon Analizi

| # | Kullanım | Veri kaynağı | Değer | Faz | Zorluk |
|---|---|---|---|---|---|
| 1 | **AI barista önerisi** ("bugün hava 30°, geçen sefer iced latte aldın, cold brew dener misin?") | Sipariş geçmişi, hava, saat, şube stoğu | Sepet +%10–15 (Starbucks Deep Brew referansı: +%12 ortalama sipariş) | V1.5 | Orta |
| 2 | **WhatsApp / Instagram DM sipariş ve destek asistanı** | Menü, şube, sadakat API | 7/24 destek, şikayet erken yakalama | V1 | Düşük |
| 3 | **Yorum sentiment ve otomatik yanıt taslağı** (Google, Yandex, Şikayetvar, app) | Yorum API'leri | Şube kalite skoru, madde 9 denetim girdisi | V1 | Düşük |
| 4 | **Talep tahmini ve stok** (şube × saat × ürün) | POS (madde 6.23), hava, takvim | Fire azalması, tedarik siparişi otomasyonu | V2 | Orta |
| 5 | **Personel vardiya önerisi** | Talep tahmini | Personel maliyeti ±%15 bandı (madde 6.16) | V2 | Orta |
| 6 | **SEO/GEO içerik motoru** (şube SSS, blog taslağı, meta) | CMS | 15 şube × 5 SSS × 2 dil otomatik | V1 | Düşük |
| 7 | **Gizli müşteri raporu özetleme ve trend** | PDF/form | HQ zaman tasarrufu, 3 uyarı kuralı takibi | V1 | Düşük |
| 8 | **Franchise lead skorlama** | Form, LinkedIn, bölge verisi | Satış ekibi önceliklendirme | V1 | Düşük |
| 9 | **Dinamik kampanya** (şube yoğunluğu düşükken push "14:00–16:00 %20") | POS + app | Ölü saat doluluğu | V2 | Orta |
| 10 | **AI video ve görsel üretimi** (P3Media) | Ürün fotoğrafı | Haftalık içerik maliyeti düşer | V1 | Düşük |
| 11 | **Sesli sipariş / kiosk** | Menü | Taksim, AVM formatları | V3 | Yüksek |
| 12 | **Kalite kontrol görsel analizi** (kamera, madde 6.23) | Kamera | Standart dışı sunum uyarısı | V3 | Yüksek (KVKK) |
| 13 | **Menü lokalizasyonu** (Karadağ fiyat/dil) | CMS | EN/ME otomatik | V1 | Düşük |
| 14 | **Ciro eşiği erken uyarı** (madde 12.3) | POS | Fesih riski öncesi müdahale | V1 | Düşük |

Yönetişim: KVKK aydınlatma, açık rıza (öneri kişiselleştirme), yorum yanıtlarında insan onayı, kamera analizi için ayrı hukuki görüş.

---

## 12. Genişletilmiş Bilgi Yükleme (Veri ve Bilgi Tabanı) Analizi

Web, app, GBP, AI asistan ve GEO'nun tamamı **tek doğru veri kaynağından** beslenmeli. Toplanacak ve yapılandırılacak veri:

| Varlık | Alanlar | Kullanım |
|---|---|---|
| Şube | ad, kod, adres (yapısal), geo, telefon, saatler (istisna günler), özellikler (manzara, Wi-Fi, priz, otopark, teras, gece), fotoğraf seti, yöneticisi, açılış tarihi, POS ID, GBP ID, Yandex ID, Yemeksepeti ID, sosyal konum ID | Şube sayfası, app, NAP senkron, şema |
| Ürün | ad TR/EN, kategori, açıklama, boylar/fiyat (şube grubu bazlı), besin (kcal, kafein), alerjen, süt seçenekleri, sezon, görsel, POS SKU, hazırlık süresi | Menü, app sipariş, öneri motoru |
| Kampanya | kural, hedef segment, şube, tarih, kupon | App, web, push |
| Sadakat kuralı | kazanım oranı, seviye eşikleri, ödüller | App |
| İçerik | blog, SSS, hikaye, basın | Web, GEO |
| Yorum | platform, şube, puan, metin, yanıt, sentiment | HQ, şube skoru |
| Franchise lead | kaynak, bölge, bütçe, durum | CRM |
| Denetim | tarih, tür, bulgular, kapanış | Portal |
| Marka | logo, renk, tipografi, ton, yasak kullanımlar | AI içerik motoru kılavuzu |
| Bilgi tabanı (LLM) | Yukarıdakilerin metinleştirilmiş özeti + politika (iade, alerjen, çalışma saatleri) | WhatsApp/AI asistan, site chat |

Yükleme yöntemi: Müşteriden Excel/Drive ile toplanır → P3Media veri temizleme → CMS import → şema ve sitemap otomatik üretim → GBP/Yandex toplu güncelleme.

---

## 13. Rakiplerin En İyisi Olma Planı (Farklılaştırma)

| Rakip güçlü yanı | Florida Coffee cevabı |
|---|---|
| Espressolab: 1M app kullanıcısı, cüzdan | Aynı mekanikleri sunmak yetmez; **"manzara + ön sipariş"**: en güzel manzaralı masayı app'ten rezerve et (Beykoz, Kavacık) |
| Kahve Dünyası: içerik ve e-ticaret | Blog + "İstanbul'un manzaralı kahve rotası" rehberleri; Mi Florida çekirdek satışı |
| Coffy: tek fiyat, basitlik | BİFLORİDA ekonomik hat (kararı müşteriye sor) |
| Starbucks: marka gücü | Yerlilik + Boğaz hikayesi + boykot sonrası alternatif |
| Hepsi: şube sayfaları zayıf | Türkiye'nin en zengin şube sayfaları (yoğunluk, manzara saatleri, etkinlik) |
| Hepsi: franchise sayfaları form odaklı | Şeffaf yatırım hesaplayıcı + video başarı hikayeleri + 3 km koruma vurgusu |
| Hiçbiri: Karadağ | EN/ME siteyle Adriyatik'te ilk Türk kahve zinciri konumu |

---

## 14. Yol Haritası

| Faz | Süre | Kapsam | Çıktı |
|---|---|---|---|
| 0. Keşif | 2 hafta | Marka kılavuzu, POS/otomasyon envanteri, şube verisi toplama, Semrush tam çekim, teknik denetim, alt marka rollerinin netleşmesi | Gereksinim dokümanı, veri şablonları |
| 1. Temel | 6–8 hafta | Yeni web (TR), 15 şube sayfası, menü, franchise hunisi, GBP/Yandex temizliği, entity/Wikidata, şema, analytics | Site canlı, yerel SEO temel |
| 2. App v2 | 8–10 hafta (paralel) | Sadakat, cüzdan, ön sipariş, kampanya, push; kart→app geçiş kampanyası | Lansman |
| 3. Portal | 6 hafta | Franchisee portalı + HQ dashboard, POS/e-fatura entegrasyonu | Sözleşme yükümlülükleri dijital |
| 4. AI | 4–6 hafta | WhatsApp asistan, yorum sentiment, içerik motoru, lead skorlama, ciro uyarısı | AI katmanı v1 |
| 5. Büyüme | Sürekli | Blog, EN/ME, e-ticaret, öneri motoru, talep tahmini, AI video | Aylık retainer |

---

## 15. Demo ve Sunum Planı

### 15.1 Demoda gösterilecekler (öncelik sırası)

1. **"Florida Coffee Türkiye" Google sonucu simülasyonu**: bugünkü SERP (ABD karışıklığı) vs. hedef SERP (knowledge panel, sitelinks, local pack, app).
2. **Ana sayfa + Kavacık şube sayfası** (manzara, yoğunluk, SSS, ön sipariş butonu).
3. **App akışı**: kart bakiyesi aktar → favori sipariş → "Geldim" → puan kazan → seviye.
4. **HQ dashboard**: 15 şube ciro/royalty/yorum skoru; ciro eşiği uyarısı (madde 12.3).
5. **AI asistan**: WhatsApp'ta "Beykoz'da laktozsuz iced latte sipariş etmek istiyorum" senaryosu.
6. **Franchise hunisi**: yatırım hesaplayıcı + başvuru → lead skor.
7. **AI video örneği**: P3Media ile 15 saniyelik şube tanıtımı.

### 15.2 Sunum ana mesajları

- "Dijitalde 208.967. sıradasınız; rakipleriniz bin civarında. Bu bir tasarım sorunu değil, altyapı sorunu."
- "Sözleşmeniz zaten dijitali merkezileştiriyor; biz onun yazılımını ve içeriğini kuruyoruz. Her yeni franchise, platformun bir müşterisi."
- "Florida adı en büyük SEO riskiniz; varlık stratejisiyle en büyük farkınız olur."
- "Manzara sizin ürününüz; hiçbir rakip bunu dijitalde satmıyor."
- "Karadağ ile Türkiye'nin ilk Adriyatik kahve zinciri hikayesini yazın."

### 15.3 Müşteriye keşif soruları

1. Alt markaların (FloridaDays, Mi Florida, BİFLORİDA, Florida Plus) gerçek rolleri?
2. Mevcut "online otomasyon" / POS hangisi? API var mı?
3. Mevcut uygulamayı kim geliştirdi, kaynak kod ve mağaza hesapları sizde mi?
4. Fiziksel sadakat kartı başladı mı, kaç kart dağıtıldı?
5. Kendi kavurma tesisi var mı; çekirdek satışı planı?
6. Sakarya Çark Caddesi şubesi ve Şal Sokak adresi ilişkisi (taşınma mı, ikinci nokta mı)?
7. Karadağ operasyonu kimde; ayrı şirket mi?
8. Yemeksepeti dışında teslimat platformları?
9. 2026–2027 şube hedefi ve franchise satış ekibi?
10. Marka kılavuzu ve görsel arşiv?
11. Kapalı görünen Çengelköy merkez şubesi gerçekten kapalı mı? (Yandex)
12. Reklam ajansı sözleşmesi (madde 7.3) kimde; P3Media bu rolü mü devralıyor?

### 15.4 Riskler

| Risk | Azaltma |
|---|---|
| Mevcut app kaynak kodu erişilemez | Yeni bundle ID ile yayın + eski uygulamada yönlendirme |
| POS API yok | Adisyo/Menulux geçişi teklifi veya günlük CSV senkron |
| Franchise alanların şube hesaplarını kapatmaya direnci | Madde 4 ve 7.2'ye dayalı geçiş, hesapları "devral" (silme değil) |
| KVKK (kamera AI, kişiselleştirme) | Aydınlatma metinleri, TR veri lokasyonu, hukuk görüşü |
| Karadağ ödeme/dil | Faz 2'de, EUR ve yerel PSP |

---

## 16. Kaynaklar

Franchise sözleşmesi özet sunumları (P3Media, Eylül 2026); Semrush TR veritabanı (Eylül 2026); floridacoffee.com.tr (/, /about, /stores); App Store id6504341925; Google Play com.floridacoffeemobile; Instagram @floridacoffeetr, @floridacoffeekavacik, @floridayahyakaptan, @florida.bahcesehir; TikTok @floridacoffee_; Facebook /floridacoffeetr; Şikayetvar /florida-coffee; Yandex Haritalar (Beykoz, Kavacık, Çark, Çengelköy kayıtları); sayfa.istanbul; Kariyer.net Florida Coffee Co.; SATSO Cadde54 Florida Coffee; Yemeksepeti Florida Coffee kayıtları; ZAM Haber (X) şube sayıları; Gıda Bülteni (Nisan 2025 şube sayıları); Ekoturk (Coffy hedefleri); Marketing Türkiye, Dünya, Karar, Gıdatarım (tüketim ve pazar); Accio (kafe sayısı); Ipsos hane paneli (Perakende Mühendisi); DergiPark kahve tüketim araştırmaları; Espressolab (O-Club, Eslab Wallet, 1M kullanıcı haberleri); Kahve Dünyası (Hazır Al, Çekirdek Kazan, SSS); Coffy (Gel Al, franchise sayfaları); Starbucks Türkiye Rewards; Gloria Jean's TR; GZT/Sabah (Starbucks boykot); Ekonomist (franchise talebi); richmenu.io ve geekssort (Core Web Vitals 2026); Sheltron, ComSuite (AI Overview/GEO 2026); GrowthHQ, AI Report (Starbucks Deep Brew); mekan.com, Foursquare, wanderlog (Sakarya mekanları).
