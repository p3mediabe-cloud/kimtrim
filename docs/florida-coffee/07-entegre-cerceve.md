# Florida Coffee · Entegre İşletme Platformu — Çerçeve

**Hazırlayan:** P3Media · 8 Eylül 2026
**Durum:** 8 Eylül görüşmesinden sonra genişleyen kapsamın çerçevesi. `00-analiz-raporu.md` ve `03-fonksiyonel-tasarim.md` üstüne kurulur, onları değiştirmez.
**Kardeş dokümanlar:** `08-deger-fiyat-roi.md` (para), `09-ilk-yil-plani.md` (kim ne zaman ne yapar)

---

## 0. Ne değişti

8 Eylül görüşmesine kadar konuştuğumuz iş "web sitesi + mobil uygulama + HQ paneli"ydi. Görüşmede işletme kendi eksiğini kendi koydu ve kapsam şuraya taşındı:

> Mevcut kasa sistemi menünün kaynağı olacak; oradan başlayarak web, uygulama, franchise iletişimi, iş başvuruları, kampanyalar, e-ticaret, şube tedarik siparişleri, HQ veri birikimi ve tek ağızdan sosyal medya yönetimi tek sistemde bağlanacak.

Bu, "birkaç dijital ürün" değil **bir işletim sistemi** talebidir. Çerçevenin tamamı tek bir cümleye dayanır:

> **Bir veri yalnızca bir yerde girilir; girildiği yerden gideceği her yüze kendiliğinden akar.**

Bugün Florida Coffee'de bir fiyat değişikliği kasada, basılı menüde, QR menüde, sitede, Yemeksepeti'nde ve uygulamada ayrı ayrı yapılıyor — 17 şube × 6 kanal. Adres değişikliği Google, Yandex, site ve haritalarda ayrı ayrı. Yeni şube açılışı sıfırdan kurulan bir proje. Bu çerçevenin tek amacı bu çarpımı yok etmektir.

---

## 1. Mimari: bir omurga, altı yüz, üç döngü

### 1.1 Omurga — tek gerçek kaynağı

Her veri türünün **tek bir sahibi** vardır. Sahibi dışında hiçbir yerden değiştirilemez.

| Veri | Sahibi (tek giriş noktası) | Aktığı yerler |
|---|---|---|
| Ürün, boy, fiyat, KDV, SKU | **Kasa / POS** | Menü sayfaları · uygulama · QR menü · barista ekranı · e-ticaret · Yemeksepeti · Flo asistan · basılı menü PDF'i |
| Stok, satış, ciro, fiş | **Kasa / POS** | HQ paneli · royalty hesabı · franchisee portalı · talep tahmini · şube yoğunluk göstergesi |
| Şube künyesi (ad, adres, telefon, saat, özellik, görsel) | **HQ paneli** | Şube sayfası · uygulama · Google İşletme Profili · Yandex · Yemeksepeti · e-posta imzası · basılı materyal · şema (schema.org) |
| Kampanya ve etkinlik | **HQ paneli** | Uygulama push · web · sosyal medya · e-posta · barista ekranı · POS promosyon kodu |
| Görsel ve video varlıkları | **İçerik havuzu** | Sosyal medya · web · uygulama · basılı · e-ticaret |
| Üye, puan, cüzdan | **Platform** | Uygulama · kasa (QR okutma) · kampanya hedefleme · CRM |
| Aday ve başvuru | **İK modülü** | Şube vardiya planı · HQ İK · kariyer sayfası |
| Franchise adayı (lead) | **Web + Flo** | CRM · HQ pipeline · bölge haritası |
| Tedarik kataloğu ve şube fiyat listesi | **HQ paneli** | Franchisee portalı B2B sepeti · e-fatura · cari hesap |

**Kural:** Bir alanı iki yerden değiştirebiliyorsanız, altı ay içinde ikisi birbirini tutmaz. Sistemin tek disiplini budur.

### 1.2 Altı yüz

Aynı omurgadan beslenen altı arayüz. Hiçbiri kendi verisini tutmaz.

