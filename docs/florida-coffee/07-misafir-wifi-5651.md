# Florida Coffee · misafir Wi-Fi ve 5651 loglama (P3Media iç dokümanı)

Durum: Müşteri, şubelerinde kullandığı **Netway** hotspot/5651 hizmetini sorguluyor; "şube başına 20.000 ₺ ve üzeri" ödediklerini, bunu bizim sağlayıp sağlayamayacağımızı soruyor. Bu doküman işi üç katmana ayırır, üç tedarik senaryosunu fiyatlar, ticari modeli ve KVKK kurallarını belirler, ISP'ye ve müşteriye gidecek metinleri hazırlar. Tarih: 12 Eylül 2026. Kur varsayımı: 1 € = 56 ₺. Tüm tutarlar KDV hariç.

İlişki: 17 Eylül'de sunulacak yazılı teklifin kapatıcı argümanı buradan çıkıyor (bkz. §5). `06-teklif-plani.md` §9'a 16. madde olarak eklendi.

---

## 0. Kısa cevap

1. **Sağlayabilir miyiz?** Evet — ama tamamını değil, doğru katmanını. Netway üç ayrı işi tek fatura altında paketliyor; bu paket çözüldüğünde iki katman çok ucuza, üçüncüsü zaten bizim işimiz.
2. **Netway pahalı mı?** Muhtemelen evet, ama **birim teyit edilmeden fiyat verilmez.** 20.000 ₺ aylıksa yıllık ≈ 72.900 € (teklifimizin %76'sı); yıllıksa ≈ 6.100 € (önemsiz). Aynı cümle iki farklı iş anlamına geliyor. **Netway faturası görülmeden hiçbir rakam söylenmeyecek.**
3. **Ne satacağız?** Katman 3'ü (markalı giriş ekranı + veri + uygulamaya dönüşüm). Katman 1 ve 2'yi (donanım, yasal loglama, saha) dışarıdan tedarik edip white-label yeniden satacağız; yasal sorumluluk lisanslı sağlayıcıda kalır.
4. **En kritik ticari karar:** Bu tasarrufu **bedava vermeyeceğiz.** Önerilen yol: ayrı fatura değil, 96.000 €'luk teklifin kapatıcısı — *"Wi-Fi faturanızı yarıya indiriyoruz, tasarruf platformun bir kısmını finanse ediyor."* Ayrı bir migrasyon ücretinden kat kat değerli.
5. **En kritik teknik karar:** Hangi sağlayıcıya gidilirse gidilsin, **giriş ekranı bizde olacak.** Kendi captive portalımıza yönlendirme (RADIUS/UAM) desteklemeyen hiçbir teklif kabul edilmeyecek — yoksa Netway silosundan çıkıp başka bir siloya girmiş oluruz.
6. **Üstlenmeyeceğimiz şey:** 17 şubenin 7/24 Wi-Fi arıza desteği. Yerel saha partneri sözleşmeye bağlanmadan Katman 1–2 taahhüt edilmez. P3Media dijital ajanstır, managed service provider değil.

---

## 1. Netway aslında ne satıyor

Tek fatura, üç ayrı iş:

| # | Katman | İçerik | Gerçek maliyeti | Kim yapmalı |
|---|---|---|---|---|
| 1 | **Şube donanımı** | Girişi zorlayan gateway; hangi cihaza hangi IP verildiğini kaydeder | Tek seferlik, düşük | Yerel partner |
| 2 | **Yasal uyum** | Zaman damgalı kayıt, 2 yıl saklama, denetim/savcılık talebine cevap | Aylık, düşük | Lisanslı sağlayıcı |
| 3 | **Hotspot deneyimi** | Giriş ekranı, SMS doğrulama, marka, rıza, yönlendirme | Geliştirme işi | **P3Media** |

Bunların üstüne satılan dördüncü bir şey var: **korku.** Türk 5651 pazarı "hapis cezası" diliyle satıyor. Gerçekte kafe gibi ikincil Wi-Fi sunan bir işletme için yaptırım idari para cezasıdır; hapis maddesi erişim sağlayıcılara yöneliktir. Satıcı sayfalarının bu ayrımı bulanık bırakması tesadüf değil — pazarlık gücümüz burada.

Kritik teknik gerçek: mevzuatın kafeden istediği asıl kayıt **iç IP dağıtım logu**, yani tam olarak Katman 1'deki gateway'in ürettiği şey. **Zorunlu bileşen, en ucuz bileşen.** 20.000 ₺, bunun üstüne kurulmuş bir paketleme marjıdır.

---

## 2. Yasal çerçeve — kısa ve kimin üstünde

5651 sayılı Kanun ve bağlı yönetmelik kapsamında Florida Coffee "ticari amaçla internet toplu kullanım sağlayıcısı" sayılır. Yükümlülükler:

- Mülki idare amirinden (kaymakamlık) **izin belgesi**
- Erişim sağlayıcıdan **sabit IP**, güncel tutulması
- Suç oluşturan içeriğe erişimi önleyici tedbir / onaylı **filtreleme**
- **Erişim kayıtlarını 2 yıl saklamak**, doğruluk ve bütünlüğü korumak (pratikte: yasal **zaman damgası** ile imzalama)
- Üstüne **KVKK (6698)**: telefon numarası ve kimlik verisi kişisel veridir → aydınlatma, hukuki sebep, saklama süresi, veri işleyen sözleşmesi

**Yükümlülük ve ceza işletmenin üstündedir, sağlayıcının değil.** Netway teknik aracı sağlar; denetimde muhatap Florida Coffee'dir. Bu bizim lehimize argümandır: "sorumluluk sizde olduğu için bunun doğru kurulması sizin çıkarınıza."

İki nokta yazılı avukat görüşüne bağlanacak (teklif öncesi, `06-teklif-plani.md` §6'daki mali müşavir teyidinin yanına):

1. **Rejim kapsamı.** İzin belgesi + onaylı filtreleme yükümlülüğünün tamamı internet kafelere mi (internetin ana iş olduğu yerler) özgü, yoksa ikincil Wi-Fi sunan kafeler de tam kapsamda mı? Mevzuatta ayrım var; satıcılar en geniş yorumu satıyor. Cevap, alacağımız hizmetin kapsamını ve fiyatını doğrudan belirliyor.
2. **Kullanıcı seviyesi kayıt.** ISP'nin hat seviyesinde tuttuğu kayıt, işletmeden istenen kullanıcı seviyesi kaydı karşılıyor mu? (Gateway bunu çözüyor, ama yazılı teyit gerekli.)

Karadağ (Budva) 5651 kapsamı dışındadır — GDPR ve yerel mevzuat geçerli. Teklifte Karadağ zaten opsiyon; bu kalem de opsiyonda kalacak.

---

## 3. Üç tedarik senaryosu

Üçünde de Katman 3 (giriş ekranı + veri) P3Media'da. Fark, Katman 1–2'nin nereden alındığı.

| | **S1 · ISP uyum servisi** | **S2 · White-label sağlayıcı** | **S3 · Tam kendi kurulum** |
|---|---|---|---|
| Katman 2 kaynağı | Turkcell / Türk Telekom kurumsal 5651 loglama | Safir Cloud, NextLog5651, Useroam, Wifilog sınıfı | Kendi log deposu + zaman damgası kontörü |
| Yasal sorumluluk taşıyıcısı | ISP (hizmet kapsamında) | Lisanslı sağlayıcı | **Florida Coffee + dolaylı olarak biz** |
| Aylık maliyet (17 şube toplam) | Teklif alınacak · tahmin **90 – 300 €** | Teklif alınacak · tahmin **75 – 245 €** | **42 – 85 €** (hesaplanmış, §4) |
| Saha desteği | ISP kendi hattına bakar (avantaj) | Sağlayıcıya göre değişir | Tamamen bizde (risk) |
| Katman 3 kontrolü | RADIUS/UAM desteğine bağlı — **sorulacak** | Genelde var, sorulacak | Tam |
| Kurulum eforu | Düşük | Düşük | Yüksek (15–20 gün geliştirme) |
| Operasyon riski | En düşük | Düşük | **En yüksek** |
| Karar | **Birinci tercih** | Yedek / pazarlık kozu | Reddedilir (tek müşteri için yapılmaz) |

Turkcell'in kurumsal 5651 loglama servisi kendini *"herhangi bir operatörden internet hizmeti alan müşteriler"* için tanımlıyor — yani **operatör bağımsız.** Pratik sonucu önemli: şubelerin interneti farklı operatörlerde olsa bile 17 şubeyi tek uyum sağlayıcıda toplayabiliriz. Bu, envanter dağınıksa S1'i daha da güçlendirir.

S1'in tek gerçek riski: ISP paketi genelde **loglama** satıyor, markalı hotspot portalı satmıyor. Bu bizim için sorun değil, **fırsat** — çünkü giriş ekranını zaten biz yapmak istiyoruz. Tek şart, ISP'nin kendi portalımıza yönlendirmeyi desteklemesi (§10'daki teklif talebinin 4. sorusu).

S3 neden reddediliyor: 2 yıl log saklama, bütünlük ve KVKK veri işleyen yükümlülüğünü tek müşteri için üstlenmek, kazanılan marja göre orantısız risk. Teknik olarak yapılabilir; ticari olarak yanlış.

---

## 4. Gerçek maliyet modeli

**Tek seferlik, şube başına**

| Kalem | ₺ | Not |
|---|---|---|
| Gateway (MikroTik RB5009 sınıfı) | 3.000 – 6.000 | Mevcut access point'ler kalır, sadece çıkış cihazı değişir |
| Yerinde kurulum (yerel partner) | 1.500 – 3.000 | |
| **Şube başına toplam** | **5.000 – 9.000** | |
| **17 şube** | **85.000 – 153.000 ₺ (1.520 – 2.730 €)** | Bazı şubelerde mevcut AP'ler yeterli olabilir → envanter şart |

**Tek seferlik, merkezi geliştirme (Katman 3)**

Captive portal + RADIUS entegrasyonu + SMS OTP + rıza akışı + uygulamaya dönüşüm + yönetim ekranı ≈ **15–20 gün.** Kapsam dışı gün ücretimizle (650 €) **10.000 – 13.000 €**. Bu bir maliyet değil satış kalemi; teklife girerse gelir.

**Aylık işletme — 17 şubenin TOPLAMI (şube başına değil)**

| Kalem | € / ay |
|---|---|
| VPS + log deposu (loglar düz metin, hacim minik) | 15 – 40 |
| Zaman damgası kontörü (17 şube × 365 günlük paket imzası ≈ 6.200 imza/yıl) | 2 – 5 |
| SMS OTP (cihaz 30 gün hatırlanırsa yeni giriş sayısı düşer) | 15 – 30 |
| İzleme / uptime | ~10 |
| **Toplam** | **42 – 85 € (şube başına 2,5 – 5 €)** |

**Ve asıl maliyet: saha desteği.** 17 şube, sabah 07:00'de arayan barista. Yerel bakım sözleşmesi tahmini **15.000 – 30.000 ₺/ay (270 – 540 €)**. S1'de ISP kendi hattına baktığı için bu kalem düşer. **Bu satır ihmal edilirse bütün marj hesabı yanlış çıkar.**

Okuma: teknoloji neredeyse bedava, hukuk ucuz, **insan pahalı.** Netway'in fiyatı yazılımın değil, sorumluluk ve saha varlığının fiyatıdır.

---

## 5. Ticari model

**Önce birim.** İki senaryo, aynı cümlenin iki okuması:

| | Senaryo A · 20.000 ₺ **aylık**/şube | Senaryo B · 20.000 ₺ **yıllık**/şube |
|---|---|---|
| Müşterinin bugün ödediği | 340.000 ₺/ay ≈ 6.070 €/ay ≈ **72.900 €/yıl** | 340.000 ₺/yıl ≈ **6.070 €/yıl** |
| Teklifimizle kıyas | 12 aylık teklifimizin **%76'sı** | %6'sı |
| Önerilen fiyatımız | 8.000 ₺/ay/şube = 136.000 ₺/ay (**2.430 €/ay**) | 12.000 ₺/yıl/şube = 204.000 ₺/yıl (**3.640 €/yıl**) |
| Müşteri tasarrufu | 204.000 ₺/ay ≈ **43.700 €/yıl** | 136.000 ₺/yıl ≈ **2.430 €/yıl** |
| Bizim maliyetimiz | ~350 – 850 €/ay (tedarik + saha) | ~1.500 – 2.500 €/yıl |
| **Net marj** | **~19.000 – 25.000 €/yıl** | **~1.100 – 2.100 €/yıl** |
| Karar | **Ayrı sözleşme kalemi yap** | **Ayrı iş kolu yapma; teklifin kapatıcısı olarak kullan** |

**Paraya çevirmenin üç yolu, sıralı tercih:**

1. **Teklifin kapatıcısı (önerilen, her iki senaryoda geçerli).** Ayrı faturalanmaz. Sunum cümlesi:
   > *"Wi-Fi faturanızı yarıya indiriyoruz. Tasarruf ettiğiniz para platformun bir kısmını kendi kendine finanse ediyor."*
   
   Senaryo A doğruysa bu, 96.000 €'luk teklifi fiyat pazarlığından tamamen çıkarır: ortaya çıkan ~43.700 €/yıl tasarruf teklifin yaklaşık yarısını müşterinin cebinden çıkmadan öder. Ayrı bir 5.000 € migrasyon ücretinden kat kat değerlidir.
2. **Migrasyon projesi.** Denetim + ISP'den teklif toplama + geçiş yönetimi + portal = tek seferlik kalem, tasarrufla gerekçelendirilir. Senaryo A'da 1'e ek olarak satılabilir.
3. **12 ay tasarruf payı.** Türkiye'de zor satılır, masaya konmayacak.

**İki kırmızı çizgi:**

- **Netway sözleşmesini biz feshetmeyeceğiz.** Analizi ve alternatifi biz koyarız; kararı ve imzayı Florida Coffee verir. Geçiş riski müşteride kalır.
- **Bedava analiz yok.** Katman 1–2 karşılaştırmasını yazılı verirsek, müşteri parayı kendi kurtarır ve bize sıfır kalır; üstüne bir şube çöktüğünde "sizin tavsiyenizdi" denir. Karşılaştırma tablosu ancak teklif kapsamında veya imza sonrası paylaşılır.

---

## 6. Asıl değer: Katman 3

Netway'den çıkış iki kazanç getiriyor, ve ikincisi daha büyük:

1. Fatura düşer.
2. **Giriş ekranı bize geçer.** Şu an 17 şubede kapıdan geçen herkes telefon numarasını Netway'in veritabanına yazıyor; Florida Coffee'ye hiçbir şey kalmıyor.

Kurulacak akış:

Wi-Fi'a bağlan → markalı portal → SMS OTP → **iki ayrı kutu** (erişim / pazarlama) → internet açılır → aynı ekranda *"Uygulamaya üye ol, ilk kahve bizden"* → uygulama üyeliği → sadakat.

Bu, `06-teklif-plani.md` §3.3'teki başarı primi eşiğini (12. ayda ≥ 40.000 aktif üye) besleyen en düşük maliyetli kanaldır: aynı SMS OTP altyapısı, ek edinim maliyeti yok, kişi zaten mağazada ve elinde telefon var. Portal aynı zamanda şube bazlı ziyaret sıklığı verisi üretir — HQ panelindeki şube karşılaştırma ekranına doğrudan girer.

---

## 7. KVKK — iki kutu kuralı

Piyasadaki hotspot portallarının çoğunun yanlış yaptığı yer, ve bizim değer kattığımız yer:

| Amaç | Hukuki sebep | Kutu |
|---|---|---|
| Erişim kaydı tutma | Kanuni yükümlülük (5651) | Rıza gerekmez, aydınlatma yeterli |
| Pazarlama iletişimi (SMS/e-posta/push) | **Açık rıza** | **Ayrı, işaretsiz kutu** |

"Kabul et yoksa Wi-Fi yok" şeklinde tek kutuda birleştirmek ihlaldir — rıza özgür iradeye dayanmaz. Doğru kurulmuş iki kutulu ekran hem uyumlu olur hem de **gerçekten izinli, temiz bir liste** bırakır; İYS (İleti Yönetim Sistemi) kaydı da bu rızaya dayanır.

Ek gereklilikler: portalda aydınlatma metni ve gizlilik politikası bağlantısı, saklama süresinin yazılı olması, veri sorumlusu Florida Coffee / veri işleyen P3Media ayrımı ve DPA eki (`06-teklif-plani.md` §9 madde 9 ile aynı çerçeve).

---

## 8. Riskler ve karşılıkları

| Risk | Karşılık |
|---|---|
| Netway donanımı onların malı → geçişte 17 şube donanımı yeniden alınır | Sözleşmeden **donanım mülkiyeti** teyit edilir; maliyet ilk yıl tasarrufundan düşülerek hesaba katılır |
| Netway fesih cezası / süre taahhüdü | Sözleşme okunmadan geçiş takvimi verilmez |
| ISP teklifi beklenenden yüksek gelir → bütün çerçeve çöker | **Yazılı ISP teklifi alınmadan müşteriye rakam söylenmez** (§10) |
| Yeni sağlayıcı da veriyi paylaşmaz → silodan siloya geçiş | RADIUS/UAM + veri dışa aktarım şartı, teklif talebinin eleme kriteri |
| 17 şubenin Wi-Fi desteği bize düşer, platform işi durur | Yerel saha partneri sözleşmesi **önkoşul**; yoksa Katman 1–2 taahhüt edilmez |
| Şubelerin izin belgesi yok → denetimde ceza, suç bizim geçişe yüklenir | Geçiş öncesi izin belgesi durumu yazılı olarak tespit edilir; eksikse müşteri tamamlar |
| Rejim kapsamı yorumu yanlış → eksik veya fazla hizmet alınır | Avukat görüşü (§2), teklif öncesi |
| Tasarruf analizi bedava verilir, karşılığı alınmaz | Karşılaştırma tablosu teklif kapsamında paylaşılır (§5) |

---

## 9. Söz vermeden önce toplanacak veriler

**Müşteriden:**

1. Netway **faturası** — birim (ay/yıl/tek sefer), şube başı mı toplam mı, KDV dahil mi
2. Netway **sözleşmesi** — süre, fesih bildirimi, cezai şart, **donanım mülkiyeti**
3. **Şube envanteri** — şube × ISP, tarife, sabit IP var mı, modem/AP marka-model
4. Her şubenin **kaymakamlık izin belgesi** durumu
5. Netway panelinden **giriş verisine erişim** var mı; dışa aktarılabiliyor mu
6. Günlük yaklaşık misafir Wi-Fi giriş sayısı (SMS maliyeti bunun fonksiyonu)

**Kendi tarafımızda:**

7. Turkcell ve Türk Telekom kurumsal'dan **yazılı teklif** (§10)
8. İki white-label sağlayıcıdan karşılaştırma teklifi (Safir Cloud, NextLog5651)
9. **Yerel saha partneri** — İstanbul + Sakarya'da 17 şubeye gidebilecek ağ firması, aylık bakım fiyatı
10. Avukat görüşü — rejim kapsamı ve kullanıcı seviyesi kayıt (§2)

Bu on kalem kapanmadan ne müşteriye fiyat verilir ne de teklife kesin bir kalem yazılır.

---

## 10. ISP'ye gidecek teklif talebi (kopyala-gönder)

> **Konu:** 17 lokasyon için misafir Wi-Fi / 5651 uyumlu erişim kaydı — teklif talebi
>
> Merhaba,
>
> Türkiye'de 17 şubeli bir kahve zinciri adına misafir Wi-Fi altyapısının 5651 uyum tarafı için teklif topluyoruz. Şubelerin internet hizmeti şu anda tek operatörde değil; bu nedenle operatör bağımsız çalışabilen bir çözüm arıyoruz.
>
> İhtiyaç: misafir kullanıcıların internet erişiminin kullanıcı seviyesinde kayıt altına alınması, kayıtların yasal zaman damgası ile imzalanması ve 2 yıl saklanması; denetim veya resmî talep hâlinde kaydın teslim edilebilmesi.
>
> Aşağıdaki başlıklarda yazılı teklif ve teknik yanıt rica ediyoruz:
>
> 1. **Fiyat.** Lokasyon başına aylık ve yıllık bedel; 17 lokasyon için toplam. Kurulum bedeli ayrı mı? Hacim indirimi var mı?
> 2. **Kapsam.** Hizmet operatör bağımsız mı — farklı operatörlerden internet alan lokasyonlar da kapsanıyor mu?
> 3. **Donanım.** Lokasyon başına cihaz gerekiyor mu; dahil mi, kira mı, satın alma mı? Mevcut access point altyapısı korunabilir mi?
> 4. **Kendi giriş ekranımız (kritik).** Müşterinin marka kimliğiyle, bizim geliştirdiğimiz captive portalı kullanmak istiyoruz. **RADIUS / UAM ile dış portala yönlendirmeyi destekliyor musunuz?** Destekliyorsanız hangi protokol ve hangi dokümantasyonla?
> 5. **Veri erişimi.** Giriş kayıtlarına (telefon numarası, zaman, lokasyon) API veya düzenli dışa aktarım ile erişebiliyor muyuz? Formatı nedir?
> 6. **Kimlik doğrulama.** SMS doğrulama dahil mi; SMS bedeli kime ait?
> 7. **Uyum sorumluluğu.** Resmî bir log talebinde muhatap kim; siz hangi taahhüdü veriyorsunuz? Zaman damgası hizmet sağlayıcınız hangisi?
> 8. **KVKK.** Veri sorumlusu / veri işleyen ayrımı nasıl kuruluyor; DPA şablonunuz var mı? Veriler nerede saklanıyor?
> 9. **Kurulum ve destek.** Lokasyon başına kurulum süresi; arıza durumunda yerinde müdahale kapsamda mı, SLA nedir?
> 10. **Sözleşme.** Asgari süre, fesih koşulları, lokasyon ekleme/çıkarma esnekliği.
>
> Not: 4 ve 5 numaralı maddeler bizim için eleme kriteridir; kendi giriş ekranımızı kullanamadığımız ve giriş verisine erişemediğimiz bir çözüm değerlendirmeye alınmayacaktır.
>
> Teşekkürler,
> P3Media

Aynı metin white-label sağlayıcılara (Safir Cloud, NextLog5651, Useroam, Wifilog) da gönderilir — 2. madde çıkarılır.

---

## 11. Müşteriye gidecek e-posta (kopyala-gönder)

> **Konu:** Misafir Wi-Fi — mevcut hizmetinize bakalım
>
> Merhaba,
>
> Netway hizmetini sorduğunuz için teşekkürler. Kısa cevap: evet, bu alanda size yardımcı olabiliriz — ve muhtemelen şu anda ödediğinizden belirgin şekilde ucuza.
>
> Bu hizmet aslında üç ayrı işin tek fatura altında paketlenmiş hâli: şubedeki cihaz, yasal kayıt tutma, ve misafirin gördüğü giriş ekranı. Bu üçü ayrıldığında ilk ikisi piyasada düşündüğünüzden çok daha ucuza tedarik ediliyor; üçüncüsü ise zaten bizim uzmanlık alanımız.
>
> Üçüncü katman burada işin asıl değerli kısmı: şu anda 17 şubenizde kapıdan giren her misafir Wi-Fi'a bağlanmak için telefon numarasını veriyor, ama o numara sizde değil, hizmet sağlayıcının veritabanında kalıyor. Giriş ekranı sizin markanıza geçtiğinde aynı numara doğrudan sadakat programınıza ve mobil uygulamanıza akar — yani bugün bir gider kalemi olan şey, müşteri kazanma kanalına dönüşür.
>
> Somut bir karşılaştırma çıkarabilmemiz için üç şeye ihtiyacımız var:
>
> 1. Netway'in son faturası (bedelin aylık mı yıllık mı olduğunu ve neyi kapsadığını görmemiz gerekiyor)
> 2. Netway sözleşmesi (özellikle süre, fesih koşulu ve şubelerdeki cihazların kime ait olduğu)
> 3. Şube listesi: hangi şubede internet hangi operatörden, modem/access point marka-modeli
>
> Bunlar elimize geçtiğinde alternatifleri fiyatlarıyla karşılaştırıp önünüze koyarız. Tahmini bir rakam vermekten kaçınıyoruz çünkü bu hizmetin fiyatlandırması sağlayıcıdan sağlayıcıya ciddi farklılık gösteriyor ve elimizde fatura olmadan söylenecek her sayı yanıltıcı olur.
>
> Bir not: şubelerin kaymakamlıktan alınmış "ticari amaçla toplu kullanım sağlayıcı izin belgesi" durumunu da kontrol etmenizi öneririz. Bu belge ve yasal kayıt yükümlülüğü hizmet sağlayıcının değil, doğrudan işletmenin sorumluluğundadır — denetimde muhatap sizsiniz. Pratikte en sık atlanan ve en çok ceza yazılan nokta burası.
>
> Sevgiler,
> P3Media

---

## 12. Kaynaklar (Eylül 2026)

- Mevcut sağlayıcı: netwayhotspot.com ürün ve loglama sayfaları; Wisnet Teknoloji A.Ş. dağıtım sayfası
- ISP: Turkcell Kurumsal "5651 Loglama Servisi" (operatör bağımsız tanımı); Turkcell Kurumsal paket ve tarifeler
- White-label alternatifler: Safir Cloud (hotspot + 5651 + misafir Wi-Fi), NextLog5651, Useroam, Wifilog.tr, Safir Teknoloji hotspot sayfaları
- Mevzuat: 5651 sayılı Kanun ve İnternet Toplu Kullanım Sağlayıcıları Hakkında Yönetmelik; kaymakamlık izin belgesi sayfaları (Nilüfer, Defne, Meram, Aladağ, Karasu); 2 yıl saklama değişikliği (Webrazzi, Nisan 2017)
- Zaman damgası ve log bütünlüğü: Berqnet 5651 loglama ve zaman damgası yazıları; Skyron, Karya Teknoloji, Subgate
- Gateway yapılandırma referansı: TC kimlik ve SMS doğrulamalı MikroTik hotspot kurulum notları (serdarkurt.com.tr)
- Kur ve iç referanslar: `06-teklif-plani.md` (1 € = 56 ₺, 8 Eylül 2026; gün ücreti 650 €; §3.3 büyüme maddeleri)

**Teyit bekleyen veriler:** Netway birim fiyatı (ay/yıl/tek sefer), ISP yazılı teklifleri, white-label karşılaştırma teklifleri, yerel saha partneri bakım fiyatı, avukat görüşü. Bu dokümandaki "tahmin" işaretli bantlar bu teyitler geldiğinde gerçek rakamlarla değiştirilecek.
