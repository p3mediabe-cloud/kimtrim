# Florida Coffee Platformu — Fonksiyonel Tasarım (Site ve Uygulama Nasıl Çalışır)

**Hazırlayan:** P3Media · 4 Eylül 2026
**Kapsam:** Web sitesi, mobil uygulama, HQ paneli, franchisee portalı, AI asistan. Demo prototipi bu dokümandaki akışları birebir izler.

---

## 1. Tek cümlelik ürün tanımı

Florida Coffee Platformu; müşterinin en yakın Florida'yı bulup sıra beklemeden sipariş verdiği ve her kahvede puan biriktirdiği, HQ'nun ise 15+ şubeyi tek ekrandan yönettiği, franchise sözleşmesinin dijital yükümlülüklerini otomatik yerine getiren merkezi bir sistemdir.

## 2. Roller

| Rol | Kim | Ne yapar | Nereden |
|---|---|---|---|
| Misafir | Siteye gelen herkes | Menü, şube, franchise bilgisi; uygulama indirme | Web |
| Üye | Uygulama kullanıcısı | Puan, cüzdan, ön sipariş, kampanya | App (PWA yedek) |
| Barista | Şube personeli | Gelen siparişleri hazırlar, "Hazır" işaretler | Barista ekranı (tablet) |
| Şube müdürü | Franchise alan / işletme sorumlusu | Ciro raporu, denetim, tedarik siparişi, eğitim, yerel kampanya talebi | Franchisee portalı |
| HQ operasyon | Florida Coffee merkez | Menü, fiyat, kampanya, şube verisi, denetim, royalty | HQ paneli |
| HQ yönetim | Korhan Bey ve ekip | Dashboard, uyarılar, franchise lead pipeline | HQ paneli |
| Ajans (P3Media) | İçerik, SEO, kampanya | CMS, sosyal takvim, AI içerik | HQ paneli (ajans rolü) |

## 3. Sistem haritası

```
┌──────────────┐   ┌──────────────┐   ┌──────────────┐   ┌──────────────┐
│  Web sitesi  │   │ Mobil uyg.   │   │ Barista ekr. │   │ WhatsApp/IG  │
│  Next.js     │   │ Flutter      │   │ (web, tablet)│   │ AI asistan   │
└──────┬───────┘   └──────┬───────┘   └──────┬───────┘   └──────┬───────┘
       └──────────────────┴─────────┬────────┴──────────────────┘
                                    ▼
                         ┌─────────────────────┐
                         │  Platform API       │  Auth · Menü · Şube · Sipariş
                         │  (Supabase/NestJS)  │  Sadakat · Cüzdan · Kampanya
                         └──────────┬──────────┘  Yorum · Lead · Denetim
              ┌─────────────────────┼─────────────────────┐
              ▼                     ▼                     ▼
     ┌────────────────┐   ┌────────────────┐   ┌────────────────┐
     │ POS / otomasyon│   │ Ödeme          │   │ Dış kanallar   │
     │ (6.23)         │   │ iyzico/PayTR   │   │ GBP, Yandex,   │
     │ e-fatura       │   │ yemek kartları │   │ Yemeksepeti,   │
     └────────────────┘   └────────────────┘   │ Firebase push  │
                                               └────────────────┘
              ▲                                          
     ┌────────┴────────┐        ┌────────────────┐
     │ HQ paneli       │        │ Franchisee     │
     │ (admin.)        │        │ portalı        │
     └─────────────────┘        └────────────────┘
```

Tek veri kaynağı: menü, fiyat, şube ve kampanya yalnızca HQ panelinden girilir; web, uygulama, barista ekranı ve AI asistan aynı API'den okur.

---

## 4. Web sitesi nasıl çalışır

### 4.1 Ana sayfa akışı
1. Sayfa açılır; konum izni isteme yerine IP tabanlı şehir tahmini ile "Size en yakın Florida: Kavacık, 1,2 km" kartı gösterilir. Kullanıcı isterse "Konumumu kullan" ile hassaslaştırır.
2. Kart üzerinde üç aksiyon: **Yol tarifi**, **Menüyü gör**, **Ön sipariş ver** (uygulamaya derin link; uygulama yoksa mağaza sayfası).
3. Sezon ürünleri (HQ panelinden "öne çıkan" işaretli), "Manzaralı şubeler" filtreli vitrin, sadakat teaser ("İlk siparişte kahve hediye"), franchise CTA.