| Yüz | Kim kullanır | Ne yapar |
|---|---|---|
| **Web sitesi** | Misafir, franchise adayı, iş adayı, basın | Keşif, menü, şube, franchise hunisi, kariyer, haber, e-ticaret vitrini |
| **Mobil uygulama** | Üye misafir | Sadakat, cüzdan, ön sipariş, kampanya, e-ticaret, etkinlik |
| **Barista ekranı** | Şube personeli | Gelen sipariş kuyruğu, hazırlık, "Geldim" sinyali |
| **Franchisee portalı** | Şube müdürü / franchise alan | Ciro onayı, tedarik siparişi, denetim, eğitim, duyuru, talep, içerik yükleme |
| **HQ paneli** | Merkez ekibi ve yönetim | Her şey: menü, fiyat, şube, kampanya, içerik onayı, royalty, uyarı, rapor |
| **Flo (AI asistan)** | Herkes, her kanalda | WhatsApp / Instagram / site / uygulama içi: soru, sipariş, başvuru, şikâyet |

### 1.3 Üç döngü

Platformun değeri modüllerde değil, bu üç döngünün dönmesindedir.

**Döngü 1 — Misafir**
Arama / harita / sosyal → şube sayfası veya uygulama → sipariş → puan → segment → kampanya → tekrar ziyaret.
*Her tur, bir sonraki turu daha isabetli yapan veriyi bırakır.*

**Döngü 2 — Şube**
Açılış → günlük operasyon (kasa + barista ekranı) → tedarik siparişi → ciro ve royalty → denetim → performans → içerik katkısı → HQ görünürlüğü.
*Şube hem veri üretir hem veriden yönetilir.*

**Döngü 3 — Büyüme (asıl çark)**
İçerik ve yerel SEO → franchise adayı → görüşme → açılış → **yeni şube 4 saatte sisteme girer** → açılış haberi ve sosyal seri tetiklenir → görünürlük artar → daha çok aday.
*Florida Coffee'nin iş modeli franchise satmaktır. Bu döngü platformun asıl ürünüdür; diğer ikisi onu besler.*

```
                       ┌───────────── Döngü 3: BÜYÜME ─────────────┐
                       │                                           │
   içerik & yerel SEO ─┴─> franchise adayı ─> görüşme ─> AÇILIŞ ───┤
            ▲                                              │       │
            │                                              ▼       │
            │                                    ┌──────────────┐  │
            │                                    │ açılış paketi│  │
            │                                    │  (4 saat)    │  │
            │                                    └──────┬───────┘  │
            │                                           │          │
            │        ┌────── Döngü 2: ŞUBE ─────────────┤          │
            │        │                                  ▼          │
            │   tedarik ─> ciro ─> denetim ─> performans           │
            │        ▲                              │              │
            │        │                              ▼              │
            │   ┌────┴──── OMURGA (tek kaynak) ─────────┐          │
            │   │  POS · şube · kampanya · içerik · üye │          │
            │   └────┬──────────────────────────────────┘          │
            │        │                                             │
            │        ▼        ┌───── Döngü 1: MİSAFİR ─────┐       │
            └── içerik ◄── ziyaret ─> sipariş ─> puan ─> kampanya ─┘
```

---

## 2. Modüller

Görüşmedeki her talebin karşılığı. Numaralar sonraki dokümanlarda referans olarak kullanılır.

### M1 · Menü ve fiyat omurgası (kasa entegrasyonu)
**Talep:** *"Hâlihazırda bir kasa sistemi kullanıyorlar, bunu menüye entegre edeceğiz."*

- Kasadaki ürün ağacı platformun ürün kataloğuna eşlenir (SKU ↔ ürün ID). Eşleme bir kez yapılır, sonra kendiliğinden yürür.
- **Fiyat grupları:** İstanbul · Anadolu · Karadağ (EUR). Bir ürünün üç fiyatı olabilir; şube hangi gruptaysa onu görür.
- Kasada fiyat değişince: menü sayfası, ürün sayfası, uygulama, QR menü, barista ekranı, e-ticaret ve Flo'nun bilgi tabanı **aynı anda** güncellenir. Basılı menü PDF'i yeniden üretilir, şubeye baskı için gider.
- Ters yön: HQ panelinden yapılan sezonluk fiyat kararı kasaya yazılır (POS API yazma izni varsa) veya kasa ekibine tek onay listesi olarak düşer.
- **Kasa API'si yoksa:** günlük CSV/e-fatura köprüsü kurulur; gecikme 24 saate çıkar ama zincir kopmaz. Bu, keşifte kapatılacak 1 numaralı belirsizliktir.

