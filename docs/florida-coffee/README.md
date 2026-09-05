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
| `demo-site/embed_images.py` | `img/` karelerini JPEG data-URI olarak `index.html` yuvalarına gömer (artifact harici dosya yükleyemez) |
| `site/build.py` | Çok sayfalı statik site üreticisi (Python 3.12). `demo-site/index.html`'den ortak CSS/JS/veriyi çeker, 77 sayfa üretir: ana sayfa, menü + 25 ürün sayfası, 17 şube sayfası, kahvemiz, taze + 8 haber, ürünler + 4 ürün, kulüp, uygulama, franchise (+ başvuru, SSS), kariyer, kurumsal, etkinlikler, hikâyemiz, SSS, iletişim, 4 yasal metin, EN özet, 404; her sayfada JSON-LD, sitemap.xml, robots.txt (demo: noindex) |
| `dist/` | Yayın paketi: `site/build.py` çıktısı + `app/` (mobil uygulama demosu) + `platform/` + `sunum/`. Vercel veya GitHub Pages'e olduğu gibi yüklenir |
| `04-sunum-deck.html` | Görüşme sunumu: 16 slayt, ok tuşlarıyla ilerler, `N` konuşmacı notları, `F` tam ekran |

## Siteyi yeniden üretmek

```
cd docs/florida-coffee/site && python3.12 build.py
```

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