### 4.2 Şube sayfası (`/subeler/{sehir}/{sube}`)
- Veri: şube kaydından otomatik (NAP, saatler, özellikler, galeri, yorum özeti, SSS).
- Canlı blok: POS'tan son 30 dakikanın sipariş sayısına göre "Şu an sakin / orta / yoğun" (eşikler HQ'da ayarlanır).
- "Bu şubeden ön sipariş ver" → uygulama derin linki `floridacoffee://order?branch=kavacik`.
- Şema: CafeOrCoffeeShop + FAQPage + BreadcrumbList; sayfa yayınlanınca sitemap ve GBP açıklaması otomatik güncellenir.

### 4.3 Menü (`/menu`, `/menu/{urun}`)
- Kategori sayfaları ve ürün detay: boy/fiyat (şube grubuna göre; İstanbul / Anadolu / Karadağ fiyat listeleri), besin, alerjen, süt seçenekleri.
- Fiyat gösterimi: kullanıcı şube seçtiyse o şubenin fiyat grubu; seçmediyse "İstanbul fiyatı" etiketiyle.
- "Uygulamada sipariş et" derin link.

### 4.4 Franchise hunisi (`/franchise/*`)
1. Neden Florida: 3 km koruma, eğitim (30+15 gün), merkezi tedarik, ulusal reklam paylaşımı, referans şube videoları.
2. Yatırım hesaplayıcı: şehir tipi, m², tahmini aylık ciro girer → örnek tablo: royalty %5, ulusal reklam en fazla %1, tahmini geri dönüş aralığı. Rakamlar "örnek, teklif değildir" etiketli; HQ panelinden güncellenir.
3. Başvuru formu (3 adım: kişi → bölge ve bütçe → deneyim) → CRM'e lead; AI skor (bölge boşluğu, bütçe, deneyim) → HQ'ya bildirim; 24 saat içinde arama SLA.

### 4.5 Diğer
- Blog, kariyer (JobPosting şeması), SSS, yasal.
- Diller: TR ana, EN, Karadağ için sr-ME/EN; hreflang otomatik.
- Performans hedefi: LCP < 2,0 s, INP < 200 ms; görseller CDN'den AVIF.

---

## 5. Mobil uygulama nasıl çalışır