**Ölçüt:** Fiyat değişikliği tek girişle ve 15 dakika içinde tüm kanallarda.

### M2 · Şube künyesi ve açılış motoru
**Talep:** *"Adres telefon ve benzeri şeylerin kolayca değişebilmesi… her açılışta otomatik olarak sisteme kayıt edilebilmeli ve çok hızlı sistemi dâhil edebilmeli, ve onun hakkında haberler ve sosyal medya ağı tetiklenmeli."*

**Künye yönetimi.** Bir şube kaydı: ad, kod, yapısal adres, koordinat, telefon, çalışma saatleri (istisna günleriyle), özellikler (manzara, teras, gece, otopark, priz, Wi-Fi, evcil hayvan), galeri, yönetici, açılış tarihi, POS ID, GBP ID, Yandex ID, Yemeksepeti ID, fiyat grubu. Tek yerden değişir, dokuz yere akar.

**Açılış paketi.** Yeni şube formu doldurulup kaydedilince şu iş kendiliğinden başlar:

| # | Tetiklenen iş | Hedef süre |
|---|---|---|
| 1 | Şube sayfası TR (+EN) yayında; sitemap, şema, iç linkler güncel | 4 saat |
| 2 | Ana sayfa şube şeridinde ve haritada görünür | 4 saat |
| 3 | Google İşletme Profili kaydı/taslağı + Yandex kaydı açılır | 1 gün |
| 4 | Uygulamada şube seçilebilir; ön sipariş açık | 4 saat |
| 5 | Fiyat grubu atanır, menü şubede canlı | 4 saat |
| 6 | Barista ekranı hesabı, tablet kurulum kılavuzu | 1 gün |
| 7 | POS ID eşleşir, ciro akışı başlar | 2 gün |
| 8 | Franchisee portal hesabı + eğitim atamaları (madde 8) | 1 gün |
| 9 | Tedarik kataloğu erişimi + açılış siparişi şablonu | 1 gün |
| 10 | "Yeni şube" haber yazısı (web) + basın bülteni taslağı | 2 gün |
| 11 | Sosyal medya açılış serisi (T-10 geri sayım → T+7) kuyruğa girer | açılıştan 10 gün önce |
| 12 | Açılış kampanyası: çevre 3 km üyelere push, ilk kahve hediye | T-3 |
| 13 | Personel ilanı yayınlanır + havuzdan aday eşleştirme başlar | T-21 |
| 14 | Şehir/ilçe yerel SEO sayfası ve iç link ağı | 1 hafta |
| 15 | Bölge üyelerine e-posta ve WhatsApp duyurusu | T-2 |
| 16 | Yemeksepeti / teslimat kanalı kaydı görevi açılır | 1 hafta |
| 17 | Denetim takvimi ve gizli müşteri planı (madde 9) kurulur | 1 ay |
| 18 | 30/60/90 gün performans izleme panosu açılır | T+30 |

**Ölçüt:** Formdan **4 saat** içinde dijital varlıklar canlı; **21 gün** içinde tam lansman zinciri tamamlanmış.

### M3 · Web sitesi
Kurumsal site: ana sayfa, şube sayfaları (şablondan otomatik), menü ve ürün sayfaları, kahvemiz, hikâyemiz, etkinlikler, haberler, franchise hunisi (+ yatırım hesaplayıcı, başvuru, SSS), kariyer (+ başvuru), kurumsal/toplu satış, e-ticaret vitrini, SSS, iletişim, yasal metinler, EN katmanı.
Teknik: SSR/ISR, JSON-LD şema, hreflang, sitemap, Core Web Vitals hedefi LCP < 2,0 s.
*Ayrıntı: `00-analiz-raporu.md` §9, `03-fonksiyonel-tasarim.md` §4.*

