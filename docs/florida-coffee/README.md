# Florida Coffee — Web + Mobil Uygulama Projesi (P3Media)

| Dosya | İçerik |
|---|---|
| `00-analiz-raporu.md` | Kapsamlı ön analiz: pazar, rakip, kitle, anahtar kelime, SEO, marka, kullanıcı, site yapısı, mobil uygulama, yapay zeka, veri katmanı, yol haritası, demo/sunum planı |
| `01-anahtar-kelime-listesi.csv` | 120 anahtar kelime; küme, niyet, hedef sayfa, öncelik. Semrush `phrase_these` (database=tr) ile hacim/zorluk doğrulaması yapılacak |
| `02-sunum.html` | Analiz raporunun okunabilir HTML sürümü |
| `03-fonksiyonel-tasarim.md` | Site, uygulama, barista ekranı, HQ paneli, franchisee portalı ve AI asistanın nasıl çalıştığı: roller, akışlar, sadakat kuralları, sipariş durum makinesi, veri modeli, kenar durumları |
| `demo/index.html` | Tıklanabilir demo prototipi: SERP karşılaştırması, web sitesi, mobil uygulama, HQ paneli, WhatsApp AI asistanı, franchise hesaplayıcı |
| `demo-site/index.html` | "Boğaz'da Bir Gün" demo sitesi; marka kimliği, gerçek el kitabı standartları, etkileşim katmanı, gömülü görseller |
| `demo-site/gen_images.py` | Nano Banana Pro (`gemini-3-pro-image`) ile 12 marka karesini üretir. `GEMINI_API_KEY` ortam değişkeninden okur, anahtar dosyaya yazılmaz |
| `demo-site/gen_video.py` | Veo 3.1 (`veo-3.1-fast-generate-preview`) ile 3 marka klibi (hero 16:9, pour 16:9, night 9:16); ilk kare `img/` karesinden, hedef orana kırpılarak verilir. `GEMINI_API_KEY` ortam değişkeninden okur |
| `demo-site/brand/` | Franchise sunumundan çıkarılan gerçek logo: orijinal, koyu zemin için krem sürüm ve "o" harfi delinmiş kelime işaretleri (delik yerine animasyonlu SVG "o" oturur) |
| `demo-site/video/` | Üretilen klipler; ana sayfa hero, Kahvemiz (pour) ve Gece (night) bölümlerinde arka plan videosu |
| `demo-site/embed_images.py` | `img/` karelerini, marka görsellerini ve hero videosunu data-URI olarak `index.html`'e gömer (artifact harici dosya yükleyemez); diğer videolar `video/` yoluyla kalır |
| `site/build.py` | Çok sayfalı statik site üreticisi (Python 3.12). `demo-site/index.html`'den ortak CSS/JS/veriyi çeker, 77 sayfa üretir: ana sayfa, menü + 25 ürün sayfası, 17 şube sayfası, kahvemiz, taze + 8 haber, ürünler + 4 ürün, kulüp, uygulama, franchise (+ başvuru, SSS), kariyer, kurumsal, etkinlikler, hikâyemiz, SSS, iletişim, 4 yasal metin, EN özet, 404; her sayfada JSON-LD, sitemap.xml, robots.txt (demo: noindex) |
| `dist/` | Yayın paketi: `site/build.py` çıktısı + `app/` (mobil uygulama demosu) + `platform/` + `sunum/`. Vercel veya GitHub Pages'e olduğu gibi yüklenir |
| `04-sunum-deck.html` | Görüşme sunumu: 16 slayt, ok tuşlarıyla ilerler, `N` konuşmacı notları, `F` tam ekran |

## Siteyi yeniden üretmek

```
cd docs/florida-coffee/site && python3.12 build.py
```

Palet logodan ölçülen gerçek değerlerdir: petrol #004854, amber #F09C1C, pas #D44808.

Ana sayfa hikâyesi, Flo motoru, şube ve menü verisi tek kaynaktan (`demo-site/index.html`) gelir; alt sayfa içerikleri `build.py` içindedir.

## Görüşme akışı

1. Sunum slayt 1–4 (durum ve sözleşme argümanı)
2. Demo: Google sekmesi → Web → Uygulama → HQ → AI → Franchise
3. Sunum slayt 11–15 (farklılaştırma, yol haritası, ticari model, pilot)
4. Keşif soruları (rapor §15.3), pilot tarihi

## Teklif öncesi kapatılacaklar

- Semrush API birimi yüklenip kelime hacimleri, backlink profili ve rakip kelime boşluğu çekilecek
- Mevcut POS/otomasyon ve uygulamanın kaynak kod durumu öğrenilecek
- Şube listesi, saatler ve marka kılavuzu müşteriden alınacak