### 5.1 Onboarding
1. Açılış → telefon numarası → OTP (SMS) → ad, doğum tarihi (isteğe bağlı), KVKK ve pazarlama izni.
2. "Fiziksel kartınız var mı?" → kart üzerindeki kodu tara → kart bakiyesi ve puanı hesaba aktarılır (madde 7.4 geçişi).
3. Hoş geldin ödülü: ilk siparişte küçük boy kahve hediye (kural HQ'dan).

### 5.2 Ana ekran
- Üstte: puan bakiyesi (çekirdek), seviye (FloridaDays Classic / Plus / Premium) ve bir sonraki ödüle kalan.
- "Her zamanki" tek dokunuş sipariş kartı (son 3 siparişten en sık).
- En yakın şube ve yoğunluk.
- Aktif kampanyalar (şube ve segment hedefli).

### 5.3 Ön sipariş akışı
1. Şube seç (harita/liste; favori şube önerilir; kapalı veya ön siparişi kapalı şubeler gri).
2. Menü → ürün → modifikasyonlar: boy, sıcak/soğuk (zorunlu seçim, soğuk seçilince buz seviyesi), süt (inek / laktozsuz / yulaf / badem; ek ücret HQ'dan), şurup, ekstra shot, şeker, not.
3. Sepet → teslim zamanı: "Hemen" (hazırlık süresi + yoğunluk = tahmini dakika) veya planlı (15 dk aralıklarla, bugün).
4. Ödeme: cüzdan bakiyesi → yetersizse kart / yemek kartı; kampanya ve puan kullanımı burada.
5. Sipariş durumu: **Alındı → Hazırlanıyor → Hazır → Teslim edildi**. Kullanıcı şubeye yaklaşınca (geofence 200 m) veya "Geldim" butonuyla barista ekranına sinyal gider; planlı siparişte hazırlık "Geldim" ile başlar (kahve soğumaz).
6. Teslim sonrası: puan yazılır, tek dokunuş memnuniyet (1–5), 4–5 ise Google yorum linki, 1–3 ise şikayet formu → HQ ve şube müdürüne bildirim.

### 5.4 Sadakat kuralları (varsayılan; HQ'dan değiştirilebilir)
- Kazanım: 1 TL = 1 çekirdek; her 10 içecekte 1 içecek hediye (damga sayacı ayrı gösterilir).
- Seviyeler: son 6 ay harcaması Classic < 2.500 TL ≤ Plus < 7.500 TL ≤ Premium.
- Plus: doğum günü içeceği, boy yükseltme ayda 2; Premium: ek shot/şurup ücretsiz, etkinlik daveti, manzaralı masa önceliği.
- Puan geçerliliği 12 ay; hatırlatma push 30 gün önce.
- Cüzdan yüklemesinde bonus: 500 TL yüklemeye 25 TL (kampanya bazlı).

### 5.5 Kart ekranı
- QR kod (ödeme + puan tek QR; barista okutur).
- Bakiye, yükleme (kredi/banka/Multinet/Sodexo/Setcard), hareketler.
- Hediye gönder: telefon numarasına kahve veya bakiye.

### 5.6 Bildirimler
- Sipariş durumları, kampanya (segment: şube yakınlığı, son ziyaret, favori ürün), seviye değişimi, puan bitiş uyarısı, ölü saat teklifi (HQ AI kuralı).

### 5.7 Barista ekranı (şube tableti)
- Gelen siparişler kartlar halinde; modifikasyonlar büyük ve renkli (laktozsuz = mor etiket, soğuk = mavi).
- "Hazırlanıyor" / "Hazır" dokunuşları; "Geldim" sinyali gelen sipariş en üste çıkar ve ses verir.
- POS'a otomatik fiş; e-fatura entegratörüne aktarım.

---

## 6. HQ paneli nasıl çalışır

| Modül | İşlev |
|---|---|
| Dashboard | Şube bazlı günlük/aylık ciro, sipariş sayısı, ortalama sepet, uygulama payı, sadakat üyeleri, yorum puanı; uyarılar: ciro eşiği (12.3), denetim uyarısı sayısı (6.18: 6 ayda 3), kapalı gün (6.28), kamera pasif (6.23) |
| Şubeler | Tek şube kaydı: NAP, saatler, özellikler, galeri, POS ID, GBP/Yandex ID; kaydet → web sayfası, uygulama, GBP açıklaması senkron |
| Menü ve fiyat | Ürün, fiyat grubu (İstanbul / Anadolu / Karadağ), modifikasyon ücretleri, sezon takvimi; yayın tarihi planlama |
| Kampanya | Kural motoru: hedef (şube, seviye, son ziyaret, saat), ödül, bütçe, süre; sonuç: kullanım, gelir, ROI |
| Sadakat | Kazanım oranları, seviye eşikleri, ödül kataloğu |
| Royalty | POS cirosundan otomatik %5 + KDV hesabı, aylık bildirim formu (6.23) otomatik doldurulur, franchise alan onaylar |
| Denetim | Denetim planı, rapor yükleme, eksik listesi ve süre sayacı, gizli müşteri raporu AI özeti, uyarı sayacı |
| Yorumlar | Google, Yandex, uygulama, Şikayetvar tek gelen kutusu; AI sentiment ve yanıt taslağı; şube skoru |
| Franchise lead | Pipeline (yeni → görüşme → lokasyon → sözleşme), AI skor, bölge boşluk haritası (3 km koruma çakışması kontrolü) |
| İçerik | Blog, SSS, sosyal takvim, AI taslak; ajans rolü |
| Kullanıcılar | Roller ve şube yetkileri; sözleşme bitiminde erişim iptali (13.2) |

## 7. Franchisee portalı nasıl çalışır

- Giriş: şube müdürü hesabı (HQ açar).
- Ana ekran: bu ayın cirosu, royalty tahmini, uygulama siparişleri, yorum puanı, açık denetim maddeleri, tedarik sipariş durumu.
- Ciro bildirimi: POS'tan gelen rakam görünür; müdür "onayla" der veya itiraz açar (6.23).
- Tedarik: merkezi liste (6.4), sepet, teslim ve 40 gün vade takibi (6.10).
- Eğitim: video modüller, sınav, sertifika; yeni personel ekleyince otomatik atama (8).
- Yerel kampanya talebi: form → HQ onayı (7.2: onaysız kampanya yasak).
- Belgeler: sözleşme, kılavuzlar; sona erme durumunda erişim kapanır (13.2).

## 8. AI asistan nasıl çalışır (WhatsApp / Instagram / site)

- Kanal: WhatsApp Business API, Instagram DM, site sohbet balonu; aynı motor.
- Bilgi tabanı: menü, fiyat, şube saatleri, sadakat kuralları, politika metinleri (HQ panelinden beslenir).
- Yetenekler: en yakın şube, menü sorusu, alerjen/süt sorusu, sipariş oluşturma (üye ise uygulama sepetine yazar ve ödeme linki gönderir), sipariş durumu, şikayet alma (HQ'ya kayıt, insan devri), franchise ön bilgi (lead oluşturma).
- Kurallar: fiyat ve stok her zaman API'den; emin olmadığında insana devret; her konuşma HQ gelen kutusunda; KVKK aydınlatma ilk mesajda.

## 8b. AI destekli aday havuzu (İK CRM) nasıl çalışır

**Amaç:** Başvuru bir dosyada beklemesin; her açık vardiya, havuzdaki müsait adaya dakikalar içinde sorulsun ve kesin bir yanıtla kapansın.

**Aday tarafı (site + uygulama)**
- Dört adımlı başvuru (kimlik, tercihler, beceri öz değerlendirmesi, tanışma). "Profil gücü" göstergesi ve adım başına motivasyon notu; tam profil eşleştirme isabetini artırır.
- Aday durumu: `müsait` / `2 hafta sonra` / `meşgul` / `havuzdan çıktı`. Aday istediği an değiştirir.
- Her bildirim bir **soru**dur ve tek dokunuşla üç yanıttan biriyle kapanır: Evet / Hayır / 2 hafta sonra. Serbest metin yok; yanıtsız bildirim bırakılmaz.
- SLA: 4 saatte yanıt yoksa hatırlatma; 24 saatte yanıt yoksa aday `belirsiz` olur, öncelik sırası düşer. Yanıt oranı yüksek adaylar sırada önde kalır.

**HQ / şube müdürü tarafı**
- Açık vardiya kaydı (şube, gün, saat, pozisyon) → yapay zekâ havuzu puanlar → ilk N adaya soru gider → ilk "Evet" ile vardiya kapanır, diğerlerine "dolduruldu" bilgisi gider.
- Şube müdürü yalnız onaylar; arama, mesajlaşma ve takip otomatiktir. Kapanma süresi, yanıt oranı ve gelmeme oranı panelde.

**Eşleştirme puanı (örnek ağırlıklar)**
- Tercih edilen şube +35 · şehir uyumu +20 · vardiya uyumu (gece/sabah/hafta sonu) +6–12 · pozisyon-şube uyumu +5 · beceri puanı ≥4 +4 · yanıt oranı ve gelmeme geçmişi ±10.
- Mesafe ve ulaşım süresi (adres verilirse) puana girer; 45 dakikanın üstü uyarı üretir.

**Veri modeli (ek)**
- `Candidate`(id, ad, iletişim, şehir, pozisyon, beceriler{}, diller, başlangıç, durum, öncelik, rıza_havuz, rıza_kvkk, silinme_tarihi)
- `ShiftNeed`(id, şube, pozisyon, başlangıç, bitiş, ihtiyaç_sayısı, durum)
- `Match`(candidate, shift_need, puan, gerekçeler[])
- `Ask`(match, kanal, gönderim, son_yanıt_tarihi, yanıt∈{evet,hayır,sonra,∅}, yanıt_süresi)

**Kenar durumları:** aday üç kez üst üste "Hayır" derse tercihleri yeniden sorulur; gelmeme durumunda şube müdürü işaretler, öncelik düşer; 18 yaş altı başvurular reddedilir; "artık arama" sonrası 30 gün içinde silme.

## 9. Veri modeli (özet)

```
Branch(id, name, slug, city, priceGroup, address, geo, hours[], features[], posId, gbpId, yandexId, status)
Product(id, name_tr, name_en, category, description, image, nutrition, allergens, seasonal, active)
Price(productId, priceGroup, size, amount)
Modifier(id, name, type, prices{priceGroup}, allergen)
User(id, phone, name, birthday, consents, level, points, stampCount, walletBalance, favoriteBranchId)
Order(id, userId, branchId, items[], modifiers[], total, paymentMethod, status, scheduledAt, arrivedAt, readyAt)
LoyaltyTxn(id, userId, orderId, points, type)
WalletTxn(id, userId, amount, method, bonus)
Campaign(id, rule, reward, targets, budget, start, end, stats)
Review(id, source, branchId, rating, text, sentiment, reply, status)
Audit(id, branchId, type, date, findings[], deadline, closedAt, warningCount)
Lead(id, contact, region, budget, experience, score, stage)
RoyaltyStatement(id, branchId, month, grossRevenue, royalty, status)
```

## 10. Sipariş durum makinesi

```
[Sepet] --öde--> [Alındı] --barista başlat--> [Hazırlanıyor] --barista--> [Hazır] --teslim--> [Teslim edildi]
   │                 │                                                          │
   └--iptal (ödeme öncesi)                                                      └--15 dk alınmazsa: hatırlatma push
[Alındı] --planlı ve "Geldim" gelmedi--> bekler (hazırlık "Geldim" veya geofence ile başlar)
[Alındı] --şube kapandı/POS arıza--> [İptal, iade cüzdana]
```

## 11. Kenar durumları

| Durum | Davranış |
|---|---|
| Şube ön siparişi kapattı (yoğunluk, arıza) | Uygulamada şube "Şu an yalnızca kasadan" etiketi; planlı siparişler korunur |
| Ürün şubede yok | Şube stok bayrağı; ürün gri, alternatif öneri |
| İnternet yok (barista) | Ekran son 50 siparişi önbellekte tutar; bağlantı gelince senkron |
| Fiyat farkı (şube grubu) | Sepette şube fiyatı; şube değişince sepet yeniden fiyatlanır ve kullanıcı bilgilendirilir |
| Puan ile ödemede iade | Puan geri yazılır, cüzdan kısmı cüzdana |
| Karadağ | EUR fiyat grubu, EN/ME dil, yerel PSP; sadakat puanı ortak, ödül kataloğu ülkeye göre |
| KVKK silme talebi | Uygulama içi "hesabımı sil" → 30 gün içinde anonimleştirme; sipariş kayıtları mali mevzuat süresince tutulur |

## 12. Demo kapsamı (prototipte gösterilen)

| Ekran | Demo davranışı |
|---|---|
| Google öncesi/sonrası | Statik iki SERP mockup'ı |
| Web ana sayfa + Kavacık şube sayfası | Filtreler çalışır, şube kartına tıklayınca şube sayfası açılır |
| Uygulama | Onboarding atlanmış; ana ekran → sipariş (modifikasyon) → ödeme → durum → "Geldim" → puan artışı; kart ekranı QR ve yükleme |
| HQ paneli | 15 şube tablosu, uyarılar, yorum gelen kutusu ve AI yanıt taslağı |
| AI asistan | WhatsApp görünümlü senaryo: laktozsuz iced latte siparişi ve şikayet devri |
| Franchise | Yatırım hesaplayıcı ve 3 adımlı form, lead skoru |

Demo veriler örnektir; gerçek menü, fiyat ve şube verisi keşif aşamasında yüklenecektir.