### M4 · Mobil uygulama
Sadakat (puan + damga), seviye (Classic/Plus/Premium), cüzdan (kredi kartı + yemek kartları), ön sipariş ve "Geldim", kampanyalar, favoriler/"her zamanki", hediye gönder, fiziksel karttan geçiş, etkinlik biletleri, **e-ticaret sekmesi** (M6 ile aynı katalog), bildirimler.
Mevcut mağaza kayıtları korunur — sıfırdan değil **v2 relaunch**.
*Ayrıntı: `03-fonksiyonel-tasarim.md` §5.*

### M5 · Barista ekranı
Şube tabletinde sipariş kuyruğu; modifikasyonlar renkli ve büyük; "Geldim" sinyali sırayı öne alır; çevrimdışı önbellek; POS'a fiş, e-fatura entegratörüne aktarım.

### M6 · E-ticaret (B2C)
**Talep:** *"E-ticaret kısmından çeşitli gadget ve perakende sundukları kahveleri ve diğer şeyler."*

- Katalog: çekirdek ve öğütülmüş kahve, kapsül, demleme ekipmanı (V60, Chemex, French press, değirmen), termos ve bardak, merch (Mi Florida hattı), hediye kutusu, hediye kartı, abonelik (aylık çekirdek).
- Aynı katalog hem web hem uygulamada. Tek stok, tek fiyat.
- Ödeme: sanal POS (iyzico/PayTR) + cüzdan bakiyesi + puan kullanımı. Kargo entegrasyonu, kargo takibi, iade akışı, mesafeli satış sözleşmesi ve ön bilgilendirme formu.
- **Şubeden teslim:** sipariş şubeye düşer, misafir uğrayıp alır (kargo maliyeti sıfır, şubeye ayak trafiği).
- Kurumsal/toplu satış talep formu → HQ satış hattı.
- Sadakat entegre: online alışverişten de puan.

**Neden önemli:** Kahve, Türkiye'de e-ticaret sepetlerindeki payını bir yılda **iki katına** çıkarmış bir kategori (%3,7). Şubesi olmayan illere ulaşmanın tek yolu ve marjı şube marjından yüksek.

### M7 · Şube tedarik siparişi (B2B)
**Talep:** *"Şubelerin siparişlerini bu yoldan e-ticaret şeklinde geçebilmelerini."*

- Merkezî tedarik kataloğu (madde 6.4): çekirdek, süt, şurup, ambalaj, tek kullanımlık, üniforma, basılı materyal, ekipman.
- Şube kendi fiyat listesini görür; sepete atar; sipariş HQ'ya düşer; onay → hazırlık → sevkiyat → irsaliye → e-fatura → cari hesap.
- **40 gün vade takibi** (madde 6.10), kredi limiti, gecikme uyarısı.
- Sipariş geçmişi ve **öneri**: "Geçen ay bu saatte 40 kg aldınız, mevcut satış hızınızla 11 gününüz kaldı." (M13 talep tahmininden)
- Şube açılış paketi: yeni şubeye standart açılış siparişi şablonu.
- Minimum sipariş, teslim günü takvimi, kısmi sevkiyat.

**Bugünkü hâli:** WhatsApp, telefon ve Excel. 17 şube × haftalık sipariş = ayda ~270 mesajlaşma turu.

### M8 · Franchisee portalı ve iletişim
**Talep:** *"Şubelerin kendi panelinden iletişime geçebilmeleri."*

- **Duyuru akışı:** HQ'dan tüm şubelere veya seçili şubelere; okundu bilgisi. WhatsApp gruplarının yerini alır — arşivlenebilir, aranabilir, kime gittiği belli.
- **Talep/destek kaydı (ticket):** kategori (teknik, tedarik, pazarlama, İK, denetim, muhasebe), öncelik, sorumlu, SLA sayacı, geçmiş.
- **Yerel kampanya talebi:** form → HQ onayı → kampanya kuyruğu. Madde 7.2'yi ihlal etmeden şubenin sesi duyulur.
- **İçerik yükleme:** şube fotoğraf/video yükler (M9 havuzuna gider).
- Ciro bildirimi ve onayı (6.23), royalty ekstresi, denetim maddeleri ve süre sayacı (9), eğitim modülleri ve sertifika (8), belge kütüphanesi, sözleşme bitiminde erişim iptali (13.2).

### M9 · İçerik havuzu ve yayın merkezi
**Talep:** *"Sosyal medya yönetiminin tek ağızdan yürümesi, onun içinde işletmelere bir altyapı oluşturmak ve gelen görüntü ve istekleri bir havuzda toplamak, ve yayını sadece HQ yapması."*

Bu modül sözleşmenin 7.2 ve 7.3 maddelerinin yazılıma dönüşmüş hâlidir.

**Akış:**
```
Şube yükler ──> otomatik etiketleme ──> HAVUZ ──> editör seçer ──> marka şablonu
(portal/app)   (şube, ürün, ışık,      (HQ)      (P3Media)      + AI metin taslağı
                kalite skoru, yüz                                       │
                bulanıklaştırma)                                        ▼
                                                              HQ ONAYI (tek ağız)
                                                                        │
                                                                        ▼
                                          yayın kuyruğu ──> Instagram · TikTok · Facebook
                                                             · web haber · uygulama · e-posta
                                                                        │
                                                                        ▼
                                              performans havuza geri döner
                                              (hangi şubenin içeriği tuttu)
```

- **Roller kesindir:** Şube *yükler ve önerir*. Ajans *üretir ve planlar*. HQ *onaylar ve yayınlar*. Şube hiçbir koşulda yayınlamaz.
- **Mevcut şube hesapları** (@floridacoffeekavacik, @floridayahyakaptan, @florida.bahcesehir) silinmez — **devralınır**, ana hesaba yönlendirilir, arşivi havuza taşınır. Madde 4 ve 7.2 dayanağıyla, çatışmasız geçiş.
- **Marka şablonları:** şube duyurusu, ürün tanıtımı, etkinlik, iş ilanı, açılış, gün batımı serisi. Şube görseli şablona düşer, marka bozulmaz.
- **Teşvik:** ayın en çok kullanılan içeriğini gönderen şube panoda görünür; aylık raporda adı geçer.
- **Kapsam dışı — fotoğrafçı:** Profesyonel çekim (menü kartları, kampanya görselleri, mekân çekimi) bu havuzun içeriği değildir. Brief'i, çekim listesini, yönetimi, seçkiyi ve retuşu P3Media yapar; **fotoğrafçı ve stüdyo müşteri tarafından temin edilir ve müşteri hesabından ödenir.** Havuz günlük içeriği besler; çekim kalıcı varlıkları üretir. İkisi karıştırılmaz.

### M10 · Etkinlik ve özel gün motoru
**Talep:** *"Her etkinlik, özel günler gibi bir sistemin kurulması."*

Yıllık takvim üç katmanlıdır ve her satırı bir **pakete** bağlanır.

| Katman | Örnekler |
|---|---|
| Ulusal / dini | Ramazan ve iftar saatleri, Ramazan ve Kurban Bayramı, yılbaşı, 23 Nisan, 19 Mayıs, 29 Ekim, anneler ve babalar günü, sevgililer günü, öğretmenler günü |
| Kategori | 1 Ekim Dünya Kahve Günü, soğuk kahve sezonu açılışı, okula dönüş, kış menüsü geçişi, hasat dönemi hikâyesi |
| Marka | Şube açılış yıldönümleri, kuruluş yıldönümü, FloridaDays kulüp günleri, gün batımı saatleri, akustik geceler, cupping atölyeleri, yeni ürün lansmanı |

**Paket içeriği (her etkinlik için aynı iskelet):** brief → görsel set → metinler → kampanya kuralı (ürün, indirim, hedef segment, bütçe, süre) → uygulama push → sosyal takvim → web/haber sayfası → barista bilgilendirme kartı → basılı materyal (masa kartı, poster) → ölçüm.

**Ritim:** T-21 planlama · T-14 üretim · T-7 onay · T-0 yayın · T+3 ölçüm ve rapor.

Takvim yılın başında bir kez kurulur; motor tarihi geldiğinde görevleri kendiliğinden açar. Kimse "yılbaşı geldi, ne yapıyoruz" diye sormaz.

### M11 · İK ve aday havuzu
**Talep:** *"İş başvuruları."*

Site ve uygulamadan 4 adımlı başvuru → aday havuzu → açık vardiya kaydı → AI eşleştirme puanı → ilk N adaya tek dokunuşluk soru (Evet / Hayır / 2 hafta sonra) → ilk "Evet" ile vardiya kapanır.
Şube müdürü yalnızca onaylar; arama ve takip otomatiktir. Kapanma süresi, yanıt oranı ve gelmeme oranı panelde.
KVKK: rıza, saklama süresi, "artık arama" sonrası 30 günde silme.
*Ayrıntı: `03-fonksiyonel-tasarim.md` §8b.*

### M12 · HQ veri ve karar merkezi
**Talep:** *"HQ data birikmesi… HQ'nun paneli tüm şubeleri kaplamalı."*

- **Dashboard:** şube bazlı günlük/aylık ciro, sipariş adedi, ortalama sepet, uygulama payı, üye sayısı, yorum puanı, e-ticaret satışı, tedarik hacmi.
- **Uyarılar:** ciro eşiği (12.3), denetim uyarı sayısı (6.18), kapalı gün (6.28), kamera pasif (6.23), stok tükenmesi, yorum puanı düşüşü, ödeme gecikmesi.
- **Royalty:** POS cirosundan otomatik %5 + KDV, aylık bildirim formu (6.23) dolu gelir, franchise alan onaylar.
- **Karşılaştırma:** şube sıralaması, benzer şube kohortu, açılıştan bu yana eğri.
- **Veri ambarı:** her işlem, her kampanya, her yorum, her başvuru saklanır. 12. ayın sonunda elinizde **kendi verinizle çalışan bir tahmin altyapısı** olur — bu, platformun zamanla artan tek varlığıdır.
- Dışa aktarma: Excel/CSV, muhasebe ve mali müşavir için hazır formatlar.

### M13 · Flo — AI katmanı
Yatay katman; her modülün içinde çalışır.

| Kullanım | Nerede | Faz |
|---|---|---|
| Misafir asistanı (WhatsApp / Instagram / site / uygulama) | M3, M4 | 1 |
| İçerik metni ve şube SSS üretimi | M9 | 1 |
| Yorum duygu analizi ve yanıt taslağı | M12 | 1 |
| Franchise adayı skorlama | M3 | 1 |
| Ciro eşiği erken uyarısı | M12 | 1 |
| Gizli müşteri raporu özeti | M8 | 1 |
| İçerik havuzu otomatik etiketleme ve kalite skoru | M9 | 2 |
| Ürün önerisi ve kişiselleştirme | M4 | 2 |
| Talep tahmini ve tedarik önerisi | M7 | 2 |
| Aday–vardiya eşleştirme | M11 | 2 |
| Ölü saat dinamik kampanyası | M10 | 2 |
| Personel vardiya önerisi | M12 | 3 |

Yönetişim: fiyat ve stok her zaman API'den okunur, modelden değil. Yorum yanıtı ve sosyal içerik **insan onayından** geçmeden yayınlanmaz. KVKK aydınlatması her kanalda ilk temasta.

---

## 3. Yayın ve karar yönetişimi

Kim neyi yapabilir. Tartışma çıktığında bakılacak tablo budur.

| İş | Şube | HQ operasyon | HQ yönetim | P3Media |
|---|---|---|---|---|
| Fiyat değiştirme | — | öneri | **karar** | uygular |
| Menüye ürün ekleme | öneri | hazırlık | **karar** | uygular |
| Şube künyesi değiştirme | talep | **yapar** | — | denetler |
| Sosyal medya gönderisi | **yükler/önerir** | **onaylar** | itiraz hakkı | üretir, planlar, yayınlar |
| Yerel kampanya | **talep eder** | **onaylar** | bütçe onayı | kurar, ölçer |
| Ulusal kampanya | — | hazırlık | **karar** | üretir, yürütür |
| Yeni şube kaydı | — | **yapar** | — | otomasyonu işletir |
| Basın açıklaması | — | hazırlık | **karar** | yazar |
| Yorum yanıtı | görür | **onaylar** | — | taslak üretir |
| İş ilanı | **talep eder** | **onaylar** | — | yayınlar |
| Tedarik siparişi | **verir** | **onaylar** | limit kararı | — |
| Uygulama sürümü | — | test | **karar** | geliştirir, yayınlar |

**Onay SLA'sı:** HQ onayı 5 iş günü içinde verilir. Verilmezse takvim kayar; ücret kaymaz. Bu madde sözleşmeye girer.

---

## 4. Entegrasyon haritası

| Sistem | Yön | Ne taşır | Risk |
|---|---|---|---|
| POS / kasa otomasyonu | çift | Ürün, fiyat, SKU, satış, ciro, stok | **API yoksa CSV köprüsü** — keşifte kapatılır |
| e-Fatura entegratörü | çıkış | Sipariş, tedarik, royalty faturaları | Entegratör kim, API'si var mı |
| Sanal POS (iyzico/PayTR) | çift | Ödeme, iade, taksit | Komisyon ~%1,95 müşteri hesabında |
| Yemek kartları (Multinet, Sodexo, Setcard) | çift | Cüzdan yükleme | Ayrı sözleşme gerekir |
| Google İşletme Profili | çıkış | Künye, saat, gönderi, ürün | API kotası |
| Yandex İşletme | çıkış | Künye, saat | Çengelköy "faal değil" kaydı acil |
| Meta (Instagram, Facebook, WhatsApp Business) | çift | Yayın, DM, katalog | WhatsApp onayı 4–8 hafta sürebilir |
| TikTok | çıkış | Yayın | API kısıtlı, yarı manuel |
| Yemeksepeti / teslimat kanalları | çift | Menü, fiyat, sipariş | Komisyon %12–38; kendi kanalı öncelikli |
| Kargo (Yurtiçi/Aras/MNG) | çift | Gönderi, takip | E-ticaret için |
| Firebase / OneSignal | çıkış | Push bildirim | — |
| Search Console, GA4, Semrush | giriş | Performans verisi | — |
| Muhasebe / ön muhasebe | çıkış | Fatura, cari | Hangisi kullanılıyor — keşif |

---

## 5. Bu çerçevenin kapsamadıkları

Sınır çizmeden fiyat savunulmaz. Aşağıdakiler **dâhil değildir**:

| Kalem | Kim yapar | Not |
|---|---|---|
| **Profesyonel fotoğraf ve video çekimi** | Müşteri temin eder | P3Media brief, çekim listesi, yönetim, seçki ve retuş yapar. Fotoğrafçı, stüdyo, model, stilist, ulaşım müşteri hesabında. |
| Reklam bütçesi (Meta, Google) | Müşteri | Madde 7.1 ulusal reklam fonundan. P3Media kurar ve yönetir. |
| Sanal POS komisyonu, kargo bedeli | Müşteri | Ciroya bağlı |
| Alan adı, e-fatura entegratörü, yemek kartı sözleşmeleri | Müşteri | P3Media kurulumda yardımcı olur |
| Kasa/POS yazılımı değişimi | Müşteri | Mevcut kasa API vermiyorsa geçiş ayrı proje |
| Şube tablet ve donanımı | Müşteri | Barista ekranı için |
| Hukuki metinlerin avukat onayı | Müşteri | P3Media taslak üretir |
| Mali müşavirlik, KVKK VERBİS kaydı | Müşteri | P3Media veri işleyen olarak sözleşme imzalar |
| Şube personelinin operasyonel eğitimi | Müşteri | P3Media yazılım eğitimi ve video modülleri sağlar |

---

## 6. Aşamalandırma mantığı

Neyin neden önce geldiği. Sıra keyfi değil — her aşama bir sonrakinin verisini üretir.

| Aşama | Neden burada | Ne açar |
|---|---|---|
| **0. Omurga ve veri** (Ay 1) | Kasa eşlemesi ve şube künyesi olmadan hiçbir yüz doğru veri gösteremez | Her şey |
| **1. Görünürlük** (Ay 1–3) | Yandex "kapalı" kaydı ve GBP hijyeni bugün para kaybettiriyor; düzeltmesi bir haftalık iş | Yerel arama trafiği, şube sayfalarına zemin |
| **2. Web** (Ay 2–3) | Franchise ve kariyer hunisi buradan akar; SEO'nun ısınması 3–6 ay sürer, en erken başlamalı | Franchise adayı, iş adayı, e-ticaret vitrini |
| **3. Uygulama v2** (Ay 3–4) | Sadakat verisi olmadan kampanya hedeflemesi, öneri motoru ve talep tahmini çalışmaz | Üye verisi, sipariş verisi, segment |
| **4. HQ paneli ve portal** (Ay 5–6) | Şube verisi akmaya başladıktan sonra anlamlı; önce kurmak boş ekran demek | Royalty otomasyonu, denetim, tedarik |
| **5. Ticaret** (Ay 6–8) | B2C ve B2B aynı katalog ve stok altyapısını paylaşır; portal ayakta olmadan B2B kurulmaz | Yeni gelir kalemi, şube sipariş disiplini |
| **6. İçerik havuzu ve etkinlik motoru** (Ay 4–7) | Şubeler portala alıştıktan sonra içerik yüklemeye başlar | Tek ağızdan yayın, sürdürülebilir içerik |
| **7. AI derinleşmesi** (Ay 7–12) | Tahmin ve kişiselleştirme için en az 3 ay veri gerekir | Öneri, talep tahmini, dinamik kampanya |

---

## 7. Keşifte kapatılacak belirsizlikler

Bu çerçevenin tamamı aşağıdaki on sorunun yanıtına göre son hâlini alır. Yanıtlar gelmeden sözleşmeye kapsam yazılmaz.

1. **Kasa/POS hangisi, API'si var mı, yazma izni veriyor mu?** (M1'in tamamı buna bağlı)
2. e-Fatura entegratörü kim, API'si var mı?
3. Mevcut uygulamanın kaynak kodu ve mağaza hesapları kimde?
4. Şube başına aylık ciro bandı ve 2027 şube hedefi?
5. Merkezî tedarikin bugünkü işleyişi: katalog var mı, fiyat listesi nasıl tutuluyor, vade takibi nerede?
6. Perakende ürün hattı: hangi ürünler, kim üretiyor/paketliyor, stok nerede, kargo anlaşması var mı?
7. Franchise alanlar bugün 6.32 kapsamında aylık ne ödüyor?
8. Ulusal reklam fonu (%1) bugün ne kadar ve nasıl harcanıyor?
9. Şube Instagram hesaplarının şifreleri kimde; devralmaya direnç var mı?
10. Marka kılavuzu, fotoğraf arşivi ve planlanan çekim takvimi?

---

## 8. Başarı ölçütleri (12. ay)

Çerçevenin çalıştığını nereden anlayacağız. Hedeftir, garanti değildir.

| Ölçüt | Bugün | 12. ay hedefi |
|---|---|---|
| Fiyat değişikliğinin tüm kanallara yayılma süresi | 3–5 gün, kanal başına ayrı iş | **15 dakika**, tek giriş |
| Yeni şubenin dijital olarak canlıya çıkma süresi | 2–4 hafta, dağınık | **4 saat** |
| Organik arama ziyareti (aylık) | ~287 | 30.000 |
| İlk 10'da anahtar kelime | 0 | 400+ |
| Aktif uygulama üyesi | ölçülemiyor | 60.000 |
| Uygulama üzerinden işlem payı | ~0 | %10–15 |
| Aylık franchise başvurusu | ölçülemiyor | 40 |
| Şube tedarik siparişinin portalden geçme oranı | %0 | %90 |
| HQ'ya ciro bildiriminin otomatik gelme oranı | %0 | %100 |
| Yayın öncesi HQ onayından geçen içerik oranı | ölçülemiyor | %100 |
| Yanıtlanan yorum oranı (Google + Yandex + Şikayetvar) | ~%0 | %90, 48 saat içinde |
| Açık vardiyanın kapanma süresi | gün | **4 saat** |
