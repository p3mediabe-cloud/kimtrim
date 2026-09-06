#!/usr/bin/env python3.12
"""Florida Coffee — çok sayfalı statik site üreticisi.
Kaynaklar: demo-site/index.html (ana sayfa hikâye demosu, Flo motoru, şube/menü verisi) + bu dosyadaki içerik.
Çıktı: ../dist/  (Vercel / GitHub Pages'e doğrudan yayınlanır)
Kullanım: python3 build.py
"""
import re, os, json, shutil, html as H
import json
from datetime import date

ROOT = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(ROOT)                 # docs/florida-coffee
DEMO = os.path.join(BASE, "demo-site", "index.html")
import sys, shutil, argparse
if sys.version_info < (3, 12): sys.exit("build.py Python 3.12+ ister (iç içe f-string).")
_ap = argparse.ArgumentParser(); _ap.add_argument("--base", default="", help="alt dizin ön eki, ör. /kimtrim (GitHub Pages)"); _ap.add_argument("--out", default=os.path.join(BASE, "dist"))
_args = _ap.parse_args()
DIST = os.path.abspath(_args.out)
BASEPATH = _args.base.rstrip("/")
def rebase(txt):
    """Kök-mutlak href/src bağlantılarını alt dizine taşır (yalnız --base verildiğinde)."""
    if not BASEPATH: return txt
    return re.sub(r'(href|src)="/(?!/)', rf'\1="{BASEPATH}/', txt)
_SRC_DIST = os.path.join(BASE, "dist")
for _src, _dst in ((os.path.join(BASE, "demo-site", "brand"), os.path.join(DIST, "img", "brand")), (os.path.join(BASE, "demo-site", "video"), os.path.join(DIST, "video")), (os.path.join(BASE, "demo-site", "img", "menu"), os.path.join(DIST, "img", "menu")), (os.path.join(BASE, "demo-site", "img", "subeler"), os.path.join(DIST, "img", "subeler"))):
    if os.path.isdir(_src): shutil.copytree(_src, _dst, dirs_exist_ok=True)
if DIST != os.path.abspath(_SRC_DIST):
    for d in ("img", "app", "platform", "sunum"):
        src = os.path.join(_SRC_DIST, d)
        if os.path.isdir(src): shutil.copytree(src, os.path.join(DIST, d), dirs_exist_ok=True)
SITE = "https://floridacoffee.com.tr"        # kanonik (demo noindex)
TODAY = date.today().isoformat()

demo = open(DEMO, encoding="utf-8").read()
def between(a, b, src=demo):
    i = src.index(a); j = src.index(b, i); return src[i:j]

# ---------- tek kaynaktan çekilen parçalar ----------
DATA_JS  = between('const reduce =', '/* ---------------- live card + clock')
MENU_JS  = between('const MENU = {', '\nlet curCat')
DIET_JS  = between('const kcalOf', 'function passDiet')
FLO_JS   = between('/* ================= FLO', '/* bölüm bazlı ipucu')
HINT_JS  = between('/* bölüm bazlı ipucu', 'setTimeout(() => showHint("safak"), 1800);')
LOGO_JS  = between('/* ---------- logo canlandırma ---------- */', '/* ---------- /logo canlandırma ---------- */')
FLO_CSS  = between('/* ---------- Flo asistanı ---------- */', '/* ---------- loyalty / phone ---------- */')
FLO_HTML = between('<!-- ============ FLO · asistan ============ -->', '<div class="drawer" id="drawer"')
ROOT_CSS = between(':root{', '*{box-sizing:border-box}')
BTN_CSS  = between('.btn{position:relative', '.scrollcue{')
SQ_CSS   = between('/* ---------- dik köşe sistemi', '/* ---------- kalıcı üst navigasyon')
NAV_CSS  = between('/* ---------- kalıcı üst navigasyon ---------- */', '/* ---------- hour rail')
CHIP_CSS = between('.chip{display:inline-flex', '/* ---------- order mini')
FILT_CSS = between('.filters{display:flex', '/* detail drawer')
NEWS_CSS = between('/* ---------- taze ---------- */', '/* ---------- branch finder')
LOGO_SVG = re.search(r'<svg class="mark[^"]*" viewBox="0 0 100 100" aria-hidden="true">.*?</svg>', demo).group(0)
# nav/footer logosu: gerçek kelime işareti (o delik) + animasyonlu SVG; img kaynağı dist yoluna çevrilir
LOGO_HTML = re.sub(r'src="[^"]*"', 'src="/img/brand/wordmark-reverse-noo.png"', re.search(r'<span class="logo">.*?</svg></span>', demo, re.S).group(0))
LOGO_FOOT = LOGO_HTML.replace('class="logo"', 'class="logo foot"').replace(' anim', '')

# JS içindeki şube verisini Python'a da al (sayfa üretimi için)
B_RAW = re.search(r'const B = \[(.*?)\n\];', demo, re.S).group(1)
def parse_branches():
    out = []
    for m in re.finditer(r'\{id:"([^"]+)", n:"([^"]+)", c:"([^"]+)", lat:([\d.]+), lng:([\d.]+), o:([\d.]+), k:([\d.]+), f:\[([^\]]*)\], r:"([^"]+)", rev:(\d+), note:"([^"]*)"\}', B_RAW):
        out.append(dict(id=m[1], n=m[2], c=m[3], lat=float(m[4]), lng=float(m[5]), o=float(m[6]), k=float(m[7]),
                        f=[x.strip().strip('"') for x in m[8].split(",") if x.strip()], r=m[9], rev=int(m[10]), note=m[11]))
    return out
BRANCHES = parse_branches(); assert len(BRANCHES) >= 15, len(BRANCHES)
FEAT = {"manzara":"Manzara","gece":"Gece açık","calisma":"Çalışma alanı","otopark":"Otopark","kahvalti":"Kahvaltı","evcil":"Evcil dostu"}
def hh(h): return f"{int(h)%24:02d}:{int(round((h%1)*60)):02d}"

# menü verisini Python'a al
MENU = {}
for cat, body in re.findall(r'(\w+): \[\n(.*?)\n  \]', MENU_JS, re.S):
    items = []
    for row in re.findall(r'\["([^"]+)","([^"]*)","(\d+)",\[([^\]]*)\]\]', body):
        items.append(dict(n=row[0], d=row[1], p=int(row[2]), tags=[t.strip().strip('"') for t in row[3].split(",") if t.strip()]))
    MENU[cat] = items
CATN = {"sicak":"Sıcak kahveler","soguk":"Soğuk kahveler","diger":"Kahve dışı","yiyecek":"Yiyecek"}
slug = lambda s: re.sub(r'[^a-z0-9]+','-', s.lower().translate(str.maketrans("çğıöşüâî","cgiosuai"))).strip("-")

# ---------- içerik ----------
NEWS = [
 dict(t="sube", d="Eylül 2026", h="Sakarya'da yeni adres: Cumhuriyet Mah. Şal Sokak", p="Çark Caddesi'ne yürüme mesafesinde, daha geniş çalışma katı ve teras. Açılış haftası filtre kahve 1 ₺.", body="Sakarya'daki ikinci noktamız Cumhuriyet Mahallesi Şal Sokak 20A'da. Üniversiteye yakın konumu, iki katlı çalışma alanı ve terasıyla şehrin sınav dönemi adresi olmayı hedefliyor. Açılış haftasında filtre kahve 1 ₺; uygulamadan ön sipariş ilk günden açık.", img="sakarya"),
 dict(t="urun", d="Eylül 2026", h="Boğaz Cold Brew sezonu açıldı", p="16 saat demleme, tonik ve portakal kabuğu. Kavacık ve Beykoz'da; diğer şubelerde Ekim'de.", body="Boğaz Cold Brew, 16 saat oda sıcaklığında demlenen cold brew'un tonik ve portakal kabuğuyla servisi. Asiditesi düşük, tatlılığı yüksek. Önce manzaralı şubelerde: Kavacık ve Beykoz. Ekim'den itibaren tüm şubelerde.", img="coldbrew"),
 dict(t="kampanya", d="Sürekli", h="Kartını uygulamaya taşı, ilk kahve bizden", p="Fiziksel sadakat kartındaki damgalar ve bakiye tek taramayla uygulamaya geçer.", body="Uygulamada Kart → Kartımı tara adımıyla kartınızdaki kodu okutun; damgalar ve bakiye anında hesabınıza geçer. Aktarımı tamamlayan herkese ilk sipariş küçük boy kahve hediye.", img="cup"),
 dict(t="etkinlik", d="Her Perşembe 21:00", h="Akustik akşamlar · Kavacık terası", p="Gün batımından sonra iki kişilik akustik set. Yer ayırma uygulamadan, Plus üyelere öncelik.", body="Her Perşembe gün batımından sonra Kavacık terasında iki kişilik akustik set. Masa ayırma uygulamadan; FloridaDays Plus ve Premium üyelere öncelik.", img="night"),
 dict(t="sube", d="Yaz 2026", h="Budva yaz saatleri: 01:00'e kadar", p="Adriyatik'teki şubemiz yaz boyunca gece bire kadar açık. Menü EN/ME.", body="Budva şubemiz yaz sezonunda gece 01:00'e kadar açık. Menü İngilizce ve Karadağca; fiyatlar EUR.", img="sunset"),
 dict(t="urun", d="Ekim 2026", h="Sonbahar Harmanı raflarda", p="Etiyopya Yirgacheffe %60, Brezilya Cerrado %40. 250 g, kavurma tarihi pakette.", body="Sezon harmanımız: Etiyopya Yirgacheffe %60, Brezilya Cerrado %40, orta kavurma. 250 g çekirdek veya öğütülmüş; kavurma tarihi her pakette. Şubeden alın ya da uygulamadan ön sipariş verin.", img="beans"),
 dict(t="kampanya", d="Hafta içi 14–16", h="Ölü saat: soğuk kahveler %20", p="Uygulamada, yoğunluğu düşük şubelerde otomatik açılır. Bildirimleri açık tutun.", body="Hafta içi 14:00–16:00 arasında yoğunluğu düşük şubelerde tüm soğuk kahveler %20 indirimli. Kampanya uygulamada otomatik açılır; bildirimleri açık tutun.", img="workspace"),
 dict(t="etkinlik", d="Ayın ilk Cumartesi'si", h="Cupping · Çengelköy", p="Sezon harmanını birlikte tadıyoruz. 12 kişilik, ücretsiz.", body="Her ayın ilk Cumartesi'si Çengelköy'de sezon harmanını birlikte tadıyoruz: kavurma dereceleri, kahve kuşağı, asidite–gövde dengesi. 12 kişilik, ücretsiz; Plus üyelere öncelik.", img="barista"),
]
TL = dict(sube="Şube", urun="Ürün", kampanya="Kampanya", etkinlik="Etkinlik")
PRODUCTS = [
 dict(n="Sonbahar Harmanı · 250 g", p="420 ₺", img="beans", d="Etiyopya Yirgacheffe %60, Brezilya Cerrado %40, orta kavurma. Çekirdek veya öğütülmüş; kavurma tarihi pakette.", tags=["Çekirdek","Öğütülmüş","Kavurmadan 7 gün"], body="Bergamot, kayısı ve kakao kabuğu notaları. Espresso ve filtre için dengeli; şubede içtiğiniz harmanla aynı kavurma partisi. Kavurmadan 7 gün sonra servis edilir; en iyi tüketim 21 gün içinde."),
 dict(n="Ev Espresso Seti", p="1.150 ₺", img="pour", d="500 g harman, 14 g ölçek kaşığı, barista kartı: doz, süre, sıcaklık. Evde aynı standart.", tags=["Hediye","El kitabı standardı"], body="Şubedeki standardı eve taşıyan set: 500 g Sonbahar Harmanı, 14 g'lık ölçek kaşığı ve barista kartı (14 g doz, 90–96 °C, 18–23 sn, 30–60 g çıktı, süt 60–65 °C)."),
 dict(n="Florida Termos · 350 ml", p="650 ₺", img="cup", d="Petrol yeşili, çift cidar, tukan amblemli. Şubede kendi bardağınızla %10 indirim.", tags=["Merch","%10 indirim"], body="Çift cidarlı paslanmaz çelik, 350 ml, petrol yeşili, amber tukan amblemi. Kendi bardağınızla gelen herkese her şubede %10 indirim."),
 dict(n="Hediye Kartı", p="250–2.000 ₺", img=None, d="Uygulamadan telefona gönderin; alan kişi bakiyeyi cüzdanına aktarır.", tags=["Dijital","Anında"], body="Dijital hediye kartı: uygulamadan telefon numarasına gönderin, alan kişi bakiyeyi FloridaDays cüzdanına aktarsın. Kartona gerek yok; 250 ₺'den 2.000 ₺'ye."),
]
FAQ = [
 ("Ön sipariş nasıl çalışır?", "Uygulamada şube ve içeceğinizi seçin, ödeyin. Hazırlık siz \"Geldim\" dediğinizde ya da şubeye 200 m yaklaştığınızda başlar; kahveniz soğumaz."),
 ("Laktozsuz ve bitkisel süt var mı?", "Evet. Laktozsuz +10 ₺, yulaf ve badem +15 ₺. Tercihinizi uygulama profilinize kaydedebilirsiniz; barista ekranında etiketli görünür."),
 ("FloridaDays Club nedir?", "Sadakat programımız. 1 ₺ = 1 çekirdek, 10 içecekte biri bizden. Seviyeler son 6 ay harcamasıyla: Classic, Plus (2.500 ₺+), Premium (7.500 ₺+)."),
 ("Fiziksel kartımı uygulamaya nasıl aktarırım?", "Uygulamada Kart → Kartımı tara. Karttaki kodu okutun; damgalar ve bakiye anında hesabınıza geçer."),
 ("Her şubede kahve aynı mı?", "Evet. Doz 14 g tartıyla, su 90–96 °C, 9 bar, shot 18–23 sn, süt 60–65 °C. Reçeteler kişisel yoruma açık değildir; barista operasyon el kitabı standarttır."),
 ("Hangi şubeler gece geç saate kadar açık?", "Kavacık, Beykoz ve Taksim Meydan 02:00'ye; Kadıköy ve Talimhane 01:00'e kadar. Güncel saatler şube sayfalarında."),
 ("Franchise şartları neler?", "3 km bölge koruması, 10 yıl sözleşme, 45 gün eğitim, merkezi tedarik. Royalty ciro %5 + KDV, ulusal reklam en fazla %1. Başvuru franchise sayfasından ya da Flo üzerinden."),
 ("Evcil hayvanla gelebilir miyim?", "Kavacık ve Beykoz teraslarında evet. Diğer şubeler için şube sayfasındaki özelliklere bakın."),
 ("Kurumsal sipariş veriyor musunuz?", "Evet. Toplantı ikramı, etkinlik barı ve hediye kartı için kurumsal sayfamızdan talep bırakın; 1 iş günü içinde dönüş."),
 ("Kargo var mı?", "Ürünler şu an uygulamadan ön sipariş, şubeden teslim. Kargo yakında."),
]
JOBS = [
 dict(t="Barista", loc="İstanbul · Kavacık, Kadıköy, Çengelköy", type="Tam zamanlı", d="15 gün barista eğitimi sonrasında şubede espresso standardını uygulayan, süt köpürtme ve latte art bilen, hijyen disiplinine sahip ekip arkadaşı. Deneyim şart değil; öğrenme isteği şart."),
 dict(t="Şube Müdürü", loc="Sakarya · Çark Caddesi / Şal Sokak", type="Tam zamanlı", d="30 gün işletme eğitimi sonrasında şube operasyonu, ekip planlaması, FIFO ve tedarik yönetimi, HQ raporlaması. En az 2 yıl kafe/restoran yöneticiliği."),
 dict(t="Kalite ve Eğitim Uzmanı", loc="İstanbul · Merkez (Çengelköy)", type="Tam zamanlı", d="Barista el kitabının şubelerde uygulanmasını denetleyen, gizli müşteri raporlarını değerlendiren, yeni şube açılışlarında eğitim veren uzman. SCA sertifikası tercih sebebi."),
]

# ---------- şablon ----------
NAV = [("Menü","/menu/"),("Şubeler","/subeler/"),("Kahvemiz","/kahvemiz/"),("Taze","/taze/"),("Ürünler","/urunler/"),("Kulüp","/kulup/"),("Franchise","/franchise/")]
EXTRA_CSS = r'''
/* ---------- menü: ürün ızgarası ---------- */
.mbar{position:sticky;top:3.3rem;z-index:30;background:rgba(237,230,216,.92);backdrop-filter:blur(10px);border-bottom:1px solid var(--paper-line);padding:.7rem 0}
.mbar .wrap{display:flex;flex-direction:column;gap:.55rem;align-items:center}
.mbar .row{display:flex;gap:.4rem;flex-wrap:wrap;justify-content:center}
.mbar .search{width:min(100%,22rem);border:1px solid var(--paper-line);background:#fff;padding:.5rem .8rem;font:inherit;color:var(--paper-ink)}
.mcat.sm{padding:.35rem .75rem;font-size:.78rem}
.msec{padding:clamp(2rem,5vh,3.5rem) 0 0}
.msec .mhead{text-align:center;margin-bottom:1.4rem}
.msec .mhead h2{font-size:clamp(1.5rem,3vw,2.2rem)}
.msec .mhead p{margin:.3rem auto 0;color:var(--paper-ink-2);font-size:.9rem;max-width:52ch}
.msec[hidden]{display:none}
.pgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,13.5rem),1fr));gap:1px;background:var(--paper-line);border:1px solid var(--paper-line)}
.pcard{background:#FBF8F2;display:flex;flex-direction:column;text-decoration:none;color:inherit;transition:background .2s}
.pcard:hover{background:#fff}
.pcard[hidden]{display:none}
.pcard .pimg{aspect-ratio:1/1;overflow:hidden;background:var(--paper-line);position:relative}
.pcard .pimg img{width:100%;height:100%;object-fit:cover;display:block;transition:transform .5s ease}
.pcard:hover .pimg img{transform:scale(1.04)}
.pcard .pimg .pph{position:absolute;inset:0;display:grid;place-items:center;font-family:var(--disp);font-size:3rem;font-weight:800;color:var(--amber)}
.pcard .pbody{padding:.9rem 1rem 1rem;display:flex;flex-direction:column;gap:.35rem;flex:1}
.pcard .prow{display:flex;justify-content:space-between;gap:.6rem;align-items:baseline}
.pcard h3{font-size:1.02rem;letter-spacing:-.01em}
.pcard .pp{font-family:var(--disp);font-weight:700;white-space:nowrap;font-variant-numeric:tabular-nums}
.pcard .pd{font-size:.82rem;color:var(--paper-ink-2);margin:0}
.pcard .ptags{display:flex;gap:.3rem;flex-wrap:wrap;margin-top:auto;padding-top:.4rem}
.mnote{text-align:center;color:var(--paper-ink-2);font-size:.82rem;margin:1.2rem auto 0;max-width:60ch}
.mempty{text-align:center;padding:2.5rem 1rem;color:var(--paper-ink-2)}
.mempty[hidden]{display:none}
@media (max-width:640px){.pgrid{grid-template-columns:1fr 1fr}.pcard .pbody{padding:.6rem .7rem .8rem;gap:.25rem}.pcard h3{font-size:.9rem}.pcard .pd{font-size:.74rem}.pcard .pp{font-size:.9rem}.pcard .ptags .tg{font-size:.6rem}}
/* ---------- ürün detay ---------- */
.pdp{padding:clamp(1.2rem,3vh,2rem) 0 clamp(3rem,7vh,5rem)}
.pdp .crumbs{justify-content:center;margin-bottom:1.4rem}
.pdp-grid{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:clamp(1.5rem,4vw,3.5rem);align-items:start}
@media (max-width:860px){.pdp-grid{grid-template-columns:1fr}}
.pdp-media{position:sticky;top:4.2rem}
.pdp-media .big{aspect-ratio:1/1;overflow:hidden;background:var(--paper-line);border:1px solid var(--paper-line)}
.pdp-media .big img{width:100%;height:100%;object-fit:cover;display:block}
.pdp-media .mini{display:grid;grid-template-columns:repeat(3,1fr);gap:1px;background:var(--paper-line);border:1px solid var(--paper-line);border-top:0}
.pdp-media .mini div{background:#FBF8F2;padding:.7rem .5rem;text-align:center}
.pdp-media .mini b{display:block;font-family:var(--disp);font-size:1.05rem}
.pdp-media .mini span{font-size:.68rem;letter-spacing:.12em;text-transform:uppercase;color:var(--paper-ink-2)}
.pdp-info .eyebrow{color:var(--rust)}
.pdp-info h1{font-size:clamp(2rem,4.5vw,3.4rem)}
.pdp-info .lede{margin-top:.6rem}
.pdp .price{display:flex;align-items:baseline;gap:.7rem;margin:1.2rem 0 .3rem}
.pdp .price b{font-family:var(--disp);font-size:2.2rem;font-weight:800;letter-spacing:-.03em;font-variant-numeric:tabular-nums;white-space:nowrap}
.pdp .price span{color:var(--paper-ink-2);font-size:.85rem}
.opt{margin-top:1rem}
.opt .lbl{margin-bottom:.45rem}
.opt .pills{display:flex;gap:.4rem;flex-wrap:wrap}
.opt .pill{border:1px solid var(--paper-line);background:#fff;padding:.45rem .8rem;font-size:.85rem;font-weight:600;color:var(--paper-ink-2);cursor:pointer;font-family:var(--ui)}
.opt .pill[aria-pressed="true"]{background:var(--paper-ink);color:var(--paper);border-color:var(--paper-ink)}
.opt .pill small{font-weight:500;opacity:.8}
.pdp .cta{display:flex;gap:.5rem;flex-wrap:wrap;margin-top:1.4rem}
.facts{display:grid;grid-template-columns:repeat(2,1fr);gap:1px;background:var(--paper-line);border:1px solid var(--paper-line);margin-top:1.6rem}
.facts div{background:#FBF8F2;padding:.85rem 1rem}
.facts .l{font-size:.66rem;letter-spacing:.14em;text-transform:uppercase;color:var(--paper-ink-2);font-weight:700;font-family:var(--disp)}
.facts .v{margin-top:.2rem;font-weight:600}
.howto{margin-top:1.6rem;border-left:3px solid var(--amber);padding:.2rem 0 .2rem 1rem;color:var(--paper-ink-2);font-size:.92rem}
.howto b{color:var(--paper-ink)}
.pair{padding:0 0 clamp(3rem,7vh,5rem)}
.pair h2{text-align:center;font-size:clamp(1.4rem,2.6vw,2rem);margin-bottom:1.2rem}
.pair .sub{text-align:center;color:var(--paper-ink-2);margin:-.8rem auto 1.4rem;font-size:.9rem}
.toastv7{position:fixed;left:50%;bottom:4.6rem;transform:translate(-50%,12px);background:var(--ink);color:#0A1420;padding:.65rem 1rem;font-weight:600;font-size:.88rem;z-index:90;opacity:0;pointer-events:none;transition:opacity .25s,transform .25s;max-width:min(92vw,28rem);text-align:center}
.toastv7.on{opacity:1;transform:translate(-50%,0)}
/* ---------- şube kartı fotoğrafı ---------- */
.cell .bimg{margin:-1.1rem -1.2rem .5rem;aspect-ratio:16/9;overflow:hidden;background:var(--hair)}
.cell .bimg img{width:100%;height:100%;object-fit:cover;display:block;transition:transform .5s}
.cell:hover .bimg img{transform:scale(1.04)}
.bphoto{aspect-ratio:16/9;overflow:hidden;border:1px solid var(--hair);margin-bottom:1.2rem}
.bphoto img{width:100%;height:100%;object-fit:cover;display:block}
'''
EXTRA_JS = r'''
/* menü: filtre + arama (statik kartlar) */
(() => {
  const cards = [...document.querySelectorAll(".pcard")]; if (!cards.length) return;
  let diet = "", q = "";
  const nrm = t => (t || "").toLowerCase().replace(/i̇/g, "i").replace(/[^a-zçğıöşü0-9 ]/g, " ").replace(/\s+/g, " ").trim();
  const pass = c => { const t = c.dataset.tags, k = +c.dataset.kcal || 0, mg = +c.dataset.mg || 0;
    if (diet === "hafif" && !(k < 100 && c.dataset.kcal)) return false;
    if (diet === "vegan" && !t.includes("vegan")) return false;
    if (diet === "sutsuz" && !t.includes("sütsüz")) return false;
    if (diet === "azkafein" && !(mg < 100)) return false;
    if (diet === "glutensiz" && !t.includes("glütensiz")) return false;
    if (q && !nrm(c.dataset.name + " " + c.dataset.desc).includes(nrm(q))) return false;
    return true; };
  const apply = () => { let total = 0;
    document.querySelectorAll(".msec").forEach(sec => { let n = 0; sec.querySelectorAll(".pcard").forEach(c => { const ok = pass(c); c.hidden = !ok; if (ok) n++; }); sec.hidden = !n; const cnt = sec.querySelector(".cnt"); if (cnt) cnt.textContent = n + " ürün"; total += n; });
    const e = document.getElementById("mempty"); if (e) e.hidden = total > 0; };
  document.querySelectorAll("#dietF .mcat").forEach(b => b.addEventListener("click", () => { document.querySelectorAll("#dietF .mcat").forEach(x => x.setAttribute("aria-pressed", "false")); b.setAttribute("aria-pressed", "true"); diet = b.dataset.d; apply(); }));
  const si = document.getElementById("msearch"); if (si) si.addEventListener("input", () => { q = si.value.trim(); apply(); });
  document.querySelectorAll("#mcats a").forEach(a => a.addEventListener("click", () => { document.querySelectorAll("#mcats a").forEach(x => x.setAttribute("aria-pressed", "false")); a.setAttribute("aria-pressed", "true"); }));
})();
/* ürün detay: boy ve süt seçimi fiyatı günceller */
(() => {
  const pr = document.getElementById("pdpPrice"); if (!pr) return;
  const base = +pr.dataset.base; let size = 0, milk = 0;
  const upd = () => { pr.textContent = (base + size + milk) + " ₺"; };
  document.querySelectorAll("[data-size]").forEach(b => b.addEventListener("click", () => { document.querySelectorAll("[data-size]").forEach(x => x.setAttribute("aria-pressed", "false")); b.setAttribute("aria-pressed", "true"); size = +b.dataset.size; upd(); }));
  document.querySelectorAll("[data-milk]").forEach(b => b.addEventListener("click", () => { document.querySelectorAll("[data-milk]").forEach(x => x.setAttribute("aria-pressed", "false")); b.setAttribute("aria-pressed", "true"); milk = +b.dataset.milk; upd(); }));
})();
'''
EXTRA_CSS2 = r'''
/* ---------- v8 ortak: alt sayfa bileşenleri ---------- */
.split{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:clamp(1.5rem,4vw,3.5rem);align-items:center}
.split.top{align-items:start}
@media (max-width:900px){.split{grid-template-columns:minmax(0,1fr)}}
.pht{margin:0;position:relative;overflow:hidden;border:1px solid var(--hair);background:var(--hair)}
.pht.r169{aspect-ratio:16/9}.pht.r43{aspect-ratio:4/3}.pht.r11{aspect-ratio:1/1}
.pht img{width:100%;height:100%;object-fit:cover;display:block;transition:transform .6s}
.pht:hover img{transform:scale(1.03)}
.pht figcaption{position:absolute;left:.9rem;bottom:.8rem;font-size:.68rem;letter-spacing:.14em;text-transform:uppercase;color:#fff;text-shadow:0 1px 8px rgba(0,0,0,.6);font-family:var(--disp);font-weight:700}
.sh{text-align:center;max-width:60ch;margin:0 auto clamp(1.4rem,3vh,2.2rem)}
.sh h2{font-size:clamp(1.6rem,3.2vw,2.5rem)}
.sh p{margin:.5rem auto 0;color:var(--ink-2)}
.paper .sh p{color:var(--paper-ink-2)}
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,9rem),1fr));gap:1px;background:var(--hair);border:1px solid var(--hair);margin:1.6rem 0}
.stats div{background:rgba(9,14,19,.55);padding:1rem 1.1rem;text-align:center}
.stats b{display:block;font-family:var(--disp);font-size:2rem;line-height:1;font-variant-numeric:tabular-nums;background:linear-gradient(90deg,var(--ink),var(--amber));-webkit-background-clip:text;background-clip:text;color:transparent}
.stats span{display:block;font-size:.72rem;color:var(--ink-3);margin-top:.35rem;letter-spacing:.06em;text-transform:uppercase}
.stdgrid{display:grid;grid-template-columns:repeat(3,1fr);gap:1px;background:var(--hair);border:1px solid var(--hair)}
@media (max-width:560px){.stdgrid{grid-template-columns:repeat(2,1fr)}}
.std{background:rgba(9,14,19,.55);padding:.95rem 1rem;text-align:left;cursor:pointer;display:flex;flex-direction:column;gap:.15rem;color:inherit;transition:background .2s;font:inherit}
.std:hover{background:rgba(10,77,92,.35)}
.std .v{font-family:var(--disp);font-size:1.35rem;line-height:1;font-variant-numeric:tabular-nums;font-weight:700}
.std .l{font-size:.66rem;letter-spacing:.12em;text-transform:uppercase;color:var(--ink-3)}
.std .why{font-size:.78rem;color:var(--ink-2);margin-top:.4rem;display:none;line-height:1.45}
.std[aria-expanded="true"]{background:rgba(10,77,92,.5)}
.std[aria-expanded="true"] .why{display:block}
.paper .std{background:#FBF8F2}.paper .std .why{color:var(--paper-ink-2)}.paper .std[aria-expanded="true"]{background:#fff}
.shot{display:grid;grid-template-columns:7rem 1fr;gap:1.2rem;align-items:center;border:1px solid var(--hair);padding:1.2rem;background:var(--glass)}
@media (max-width:560px){.shot{grid-template-columns:1fr;text-align:center;justify-items:center}}
.shot svg{width:7rem;height:7rem;display:block}
.shot .big{font-family:var(--disp);font-size:1.6rem;font-variant-numeric:tabular-nums;line-height:1;margin:.3rem 0}
.check{list-style:none;margin:0;padding:0;display:grid;gap:.5rem}
.check label{display:flex;gap:.6rem;align-items:flex-start;cursor:pointer;font-size:.92rem;color:var(--ink-2)}
.check input{margin:.3rem 0 0;accent-color:var(--amber);flex:none}
.check b{color:var(--ink)}
.check li.ok span{color:var(--ink-3)}.check li.ok b{color:var(--ok)}
.tabs{display:flex;gap:.4rem;flex-wrap:wrap;margin-bottom:1rem}
[data-pane][hidden]{display:none}
.bars{display:grid;gap:.6rem;margin:1rem 0}
.bars div{display:grid;grid-template-columns:7rem 1fr 2.5rem;gap:.7rem;align-items:center;font-size:.85rem;color:var(--ink-2)}
.bars i{height:.5rem;background:var(--hair);position:relative;display:block}
.bars i::after{content:"";position:absolute;left:0;top:0;bottom:0;width:var(--w,0%);background:linear-gradient(90deg,var(--amber),var(--rust));transition:width .8s cubic-bezier(.3,.7,.2,1)}
.bars b{font-family:var(--disp);text-align:right;font-variant-numeric:tabular-nums}
.quiz{border:1px solid var(--hair);background:var(--glass);padding:1.4rem;display:grid;gap:1rem}
.quiz .q{font-family:var(--disp);font-size:1.15rem;font-weight:700}
.quiz .opts{display:flex;gap:.4rem;flex-wrap:wrap}
.quiz .opt{padding:.5rem .9rem;border:1px solid var(--hair-2);font:inherit;font-size:.88rem;color:var(--ink-2);cursor:pointer;background:transparent}
.quiz .opt[aria-pressed="true"]{background:var(--ink);color:#0A1420;border-color:var(--ink);font-weight:600}
.quiz .res{display:grid;grid-template-columns:7rem 1fr;gap:1rem;align-items:center;border-top:1px solid var(--hair);padding-top:1rem}
.quiz .res img{width:7rem;height:7rem;object-fit:cover;display:block}
.quiz .res b{font-family:var(--disp);font-size:1.3rem;display:block}
.qprog{display:flex;gap:.3rem}.qprog i{flex:1;height:3px;background:var(--hair)}.qprog i.on{background:var(--amber)}
.timeline{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,11rem),1fr));gap:1px;background:var(--hair);border:1px solid var(--hair);counter-reset:tl}
.timeline div{background:rgba(9,14,19,.55);padding:1rem 1.1rem;counter-increment:tl;position:relative;cursor:default}
.timeline div::before{content:counter(tl,decimal-leading-zero);font-family:var(--disp);font-size:.7rem;letter-spacing:.2em;color:var(--amber);font-weight:700;display:block;margin-bottom:.4rem}
.timeline h3{font-size:1rem;margin-bottom:.3rem}
.timeline p{margin:0;font-size:.85rem;color:var(--ink-2)}
.timeline div.on{background:rgba(10,77,92,.5)}
.timeline .pht{margin:-1rem -1.1rem .7rem;border:0;aspect-ratio:16/8}
.paper .timeline div{background:#FBF8F2}.paper .timeline p{color:var(--paper-ink-2)}
.tcard{background:rgba(6,24,31,.72);display:flex;flex-direction:column;text-decoration:none;color:inherit;transition:background .2s}
.tcard:hover{background:rgba(10,77,92,.55)}
.tcard[hidden]{display:none}
.tcard .pht{border:0;margin:0}
.tcard .tb{padding:1rem 1.1rem 1.1rem;display:flex;flex-direction:column;gap:.45rem;flex:1}
.tcard .meta{display:flex;justify-content:space-between;gap:.6rem;font-size:.68rem;letter-spacing:.14em;text-transform:uppercase;color:var(--ink-3);font-family:var(--disp);font-weight:700}
.tcard .meta b{color:var(--amber)}
.tcard h3{font-size:1.05rem}
.tcard p{margin:0;font-size:.86rem;color:var(--ink-2)}
.tcard .nact{display:flex;justify-content:space-between;align-items:center;margin-top:auto;padding-top:.5rem}
.nico{border:1px solid var(--hair-2);width:2rem;height:2rem;color:var(--ink-2);font-size:1rem;margin-left:.3rem;background:transparent;cursor:pointer}
.nico[aria-pressed="true"]{color:var(--rust);border-color:var(--rust)}
.sbar{display:flex;gap:.5rem;flex-wrap:wrap;align-items:center;margin:0 0 1.4rem}
.sbar input{flex:1;min-width:12rem;background:rgba(9,14,19,.6);border:1px solid var(--hair-2);color:var(--ink);padding:.6rem .8rem;font:inherit}
.paper .sbar input{background:#fff;border-color:var(--paper-line);color:var(--paper-ink)}
.calc{border:1px solid var(--hair);background:var(--glass);padding:1.3rem;display:grid;gap:1rem}
.calc label{display:grid;gap:.35rem;font-size:.8rem;letter-spacing:.1em;text-transform:uppercase;color:var(--ink-3);font-weight:700;font-family:var(--disp)}
.calc label b{color:var(--amber);font-size:.95rem;letter-spacing:0;text-transform:none;font-family:var(--ui)}
.calc input[type=range]{width:100%;accent-color:var(--amber)}
.calc select,.calc input{width:100%;max-width:100%;min-width:0;box-sizing:border-box}
.calc .out{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,8rem),1fr));gap:1px;background:var(--hair);border:1px solid var(--hair)}
.calc .out div{background:rgba(9,14,19,.55);padding:.85rem .9rem}
.calc .out b{display:block;font-family:var(--disp);font-size:1.3rem;font-variant-numeric:tabular-nums}
.calc .out span{font-size:.66rem;letter-spacing:.12em;text-transform:uppercase;color:var(--ink-3)}
.tiers{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,14rem),1fr));gap:1px;background:var(--hair);border:1px solid var(--hair)}
.tier{background:rgba(9,14,19,.55);padding:1.2rem;display:flex;flex-direction:column;gap:.5rem;transition:background .3s}
.tier.on{background:rgba(10,77,92,.55);box-shadow:inset 0 3px 0 var(--amber)}
.tier .tn{font-family:var(--disp);font-size:1.4rem;font-weight:700}
.tier .tr{font-size:.72rem;letter-spacing:.12em;text-transform:uppercase;color:var(--ink-3)}
.tier ul{margin:.3rem 0 0;padding-left:1.1rem;color:var(--ink-2);font-size:.88rem;display:grid;gap:.25rem}
.stamps{display:grid;grid-template-columns:repeat(5,1fr);gap:.5rem;max-width:22rem}
.stamps button{aspect-ratio:1;border:1px dashed var(--hair-2);background:transparent;color:var(--ink-3);cursor:pointer;display:grid;place-items:center;font-family:var(--disp);font-weight:700;transition:all .2s}
.stamps button.on{background:var(--amber);border-style:solid;border-color:var(--amber);color:#2A1703}
.stamps button:last-child.on{background:var(--ok);border-color:var(--ok)}
.stepper{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,12rem),1fr));gap:1px;background:var(--hair);border:1px solid var(--hair)}
.stepper div{background:rgba(9,14,19,.55);padding:1.1rem;transition:background .3s}
.stepper div.on{background:rgba(10,77,92,.55)}
.stepper .n{font-family:var(--disp);font-size:2rem;font-weight:800;color:var(--amber);line-height:1}
.stepper h3{font-size:1rem;margin:.4rem 0 .2rem}
.stepper p{margin:0;font-size:.85rem;color:var(--ink-2)}
.pcard .pimg .pph{position:absolute;inset:0;display:grid;place-items:center;font-family:var(--disp);font-size:3rem;font-weight:800;color:var(--amber)}
.regions{display:flex;gap:.4rem;flex-wrap:wrap}
.regions .chip.open{border-color:var(--ok);color:var(--ok)}
.regions .chip.full{opacity:.5;text-decoration:line-through}
.contact{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,13rem),1fr));gap:1px;background:var(--hair);border:1px solid var(--hair)}
.contact a,.contact div{background:rgba(9,14,19,.55);padding:1.1rem;text-decoration:none;color:inherit;display:flex;flex-direction:column;gap:.25rem}
.contact a:hover{background:rgba(10,77,92,.5)}
.contact .l{font-size:.66rem;letter-spacing:.14em;text-transform:uppercase;color:var(--ink-3);font-family:var(--disp);font-weight:700}
.contact b{font-family:var(--disp);font-size:1.05rem}
.contact span{font-size:.85rem;color:var(--ink-2)}
.toc{position:sticky;top:4.2rem;border:1px solid var(--paper-line);background:#FBF8F2;padding:1rem 1.1rem;font-size:.85rem}
.toc a{display:block;padding:.25rem 0;color:var(--paper-ink-2);text-decoration:none}.toc a:hover{color:var(--paper-ink)}
.fsteps{display:flex;gap:.4rem;margin-bottom:1rem}.fsteps i{flex:1;height:4px;background:var(--hair)}.fsteps i.on{background:var(--amber)}
[data-step][hidden]{display:none}
.milk{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,11rem),1fr));gap:1px;background:var(--hair);border:1px solid var(--hair)}
.milk div{background:rgba(9,14,19,.55);padding:1rem 1.1rem}
.milk h3{font-size:1rem;display:flex;justify-content:space-between}
.milk h3 small{color:var(--amber);font-family:var(--disp)}
.milk p{margin:.3rem 0 0;font-size:.84rem;color:var(--ink-2)}
.ratingrow{display:flex;gap:.2rem;font-size:.75rem;color:var(--ink-3)}
.ratingrow b{color:var(--amber)}
.evday{display:grid;grid-template-columns:repeat(7,1fr);gap:1px;background:var(--hair);border:1px solid var(--hair);margin-bottom:1.4rem}
.evday button{background:rgba(9,14,19,.55);padding:.7rem .3rem;text-align:center;color:var(--ink-2);font:inherit;font-size:.8rem;cursor:pointer;border:0}
.evday button b{display:block;font-family:var(--disp);font-size:1.1rem;color:var(--ink)}
.evday button.on{background:rgba(10,77,92,.55);box-shadow:inset 0 -3px 0 var(--amber)}
.evday button.has b{color:var(--amber)}
.quote{font-family:var(--disp);font-size:clamp(1.3rem,2.6vw,1.9rem);font-weight:700;line-height:1.25;border-left:.25rem solid var(--amber);padding-left:1rem;max-width:30ch;margin:1.4rem 0}
'''
EXTRA_JS2 = r'''
/* ---------- v8: alt sayfa etkileşimleri (öğe yoksa sessizce atlanır) ---------- */
(() => {
  const T = m => (typeof showToast === "function") && showToast(m);
  // açılır standart kartları
  document.querySelectorAll(".std[aria-expanded]").forEach(b => b.addEventListener("click", () => b.setAttribute("aria-expanded", b.getAttribute("aria-expanded") !== "true")));
  // genel sekmeler
  document.querySelectorAll("[data-tabs]").forEach(box => { const btns = [...box.querySelectorAll("[data-tab]")]; const panes = [...document.querySelectorAll(`[data-pane^="${box.dataset.tabs}:"]`)];
    const show = k => { btns.forEach(b => b.setAttribute("aria-pressed", String(b.dataset.tab === k))); panes.forEach(p => p.hidden = p.dataset.pane !== box.dataset.tabs + ":" + k); box.querySelectorAll(".bars i").forEach(i => { i.style.setProperty("--w", i.dataset.w); }); };
    btns.forEach(b => b.addEventListener("click", () => show(b.dataset.tab))); if (btns[0]) show(btns[0].dataset.tab); });
  document.querySelectorAll(".bars i[data-w]").forEach(i => requestAnimationFrame(() => i.style.setProperty("--w", i.dataset.w)));
  // shot simülatörü
  const sb = document.getElementById("shotBtn"); if (sb) { const stop = document.getElementById("shotStop"), arc = document.getElementById("shotArc"), tt = document.getElementById("shotT"), g = document.getElementById("shotG"), msg = document.getElementById("shotMsg"); let raf = 0, t0 = 0, t = 0;
    const paint = () => { arc.setAttribute("stroke-dashoffset", String(264 - 264 * Math.min(1, t / 30))); arc.setAttribute("stroke", t < 18 ? "var(--busy)" : t <= 23 ? "var(--ok)" : "var(--rust)"); tt.textContent = t.toFixed(1); g.textContent = Math.round(t * 1.6) + " g"; msg.textContent = t < 8 ? "Ön ıslatma… krema oluşuyor." : t < 18 ? "Erken kesersen ekşi ve zayıf olur." : t <= 23 ? "İdeal aralık · şimdi kes." : t < 30 ? "Geç kaldın: acı ve yanık notalar." : "Shot atıldı. Yeniden dene."; };
    const loop = () => { t = Math.min(30, (Date.now() - t0) / 250); paint(); if (t < 30) raf = requestAnimationFrame(loop); else { sb.disabled = false; stop.disabled = true; sb.textContent = "Tekrar"; } };
    sb.addEventListener("click", () => { cancelAnimationFrame(raf); t0 = Date.now(); t = 0; sb.disabled = true; stop.disabled = false; loop(); });
    stop.addEventListener("click", () => { cancelAnimationFrame(raf); sb.disabled = false; stop.disabled = true; sb.textContent = "Tekrar"; const ok = t >= 18 && t <= 23; msg.textContent = ok ? `Tam zamanında: ${t.toFixed(1)} sn, ${Math.round(t*1.6)} g. Standarda uygun.` : `${t.toFixed(1)} sn: ${t < 18 ? "erken" : "geç"}. Bu shot dökülür, yeniden çekilir.`; if (ok) T("Standarda uygun shot ✓"); }); }
  // kontrol listeleri
  document.querySelectorAll(".check").forEach(ol => { const boxes = [...ol.querySelectorAll("input")], prog = document.querySelector(ol.dataset.prog || "#none"); const upd = () => { const n = boxes.filter(b => b.checked).length; boxes.forEach(b => b.closest("li").classList.toggle("ok", b.checked)); if (prog) prog.textContent = n + " / " + boxes.length; if (n === boxes.length) T(ol.dataset.done || "Tamam ✓"); }; boxes.forEach(b => b.addEventListener("change", upd)); });
  // kahve testi
  const qz = document.getElementById("quiz"); if (qz) { const Q = JSON.parse(qz.dataset.q); let step = 0; const ans = [];
    const render = () => { const q = Q[step]; qz.innerHTML = `<div class="qprog">${Q.map((_, i) => `<i class="${i <= step ? "on" : ""}"></i>`).join("")}</div><div class="q">${q.q}</div><div class="opts">${q.o.map((o, i) => `<button class="opt" data-i="${i}">${o}</button>`).join("")}</div>`;
      qz.querySelectorAll(".opt").forEach(b => b.addEventListener("click", () => { ans.push(+b.dataset.i); step++; step < Q.length ? render() : result(); })); };
    const result = () => { const key = ans.join(""); const R = JSON.parse(qz.dataset.r); const r = R[key] || R["*"]; const sl = r.s;
      qz.innerHTML = `<div class="qprog">${Q.map(() => `<i class="on"></i>`).join("")}</div><div class="q">Size göre: ${r.n}</div><div class="res"><img src="/img/menu/${sl}.jpg" alt=""><div><b>${r.n}</b><span style="color:var(--ink-2)">${r.w}</span><div style="display:flex;gap:.5rem;flex-wrap:wrap;margin-top:.7rem"><a class="btn amber sm" href="/menu/${sl}/">Ürün sayfası</a><button class="btn ghost sm" id="qAgain">Tekrar</button></div></div></div>`;
      document.getElementById("qAgain").addEventListener("click", () => { step = 0; ans.length = 0; render(); }); };
    render(); }
  // kulüp çekirdek hesabı
  const kc = document.getElementById("kcWeek"); if (kc) { const kp = document.getElementById("kcPrice"); const upd = () => { const w = +kc.value, p = +kp.value, yearly = w * 52 * p, free = Math.floor(w * 52 / 10), tier = yearly / 2 >= 7500 ? "Premium" : yearly / 2 >= 2500 ? "Plus" : "Classic";
      document.getElementById("kcW").textContent = w; document.getElementById("kcP").textContent = p; document.getElementById("kcBeans").textContent = yearly.toLocaleString("tr-TR"); document.getElementById("kcFree").textContent = free; document.getElementById("kcTier").textContent = tier; document.getElementById("kcSave").textContent = (free * p).toLocaleString("tr-TR") + " ₺";
      document.querySelectorAll(".tier").forEach(t => t.classList.toggle("on", t.dataset.tier === tier)); }; kc.addEventListener("input", upd); kp.addEventListener("input", upd); upd(); }
  // damga kartı
  const st = document.getElementById("stamps"); if (st) { let n = 0; const bs = [...st.querySelectorAll("button")]; const paint = () => bs.forEach((b, i) => b.classList.toggle("on", i < n)); bs.forEach((b, i) => b.addEventListener("click", () => { n = i + 1 === n ? i : i + 1; paint(); document.getElementById("stampMsg").textContent = n >= 10 ? "10 damga: bir sonraki içecek bizden 🎉" : `${10 - n} damga kaldı`; if (n >= 10) T("Hediye içecek kazandın"); })); paint(); }
  // abonelik / gramaj hesabı
  const sw = document.getElementById("subWeek"); if (sw) { const upd = () => { const cups = +sw.value, g = cups * 14 * 30, bags = Math.ceil(g / 250), base = bags * 420, sub = Math.round(base * 0.9); document.getElementById("subCups").textContent = cups; document.getElementById("subG").textContent = (g / 1000).toFixed(1) + " kg"; document.getElementById("subBags").textContent = bags; document.getElementById("subBase").textContent = base.toLocaleString("tr-TR") + " ₺"; document.getElementById("subSub").textContent = sub.toLocaleString("tr-TR") + " ₺"; }; sw.addEventListener("input", upd); upd(); }
  // ürün varyantları
  const pv = document.getElementById("pvPrice"); if (pv) { const base = +pv.dataset.base; let mult = 1, extra = 0; const upd = () => pv.textContent = Math.round(base * mult + extra).toLocaleString("tr-TR") + " ₺";
    document.querySelectorAll("[data-mult]").forEach(b => b.addEventListener("click", () => { document.querySelectorAll("[data-mult]").forEach(x => x.setAttribute("aria-pressed", "false")); b.setAttribute("aria-pressed", "true"); mult = +b.dataset.mult; upd(); }));
    document.querySelectorAll("[data-extra]").forEach(b => b.addEventListener("click", () => { document.querySelectorAll("[data-extra]").forEach(x => x.setAttribute("aria-pressed", "false")); b.setAttribute("aria-pressed", "true"); extra = +b.dataset.extra; upd(); })); }
  // stepper otomatik ilerler
  document.querySelectorAll(".stepper[data-auto]").forEach(sp => { const items = [...sp.children]; let i = 0; const paint = () => items.forEach((d, k) => d.classList.toggle("on", k === i)); paint(); items.forEach((d, k) => d.addEventListener("click", () => { i = k; paint(); })); if (!matchMedia("(prefers-reduced-motion:reduce)").matches) setInterval(() => { if (!sp.matches(":hover")) { i = (i + 1) % items.length; paint(); } }, 2800); });
  // etkinlik günü + yer ayır + takvim
  const ed = document.getElementById("evday"); if (ed) { const cards = [...document.querySelectorAll("[data-day]")]; ed.querySelectorAll("button").forEach(b => b.addEventListener("click", () => { const on = b.classList.contains("on"); ed.querySelectorAll("button").forEach(x => x.classList.remove("on")); if (!on) b.classList.add("on"); cards.forEach(c => c.hidden = !on && !c.dataset.day.split(",").includes(b.dataset.d)); })); }
  document.querySelectorAll("[data-reserve]").forEach(b => b.addEventListener("click", () => { b.textContent = "Yer ayrıldı ✓"; b.disabled = true; T("Yer ayrıldı · uygulamada hatırlatma kuruldu"); }));
  document.querySelectorAll("[data-ics]").forEach(b => b.addEventListener("click", () => { const d = new Date(); d.setDate(d.getDate() + ((+b.dataset.dow - d.getDay() + 7) % 7 || 7)); const [hh, mm] = b.dataset.time.split(":"); d.setHours(+hh, +mm, 0, 0); const f = x => x.toISOString().replace(/[-:]/g, "").split(".")[0] + "Z"; const e = new Date(d.getTime() + 2 * 36e5);
    const ics = ["BEGIN:VCALENDAR","VERSION:2.0","PRODID:-//Florida Coffee//TR","BEGIN:VEVENT","UID:" + Date.now() + "@floridacoffee","DTSTAMP:" + f(new Date()),"DTSTART:" + f(d),"DTEND:" + f(e),"SUMMARY:" + b.dataset.ics,"LOCATION:" + (b.dataset.loc || "Florida Coffee"),"END:VEVENT","END:VCALENDAR"].join("\r\n");
    const a = document.createElement("a"); a.href = "data:text/calendar;charset=utf-8," + encodeURIComponent(ics); a.download = "florida-coffee.ics"; document.body.appendChild(a); a.click(); a.remove(); T("Takvim dosyası indirildi"); }));
  // SSS / haber / iş arama ve filtre
  document.querySelectorAll("[data-search]").forEach(inp => { const items = [...document.querySelectorAll(inp.dataset.search)]; const nrm = t => (t || "").toLowerCase().replace(/i̇/g, "i");
    inp.addEventListener("input", () => { const q = nrm(inp.value.trim()); let n = 0; items.forEach(it => { const ok = !q || nrm(it.textContent).includes(q); it.hidden = !ok; if (ok) n++; }); const c = document.querySelector(inp.dataset.count || "#none"); if (c) c.textContent = n + " sonuç"; }); });
  document.querySelectorAll("[data-filter]").forEach(bar => { const items = [...document.querySelectorAll(bar.dataset.filter)]; bar.querySelectorAll("[data-f]").forEach(b => b.addEventListener("click", () => { bar.querySelectorAll("[data-f]").forEach(x => x.setAttribute("aria-pressed", "false")); b.setAttribute("aria-pressed", "true"); const f = b.dataset.f; items.forEach(it => it.hidden = f !== "hepsi" && !(it.dataset.f || "").split(",").includes(f)); })); });
  // kaydet / paylaş
  const SAVED = new Set((() => { try { return JSON.parse(localStorage.getItem("fc_saved") || "[]"); } catch (e) { return []; } })());
  document.querySelectorAll(".nico.save").forEach(b => { const k = b.dataset.h; b.setAttribute("aria-pressed", String(SAVED.has(k))); b.textContent = SAVED.has(k) ? "♥" : "♡"; b.addEventListener("click", e => { e.preventDefault(); SAVED.has(k) ? SAVED.delete(k) : SAVED.add(k); try { localStorage.setItem("fc_saved", JSON.stringify([...SAVED])); } catch (x) {} b.setAttribute("aria-pressed", String(SAVED.has(k))); b.textContent = SAVED.has(k) ? "♥" : "♡"; T(SAVED.has(k) ? "Kaydedildi" : "Kayıt kaldırıldı"); }); });
  document.querySelectorAll(".nico.share").forEach(b => b.addEventListener("click", async e => { e.preventDefault(); const data = { title: "Florida Coffee", text: b.dataset.h, url: b.dataset.url || location.href }; try { if (navigator.share) await navigator.share(data); else { await navigator.clipboard.writeText(data.url); T("Bağlantı kopyalandı"); } } catch (x) {} }));
  // çok adımlı form
  document.querySelectorAll("form[data-steps]").forEach(f => { const steps = [...f.querySelectorAll("[data-step]")], bar = f.querySelector(".fsteps"); let i = 0; const paint = () => { steps.forEach((s, k) => s.hidden = k !== i); if (bar) [...bar.children].forEach((b, k) => b.classList.toggle("on", k <= i)); };
    f.querySelectorAll("[data-next]").forEach(b => b.addEventListener("click", () => { const req = [...steps[i].querySelectorAll("[required]")]; if (req.some(r => !r.reportValidity())) return; i = Math.min(steps.length - 1, i + 1); paint(); })); f.querySelectorAll("[data-prev]").forEach(b => b.addEventListener("click", () => { i = Math.max(0, i - 1); paint(); })); paint(); });
  // bölge kontrolü (3 km)
  const rc = document.getElementById("regionCheck"); if (rc && typeof B !== "undefined") { const out = document.getElementById("regionOut"); rc.addEventListener("input", () => { const q = rc.value.trim().toLowerCase(); if (q.length < 3) { out.textContent = ""; return; } const hit = B.find(b => (b.n + " " + b.c).toLowerCase().includes(q)); out.innerHTML = hit ? `<span style="color:var(--busy)">${hit.n} şubemiz var; 3 km koruma alanı dışında bir nokta gerekir.</span>` : `<span style="color:var(--ok)">Bu bölgede şubemiz yok: başvuruya açık.</span>`; }); }
  // iletişim: şehir → şubeler
  const cs = document.getElementById("citySel"); if (cs && typeof B !== "undefined") { const out = document.getElementById("cityOut"); const paint = () => { const c = cs.value; const list = B.filter(b => b.c.includes(c)); out.innerHTML = list.map(b => `<a class="cell" href="/subeler/${b.id}/"><h3>${b.n}</h3><p>${b.c} · ${hourStr(b.o)}–${hourStr(b.k)}</p><span class="more">Şube sayfası →</span></a>`).join(""); }; cs.addEventListener("change", paint); paint(); }
  // kariyer: pozisyona başvur
  document.querySelectorAll("[data-apply]").forEach(b => b.addEventListener("click", () => { const sel = document.getElementById("jobPos"); if (sel) { sel.value = b.dataset.apply; document.getElementById("basvur").scrollIntoView({ behavior: "smooth" }); T(b.dataset.apply + " için form hazır"); } }));
  // kurumsal teklif
  const cp = document.getElementById("cpPeople"); if (cp) { const ch = document.getElementById("cpHours"); const upd = () => { const p = +cp.value, hrs = +ch.value, cost = 12000 + p * 95 + hrs * 4500; document.getElementById("cpP").textContent = p; document.getElementById("cpH").textContent = hrs; document.getElementById("cpCups").textContent = Math.round(p * 1.6); document.getElementById("cpCost").textContent = cost.toLocaleString("tr-TR") + " ₺"; document.getElementById("cpBar").textContent = p > 250 ? "2 bar, 4 barista" : "1 bar, 2 barista"; }; cp.addEventListener("input", upd); ch.addEventListener("input", upd); upd(); }
  // SSS: Flo'ya sor
  document.querySelectorAll("[data-ask-flo]").forEach(b => b.addEventListener("click", () => { const fab = document.getElementById("floFab"); if (fab) fab.click(); }));
})();
'''
CSS = f'''
{ROOT_CSS}
*{{box-sizing:border-box}}[hidden]{{display:none!important}}
html{{scroll-behavior:smooth}}
body{{margin:0;background:#05202A;color:var(--ink);font-family:var(--ui);font-size:clamp(15px,.55vw + 12px,17px);line-height:1.6;-webkit-font-smoothing:antialiased}}
body::before{{content:"";position:fixed;inset:0;z-index:-1;background:radial-gradient(90% 60% at 15% 0%,#0B4353,transparent 60%),radial-gradient(60% 50% at 90% 100%,rgba(184,122,62,.35),transparent 60%),linear-gradient(178deg,#05202A,#041A22)}}
img{{max-width:100%}}
h1,h2,h3{{font-family:var(--disp);font-weight:700;letter-spacing:-.03em;text-wrap:balance;margin:0;line-height:1.05}}
h1{{font-size:clamp(2.2rem,5.5vw,4.2rem);font-weight:800;letter-spacing:-.04em}}
h2{{font-size:clamp(1.6rem,3.4vw,2.6rem)}}h3{{font-size:clamp(1.05rem,1.4vw,1.3rem);letter-spacing:-.015em}}
p{{margin:0 0 1rem;max-width:64ch}}a{{color:inherit}}
button,input,select,textarea{{font:inherit;color:inherit}}button{{background:none;border:none;cursor:pointer}}
:focus-visible{{outline:2px solid var(--amber);outline-offset:3px}}
.eyebrow{{font-family:var(--disp);font-size:.68rem;letter-spacing:.2em;text-transform:uppercase;color:var(--amber);font-weight:700}}
.lede{{font-size:clamp(1.02rem,1.4vw,1.25rem);color:var(--ink-2);max-width:58ch;margin-top:1rem}}
.lbl{{font-size:.68rem;letter-spacing:.16em;text-transform:uppercase;color:var(--ink-3);font-weight:700;font-family:var(--disp)}}
.wrap{{max-width:1180px;margin:0 auto;padding:0 clamp(1.2rem,5vw,4rem)}}
.sec{{padding:clamp(3rem,7vh,5.5rem) 0}}
.hero{{padding:clamp(3.5rem,9vh,7rem) 0 clamp(2rem,5vh,3.5rem);border-bottom:1px solid var(--hair)}}
.hero.img{{position:relative;min-height:22rem;display:flex;align-items:flex-end}}
.hero.img .bg{{position:absolute;inset:0;z-index:-1;overflow:hidden}}
.hero.img .bg img{{width:100%;height:100%;object-fit:cover;opacity:.55}}
.hero.img .bg::after{{content:"";position:absolute;inset:0;background:linear-gradient(90deg,rgba(4,20,26,.92),rgba(4,20,26,.55) 60%,rgba(4,20,26,.3)),linear-gradient(180deg,rgba(4,20,26,.2),rgba(4,20,26,.85))}}
.crumbs{{font-size:.75rem;color:var(--ink-3);display:flex;gap:.5rem;flex-wrap:wrap;margin-bottom:1rem}}.crumbs a{{text-decoration:none;color:var(--ink-3)}}.crumbs a:hover{{color:var(--ink)}}
.grid{{display:grid;gap:1px;background:var(--hair);border:1px solid var(--hair)}}
.g2{{grid-template-columns:repeat(auto-fill,minmax(min(100%,20rem),1fr))}}.g3{{grid-template-columns:repeat(auto-fill,minmax(min(100%,15rem),1fr))}}.g4{{grid-template-columns:repeat(auto-fill,minmax(min(100%,12rem),1fr))}}
.cell{{background:rgba(6,24,31,.72);padding:1.1rem 1.2rem;display:flex;flex-direction:column;gap:.5rem;text-decoration:none;color:inherit;transition:background .2s}}
a.cell:hover{{background:rgba(10,77,92,.55)}}
.cell p{{margin:0;font-size:.9rem;color:var(--ink-2)}}
.cell .more{{margin-top:auto;font-family:var(--disp);font-size:.75rem;letter-spacing:.1em;text-transform:uppercase;font-weight:700;color:var(--amber)}}
.panel{{background:var(--glass);border:1px solid var(--hair);padding:1.2rem 1.3rem}}
.paper{{background:var(--paper);color:var(--paper-ink)}}.paper h1,.paper h2,.paper h3{{color:var(--paper-ink)}}.paper .lede,.paper p{{color:var(--paper-ink-2)}}.paper .lbl{{color:var(--paper-ink-2)}}
.paper .grid{{background:var(--paper-line);border-color:var(--paper-line)}}.paper .cell{{background:#FBF8F2}}.paper a.cell:hover{{background:#F1EBDF}}.paper .cell p{{color:var(--paper-ink-2)}}
.paper .panel{{background:#FBF8F2;border-color:var(--paper-line)}}
.paper .btn.ghost{{color:var(--paper-ink);border-color:var(--paper-ink)}}.paper .btn.ghost::before{{background:var(--paper-ink)}}.paper .btn.ghost:hover{{color:var(--paper)}}
{CHIP_CSS}
{BTN_CSS}
{SQ_CSS}
{NAV_CSS}
.nav{{background:rgba(4,20,26,.9)}}
{FILT_CSS}
{NEWS_CSS}
{FLO_CSS}
{EXTRA_CSS}
{EXTRA_CSS2}
.hrs{{display:grid;grid-template-columns:1fr auto;gap:.25rem .9rem;font-size:.9rem;font-variant-numeric:tabular-nums}}
.kv{{display:grid;grid-template-columns:auto 1fr;gap:.45rem 1rem;font-size:.92rem}}.kv dt{{color:var(--ink-3)}}.kv dd{{margin:0}}
.faq details{{border-top:1px solid var(--hair);padding:.8rem 0}}.faq summary{{cursor:pointer;font-weight:700;font-family:var(--disp);font-size:1rem}}.faq p{{margin:.5rem 0 0;color:var(--ink-2)}}
.paper .faq details{{border-color:var(--paper-line)}}.paper .faq p{{color:var(--paper-ink-2)}}
.mitem{{display:grid;grid-template-columns:3.6rem 1fr auto;grid-template-areas:"img n p" "img d d" "img tags tags";gap:.3rem 1rem;padding:.9rem 0;border-bottom:1px solid var(--paper-line);align-items:baseline;text-decoration:none;color:inherit}}
.mitem:not(:has(.thumb)){{grid-template-columns:1fr auto;grid-template-areas:"n p" "d d" "tags tags"}}
.mitem .thumb{{grid-area:img;align-self:start;width:3.6rem;height:3.6rem;overflow:hidden;background:var(--paper-line)}}.mitem .thumb img{{width:100%;height:100%;object-fit:cover;display:block;transition:transform .3s}}.mitem:hover .thumb img{{transform:scale(1.06)}}
.mitem .n{{grid-area:n}}.mitem .p{{grid-area:p}}.mitem .d{{grid-area:d}}.mitem .tags{{grid-area:tags}}
.mitem .n{{font-family:var(--disp);font-weight:700;font-size:1.05rem}}.mitem .d{{font-size:.84rem;color:var(--paper-ink-2)}}.mitem .p{{font-family:var(--disp);font-weight:700;font-variant-numeric:tabular-nums}}
.mitem .tags{{display:flex;gap:.3rem;flex-wrap:wrap}}
.tg{{font-size:.68rem;padding:.12rem .5rem;border:1px solid var(--paper-line);color:var(--paper-ink-2)}}.tg.v{{border-color:#8FBF9A;color:#3D6B48}}.tg.c{{border-color:#D8B48A;color:#8A5A24}}
.mcat{{padding:.45rem .95rem;border:1px solid var(--paper-line);font-size:.85rem;font-weight:600;color:var(--paper-ink-2)}}.mcat[aria-pressed="true"]{{background:var(--paper-ink);color:var(--paper);border-color:var(--paper-ink)}}
.mcats{{display:flex;gap:.4rem;flex-wrap:wrap;margin:1.2rem 0 .8rem}}
form.f{{display:grid;gap:.9rem}}form.f label{{display:grid;gap:.3rem;font-size:.82rem;font-weight:600;color:var(--ink-2)}}
form.f input,form.f select,form.f textarea{{background:rgba(9,14,19,.6);border:1px solid var(--hair-2);color:var(--ink);padding:.7rem .85rem;font-size:.95rem}}
.paper form.f input,.paper form.f select,.paper form.f textarea{{background:#fff;border-color:var(--paper-line);color:var(--paper-ink)}}.paper form.f label{{color:var(--paper-ink-2)}}
.ok{{border:1px solid var(--ok);color:var(--ok);padding:.8rem 1rem;font-size:.9rem}}
.two{{display:grid;grid-template-columns:minmax(0,1.1fr) minmax(0,.9fr);gap:clamp(1.2rem,3vw,2.5rem);align-items:start}}@media (max-width:860px){{.two{{grid-template-columns:1fr}}}}
.imgband{{aspect-ratio:16/7;overflow:hidden;border:1px solid var(--hair)}}.imgband img{{width:100%;height:100%;object-fit:cover;display:block}}
footer{{background:#030F14;border-top:1px solid var(--hair);padding:clamp(2.5rem,6vh,4rem) 0 2rem;font-size:.85rem;color:var(--ink-3);margin-top:3rem}}
footer .cols{{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,12rem),1fr));gap:2rem}}footer h4{{font-family:var(--disp);font-size:.95rem;color:var(--ink);margin:0 0 .6rem}}
footer ul{{list-style:none;margin:0;padding:0;display:grid;gap:.3rem}}footer a{{text-decoration:none;color:var(--ink-3)}}footer a:hover{{color:var(--ink)}}
footer .end{{margin-top:2.5rem;padding-top:1.2rem;border-top:1px solid var(--hair);display:flex;justify-content:space-between;gap:1rem;flex-wrap:wrap;font-size:.76rem}}
.dot-s{{width:7px;height:7px;display:inline-block;border-radius:50%}}.dot-s.g{{background:var(--ok)}}.dot-s.r{{background:var(--busy)}}
.notice{{border:1px solid var(--rust);color:#F0916C;padding:.7rem 1rem;font-size:.85rem;margin-bottom:1.4rem}}
.paper .notice{{border-color:var(--rust);color:#8A3A10;background:#FBEFE6}}
.prose h2{{font-size:1.35rem;margin:2rem 0 .6rem}}.prose h3{{font-size:1.05rem;margin:1.4rem 0 .4rem}}.prose p,.prose li{{max-width:70ch}}.prose ul{{padding-left:1.2rem}}
.badges{{display:flex;gap:.6rem;flex-wrap:wrap}}.badge{{border:1px solid var(--hair-2);padding:.6rem .9rem;font-family:var(--disp);font-weight:700;font-size:.85rem;display:flex;gap:.5rem;align-items:center}}
@media (max-width:640px){{.flo{{right:0;bottom:0;width:100vw;max-height:88dvh}}.flo-fab{{right:.9rem;bottom:1rem}}}}
'''
JS = f'''"use strict";
{DATA_JS}
{LOGO_JS}
{EXTRA_JS}
{EXTRA_JS2}
(() => {{ const ns = document.getElementById("navStatus"); if (!ns || typeof B === "undefined") return;
  const paint = () => {{ const b = B[0], now = new Date(), o = isOpen(b, now); const t = b.n + " · " + (o ? "açık" : "kapalı") + " · gün batımı " + zhm(sunTimes(now, b.lat, b.lng).set, tzOf(b)); ns.querySelector("span").textContent = t; ns.classList.toggle("off", !o); const m = document.getElementById("mnavStatus"); if (m) m.textContent = t; }};
  paint(); setInterval(paint, 60000); }})();
(() => {{ const f = document.getElementById("fnews"); if (f) f.addEventListener("submit", e => {{ e.preventDefault(); showToast("Kaydedildi. Ayda en fazla iki e-posta."); f.reset(); }}); }})();
{MENU_JS}
{DIET_JS}
/* nav aktif */
document.querySelectorAll(".navlinks a").forEach(a => {{ if (location.pathname.startsWith(a.getAttribute("href")) && a.getAttribute("href") !== "/") a.setAttribute("aria-current","page"); }});
/* şube canlı durumu */
document.querySelectorAll("[data-branch]").forEach(el => {{ const b = B.find(x => x.id === el.dataset.branch); if (!b) return; const now = new Date(), open = isOpen(b, now);
  el.innerHTML = `<span class="dot-s ${{open?"g":"r"}}"></span> ${{open ? "Şu an açık" : "Şu an kapalı"}}` + (b.f.includes("manzara") ? ` · gün batımı ${{zhm(sunTimes(now,b.lat,b.lng).set, tzOf(b))}}` : ""); }});
/* formlar (demo) */
document.querySelectorAll("form.f").forEach(f => f.addEventListener("submit", e => {{ e.preventDefault(); const ok = f.querySelector(".ok"); if (ok) ok.hidden = false; f.querySelectorAll("input,textarea").forEach(i => i.value = ""); }}));
/* menü filtreleri */
const ml = document.getElementById("mlist");
if (ml) {{
  let cat = document.querySelector("#mcats [aria-pressed=true]")?.dataset.c || "sicak", diet = "";
  const passDiet = tags => !diet || (diet==="hafif" ? kcalOf(tags)<100 : diet==="vegan" ? tags.includes("vegan") : diet==="sutsuz" ? (tags.includes("sütsüz")||tags.includes("vegan")) : diet==="azkafein" ? cafOf(tags)<80 : diet==="glutensiz" ? !tags.includes("glüten") : true);
  const slug = s => s.toLowerCase().replace(/[çğıöşüâî]/g, c => ({{"ç":"c","ğ":"g","ı":"i","ö":"o","ş":"s","ü":"u","â":"a","î":"i"}})[c]).replace(/[^a-z0-9]+/g,"-").replace(/^-|-$/g,"");
  const render = () => {{ const items = MENU[cat].filter(([,,,t]) => passDiet(t)); ml.innerHTML = items.length ? items.map(([n,d,p,t]) => `<a class="mitem" href="/menu/${{slug(n)}}/"><span class="thumb"><img src="/img/menu/${{slug(n)}}.jpg" alt="" loading="lazy" decoding="async" onerror="this.parentNode.remove()"></span><span class="n">${{n}}</span><span class="p">${{p}} ₺</span><span class="d">${{d}}</span><span class="tags">${{t.filter(x=>x!=="sütsüz"||diet==="sutsuz").map(x=>`<span class="tg ${{/vegan|glütensiz|kafeinsiz/.test(x)?"v":/kafein|mg/.test(x)?"c":""}}">${{x}}</span>`).join("")}}</span></a>`).join("") : `<p style="padding:1rem 0">Bu filtrede ürün yok.</p>`; }};
  document.querySelectorAll("#mcats .mcat").forEach(b => b.addEventListener("click", () => {{ document.querySelectorAll("#mcats .mcat").forEach(x=>x.setAttribute("aria-pressed","false")); b.setAttribute("aria-pressed","true"); cat = b.dataset.c; render(); }}));
  document.querElementsAll = null;
  document.querySelectorAll("#dietF .mcat").forEach(b => b.addEventListener("click", () => {{ document.querySelectorAll("#dietF .mcat").forEach(x=>x.setAttribute("aria-pressed","false")); b.setAttribute("aria-pressed","true"); diet = b.dataset.d; render(); }}));
  render();
}}
/* şube bulucu */
const bl = document.getElementById("branches");
if (bl) {{
  const F2 = {{manzara:"Manzara",gece:"Gece açık",calisma:"Çalışma alanı",otopark:"Otopark",kahvalti:"Kahvaltı",evcil:"Evcil dostu"}};
  const active = new Set();
  const render = () => {{ const now = new Date(); const list = B.filter(b => [...active].every(f => f==="acik" ? isOpen(b,now) : b.f.includes(f)));
    document.getElementById("fcount").textContent = list.length + " / " + B.length + " şube";
    bl.innerHTML = list.map(b => {{ const open = isOpen(b,now); return `<a class="cell" href="/subeler/${{b.id}}/"><figure class="bimg"><img src="/img/subeler/${{b.id}}.jpg" alt="" loading="lazy" decoding="async" onerror="this.parentNode.remove()"></figure><div style="display:flex;justify-content:space-between;gap:.5rem"><h3>${{b.n}}</h3><span style="font-size:.78rem;color:${{open?"var(--ok)":"var(--ink-3)"}}">${{open?"Açık":"Kapalı"}}</span></div><p>${{b.c}} · ${{hourStr(b.o)}}–${{hourStr(b.k)}} · ★ ${{b.r}}</p>${{b.f.includes("manzara")?`<p style="color:var(--amber)">Gün batımı ${{zhm(sunTimes(now,b.lat,b.lng).set,tzOf(b))}}</p>`:""}}<div style="display:flex;gap:.3rem;flex-wrap:wrap">${{b.f.map(f=>`<span class="chip">${{F2[f]}}</span>`).join("")}}</div><span class="more">Şube sayfası →</span></a>`; }}).join(""); }};
  document.querySelectorAll("#filters .fbtn").forEach(btn => btn.addEventListener("click", () => {{ const f = btn.dataset.f, on = btn.getAttribute("aria-pressed")==="true"; btn.setAttribute("aria-pressed", String(!on)); on ? active.delete(f) : active.add(f); render(); }}));
  render();
}}
/* haber filtreleri */
const nl = document.getElementById("news");
if (nl) {{ document.querySelectorAll("#tazeF .fbtn").forEach(b => b.addEventListener("click", () => {{ document.querySelectorAll("#tazeF .fbtn").forEach(x=>x.setAttribute("aria-pressed","false")); b.setAttribute("aria-pressed","true"); const t = b.dataset.t; nl.querySelectorAll("[data-t]").forEach(el => el.hidden = !(t==="hepsi" || el.dataset.t===t)); }})); }}
/* franchise hesaplayıcı */
const fC = document.getElementById("fCity");
if (fC) {{ const fmt = n => n.toLocaleString("tr-TR"); const calc = () => {{ const city=+fC.value, m2=+document.getElementById("fM2").value, rev=+document.getElementById("fRev").value;
  document.getElementById("fM2v").textContent=m2; document.getElementById("fRevv").textContent=fmt(rev);
  const inv=Math.round((m2*28000*city+900000)/50000)*50000, roy=rev*0.05*1.2, ad=rev*0.01, margin=rev*0.22-roy-ad;
  document.getElementById("oInv").textContent=fmt(inv)+" ₺"; document.getElementById("oRoy").textContent=fmt(Math.round(roy))+" ₺"; document.getElementById("oAd").textContent="≤ "+fmt(Math.round(ad))+" ₺"; document.getElementById("oPb").textContent=margin>0?Math.round(inv/margin)+"–"+Math.round(inv/margin*1.4)+" ay":"—"; }};
  ["fCity","fM2","fRev"].forEach(id => document.getElementById(id).addEventListener("input", calc)); calc(); }}
{FLO_JS}
{HINT_JS}
showHint(document.body.dataset.page || "safak");
'''.replace("  document.querElementsAll = null;\n","")

def head(title, desc, path, jsonld=None, noindex=True):
    ld = f'<script type="application/ld+json">{json.dumps(jsonld, ensure_ascii=False)}</script>' if jsonld else ""
    return f'''<!doctype html><html lang="tr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{H.escape(title)}</title><meta name="description" content="{H.escape(desc)}">{'<meta name="robots" content="noindex">' if noindex else ''}
<link rel="canonical" href="{SITE}{path}"><meta name="theme-color" content="#004854">
<meta property="og:title" content="{H.escape(title)}"><meta property="og:description" content="{H.escape(desc)}"><meta property="og:image" content="{SITE}/img/hero.jpg"><meta property="og:type" content="website">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Outfit:wght@500;600;700;800&family=Manrope:wght@400;500;600;700&family=Poppins:wght@600&display=swap">
<link rel="stylesheet" href="/assets/site.css">{ld}</head>'''

def shell(body, page, title, desc, path, jsonld=None, cls=""):
    nav = "".join(f'<a href="{h}">{t}</a>' for t,h in NAV)
    # tema sınıfı (ör. paper) hero'dan sonra gelen <main>'e uygulanır; hero, nav ve footer koyu kalır
    end = body.find('</section>') + len('</section>') if body.startswith('<section class="hero') else 0
    body = body[:end] + f'<main id="main" class="{cls}">' + body[end:] + '</main>'
    return head(title, desc, path, jsonld) + f'''<body data-page="{page}">
<a class="skip" href="#main">İçeriğe geç</a>
<header class="nav" role="banner"><a class="home" href="/" aria-label="Florida Coffee ana sayfa">{LOGO_HTML}</a>
<nav class="navlinks" id="navlinks" aria-label="Ana menü">{nav}</nav>
<div class="navr"><a class="status" id="navStatus" href="/subeler/" title="En yakın şube"><i></i><span>Kavacık</span></a><a class="lang" href="/en/" hreflang="en" title="English">EN</a><a class="btn amber sm cta" href="/app/">Ön sipariş</a><button class="burger" id="burger" aria-expanded="false" aria-controls="mnav" aria-label="Menüyü aç"><span></span><span></span><span></span></button></div></header>
<div class="mnav" id="mnav" hidden><nav aria-label="Mobil menü" class="mnav-links">{nav}</nav><div class="mnav-foot"><a class="status" href="/subeler/"><i></i><span id="mnavStatus">Kavacık</span></a><a class="btn amber" href="/app/">Ön sipariş ver</a><div class="mnav-langs"><b>TR</b><a href="/en/">EN</a><span>ME · yakında</span></div></div></div>
{body}
<footer id="footer"><div class="fwrap"><div class="fgrid">
<div class="fbrand">{LOGO_FOOT}<span class="sr">Florida Coffee</span><p class="tag">Taste of Joy. İstanbul doğumlu, 17 şube, iki ülke; her fincanda aynı reçete.</p><address>Çengelköy Mah. Görgeç Sok. No:6<br>Üsküdar / İstanbul</address><div class="contact"><a href="tel:+902160000000">+90 216 000 00 00</a><a href="mailto:merhaba@floridacoffee.com.tr">merhaba@floridacoffee.com.tr</a><a href="/franchise/basvuru/">Franchise başvurusu →</a></div><div class="social"><a href="https://www.instagram.com/floridacoffeetr/" rel="noopener" aria-label="Instagram"><svg viewBox="0 0 24 24"><path d="M12 7.3a4.7 4.7 0 1 0 0 9.4 4.7 4.7 0 0 0 0-9.4zm0 7.7a3 3 0 1 1 0-6 3 3 0 0 1 0 6zm5.9-7.9a1.1 1.1 0 1 1-2.2 0 1.1 1.1 0 0 1 2.2 0zM12 2c-2.7 0-3 0-4.1.1-2.9.1-4.7 1.9-4.8 4.8C3 8 3 8.3 3 12s0 4 .1 5.1c.1 2.9 1.9 4.7 4.8 4.8 1.1.1 1.4.1 4.1.1s3 0 4.1-.1c2.9-.1 4.7-1.9 4.8-4.8.1-1.1.1-1.4.1-4.1s0-3-.1-4.1c-.1-2.9-1.9-4.7-4.8-4.8C15 2 14.7 2 12 2zm0 1.8c2.7 0 3 0 4 .1 2 .1 2.9 1 3 3 .1 1 .1 1.3.1 4s0 3-.1 4c-.1 2-1 2.9-3 3-1 .1-1.3.1-4 .1s-3 0-4-.1c-2-.1-2.9-1-3-3-.1-1-.1-1.3-.1-4s0-3 .1-4c.1-2 1-2.9 3-3 1-.1 1.3-.1 4-.1z"/></svg></a><a href="#" aria-label="TikTok"><svg viewBox="0 0 24 24"><path d="M16.6 5.8A4.3 4.3 0 0 1 15.5 3h-3.1v12.4a2.6 2.6 0 1 1-2.6-2.6c.3 0 .5 0 .8.1V9.7a5.7 5.7 0 1 0 4.9 5.6V9.1a7.4 7.4 0 0 0 4.3 1.4V7.4a4.3 4.3 0 0 1-3.2-1.6z"/></svg></a><a href="https://www.facebook.com/floridacoffeetr/" rel="noopener" aria-label="Facebook"><svg viewBox="0 0 24 24"><path d="M13.5 22v-8h2.7l.4-3.2h-3.1V8.8c0-.9.3-1.6 1.6-1.6h1.7V4.4c-.3 0-1.3-.1-2.5-.1-2.5 0-4.1 1.5-4.1 4.2v2.3H7.4V14h2.8v8h3.3z"/></svg></a><a href="#" aria-label="YouTube"><svg viewBox="0 0 24 24"><path d="M21.6 7.2a2.5 2.5 0 0 0-1.8-1.8C18.3 5 12 5 12 5s-6.3 0-7.8.4A2.5 2.5 0 0 0 2.4 7.2 26 26 0 0 0 2 12a26 26 0 0 0 .4 4.8 2.5 2.5 0 0 0 1.8 1.8C5.7 19 12 19 12 19s6.3 0 7.8-.4a2.5 2.5 0 0 0 1.8-1.8A26 26 0 0 0 22 12a26 26 0 0 0-.4-4.8zM10 15V9l5.2 3L10 15z"/></svg></a></div></div>
<div><h4>Keşfet</h4><ul><li><a href="/menu/">Menü</a></li><li><a href="/subeler/">Şubeler</a></li><li><a href="/kahvemiz/">Kahvemiz</a></li><li><a href="/taze/">Taze</a></li><li><a href="/urunler/">Ürünler</a></li><li><a href="/etkinlikler/">Etkinlikler</a></li></ul></div>
<div><h4>Kulüp</h4><ul><li><a href="/kulup/">FloridaDays Club</a></li><li><a href="/uygulama/">Uygulama</a></li><li><a href="/app/">Uygulama demosu</a></li><li><a href="/hikayemiz/">Hikâyemiz</a></li><li><a href="/sss/">SSS</a></li></ul></div>
<div><h4>Kurumsal</h4><ul><li><a href="/franchise/">Franchise</a></li><li><a href="/kurumsal/">Kurumsal satış</a></li><li><a href="/kariyer/">Kariyer</a></li><li><a href="/iletisim/">İletişim</a></li><li><a href="/platform/">Platform prototipi</a></li><li><a href="/sunum/">Sunum</a></li></ul></div>
<div class="fapp"><h4>Uygulama</h4><p style="margin:0 0 .6rem;color:var(--ink-2)">Ön sipariş, FloridaDays Club, cüzdan.</p><div class="badges"><a class="badge" href="/uygulama/"><svg viewBox="0 0 24 24"><path d="M16.4 12.7c0-2.4 2-3.6 2.1-3.7-1.1-1.7-2.9-1.9-3.5-1.9-1.5-.2-2.9.9-3.7.9-.8 0-1.9-.9-3.2-.8-1.6 0-3.1 1-4 2.4-1.7 2.9-.4 7.3 1.2 9.7.8 1.2 1.8 2.5 3 2.4 1.2 0 1.7-.8 3.2-.8s1.9.8 3.2.8 2.1-1.2 2.9-2.4c.9-1.3 1.3-2.6 1.3-2.7 0 0-2.5-1-2.5-3.9zM14 5.5c.7-.8 1.1-1.9 1-3-1 0-2.1.7-2.8 1.5-.6.7-1.2 1.8-1 2.9 1.1.1 2.2-.6 2.8-1.4z"/></svg><span><small>App Store</small><b>iPhone için indir</b></span></a><a class="badge" href="/uygulama/"><svg viewBox="0 0 24 24"><path d="M3.6 2.3 13 12l-9.4 9.7c-.3-.2-.6-.6-.6-1.1V3.4c0-.5.3-.9.6-1.1zM16 15l-2.3-3L16 9l3.9 2.2c.8.5.8 1.2 0 1.6L16 15zM14.7 12.9 5.4 22.5l9.9-5.7-1.9-1.9zM5.4 1.5l9.3 9.6 1.9-1.9-9.9-5.7-1.3-2z"/></svg><span><small>Google Play</small><b>Android için indir</b></span></a></div><h4>Haber al</h4><form class="fnews" id="fnews" autocomplete="off"><input type="email" required placeholder="e-posta" aria-label="E-posta"><button class="btn amber sm" type="submit">Kaydol</button></form></div>
</div><div class="fend"><span>© 2026 Florida Coffee Kahve Gıda San. ve Tic. A.Ş.</span><nav class="legal" aria-label="Yasal"><a href="/yasal/kvkk/">KVKK aydınlatma</a><a href="/yasal/cerez/">Çerez politikası</a><a href="/yasal/kullanici-sozlesmesi/">Kullanıcı sözleşmesi</a><a href="/yasal/mesafeli-satis/">Mesafeli satış</a></nav><span class="langs"><b>TR</b><a href="/en/">EN</a><span>ME</span></span></div><p class="demo-note">Demo · P3Media tarafından Florida Coffee için hazırlanmış tasarım önerisi; içerik ve iletişim bilgileri örnektir.</p></div></footer>
{FLO_HTML}
<script src="/assets/site.js" defer></script></body></html>'''

def hero(eyebrow, h1, lede, crumbs=None, img=None, extra=""):
    c = f'<div class="crumbs"><a href="/">Ana sayfa</a> › ' + " › ".join(f'<a href="{h}">{t}</a>' if h else t for t,h in crumbs) + '</div>' if crumbs else ""
    bg = f'<div class="bg"><img src="/img/{img}.jpg" alt=""></div>' if img else ""
    return f'<section class="hero{" img" if img else ""}">{bg}<div class="wrap">{c}<div class="eyebrow">{eyebrow}</div><h1>{h1}</h1><p class="lede">{lede}</p>{extra}</div></section>'

PAGES = []  # (path, html)
def page(path, html_): PAGES.append((path, html_))

# ---------- MENÜ ----------
def tagnum(tags, key):
    for t in tags:
        if key in t:
            m = re.search(r"\d+", t)
            if m: return int(m.group(0))
    return None
def has_menu_img(sl): return os.path.exists(os.path.join(BASE, "demo-site", "img", "menu", sl + ".jpg"))
def pcard(it):
    sl = slug(it["n"]); kcal = tagnum(it["tags"], "kcal"); mg = tagnum(it["tags"], "mg")
    img = f'<img src="/img/menu/{sl}.jpg" alt="{it["n"]}" loading="lazy" decoding="async">' if has_menu_img(sl) else f'<span class="pph">{it["n"][0]}</span>'
    small = [t for t in it["tags"] if ("kcal" in t or "mg" in t)]
    badges = [t for t in it["tags"] if t in ("vegan","glütensiz","kafeinsiz")]
    tags = "".join(f'<span class="tg c">{t}</span>' for t in small) + "".join(f'<span class="tg v">{t}</span>' for t in badges)
    return (f'<a class="pcard" href="/menu/{sl}/" data-name="{it["n"]}" data-desc="{it["d"]}" data-tags="{" ".join(it["tags"])}" data-kcal="{kcal if kcal is not None else ""}" data-mg="{mg if mg is not None else ""}">'
            f'<div class="pimg">{img}</div><div class="pbody"><div class="prow"><h3>{it["n"]}</h3><span class="pp">{it["p"]} ₺</span></div><p class="pd">{it["d"]}</p><div class="ptags">{tags}</div></div></a>')
CATLEDE = {"sicak":"Espresso bazlı içecekler ve elde demlemeler. Her shot 14 g, 18–23 saniye.","soguk":"Cold brew 16 saat demlenir; buzlu espresso içeceklerinde shot buza dökülür.","diger":"Kahve içmeyenler için: çikolata, çay, matcha, taze sıkım ve mevsimlik içecekler.","yiyecek":"Günlük üretim; alerjen bilgisi her üründe, baristada da sorabilirsiniz."}
cats = "".join(f'<a class="mcat sm" aria-pressed="{"true" if i==0 else "false"}" href="#c-{k}">{v}</a>' for i,(k,v) in enumerate(CATN.items()))
diet = '<div class="row" id="dietF"><button class="mcat sm" aria-pressed="true" data-d="">Hepsi</button><button class="mcat sm" aria-pressed="false" data-d="hafif">Hafif · &lt;100 kcal</button><button class="mcat sm" aria-pressed="false" data-d="vegan">Vegan</button><button class="mcat sm" aria-pressed="false" data-d="sutsuz">Sütsüz</button><button class="mcat sm" aria-pressed="false" data-d="azkafein">Az kafein</button><button class="mcat sm" aria-pressed="false" data-d="glutensiz">Glütensiz</button></div>'
msecs = "".join(f'<section class="msec" id="c-{c}"><div class="mhead"><h2>{CATN[c]}</h2><p>{CATLEDE[c]} <span class="cnt">{len(items)} ürün</span></p></div><div class="pgrid">{"".join(pcard(it) for it in items)}</div></section>' for c, items in MENU.items())
menu_ld = {"@context":"https://schema.org","@type":"Menu","name":"Florida Coffee Menü","hasMenuSection":[{"@type":"MenuSection","name":CATN[c],"hasMenuItem":[{"@type":"MenuItem","name":i["n"],"description":i["d"],"offers":{"@type":"Offer","price":i["p"],"priceCurrency":"TRY"}} for i in items]} for c,items in MENU.items()]}
page("/menu/", shell(hero("Bölüm 15:00 · Menü","Fiyat, kalori, alerjen.<br>Hepsi burada.",f"{sum(len(v) for v in MENU.values())} ürün, dört kategori. Fiyatlar İstanbul şubeleri içindir; Anadolu ve Karadağ fiyatları şube sayfalarında. Süt: inek dahil, laktozsuz +10 ₺, yulaf ve badem +15 ₺.",[("Menü",None)]) +
  f'<div class="mbar"><div class="wrap"><div class="row" id="mcats">{cats}</div>{diet}<input class="search" id="msearch" type="search" placeholder="Ürün ara: latte, vegan, cheesecake…" aria-label="Menüde ara"></div></div>'
  f'<div class="wrap">{msecs}<p class="mempty" id="mempty" hidden>Bu filtreyle ürün yok. Filtreyi kaldırın ya da başka bir şey arayın.</p>'
  f'<section class="sec"><div class="grid g3"><div class="cell"><h3>Süt seçenekleri</h3><p>İnek sütü dahil · laktozsuz +10 ₺ · yulaf ve badem +15 ₺. Tercihinizi uygulamada profilinize kaydedin, her siparişte hatırlanır.</p></div><div class="cell"><h3>Boylar</h3><p>Küçük −15 ₺ · orta · büyük +20 ₺. Fiyatlar orta boy içindir.</p></div><div class="cell"><h3>Alerjenler</h3><p>Her üründe etiket var; kuruyemiş, süt, glüten ve yumurta belirtilir. Emin değilseniz baristaya sorun.</p></div></div><p class="mnote">Örnek fiyatlar; gerçek menü merkezden yönetilir ve şube fiyat grubuna göre otomatik güncellenir.</p></div></section></div>',
  "menu","Menü ve Fiyatlar · Florida Coffee","Florida Coffee menüsü: sıcak ve soğuk kahveler, kahve dışı içecekler ve yiyecekler; fotoğraf, kalori, kafein ve alerjen bilgisiyle.","/menu/",menu_ld,"paper"))

ESPRESSO = {"Espresso","Americano","Cortado","Flat White","Cappuccino","Latte","Caramel Latte","Vanilla Latte","Mocha","White Mocha","Caramel Macchiato","Iced Americano","Iced Latte","Iced Caramel Latte","Iced Mocha","Iced White Mocha","Frappe","Çikolatalı Frappe","Affogato"}
BREW = {"Florida Filtre","V60","Chemex","Iced Filtre"}
def howto(it, c):
    n = it["n"]
    if n in ESPRESSO: return "<b>Her şubede aynı reçete.</b> 14 g doz tartıyla, 90–96 °C su, 9 bar, 18–23 saniyede 30–60 g çıktı. Sütlü içeceklerde süt 60–65 °C'ye kadar ısıtılır; ipeksi mikro köpük, büyük kabarcık yok."
    if n in BREW: return "<b>Günün çekirdeği, taze öğütüm.</b> Kavurma tarihi 7–21 gün arası çekirdek, demleme öncesi öğütülür; 90–96 °C su ile kontrollü akış. Çekirdek tahtada yazar, baristaya sorabilirsiniz."
    if "Türk Kahvesi" in n: return "<b>7 g, közde.</b> İnce öğütüm, soğuk suyla başlanır, köpüğü kaçırmadan yavaş pişirilir; lokum ve suyla servis."
    if "Cold Brew" in n: return "<b>16 saat soğuk demleme.</b> Kaba öğütüm, oda sıcaklığında su, 16 saat; süzülüp 48 saat içinde tüketilir. Sıcak temas yok, asit düşük."
    if c == "diger": return "<b>Kahve içermez</b> ya da düşük kafeinli. Şuruplar ve konsantreler şubede hazırlanır; şeker oranı azaltılabilir."
    return "<b>Günlük üretim.</b> Merkez mutfaktan her sabah şubeye gelir; gün sonunda kalan satılmaz. Alerjen bilgisi etikette ve baristada."
def pairings(it, c):
    foods = MENU["yiyecek"]; drinks = MENU["sicak"] + MENU["soguk"]
    pool = drinks if c == "yiyecek" else foods
    k = sum(ord(ch) for ch in it["n"])
    return [pool[(k + i * 7) % len(pool)] for i in range(3)]
for c, items in MENU.items():
    for it in items:
        sl = slug(it["n"]); kcal = tagnum(it["tags"], "kcal"); mg = tagnum(it["tags"], "mg")
        kcal_s = next((t for t in it["tags"] if "kcal" in t), None); caf_s = next((t for t in it["tags"] if "mg" in t), None)
        has_img = has_menu_img(sl)
        ld = {"@context":"https://schema.org","@type":"MenuItem","name":it["n"],"description":it["d"],"offers":{"@type":"Offer","price":it["p"],"priceCurrency":"TRY","availability":"https://schema.org/InStock"}}
        if kcal_s: ld["nutrition"] = {"@type":"NutritionInformation","calories":kcal_s}
        if has_img: ld["image"] = f"{SITE}/img/menu/{sl}.jpg"
        drink = c != "yiyecek"; milky = drink and "sütsüz" not in it["tags"] and "vegan" not in it["tags"]
        allergens = [t for t in it["tags"] if t in ("glüten","süt","yumurta","fıstık","ceviz")]
        diet_b = [t for t in it["tags"] if t in ("vegan","glütensiz","kafeinsiz","sütsüz")]
        big = f'<img src="/img/menu/{sl}.jpg" alt="{it["n"]}">' if has_img else f'<span class="pph" style="display:grid;place-items:center;height:100%;font-family:var(--disp);font-size:5rem;color:var(--amber)">{it["n"][0]}</span>'
        mini = f'<div><b>{kcal if kcal is not None else "—"}</b><span>kcal</span></div><div><b>{mg if mg is not None else ("0" if "kafeinsiz" in it["tags"] else "—")}</b><span>mg kafein</span></div><div><b>{it["p"]} ₺</b><span>orta boy</span></div>' if drink else f'<div><b>{CATN[c]}</b><span>kategori</span></div><div><b>{", ".join(allergens) if allergens else "—"}</b><span>alerjen</span></div><div><b>{it["p"]} ₺</b><span>fiyat</span></div>'
        sizes = '<div class="opt"><div class="lbl">Boy</div><div class="pills"><button class="pill" data-size="-15" aria-pressed="false">Küçük <small>−15 ₺</small></button><button class="pill" data-size="0" aria-pressed="true">Orta</button><button class="pill" data-size="20" aria-pressed="false">Büyük <small>+20 ₺</small></button></div></div>' if drink else ""
        milk = '<div class="opt"><div class="lbl">Süt</div><div class="pills"><button class="pill" data-milk="0" aria-pressed="true">İnek</button><button class="pill" data-milk="10" aria-pressed="false">Laktozsuz <small>+10 ₺</small></button><button class="pill" data-milk="15" aria-pressed="false">Yulaf <small>+15 ₺</small></button><button class="pill" data-milk="15" aria-pressed="false">Badem <small>+15 ₺</small></button></div></div>' if milky else ""
        facts = (f'<div><div class="l">Enerji</div><div class="v">{kcal_s or "—"}</div></div><div><div class="l">Kafein</div><div class="v">{caf_s or ("Kafeinsiz" if "kafeinsiz" in it["tags"] else "—")}</div></div>'
                 f'<div><div class="l">Uygunluk</div><div class="v">{", ".join(diet_b) if diet_b else "Standart"}</div></div><div><div class="l">Alerjen</div><div class="v">{", ".join(allergens) if allergens else ("Süt içerir" if milky else "Belirtilmedi")}</div></div>')
        pair = "".join(pcard(p) for p in pairings(it, c))
        others = "".join(pcard(o) for o in items if o is not it)[:16000]
        page(f"/menu/{sl}/", shell(
          f'''<section class="pdp"><div class="wrap"><div class="crumbs"><a href="/">Ana sayfa</a> › <a href="/menu/">Menü</a> › <a href="/menu/#c-{c}">{CATN[c]}</a> › {it["n"]}</div>
          <div class="pdp-grid"><div class="pdp-media"><div class="big">{big}</div><div class="mini">{mini}</div></div>
          <div class="pdp-info"><div class="eyebrow">{CATN[c]}</div><h1>{it["n"]}</h1><p class="lede">{it["d"]}</p>
          <div class="price"><b id="pdpPrice" data-base="{it["p"]}">{it["p"]} ₺</b><span>İstanbul şubeleri · Anadolu ve Karadağ fiyatı şube sayfasında</span></div>{sizes}{milk}
          <div class="cta"><a class="btn amber" href="/app/">Ön sipariş ver</a><a class="btn ghost" href="/subeler/">En yakın şube</a></div>
          <div class="facts">{facts}</div><p class="howto">{howto(it, c)} <a href="/kahvemiz/">Standartlarımız →</a></p></div></div></div></section>
          <section class="pair"><div class="wrap"><h2>Birlikte iyi gider</h2><p class="sub">{"Bu içeceğin yanına baristalarımızın önerdiği üç lezzet." if drink else "Bu ürünün yanına en çok sipariş edilen üç içecek."}</p><div class="pgrid">{pair}</div></div></section>
          <section class="pair"><div class="wrap"><h2>{CATN[c]} · diğerleri</h2><div class="pgrid">{others}</div><p class="mnote"><a href="/menu/#c-{c}">Tüm {CATN[c].lower()} →</a></p></div></section>''',
          "menu", f"{it['n']} · {it['p']} ₺ · Florida Coffee", f"{it['n']}: {it['d']}. {it['p']} ₺.{' ' + kcal_s + '.' if kcal_s else ''}", f"/menu/{sl}/", ld, "paper"))

# ---------- ŞUBELER ----------
filters = "".join(f'<button class="fbtn" aria-pressed="false" data-f="{k}">{v}</button>' for k,v in [("acik","Şu an açık"),("manzara","Manzara"),("gece","Gece açık"),("calisma","Çalışma alanı"),("otopark","Otopark"),("kahvalti","Kahvaltı")])
page("/subeler/", shell(hero("Bölüm 19:38 · Şubeler","Manzarayı da<br>menüye koyduk.","17 şube, iki ülke. Filtreleyin, o an açık olanları görün; gün batımı saatleri bugüne göre hesaplanır.",[("Şubeler",None)],"sunset") +
  f'<section class="sec"><div class="wrap"><div class="filters" id="filters">{filters}<span class="fcount" id="fcount"></span></div><div class="grid g3" id="branches"></div></div></section>',
  "subeler","Şubeler · Florida Coffee","Florida Coffee şubeleri: İstanbul, Kocaeli, Sakarya, Bursa, Samsun, Rize, Erzincan ve Karadağ. Saatler, özellikler, gün batımı.","/subeler/",
  {"@context":"https://schema.org","@type":"ItemList","itemListElement":[{"@type":"ListItem","position":i+1,"url":f"{SITE}/subeler/{b['id']}/","name":f"Florida Coffee {b['n']}"} for i,b in enumerate(BRANCHES)]}))
for b in BRANCHES:
    tz = "Europe/Podgorica" if "Karadağ" in b["c"] else "Europe/Istanbul"
    near = sorted([x for x in BRANCHES if x is not b], key=lambda x: (x["lat"]-b["lat"])**2+(x["lng"]-b["lng"])**2)[:3]
    ld = {"@context":"https://schema.org","@type":"CafeOrCoffeeShop","name":f"Florida Coffee {b['n']}","address":{"@type":"PostalAddress","addressLocality":b["c"].split("·")[0].strip(),"addressCountry":"ME" if "Karadağ" in b["c"] else "TR"},
          "geo":{"@type":"GeoCoordinates","latitude":b["lat"],"longitude":b["lng"]},"openingHours":f"Mo-Su {hh(b['o'])}-{hh(b['k'])}","servesCuisine":"Coffee","priceRange":"₺₺",
          "amenityFeature":[{"@type":"LocationFeatureSpecification","name":FEAT[f],"value":True} for f in b["f"]],"aggregateRating":{"@type":"AggregateRating","ratingValue":b["r"].replace(",","."),"reviewCount":b["rev"]},"url":f"{SITE}/subeler/{b['id']}/","parentOrganization":{"@type":"Organization","name":"Florida Coffee"}}
    faq = [("Kaça kadar açık?", f"{b['n']} her gün {hh(b['o'])}–{hh(b['k'])} arası hizmet verir. Bayram günlerinde saatler bu sayfada güncellenir."),
           ("Otopark var mı?", "Evet, şubeye ait park alanı mevcut." if "otopark" in b["f"] else "Şubeye ait otopark yok; çevrede ücretli otopark bulunur."),
           ("Laktozsuz süt var mı?", "Evet. Laktozsuz, yulaf ve badem sütü mevcut; tercihinizi uygulamada profilinize kaydedebilirsiniz."),
           ("Çalışmaya uygun mu?", "Evet, priz ve sessiz bölge var." if "calisma" in b["f"] else "Sohbet için ideal; uzun çalışma için Kadıköy veya Bahçeşehir şubemizi öneririz.")]
    ld_faq = {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in faq]}
    has_b = os.path.exists(os.path.join(BASE, "demo-site", "img", "subeler", b["id"] + ".jpg"))
    img = f"subeler/{b['id']}" if has_b else ("sunset" if "manzara" in b["f"] else ("night" if "gece" in b["f"] else "workspace"))
    if has_b: ld["image"] = f"{SITE}/img/subeler/{b['id']}.jpg"
    bphoto = f'<figure class="bphoto"><img src="/img/subeler/{b["id"]}.jpg" alt="Florida Coffee {b["n"]}"></figure>' if has_b else ""
    page(f"/subeler/{b['id']}/", shell(hero(b["c"], f"Florida Coffee {b['n']}", b["note"], [("Şubeler","/subeler/"),(b["n"],None)], img,
        f'<div style="margin-top:1rem;display:flex;gap:.5rem;flex-wrap:wrap;align-items:center"><span class="panel" style="padding:.5rem .8rem;font-size:.88rem" data-branch="{b["id"]}">…</span>' + "".join(f'<span class="chip">{FEAT[f]}</span>' for f in b["f"]) + '</div>') +
      f'''<section class="sec"><div class="wrap two"><div>
        <div class="panel"><div class="lbl" style="margin-bottom:.6rem">Çalışma saatleri</div><div class="hrs">{"".join(f"<span>{d}</span><span>{hh(b['o'])}–{hh(b['k'])}</span>" for d in ["Pazartesi","Salı","Çarşamba","Perşembe","Cuma","Cumartesi","Pazar"])}</div>
        <div style="display:flex;gap:.5rem;flex-wrap:wrap;margin-top:1.1rem"><a class="btn amber" href="/app/">Bu şubeden ön sipariş</a><a class="btn ghost" href="https://www.google.com/maps/search/?api=1&query={b['lat']},{b['lng']}" rel="noopener">Yol tarifi</a></div></div>
        <div class="faq" style="margin-top:1.4rem"><div class="lbl" style="margin-bottom:.4rem">Sık sorulanlar</div>{"".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q,a in faq)}</div></div>
        <div>{bphoto}<div class="lbl" style="margin-bottom:.6rem">Yakın şubeler</div><div class="grid" style="grid-template-columns:1fr">{"".join(f'<a class="cell" href="/subeler/{x["id"]}/"><h3>{x["n"]}</h3><p>{x["c"]} · {hh(x["o"])}–{hh(x["k"])}</p><span class="more">Şube sayfası →</span></a>' for x in near)}</div>
        <p style="margin-top:1.2rem;font-size:.85rem;color:var(--ink-3)">Puan ★ {b["r"]} · {b["rev"]} yorum (örnek). Yorumlar Google ve Yandex'ten otomatik çekilir.</p></div></div></section>''',
      "subeler", f"Florida Coffee {b['n']} · Saatler, Özellikler, Yol Tarifi", f"Florida Coffee {b['n']} ({b['c']}): {hh(b['o'])}–{hh(b['k'])}. {b['note']}", f"/subeler/{b['id']}/", [ld, ld_faq]))

# ---------- v8 ortak yardımcılar ----------
def pht(name, cap="", ratio="r169", sub=""):
    src = f"/img/{sub}{name}.jpg"
    return f'<figure class="pht {ratio}"><img src="{src}" alt="{cap}" loading="lazy" decoding="async">{f"<figcaption>{cap}</figcaption>" if cap else ""}</figure>'
def sh(h2, p=""): return f'<div class="sh"><h2>{h2}</h2>{f"<p>{p}</p>" if p else ""}</div>'
def stats(items): return '<div class="stats">' + "".join(f'<div><b data-count="{n}">{n}</b><span>{l}</span></div>' if str(n).isdigit() else f'<div><b>{n}</b><span>{l}</span></div>' for n, l in items) + '</div>'
def stdtiles(items): return '<div class="stdgrid">' + "".join(f'<button class="std" aria-expanded="false"><span class="v">{v}</span><span class="l">{l}</span><span class="why">{w}</span></button>' for v, l, w in items) + '</div>'
def cells(items, g="g3"): return f'<div class="grid {g}">' + "".join(f'<div class="cell">{("<div class=lbl style=color:var(--amber)>" + lb + "</div>") if lb else ""}<h3>{t}</h3><p>{p}</p>{x}</div>' for lb, t, p, x in items) + '</div>'
def faqhtml(items, idp="faq"): return f'<div class="faq" id="{idp}">' + "".join(f'<details class="fq" data-f="{c}"><summary>{q}</summary><p>{a}</p></details>' for q, a, c in items) + '</div>'
def menu_item(name):
    for c, items in MENU.items():
        for it in items:
            if it["n"] == name: return it
    return None
SHOT_HTML = '''<div class="shot" id="shot"><svg viewBox="0 0 100 100" aria-hidden="true"><circle cx="50" cy="50" r="42" fill="none" stroke="var(--hair)" stroke-width="8"/><circle id="shotArc" cx="50" cy="50" r="42" fill="none" stroke="var(--amber)" stroke-width="8" stroke-dasharray="264" stroke-dashoffset="264" transform="rotate(-90 50 50)"/><text id="shotT" x="50" y="55" text-anchor="middle" font-size="22" font-weight="700" fill="currentColor" font-family="var(--disp)">0.0</text><text x="50" y="70" text-anchor="middle" font-size="9" fill="var(--ink-3)">saniye</text></svg><div><div class="lbl">Shot simülatörü · 4× hız</div><div class="big" id="shotG">0 g</div><p id="shotMsg" style="margin:.2rem 0 .7rem;color:var(--ink-2);font-size:.9rem">Başlatın; 18–23 saniye aralığında kesilmesi gerekir.</p><div style="display:flex;gap:.5rem;flex-wrap:wrap"><button class="btn amber sm" id="shotBtn">Shot'ı başlat</button><button class="btn ghost sm" id="shotStop" disabled>Kes</button></div></div></div>'''
STD6 = [("14 g","Doz","Double shot dozu tartıyla doğrulanır; 1 g sapma shot süresini 2–3 saniye kaydırır."),("90–96 °C","Su","Daha düşük su ekşi ve zayıf, daha yüksek su yanık ve acı çıkarır."),("9 bar","Basınç","Kremanın oluştuğu ve yağların dengeli çözündüğü basınç."),("18–23 sn","Shot süresi","Kronometreyle izlenir. 18'in altı ekşi, 23'ün üstü acı."),("30–60 g","Çıktı","Tartıda ölçülür; oran içeceğe göre 1:2 ile 1:4 arasında."),("60–65 °C","Süt","Mikro köpük parlak ve boya kıvamında; 70 °C üstünde süt yanar, tatlılığını kaybeder.")]

# ---------- KAHVEMİZ ----------
QUIZ_Q = [{"q":"Sabah mı, öğleden sonra mı?","o":["Sabah","Öğleden sonra"]},{"q":"Sütlü mü, sade mi?","o":["Sütlü","Sade"]},{"q":"Sıcak mı, soğuk mu?","o":["Sıcak","Soğuk"]}]
QUIZ_R = {"000":{"n":"Flat White","s":"flat-white","w":"Çift shot, ince süt: sabahı açar, sütü baskın değil."},"001":{"n":"Iced Latte","s":"iced-latte","w":"Espresso soğuk sütle; sabah serinliği."},"010":{"n":"Florida Filtre","s":"florida-filtre","w":"Günün çekirdeği, sade ve uzun içim."},"011":{"n":"Cold Brew","s":"cold-brew","w":"16 saat demleme, asidi düşük, sabah için temiz enerji."},"100":{"n":"Cappuccino","s":"cappuccino","w":"Bol köpük, öğleden sonra molası."},"101":{"n":"Frappe","s":"frappe","w":"Öğleden sonra tatlı ve serin."},"110":{"n":"Cortado","s":"cortado","w":"Kısa ve dengeli; öğleden sonra ağır kaçmaz."},"111":{"n":"Boğaz Cold Brew","s":"bogaz-cold-brew","w":"Tonik ve portakal kabuğu; akşamüstü ferahlığı."},"*":{"n":"Latte","s":"latte","w":"Her saate uyar."}}
page("/kahvemiz/", shell(hero("Bölüm 10:00 · Standart","Aynı fincan,<br>on yedi şubede.","Kavacık'taki latte, Bursa'dakiyle aynı olmak zorunda. Bunu sağlayan iyi niyet değil, ölçülebilir standart. Reçetelerimiz kişisel yoruma açık değildir.",[("Kahvemiz",None)],"barista") +
  f'''<section class="sec"><div class="wrap">{stats([("14","g doz"),("9","bar"),("23","sn üst sınır"),("17","şube, tek reçete")])}
  <div class="split top"><div>{pht("pour","Espresso · 18–23 sn")}<div class="lbl" style="margin:1rem 0 .5rem">Espresso standardımız · tıklayın, nedenini görün</div>{stdtiles(STD6)}</div>
  <div>{pht("latteart","Süt · 60–65 °C mikro köpük")}<div class="lbl" style="margin:1rem 0 .5rem">Deneyin</div>{SHOT_HTML}
  <div class="lbl" style="margin:1.2rem 0 .5rem;display:flex;justify-content:space-between"><span>Shot öncesi zorunlu 5 adım</span><span id="stepProg" style="color:var(--amber)">0 / 5</span></div>
  <ol class="check" data-prog="#stepProg" data-done="Beş adım tamam: shot çekilebilir">{"".join(f"<li><label><input type=checkbox><span><b>{b}</b> — {t}</span></label></li>" for b,t in [("Grup başlığı flush edilir","2–3 saniye su akıtılır, kalıntı temizlenir."),("Portafiltre temizlenir","sepet içi kuru; partikül kalmaz."),("Gramaj tartılır","14 g tartı ile doğrulanır."),("Tamp uygulanır","eşit basınç, düz yüzey."),("Süre takip edilir","kronometre 18–23 sn.")])}</ol></div></div></div></section>
  <section class="sec" style="padding-top:0"><div class="wrap">{sh("Çekirdek nereden geliyor","Kahve kuşağının üç bölgesi, üç karakter. Sekmeye dokunun, tat profili değişsin.")}
  <div class="split top"><div>{pht("beans","Orta kavurma · arabica","r43")}</div><div><div class="tabs" data-tabs="bean"><button class="fbtn" data-tab="latin" aria-pressed="true">Latin Amerika</button><button class="fbtn" data-tab="afrika" aria-pressed="false">Afrika</button><button class="fbtn" data-tab="asya" aria-pressed="false">Asya-Pasifik</button></div>
  <div data-pane="bean:latin"><p><b>Denge.</b> Fındık, badem, kakao, sütlü çikolata, karamel, narenciye. Brezilya, Kolombiya, Guatemala. Espresso için en stabil profil.</p><div class="bars"><div>Asidite<i data-w="55%"></i><b>3</b></div><div>Gövde<i data-w="60%"></i><b>3</b></div><div>Tatlılık<i data-w="80%"></i><b>4</b></div><div>Aroma<i data-w="55%"></i><b>3</b></div></div></div>
  <div data-pane="bean:afrika" hidden><p><b>Aroma ve asidite.</b> Çiçeksi, kırmızı ve tropikal meyveler, çay benzeri yapı. Etiyopya, Kenya, Tanzanya. Filtre ve V60 için.</p><div class="bars"><div>Asidite<i data-w="90%"></i><b>5</b></div><div>Gövde<i data-w="35%"></i><b>2</b></div><div>Tatlılık<i data-w="60%"></i><b>3</b></div><div>Aroma<i data-w="95%"></i><b>5</b></div></div></div>
  <div data-pane="bean:asya" hidden><p><b>Gövde.</b> Topraksı, baharatsı, bitter çikolata, tütün. Endonezya, Vietnam, Hindistan. Sert içim ve sütlü içecekler için.</p><div class="bars"><div>Asidite<i data-w="25%"></i><b>1</b></div><div>Gövde<i data-w="95%"></i><b>5</b></div><div>Tatlılık<i data-w="45%"></i><b>2</b></div><div>Aroma<i data-w="50%"></i><b>3</b></div></div></div>
  <p style="font-size:.9rem;color:var(--ink-3)">Harmanımız: Etiyopya Yirgacheffe %60 + Brezilya Cerrado %40. <a href="/urunler/sonbahar-harmani-250-g/">Eve götürün →</a></p></div></div></div></section>
  <section class="sec" style="padding-top:0"><div class="wrap">{sh("Süt rehberi","Hangi süt hangi içecekte iyi çalışır; köpük kalitesi ve fiyat farkı.")}
  <div class="milk"><div><h3>İnek <small>dahil</small></h3><div class="ratingrow">Köpük <b>★★★★★</b></div><p>Krema ve gövde için ideal; cappuccino ve latte'de tercih edilir.</p></div><div><h3>Laktozsuz <small>+10 ₺</small></h3><div class="ratingrow">Köpük <b>★★★★☆</b></div><p>Tat ve köpük inek sütüne yakın; hafif daha tatlı.</p></div><div><h3>Yulaf <small>+15 ₺</small></h3><div class="ratingrow">Köpük <b>★★★★☆</b></div><p>Barista serisi; flat white ve latte'de en iyi bitkisel seçenek.</p></div><div><h3>Badem <small>+15 ₺</small></h3><div class="ratingrow">Köpük <b>★★★☆☆</b></div><p>Hafif ve fındıksı; buzlu içeceklerde daha iyi.</p></div></div></div></section>
  <section class="sec" style="padding-top:0"><div class="wrap"><div class="split"><div>{sh("Hangi kahve size göre?","Üç soru, bir öneri. Sonuç doğrudan ürün sayfasına gider.")}</div><div class="quiz" id="quiz" data-q='{json.dumps(QUIZ_Q, ensure_ascii=False)}' data-r='{json.dumps(QUIZ_R, ensure_ascii=False)}'></div></div></div></section>''',
  "kahvemiz","Kahvemiz ve Standartlarımız · Florida Coffee","Florida Coffee espresso standardı: 14 g doz, 90–96 °C, 9 bar, 18–23 sn, süt 60–65 °C. Shot simülatörü, kahve kuşağı, süt rehberi ve kahve testi.","/kahvemiz/"))

# ---------- TAZE ----------
def tcard(n):
    sl = slug(n["h"])
    return f'<a class="tcard" data-f="{n["t"]}" href="/taze/{sl}/">{pht(n["img"], "", "r169")}<div class="tb"><div class="meta"><b>{TL[n["t"]]}</b><span>{n["d"]}</span></div><h3>{n["h"]}</h3><p>{n["p"]}</p><div class="nact"><span class="more">Devamı →</span><span><button class="nico save" data-h="{n["h"]}" aria-label="Kaydet">♡</button><button class="nico share" data-h="{n["h"]}" data-url="{SITE}/taze/{sl}/" aria-label="Paylaş">↗</button></span></div></div></a>'
tf = "".join(f'<button class="fbtn" aria-pressed="{"true" if k=="hepsi" else "false"}" data-f="{k}">{v}</button>' for k,v in [("hepsi","Hepsi"),("sube","Şube"),("urun","Ürün"),("kampanya","Kampanya"),("etkinlik","Etkinlik")])
page("/taze/", shell(hero("Bölüm 11:30 · Taze","Yeni ne var,<br>ilk siz duyun.","Yeni şube, sezon ürünü, kampanya ve etkinlikler. Kaydedin, paylaşın; uygulamada bildirim olarak da gelir.",[("Taze",None)],"sakarya") +
  f'''<section class="sec"><div class="wrap"><div class="sbar"><div class="filters" data-filter=".tcard" style="margin:0">{tf}</div><input type="search" data-search=".tcard" data-count="#tcount" placeholder="Haberlerde ara…" aria-label="Haberlerde ara"><span id="tcount" style="font-size:.8rem;color:var(--ink-3)"></span></div>
  <div class="grid g3">{"".join(tcard(n) for n in NEWS)}</div>
  <div class="split" style="margin-top:2.5rem"><div>{sh("Ayda en fazla iki e-posta","Yeni şube ve sezon ürünleri ilk size. İstediğiniz an çıkarsınız.")}</div><form class="f panel"><label>E-posta<input type="email" required placeholder="e-posta adresiniz"></label><label>İlgi alanı<select><option>Hepsi</option><option>Yeni şubeler</option><option>Sezon ürünleri</option><option>Etkinlikler</option></select></label><button class="btn amber" type="submit">Kaydol</button><div class="ok" hidden>Kaydedildi. İlk haber Sakarya açılışı olacak.</div></form></div></div></section>''',
  "taze","Taze · Haberler ve Yenilikler · Florida Coffee","Florida Coffee'den yeni şubeler, sezon ürünleri, kampanyalar ve etkinlikler; fotoğraflı, kaydedilebilir, paylaşılabilir.","/taze/"))
for n in NEWS:
    sl = slug(n["h"]); ld = {"@context":"https://schema.org","@type":"NewsArticle","headline":n["h"],"description":n["p"],"image":f"{SITE}/img/{n['img']}.jpg","publisher":{"@type":"Organization","name":"Florida Coffee"}}
    rel = [o for o in NEWS if o is not n and o["t"] == n["t"]] + [o for o in NEWS if o is not n and o["t"] != n["t"]]
    cta = {"sube":("/subeler/","Şubeyi gör"),"urun":("/menu/","Menüde gör"),"kampanya":("/kulup/","Kulübe katıl"),"etkinlik":("/etkinlikler/","Etkinlikler")}[n["t"]]
    page(f"/taze/{sl}/", shell(hero(f'{TL[n["t"]]} · {n["d"]}', n["h"], n["p"], [("Taze","/taze/"),(n["h"],None)], n["img"]) +
      f'''<section class="sec"><div class="wrap split top"><div class="prose"><p style="font-size:1.05rem">{n["body"]}</p><div style="display:flex;gap:.5rem;flex-wrap:wrap;margin-top:1.2rem"><a class="btn amber" href="{cta[0]}">{cta[1]}</a><button class="btn ghost nico share" data-h="{n["h"]}" data-url="{SITE}/taze/{sl}/" style="width:auto;height:auto;padding:.8rem 1.25rem">Paylaş ↗</button><button class="btn ghost nico save" data-h="{n["h"]}" style="width:auto;height:auto;padding:.8rem 1.25rem">Kaydet</button></div></div>
      <div><div class="lbl" style="margin-bottom:.6rem">İlgili</div><div class="grid" style="grid-template-columns:1fr">{"".join(tcard(o) for o in rel[:3])}</div></div></div></section>''',
      "taze", f"{n['h']} · Florida Coffee", n["p"], f"/taze/{sl}/", ld))

# ---------- ÜRÜNLER ----------
def prodcard(p):
    sl = slug(p["n"]); img = f'<img src="/img/{p["img"]}.jpg" alt="{p["n"]}" loading="lazy">' if p["img"] else f'<span class="pph">{p["n"][0]}</span>'
    return f'<a class="pcard" href="/urunler/{sl}/"><div class="pimg">{img}</div><div class="pbody"><div class="prow"><h3>{p["n"]}</h3><span class="pp">{p["p"]}</span></div><p class="pd">{p["d"]}</p><div class="ptags">{"".join(f"<span class=chip>{t}</span>" for t in p["tags"])}</div></div></a>'
page("/urunler/", shell(hero("Bölüm 17:00 · Ürünler","Aynı çekirdek,<br>sizin mutfağınızda.","Şubede içtiğiniz harman, aynı kavurma tarihiyle. Uygulamadan ön sipariş, şubeden teslim; kargo yakında.",[("Ürünler",None)],"beans") +
  f'''<section class="sec"><div class="wrap"><div class="pgrid">{"".join(prodcard(p) for p in PRODUCTS)}</div>
  <div class="split" style="margin-top:2.5rem"><div>{sh("Evde ne kadar lazım?","Haftalık fincan sayınızı seçin; aylık gramajı, paket sayısını ve abonelik fiyatını hesaplayalım. Abonelikte %10 indirim, kavurma tarihi her pakette.")}</div>
  <div class="calc"><label>Haftada kaç fincan? <b><span id="subCups">10</span> fincan</b><input type="range" id="subWeek" min="3" max="35" step="1" value="10"></label><div class="out"><div><b id="subG">—</b><span>aylık kahve</span></div><div><b id="subBags">—</b><span>250 g paket</span></div><div><b id="subBase">—</b><span>tek seferlik</span></div><div><b id="subSub" style="color:var(--amber)">—</b><span>abonelik · %10</span></div></div><a class="btn amber" href="/app/">Aboneliği uygulamada başlat</a></div></div>
  <p class="mnote" style="color:var(--ink-3)">Fiyatlar örnektir; katalog merkezden yönetilir. 14 g doz üzerinden hesaplanır.</p></div></section>''',
  "urunler","Ürünler · Çekirdek, Set, Termos, Hediye Kartı · Florida Coffee","Florida Coffee ürünleri: Sonbahar Harmanı 250 g, Ev Espresso Seti, Florida Termos, dijital hediye kartı; abonelik hesaplayıcı.","/urunler/"))
BREWTAB = '''<div class="tabs" data-tabs="brew"><button class="fbtn" data-tab="esp" aria-pressed="true">Espresso</button><button class="fbtn" data-tab="v60" aria-pressed="false">V60</button><button class="fbtn" data-tab="fp" aria-pressed="false">French press</button><button class="fbtn" data-tab="cb" aria-pressed="false">Cold brew</button></div>
<div data-pane="brew:esp"><dl class="kv"><dt>Doz</dt><dd>14 g double shot</dd><dt>Öğütüm</dt><dd>İnce</dd><dt>Su</dt><dd>90–96 °C, 9 bar</dd><dt>Süre</dt><dd>18–23 sn · 30–60 g</dd></dl></div>
<div data-pane="brew:v60" hidden><dl class="kv"><dt>Doz</dt><dd>15 g / 250 ml</dd><dt>Öğütüm</dt><dd>Orta-ince, tuz kıvamı</dd><dt>Su</dt><dd>92–96 °C</dd><dt>Süre</dt><dd>2:30–3:00 · 45 sn ön ıslatma</dd></dl></div>
<div data-pane="brew:fp" hidden><dl class="kv"><dt>Doz</dt><dd>30 g / 500 ml</dd><dt>Öğütüm</dt><dd>Kaba</dd><dt>Su</dt><dd>93 °C</dd><dt>Süre</dt><dd>4 dk · üstteki kabuğu kır, bastır</dd></dl></div>
<div data-pane="brew:cb" hidden><dl class="kv"><dt>Doz</dt><dd>60 g / 700 ml</dd><dt>Öğütüm</dt><dd>Kaba</dd><dt>Su</dt><dd>Oda sıcaklığı</dd><dt>Süre</dt><dd>16 saat · süz, 48 saat içinde tüket</dd></dl></div>'''
for p in PRODUCTS:
    sl = slug(p["n"]); ld = {"@context":"https://schema.org","@type":"Product","name":p["n"],"description":p["d"],"brand":{"@type":"Brand","name":"Florida Coffee"},"offers":{"@type":"Offer","priceCurrency":"TRY","price":re.sub(r"[^\d]","",p["p"].split("–")[0]),"availability":"https://schema.org/InStoreOnly"}}
    if p["img"]: ld["image"] = f"{SITE}/img/{p['img']}.jpg"
    base = int(re.sub(r"[^\d]","",p["p"].split("–")[0]))
    big = f'<img src="/img/{p["img"]}.jpg" alt="{p["n"]}">' if p["img"] else f'<span class="pph" style="display:grid;place-items:center;height:100%;font-family:var(--disp);font-size:5rem;color:var(--amber)">{p["n"][0]}</span>'
    is_bean = "Harman" in p["n"]; is_gift = "Hediye" in p["n"]
    opts = ('<div class="opt"><div class="lbl">Öğütüm</div><div class="pills"><button class="pill" data-extra="0" aria-pressed="true">Çekirdek</button><button class="pill" data-extra="0" aria-pressed="false">Espresso</button><button class="pill" data-extra="0" aria-pressed="false">Filtre</button><button class="pill" data-extra="0" aria-pressed="false">French press</button></div></div>'
            '<div class="opt"><div class="lbl">Gramaj</div><div class="pills"><button class="pill" data-mult="1" aria-pressed="true">250 g</button><button class="pill" data-mult="1.9" aria-pressed="false">500 g <small>−5%</small></button><button class="pill" data-mult="3.6" aria-pressed="false">1 kg <small>−10%</small></button></div></div>') if is_bean else (
            '<div class="opt"><div class="lbl">Tutar</div><div class="pills"><button class="pill" data-mult="1" aria-pressed="true">250 ₺</button><button class="pill" data-mult="2" aria-pressed="false">500 ₺</button><button class="pill" data-mult="4" aria-pressed="false">1.000 ₺</button><button class="pill" data-mult="8" aria-pressed="false">2.000 ₺</button></div></div>' if is_gift else "")
    others = "".join(prodcard(o) for o in PRODUCTS if o is not p)
    pair = [menu_item(x) for x in (["Flat White","Florida Filtre","Cold Brew"] if is_bean else ["Latte","San Sebastian","Tereyağlı Kruvasan"])]
    page(f"/urunler/{sl}/", shell(
      f'''<section class="pdp"><div class="wrap"><div class="crumbs"><a href="/">Ana sayfa</a> › <a href="/urunler/">Ürünler</a> › {p["n"]}</div>
      <div class="pdp-grid"><div class="pdp-media"><div class="big">{big}</div><div class="mini"><div><b>{p["tags"][0]}</b><span>etiket</span></div><div><b>Şubeden</b><span>teslim</span></div><div><b>{p["p"]}</b><span>fiyat</span></div></div></div>
      <div class="pdp-info"><div class="eyebrow">Ürün</div><h1>{p["n"]}</h1><p class="lede">{p["d"]}</p><div class="price"><b id="pvPrice" data-base="{base}">{p["p"]}</b><span>uygulamadan ön sipariş · şubeden teslim</span></div>{opts}
      <div class="cta"><a class="btn amber" href="/app/">Ön sipariş ver</a><a class="btn ghost" href="/subeler/">Teslim şubesi seç</a></div>
      <p class="howto" style="margin-top:1.4rem">{p["body"]}</p></div></div></div></section>
      {"<section class='pair'><div class='wrap'>" + sh("Evde nasıl demlenir","Aynı çekirdek dört yöntem; oranlar el kitabından.") + BREWTAB + "</div></section>" if is_bean else ""}
      <section class="pair"><div class="wrap"><h2>Birlikte iyi gider</h2><div class="pgrid">{"".join(pcard(x) for x in pair if x)}</div></div></section>
      <section class="pair"><div class="wrap"><h2>Diğer ürünler</h2><div class="pgrid">{others}</div></div></section>''',
      "urunler", f"{p['n']} · {p['p']} · Florida Coffee", p["d"], f"/urunler/{sl}/", ld, "paper"))

# ---------- KULÜP / UYGULAMA / ETKİNLİKLER ----------
page("/kulup/", shell(hero("Bölüm 21:00 · FloridaDays Club","Sadakat kartınız<br>cüzdanınızda kaybolmasın.","Her harcama 1 ₺ = 1 çekirdek; 10 içecekte biri bizden. Seviye son 6 ayın harcamasıyla belirlenir. Ödeme ve puan tek QR.",[("Kulüp",None)],"cup") +
  f'''<section class="sec"><div class="wrap"><div class="split top"><div>{sh("Sizin için hesaplayalım","Haftada kaç kahve içiyorsunuz? Yıllık çekirdek, hediye içecek ve seviyeniz anında.")}
  <div class="calc"><label>Haftada <b><span id="kcW">5</span> kahve</b><input type="range" id="kcWeek" min="1" max="21" value="5"></label><label>Ortalama fincan <b><span id="kcP">150</span> ₺</b><input type="range" id="kcPrice" min="95" max="220" step="5" value="150"></label>
  <div class="out"><div><b id="kcBeans">—</b><span>yıllık çekirdek</span></div><div><b id="kcFree">—</b><span>hediye içecek</span></div><div><b id="kcSave" style="color:var(--amber)">—</b><span>yıllık kazanç</span></div><div><b id="kcTier">—</b><span>seviyeniz</span></div></div></div></div>
  <div class="tiers"><div class="tier" data-tier="Classic"><div class="tr">0–2.500 ₺ · 6 ay</div><div class="tn">Classic</div><ul><li>Doğum günü içeceği</li><li>Kampanyalara erişim</li><li>Çekirdek biriktirme</li></ul></div><div class="tier" data-tier="Plus"><div class="tr">2.500–7.500 ₺</div><div class="tn">Plus</div><ul><li>Ayda 2 boy yükseltme</li><li>Erken sezon menüsü</li><li>Etkinliklerde öncelik</li></ul></div><div class="tier" data-tier="Premium"><div class="tr">7.500 ₺ +</div><div class="tn">Premium</div><ul><li>Ücretsiz ekstra shot</li><li>Gün batımında manzaralı masa</li><li>Özel cupping</li></ul></div></div></div></div></section>
  <section class="sec" style="padding-top:0"><div class="wrap"><div class="split"><div>{sh("Damga kartından uygulamaya","Karttaki 10 damga uygulamada da 10 damga. Deneyin: damgalara dokunun.")}<div class="stamps" id="stamps">{"".join("<button aria-label='damga'>"+str(i)+"</button>" for i in range(1,11))}</div><p id="stampMsg" style="margin:.8rem 0 0;color:var(--ink-2)">10 damga kaldı</p></div>
  <div>{cells([("1","Kartımı tara","Uygulamada Kart → Kartımı tara; karttaki kodu okutun.",""),("2","Damga ve bakiye geçer","Anında hesabınıza yazılır; kart da çalışmaya devam eder.",""),("3","İlk kahve bizden","Aktarımı tamamlayanlara bir içecek hediye.","")], "g3")}
  <div class="grid g2" style="margin-top:1px"><div class="cell"><h3>Cüzdan</h3><p>Kredi kartı, Multinet, Sodexo, Setcard ile yükleme; 500 ₺ yüklemeye 25 ₺ bonus. Arkadaşınıza kahve veya bakiye gönderin.</p></div><div class="cell"><h3>Tek QR</h3><p>Ödeme ve puan aynı kodla; kasada iki işlem yerine bir tarama.</p></div></div>
  <div style="display:flex;gap:.5rem;flex-wrap:wrap;margin-top:1.4rem"><a class="btn amber" href="/app/">Uygulama demosunu aç</a><a class="btn ghost" href="/uygulama/">Uygulama hakkında</a></div></div></div></div></section>''',
  "kulup","FloridaDays Club · Sadakat Programı · Florida Coffee","Florida Coffee sadakat programı: 1 ₺ = 1 çekirdek, 10 içecekte biri hediye, Classic/Plus/Premium seviyeleri, çekirdek hesaplayıcı, kart aktarımı.","/kulup/"))
page("/uygulama/", shell(hero("Uygulama","Sıra sizi bekletmesin.<br>Kahve sizi beklesin.","Ön sipariş, \"Geldim\", cüzdan, sadakat ve kampanyalar tek uygulamada. iOS ve Android.",[("Uygulama",None)],"workspace") +
  f'''<section class="sec"><div class="wrap">{sh("Nasıl çalışır","Dört adım; kartlar kendiliğinden ilerler, dokununca durur.")}
  <div class="stepper" data-auto><div><div class="n">1</div><h3>Seç</h3><p>Şube, içecek, boy, süt. Süt tercihi profilde kalır.</p></div><div><div class="n">2</div><h3>Öde</h3><p>Cüzdan, kart veya yemek kartı; tek QR ile puan.</p></div><div><div class="n">3</div><h3>Geldim</h3><p>Kapıya 200 m kala ya da tek dokunuşla hazırlık başlar.</p></div><div><div class="n">4</div><h3>Al</h3><p>Tezgâhta kodunuzla teslim; çekirdekler hesaba yazılır.</p></div></div>
  <div class="split" style="margin-top:2.5rem"><div>{pht("workspace","Kadıköy · üst kat","r43")}</div><div>{cells([("","Ön sipariş","Şube ve içecek seçin, ödeyin; hazırlık siz gelince başlar.",""),("","Süt tercihi profilde","Bir kez seçin, barista ekranında etiketli görünür.",""),("","Kampanyalar","Şube, seviye ve saat bazlı; ölü saatlerde otomatik indirim.",""),("","Yer ayırma","Akustik akşamlar ve cupping için tek dokunuş.","")], "g2")}
  <div class="badges" style="margin-top:1.2rem;display:grid;grid-template-columns:1fr 1fr;gap:.5rem"><a class="badge" href="#"><span><small>App Store</small><b>iPhone için indir</b></span></a><a class="badge" href="#"><span><small>Google Play</small><b>Android için indir</b></span></a></div><p style="margin:.8rem 0 0"><a class="btn amber" href="/app/">Tarayıcıda dene</a></p></div></div></div></section>''',
  "kulup","Florida Coffee Uygulaması · Ön Sipariş ve Sadakat","Florida Coffee mobil uygulaması: ön sipariş, Geldim, cüzdan, FloridaDays Club; dört adımda nasıl çalışır.","/uygulama/",
  {"@context":"https://schema.org","@type":"MobileApplication","name":"Florida Coffee","operatingSystem":"iOS, Android","applicationCategory":"FoodApplication","offers":{"@type":"Offer","price":"0","priceCurrency":"TRY"}}))
EVENTS = [dict(d="4", dn="Per", t="21:00", h="Akustik set", loc="Kavacık terası", b="kavacik", p="İki kişilik akustik, gün batımından sonra. Plus ve Premium öncelikli."),
          dict(d="6", dn="Cmt", t="11:00", h="Cupping", loc="Çengelköy", b="cengelkoy", p="Sezon harmanını birlikte tadıyoruz. 12 kişilik, ücretsiz; ayın ilk Cumartesi'si."),
          dict(d="0,1,2,3,4,5,6", dn="Her gün", t="22:00", h="Gece filtresi", loc="Kavacık · Beykoz · Taksim", b="beykoz", p="22:00 sonrası kafeinsiz seçenekle aynı fiyat."),
          dict(d="0", dn="Paz", t="09:00", h="Kahvaltı sofrası", loc="Beykoz · Bahçeşehir · Samsun", b="samsun", p="Hafta sonu 09:00–13:00 iki kişilik kahvaltı; masa uygulamadan."),
          dict(d="3", dn="Çar", t="19:00", h="Latte art atölyesi", loc="Kadıköy", b="kadikoy", p="8 kişilik, 90 dakika; süt dokusu ve rosetta. Uygulamadan kayıt.")]
DAYS = [("1","Pzt"),("2","Sal"),("3","Çar"),("4","Per"),("5","Cum"),("6","Cmt"),("0","Paz")]
evcards = "".join(f'<div class="tcard" data-day="{e["d"]}">{pht(e["b"], "", "r169", "subeler/")}<div class="tb"><div class="meta"><b>{e["dn"]} · {e["t"]}</b><span>{e["loc"]}</span></div><h3>{e["h"]}</h3><p>{e["p"]}</p><div class="nact" style="gap:.4rem;flex-wrap:wrap"><button class="btn amber sm" data-reserve>Yer ayır</button><button class="btn ghost sm" data-ics="{e["h"]} · Florida Coffee" data-dow="{e["d"].split(",")[0]}" data-time="{e["t"]}" data-loc="{e["loc"]}">Takvime ekle</button></div></div></div>' for e in EVENTS)
page("/etkinlikler/", shell(hero("Bölüm 23:30 · Etkinlikler","Şehir susunca<br>Boğaz konuşur.","Akustik akşamlar, cupping, atölyeler ve gece filtresi. Güne dokunun, o günün programı kalsın.",[("Etkinlikler",None)],"night") +
  f'''<section class="sec"><div class="wrap"><div class="evday" id="evday">{"".join(f"<button data-d='{d}' class='{'has' if any(d in e['d'].split(',') for e in EVENTS) else ''}'><b>{n}</b>{'●' if any(d in e['d'].split(',') for e in EVENTS) else ' '}</button>" for d,n in DAYS)}</div>
  <div class="grid g3">{evcards}</div><p class="mnote" style="color:var(--ink-3)">Yer ayırma ve hatırlatma uygulamada; takvim dosyası telefonunuza iner.</p></div></section>''',
  "gece","Etkinlikler · Florida Coffee","Florida Coffee etkinlikleri: akustik akşamlar, cupping, latte art atölyesi, gece filtresi; güne göre program ve takvime ekleme.","/etkinlikler/",
  {"@context":"https://schema.org","@type":"Event","name":"Akustik akşamlar · Kavacık terası","eventSchedule":{"@type":"Schedule","byDay":"https://schema.org/Thursday","startTime":"21:00"},"location":{"@type":"Place","name":"Florida Coffee Kavacık"}}))

# ---------- FRANCHISE ----------
ffaq = [("Yatırım ne kadar?","Konuma ve metrekareye göre değişir; büyükşehir caddesinde 100–120 m² için örnek hesap 3,5–4,5 M ₺ bandında. Kesin rakam keşif görüşmesinde."),("Royalty ve reklam payı?","Aylık ciro üzerinden %5 + KDV royalty; ulusal reklam bütçesi en fazla %1. Her ikisi sözleşmede yazılıdır."),("Bölge koruması var mı?","Evet, 3 km. Sözleşme süresince aynı bölgede ikinci Florida açılmaz."),("Eğitim nasıl?","Toplam 45 gün: 30 gün işletme yönetimi, 15 gün barista. Açılışta merkez ekibi şubede."),("Tedarik nasıl işler?","Çekirdek, ambalaj ve ekipman merkezden; 40 gün vade. FIFO zorunlu."),("Dijital altyapı dahil mi?","Evet: şube sayfası, uygulamada yer, sadakat programı, raporlama paneli, ciro bildirimi otomasyonu."),("Sözleşme süresi?","10 yıl."),("Deneyim şart mı?","Şart değil; işletme deneyimi başvuru puanını yükseltir. Eğitim programı sıfırdan başlayanlar için tasarlanmıştır.")]
calc = '''<div class="calc"><label for="fCity">Konum tipi<select id="fCity" style="background:rgba(9,14,19,.6);border:1px solid var(--hair-2);color:var(--ink);padding:.6rem;font:inherit"><option value="1.15">İstanbul cadde</option><option value="1" selected>Büyükşehir cadde (Bursa, Sakarya, Samsun)</option><option value="0.85">Anadolu şehir merkezi</option><option value="1.1">Karadağ sahil</option></select></label>
<label for="fM2">Mağaza alanı <b><span id="fM2v">110</span> m²</b><input type="range" id="fM2" min="60" max="220" step="5" value="110"></label>
<label for="fRev">Tahmini aylık ciro <b><span id="fRevv">1.400.000</span> ₺</b><input type="range" id="fRev" min="500000" max="4000000" step="50000" value="1400000"></label>
<div class="out"><div><b id="oInv">—</b><span>Kuruluş yatırımı</span></div><div><b id="oRoy">—</b><span>Aylık royalty · %5 + KDV</span></div><div><b id="oAd">—</b><span>Ulusal reklam · ≤ %1</span></div><div><b id="oPb" style="color:var(--amber)">—</b><span>Örnek geri dönüş</span></div></div>
<p style="font-size:.78rem;color:var(--ink-3);margin:0">Örnek hesaplamadır, teklif değildir. Giriş bedeli ve platform lisansı merkez tarafından belirlenir.</p></div>'''
REGIONS = [("Eskişehir","open"),("Ankara Çayyolu","open"),("İzmir Alsancak","open"),("Antalya Lara","open"),("Trabzon","open"),("Konya","open"),("Kavacık","full"),("Kadıköy","full"),("Bursa Nilüfer","full"),("Saraybosna","open"),("Tiran","open")]
page("/franchise/", shell(hero("Bölüm 02:00 · Franchise","Bu günü kendi<br>şehrinizde kurun.","3 km bölge koruması, 45 gün eğitim, merkezi tedarik ve dijital altyapının tamamı. Hesaplayıcı örnek bir yatırım tablosu çıkarır.",[("Franchise",None)],"franchise") +
  f'''<section class="sec"><div class="wrap">{stats([("17","şube"),("2","ülke"),("45","gün eğitim"),("3","km bölge koruması")])}
  <div class="split top"><div>{sh("Örnek yatırım tablosu","Konum, metrekare ve ciro; gerisi otomatik.")}{calc}</div>
  <div>{sh("Sizin için ne yapıyoruz","Dört başlık, dokunup nedenini görün.")}{stdtiles([("3 km","Bölge koruması","Sözleşme süresince aynı bölgede ikinci Florida açılmaz."),("45 gün","Eğitim","30 gün işletme yönetimi, 15 gün barista; açılışta merkez ekibi şubede."),("1","Tedarik kaynağı","Çekirdek, ambalaj ve ekipman tek kaynaktan; 40 gün vade."),("%5","Royalty + KDV","Ciro üzerinden; ulusal reklam en fazla %1. Şeffaf, sözleşmede."),("Dahil","Dijital altyapı","Şube sayfanız, uygulamada yeriniz, sadakat, HQ raporlama paneli."),("24 sa","İlk arama","Ön başvurudan sonra franchise ekibi bir gün içinde arar.")])}
  <div class="lbl" style="margin:1.4rem 0 .5rem">Bölgeler · <span style="color:var(--ok)">açık</span> / dolu</div><div class="regions">{"".join(f'<span class="chip {st}">{c}</span>' for c,st in REGIONS)}</div>
  <div class="calc" style="margin-top:1.2rem"><label>3 km kontrolü · şehir ya da ilçe yazın<input type="text" id="regionCheck" placeholder="ör. Eskişehir, Kadıköy" style="background:rgba(9,14,19,.6);border:1px solid var(--hair-2);color:var(--ink);padding:.6rem;font:inherit;letter-spacing:0;text-transform:none;font-weight:400"></label><div id="regionOut" style="font-size:.9rem;min-height:1.4em"></div></div></div></div></div></section>
  <section class="sec" style="padding-top:0"><div class="wrap">{sh("Süreç","Ön başvurudan açılışa altı adım.")}<div class="timeline">{"".join(f"<div><h3>{t}</h3><p>{p}</p></div>" for t,p in [("Ön başvuru","Form ya da Flo; 24 saat içinde arama."),("Keşif görüşmesi","Bölge, bütçe, lokasyon."),("3 km kontrolü","Çakışma yoksa lokasyon onayı."),("Sözleşme","10 yıl; royalty, reklam, tedarik şartları yazılı."),("45 gün eğitim","30 gün işletme, 15 gün barista."),("Açılış","Merkez ekibi ilk hafta şubede; dijital altyapı gün 1'de canlı.")])}</div>
  <div class="split" style="margin-top:2.5rem"><div>{pht("franchise","Yeni şube · açılış haftası")}</div><div><p class="quote">Her yeni franchise, platformun bir müşterisi. Her şube açılışı merkez için gelir.</p><div style="display:flex;gap:.5rem;flex-wrap:wrap"><a class="btn amber" href="/franchise/basvuru/">Başvuru formu</a><a class="btn ghost" href="/franchise/sss/">Franchise SSS</a></div></div></div></div></section>''',
  "franchise","Franchise · Florida Coffee","Florida Coffee franchise: 3 km bölge koruması, 45 gün eğitim, merkezi tedarik, royalty %5. Yatırım hesaplayıcı, bölge kontrolü, süreç ve başvuru.","/franchise/"))
page("/franchise/basvuru/", shell(hero("Franchise · Başvuru","Ön başvuru.<br>Üç kısa adım.","Formu doldurun; franchise ekibimiz 24 saat içinde arar. Flo ile sohbet ederek de bırakabilirsiniz.",[("Franchise","/franchise/"),("Başvuru",None)]) +
  f'''<section class="sec"><div class="wrap split top"><form class="f panel" data-steps><div class="fsteps"><i class="on"></i><i></i><i></i></div>
  <div data-step="1"><label>Ad Soyad<input required></label><label>Telefon<input type="tel" required placeholder="05xx xxx xx xx"></label><label>E-posta<input type="email" required></label><button type="button" class="btn amber" data-next>Devam</button></div>
  <div data-step="2" hidden><label>Hedef şehir / ilçe<input required></label><label>Bütçe<select><option>2 M ₺ altı</option><option>2–4 M ₺</option><option>4 M ₺ üstü</option></select></label><label>Lokasyon durumu<select><option>Henüz yok</option><option>Bakıyorum</option><option>Kiralık dükkânım var</option></select></label><div style="display:flex;gap:.5rem"><button type="button" class="btn ghost" data-prev>Geri</button><button type="button" class="btn amber" data-next>Devam</button></div></div>
  <div data-step="3" hidden><label>Kafe / restoran deneyimi<select><option>Yok</option><option>1–3 yıl</option><option>3 yıl üstü</option></select></label><label>Not<textarea rows="3" placeholder="İsteğe bağlı"></textarea></label><label style="display:flex;gap:.5rem;align-items:center;text-transform:none;letter-spacing:0"><input type="checkbox" required style="width:auto"> KVKK aydınlatma metnini okudum.</label><div style="display:flex;gap:.5rem"><button type="button" class="btn ghost" data-prev>Geri</button><button class="btn amber" type="submit">Başvuruyu gönder</button></div><div class="ok" hidden>Alındı. 24 saat içinde arayacağız.</div></div></form>
  <div>{cells([("1","24 saat","Ön başvurunuz ekibe düşer, bir iş günü içinde ararız.",""),("2","Keşif","Bölge, bütçe ve lokasyonu birlikte netleştiririz.",""),("3","Onay","3 km çakışma kontrolü ve lokasyon onayı.",""),("4","Açılış","Sözleşme, 45 gün eğitim, açılış haftası merkez ekibi şubede.","")], "g2")}<p style="margin-top:1rem;font-size:.9rem;color:var(--ink-3)">Formu doldurmak yerine <button class="btn ghost sm" data-ask-flo>Flo'ya anlatın</button></p></div></div></section>''',
  "franchise","Franchise Başvurusu · Florida Coffee","Florida Coffee franchise ön başvuru formu; üç adım, 24 saat içinde dönüş.","/franchise/basvuru/"))
page("/franchise/sss/", shell(hero("Franchise · SSS","Sık sorulan<br>franchise soruları.","Kısa ve net. Daha fazlası için başvuru sonrası keşif görüşmesi.",[("Franchise","/franchise/"),("SSS",None)]) +
  f'''<section class="sec"><div class="wrap"><div class="sbar"><input type="search" data-search="#ffaq details" data-count="#ffc" placeholder="Soru ara: royalty, eğitim, bölge…" aria-label="Ara"><span id="ffc" style="font-size:.8rem;color:var(--ink-3)"></span></div>{faqhtml([(q,a,"f") for q,a in ffaq], "ffaq")}<div style="margin-top:1.4rem;display:flex;gap:.5rem;flex-wrap:wrap"><a class="btn amber" href="/franchise/basvuru/">Başvuru formu</a><button class="btn ghost" data-ask-flo>Flo'ya sor</button></div></div></section>''',
  "franchise","Franchise SSS · Florida Coffee","Florida Coffee franchise sık sorulan sorular: yatırım, royalty, bölge koruması, eğitim, tedarik.","/franchise/sss/",
  {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in ffaq]}))

# ---------- HİKÂYE / KURUMSAL / KARİYER / SSS / İLETİŞİM ----------
STORY = [("cengelkoy","Çengelköy","İlk şube. Boğaz'ın sabah ışığını en iyi gören sokaklardan birinde; cupping akşamları hâlâ burada."),("kavacik","Boğaz hattı","Kavacık ve Beykoz: gün batımına bakan teraslar, geceye kadar açık."),("kadikoy","Şehrin içi","Kadıköy, Taksim, Ümraniye, Bahçeşehir, Esenyurt: çalışma katları ve hızlı servis."),("sakarya","Anadolu","İzmit, Sakarya, Bursa, Samsun, Rize, Erzincan: her şehirde aynı fincan."),("budva","Karadağ","Podgorica ve Budva: Adriyatik'te ilk Türk kahve zinciri.")]
page("/hikayemiz/", shell(hero("Hikâyemiz","Çengelköy'de bir sabah<br>başladı.","Boğaz'a bakan bir köşede, aynı fincanı her gün aynı standartla verme sözüyle. Bugün 17 nokta, iki ülke; söz aynı.",[("Hikâyemiz",None)],"hero") +
  f'''<section class="sec"><div class="wrap">{stats([("17","şube"),("2","ülke"),("53","menü ürünü"),("45","gün eğitim")])}
  {sh("Beş durak","Çengelköy'den Adriyatik'e; her durakta bir fotoğraf, bir cümle.")}<div class="timeline">{"".join(f"<div>{pht(b, '', 'r169', 'subeler/')}<h3>{t}</h3><p>{p}</p></div>" for b,t,p in STORY)}</div>
  <div class="split" style="margin-top:2.5rem"><div><p class="quote">Kahveyi bir ürün olarak değil, günün ritmi olarak düşündük.</p><p style="color:var(--ink-2)">Şafakta ilk filtre, öğle arasında hızlı bir espresso, gün batımında terasta bir cold brew, gece yarısı kafeinsiz. Sayfamızın "Boğaz'da Bir Gün" diye kurulmasının nedeni bu.</p></div>
  <div>{cells([("","Standart","Tartılan gramaj, kronometreyle izlenen shot; reçete yoruma açık değil.",""),("","Yerlilik","İstanbul doğumlu; Boğaz manzarası menünün parçası.",""),("","Erişim","Sadakat, ön sipariş ve şube bilgisi tek uygulamada.",""),("","Büyüme","Her yeni franchise aynı fincanı kendi şehrine taşır.","")], "g2")}</div></div></div></section>''',
  "safak","Hikâyemiz · Florida Coffee","Florida Coffee'nin hikâyesi: Çengelköy'den 17 şubeye, İstanbul'dan Karadağ'a; her fincanda aynı standart.","/hikayemiz/",
  {"@context":"https://schema.org","@type":"Organization","name":"Florida Coffee","alternateName":["Florida Coffee Türkiye","Florida Coffee Co."],"url":SITE,"logo":f"{SITE}/img/brand/logo.png","address":{"@type":"PostalAddress","streetAddress":"Çengelköy Mah. Görgeç Sok. No:6","addressLocality":"Üsküdar","addressRegion":"İstanbul","addressCountry":"TR"},"sameAs":["https://www.instagram.com/floridacoffeetr/","https://www.facebook.com/floridacoffeetr/"]}))
page("/kurumsal/", shell(hero("Kurumsal","Toplantınıza kahve,<br>etkinliğinize bar.","Ofis ikramı, etkinlik kahve barı, toplu hediye kartı. Talebinizi bırakın; 1 iş günü içinde dönüş.",[("Kurumsal",None)],"pour") +
  f'''<section class="sec"><div class="wrap"><div class="grid g3"><div class="cell">{pht("beans","","r169")}<h3>Ofis ikramı</h3><p>Haftalık çekirdek ve filtre teslimi; barista eğitimi opsiyonu; makine kurulumu.</p></div><div class="cell">{pht("pour","","r169")}<h3>Etkinlik kahve barı</h3><p>Mobil espresso barı, 2 barista, 4 saat; 100–400 kişilik etkinlikler.</p></div><div class="cell">{pht("cup","","r169")}<h3>Toplu hediye kartı</h3><p>Ekibinize dijital kart; tutar ve mesaj kurumsal panelden.</p></div></div>
  <div class="split top" style="margin-top:2.5rem"><div>{sh("Etkinlik barı için örnek bütçe","Kişi sayısı ve süre; gerisi otomatik.")}<div class="calc"><label>Kişi <b><span id="cpP">150</span></b><input type="range" id="cpPeople" min="30" max="600" step="10" value="150"></label><label>Süre <b><span id="cpH">4</span> saat</b><input type="range" id="cpHours" min="2" max="10" value="4"></label><div class="out"><div><b id="cpCups">—</b><span>tahmini fincan</span></div><div><b id="cpBar">—</b><span>kurulum</span></div><div><b id="cpCost" style="color:var(--amber)">—</b><span>örnek bütçe</span></div></div></div></div>
  <form class="f panel"><label>Kurum<input required></label><label>Ad Soyad<input required></label><label>E-posta<input type="email" required></label><label>İhtiyaç<select><option>Ofis ikramı</option><option>Etkinlik kahve barı</option><option>Toplu hediye kartı</option><option>Diğer</option></select></label><label>Not<textarea rows="3"></textarea></label><button class="btn amber" type="submit">Talep bırak</button><div class="ok" hidden>Alındı. 1 iş günü içinde dönüş yapacağız.</div></form></div></div></section>''',
  "kulup","Kurumsal Satış · Florida Coffee","Florida Coffee kurumsal: ofis ikramı, etkinlik kahve barı, toplu hediye kartı; örnek bütçe hesaplayıcı.","/kurumsal/"))
jobs = "".join(f'<div class="cell" data-f="{j["loc"].split(" ")[0].lower()}"><div class="lbl">{j["loc"]} · {j["type"]}</div><h3>{j["t"]}</h3><p>{j["d"]}</p><button class="btn amber sm" data-apply="{j["t"]}" style="align-self:flex-start">Başvur</button></div>' for j in JOBS)
page("/kariyer/", shell(hero("Kariyer","Barista standardı üretir.<br>Siz de üretin.","Her barista hazırladığı her fincanla markayı temsil eder. Deneyim şart değil; 45 günlük eğitimimiz var.",[("Kariyer",None)],"barista") +
  f'''<section class="sec"><div class="wrap">{sh("Açık pozisyonlar","Şehre göre süzün; Başvur'a dokunun, form pozisyonla dolsun.")}<div class="filters" data-filter="#jobs .cell" style="margin:0 0 1rem"><button class="fbtn" data-f="hepsi" aria-pressed="true">Hepsi</button><button class="fbtn" data-f="i̇stanbul" aria-pressed="false">İstanbul</button><button class="fbtn" data-f="sakarya" aria-pressed="false">Sakarya</button></div><div class="grid g3" id="jobs">{jobs}</div>
  {sh("Barista yolculuğu","İlk günden şube müdürlüğüne.")}<div class="stepper" data-auto><div><div class="n">1</div><h3>15 gün eğitim</h3><p>Ekstraksiyon, süt dokusu, latte art, hijyen.</p></div><div><div class="n">2</div><h3>Sertifika</h3><p>Standart testi: 14 g, 18–23 sn, 60–65 °C.</p></div><div><div class="n">3</div><h3>Şube</h3><p>Front bar / back bar; haftalık kalibrasyon.</p></div><div><div class="n">4</div><h3>Vardiya lideri</h3><p>Denetim ve gizli müşteri puanına göre.</p></div><div><div class="n">5</div><h3>Şube müdürü</h3><p>30 gün işletme eğitimi; yeni açılışlarda görev.</p></div></div>
  <div class="split top" style="margin-top:2.5rem" id="basvur"><form class="f panel"><label>Ad Soyad<input required></label><label>Telefon<input type="tel" required></label><label>E-posta<input type="email" required></label><label>Pozisyon<select id="jobPos">{"".join(f"<option>{j['t']}</option>" for j in JOBS)}</select></label><label>Şehir<select><option>İstanbul</option><option>Sakarya</option><option>Diğer</option></select></label><label>Not<textarea rows="3" placeholder="Deneyim, uygun günler"></textarea></label><button class="btn amber" type="submit">Başvur</button><div class="ok" hidden>Başvurunuz alındı. 3 iş günü içinde dönüş.</div></form>
  <div>{cells([("","Nasıl çalışıyoruz","FIFO zorunlu; front bar / back bar net görev ayrımı; haftalık kalibrasyon, aylık kalite denetimi.",""),("","Yan haklar","Vardiya yemeği, günlük kahve, sağlık sigortası, şubeler arası transfer.",""),("","Gelişim","Kalite ve eğitim ekibine geçiş; yeni şube açılışlarında görev.","")], "g3")}</div></div></div></section>''',
  "kahvemiz","Kariyer · Florida Coffee","Florida Coffee'de barista, şube müdürü ve kalite uzmanı pozisyonları; barista yolculuğu ve başvuru.","/kariyer/",
  [{"@context":"https://schema.org","@type":"JobPosting","title":j["t"],"description":j["d"],"datePosted":TODAY,"employmentType":"FULL_TIME","hiringOrganization":{"@type":"Organization","name":"Florida Coffee"},"jobLocation":{"@type":"Place","address":{"@type":"PostalAddress","addressLocality":j["loc"].split("·")[0].strip(),"addressCountry":"TR"}}} for j in JOBS]))
FAQC = {"Ön sipariş":"siparis","Laktozsuz":"menu","FloridaDays":"kulup","Fiziksel":"kulup","Her şubede":"menu","Hangi şubeler":"sube","Franchise":"franchise","Evcil":"sube","Kurumsal":"kurumsal","Kargo":"urun"}
faqc = [(q,a,next((v for k,v in FAQC.items() if q.startswith(k)), "genel")) for q,a in FAQ]
page("/sss/", shell(hero("SSS","Sık sorulanlar.","Ön sipariş, süt seçenekleri, sadakat, şubeler, franchise. Arayın ya da Flo'ya sorun.",[("SSS",None)]) +
  f'''<section class="sec"><div class="wrap"><div class="sbar"><input type="search" data-search="#faq details" data-count="#fc" placeholder="Soru ara: süt, kart, saat…" aria-label="Ara"><span id="fc" style="font-size:.8rem;color:var(--ink-3)"></span></div>
  <div class="filters" data-filter="#faq details" style="margin:0 0 1rem"><button class="fbtn" data-f="hepsi" aria-pressed="true">Hepsi</button><button class="fbtn" data-f="siparis" aria-pressed="false">Sipariş</button><button class="fbtn" data-f="menu" aria-pressed="false">Menü</button><button class="fbtn" data-f="kulup" aria-pressed="false">Kulüp</button><button class="fbtn" data-f="sube" aria-pressed="false">Şubeler</button><button class="fbtn" data-f="franchise" aria-pressed="false">Franchise</button></div>
  {faqhtml(faqc)}<div class="panel" style="margin-top:1.6rem;display:flex;gap:1rem;align-items:center;flex-wrap:wrap;justify-content:space-between"><div><h3>Cevabı bulamadınız mı?</h3><p style="margin:.2rem 0 0;color:var(--ink-2)">Flo menüyü, şubeleri ve kulüp kurallarını bilir; franchise sorularını da alır.</p></div><button class="btn amber" data-ask-flo>Flo'ya sor</button></div></div></section>''',
  "safak","Sık Sorulan Sorular · Florida Coffee","Florida Coffee SSS: ön sipariş, süt seçenekleri, FloridaDays Club, şube saatleri, franchise; arama ve kategori.","/sss/",
  {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in FAQ]}))
CITIES = ["İstanbul","Kocaeli","Adapazarı","Bursa","Atakum","Rize","Erzincan","Karadağ"]
page("/iletisim/", shell(hero("İletişim","Yazın, arayın,<br>ya da gelin.","Merkez Çengelköy'de. Şube telefonları şube sayfalarında. Franchise ve kurumsal için ilgili formlar.",[("İletişim",None)],"subeler/cengelkoy" if os.path.exists(os.path.join(BASE,"demo-site","img","subeler","cengelkoy.jpg")) else "hero") +
  f'''<section class="sec"><div class="wrap"><div class="contact"><a href="https://www.google.com/maps/search/?api=1&query=Çengelköy+Görgeç+Sokak+6" rel="noopener"><span class="l">Merkez</span><b>Çengelköy</b><span>Görgeç Sok. No:6, Üsküdar / İstanbul · yol tarifi →</span></a><a href="tel:+902160000000"><span class="l">Telefon</span><b>+90 216 000 00 00</b><span>Hafta içi 09:00–18:00</span></a><a href="mailto:merhaba@floridacoffee.com.tr"><span class="l">E-posta</span><b>merhaba@floridacoffee.com.tr</b><span>1 iş günü içinde yanıt</span></a><a href="https://wa.me/905000000000" rel="noopener"><span class="l">WhatsApp</span><b>Flo ile yazışın</b><span>Sipariş, şube, franchise</span></a></div>
  <div class="split top" style="margin-top:2.5rem"><div>{sh("Şubeye ulaşın","Şehri seçin; saatler ve şube sayfası.")}<label class="lbl" for="citySel">Şehir</label><select id="citySel" style="width:100%;margin:.4rem 0 1rem;background:rgba(9,14,19,.6);border:1px solid var(--hair-2);color:var(--ink);padding:.6rem;font:inherit">{"".join(f"<option>{c}</option>" for c in CITIES)}</select><div class="grid" style="grid-template-columns:1fr" id="cityOut"></div></div>
  <form class="f panel"><label>Ad Soyad<input required></label><label>E-posta<input type="email" required></label><label>Konu<select><option>Genel</option><option>Şube geri bildirimi</option><option>Uygulama</option><option>Basın</option><option>Franchise</option><option>Kurumsal</option></select></label><label>Mesaj<textarea rows="4" required></textarea></label><button class="btn amber" type="submit">Gönder</button><div class="ok" hidden>Mesajınız alındı. 1 iş günü içinde yanıtlayacağız.</div></form></div></div></section>''',
  "safak","İletişim · Florida Coffee","Florida Coffee iletişim: merkez adresi, telefon, e-posta, WhatsApp, şehre göre şube bulucu, form.","/iletisim/"))

# ---------- YASAL ----------
LEGAL = {
 "kvkk": ("KVKK Aydınlatma Metni", ["<h2>Veri sorumlusu</h2><p>Florida Coffee Kahve Gıda San. ve Tic. A.Ş., Çengelköy Mah. Görgeç Sok. No:6, Üsküdar / İstanbul.</p>","<h2>İşlenen veriler ve amaçlar</h2><ul><li>Uygulama üyeliği: ad, telefon, e-posta, doğum tarihi (isteğe bağlı) — hesap oluşturma, sadakat programı</li><li>Sipariş ve ödeme verileri — siparişin yerine getirilmesi, muhasebe</li><li>Konum (izinle) — en yakın şube, \"Geldim\" tetikleme</li><li>Süt ve alerjen tercihleri — sipariş doğruluğu</li><li>Franchise başvuru bilgileri — değerlendirme ve iletişim</li></ul>","<h2>Hukuki sebepler</h2><p>Sözleşmenin kurulması ve ifası, meşru menfaat, açık rıza (pazarlama izni, kişiselleştirme).</p>","<h2>Aktarım</h2><p>Ödeme kuruluşları, SMS/e-posta altyapısı, bulut barındırma (Türkiye veri lokasyonu tercih edilir). Yurt dışına aktarımda KVKK m.9 şartları uygulanır.</p>","<h2>Haklarınız</h2><p>KVKK m.11 kapsamında bilgi talep etme, düzeltme, silme, itiraz. Uygulamada Profil → Hesabımı sil ile 30 gün içinde anonimleştirme; mali kayıtlar mevzuat süresince saklanır.</p>"]),
 "cerez": ("Çerez Politikası", ["<h2>Kullanılan çerezler</h2><ul><li>Zorunlu: oturum, güvenlik, dil</li><li>Tercih: son seçilen şube ve filtreler (localStorage)</li><li>Analitik: anonimleştirilmiş kullanım istatistikleri (rıza ile)</li><li>Pazarlama: kampanya ölçümü (rıza ile)</li></ul>","<h2>Yönetim</h2><p>Tarayıcı ayarlarından çerezleri silebilir ve engelleyebilirsiniz. Zorunlu çerezler dışındakiler için açık rıza alınır; rıza her zaman geri alınabilir.</p>"]),
 "kullanici-sozlesmesi": ("Kullanıcı Sözleşmesi", ["<h2>Konu</h2><p>Bu sözleşme Florida Coffee web sitesi ve mobil uygulamasının kullanım şartlarını düzenler.</p>","<h2>Üyelik ve sadakat</h2><p>FloridaDays Club puanları nakde çevrilemez, 12 ay geçerlidir, devredilemez. Seviye son 6 aylık harcamayla belirlenir.</p>","<h2>Ön sipariş</h2><p>Ödeme anında sipariş kesinleşir. Şube kaynaklı iptallerde bedel cüzdana iade edilir. Teslim alınmayan siparişler 15 dakika hatırlatma sonrası sonlandırılır.</p>","<h2>Cüzdan</h2><p>Bakiye yalnızca Florida Coffee şubelerinde ve uygulamada kullanılır; bonus bakiyeler iade kapsamı dışındadır.</p>"]),
 "mesafeli-satis": ("Mesafeli Satış Sözleşmesi", ["<h2>Taraflar</h2><p>Satıcı: Florida Coffee Kahve Gıda San. ve Tic. A.Ş. Alıcı: uygulama üzerinden sipariş veren kullanıcı.</p>","<h2>Konu</h2><p>Uygulama üzerinden ön sipariş edilen içecek, yiyecek ve ürünlerin satışı; şubeden teslim.</p>","<h2>Cayma hakkı</h2><p>Kişiye özel hazırlanan ve çabuk bozulan gıda ürünlerinde cayma hakkı kullanılamaz. Paketli ürünlerde (çekirdek, termos, set) teslimden itibaren 14 gün içinde ambalajı açılmamış ürünler için cayma hakkı vardır.</p>","<h2>Uyuşmazlık</h2><p>Tüketici hakem heyetleri ve tüketici mahkemeleri yetkilidir.</p>"]),
}
for k,(t,secs) in LEGAL.items():
    page(f"/yasal/{k}/", shell(hero("Yasal", t, "Bu metin demo amaçlı taslaktır.", [("Yasal",None),(t,None)]) +
      f'<section class="sec"><div class="wrap split top" style="grid-template-columns:minmax(0,1fr) 16rem"><div class="prose"><div class="notice">Taslak — yayın öncesi hukuk müşaviri onayı gerekir. Şirket bilgileri sözleşme özetinden alınmıştır.</div>{"".join(x.replace("<h2>", f"<h2 id=s{i}>", 1) for i,x in enumerate(secs))}<p style="margin-top:2rem;font-size:.85rem">Son güncelleme: {TODAY}</p></div><nav class="toc" aria-label="İçindekiler"><div class="lbl" style="margin-bottom:.5rem">İçindekiler</div>{"".join(f'<a href="#s{i}">{re.sub("<[^>]+>","",x.split("</h2>")[0])}</a>' for i,x in enumerate(secs))}</nav></div></section>',
      "safak", f"{t} · Florida Coffee", f"Florida Coffee {t.lower()} (taslak).", f"/yasal/{k}/", cls="paper"))

# ---------- EN ----------
en_branches = "".join(f'<a class="cell" href="/subeler/{b["id"]}/"><h3>{b["n"]}</h3><p>{b["c"]} · {hh(b["o"])}–{hh(b["k"])}</p><span class="more">Branch page →</span></a>' for b in BRANCHES if "manzara" in b["f"] or "Karadağ" in b["c"])
page("/en/", head("Florida Coffee · Istanbul-born coffee, 17 locations, 2 countries","Florida Coffee: Bosphorus-view cafés in Istanbul, locations across Turkey and Montenegro. Same cup everywhere: 14 g dose, 18–23 s shot.","/en/",
  {"@context":"https://schema.org","@type":"Organization","name":"Florida Coffee","alternateName":"Florida Coffee Turkey","url":f"{SITE}/en/"}).replace('lang="tr"','lang="en"') +
  f'''<body data-page="safak">
<header class="nav"><a class="home" href="/" aria-label="Florida Coffee home">{LOGO_HTML}</a><nav class="navlinks"><a href="/menu/">Menu</a><a href="/subeler/">Locations</a><a href="/kahvemiz/">Our coffee</a><a href="/franchise/">Franchise</a><a href="/">Türkçe</a></nav><a class="btn amber sm cta" href="/app/">Order ahead</a></header>
<section class="hero img"><div class="bg"><img src="/img/hero.jpg" alt=""></div><div class="wrap"><div class="eyebrow">Istanbul-born · Taste of Joy</div><h1>The Bosphorus wakes up.<br>The coffee is already <span style="color:var(--amber)">ready</span>.</h1><p class="lede">Born in Çengelköy. Now 17 locations in Turkey and Montenegro, one recipe everywhere: 14 g dose weighed, 90–96 °C, 9 bar, 18–23 s shot, milk at 60–65 °C.</p><div style="display:flex;gap:.5rem;flex-wrap:wrap;margin-top:1.4rem"><a class="btn amber" href="/subeler/">Find a location</a><a class="btn ghost" href="/franchise/">Franchise</a></div></div></section>
<section class="sec"><div class="wrap"><h2 style="margin-bottom:1rem">Sunset terraces and the Adriatic</h2><div class="grid g3">{en_branches}</div><p style="margin-top:1.4rem;font-size:.9rem;color:var(--ink-3)">Full English and Montenegrin site coming with the Podgorica and Budva menus. Ask Flo — our toucan — in English or Turkish.</p></div></section>
<footer><div class="wrap"><div class="end"><span>© 2026 Florida Coffee · Demo by P3Media</span><a href="/">Türkçe</a></div></div></footer>{FLO_HTML}<script src="/assets/site.js" defer></script></body></html>''')

# ---------- 404 ----------
page("/404.html", shell('<section class="hero"><div class="wrap"><div class="eyebrow">404</div><h1>Bu masa boş.</h1><p class="lede">Aradığınız sayfa yok ya da taşındı. Flo size yolu gösterebilir.</p><div style="display:flex;gap:.5rem;flex-wrap:wrap;margin-top:1.4rem"><a class="btn amber" href="/">Ana sayfa</a><a class="btn ghost" href="/subeler/">Şubeler</a></div></div></section>',
  "safak","Sayfa bulunamadı · Florida Coffee","Aradığınız sayfa yok.","/404.html"))

# ---------- yaz ----------
os.makedirs(os.path.join(DIST, "assets"), exist_ok=True)
open(os.path.join(DIST, "assets", "site.css"), "w", encoding="utf-8").write(CSS)
open(os.path.join(DIST, "assets", "site.js"), "w", encoding="utf-8").write(rebase(JS))
open(os.path.join(DIST, "favicon.svg"), "w", encoding="utf-8").write('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><rect width="100" height="100" fill="#004854"/><g transform="translate(10 10) scale(.8)"><circle cx="50" cy="50" r="38.3" fill="none" stroke="#EDE6D8" stroke-width="23.4"/><path d="M50 50 L50 0 A50 50 0 0 0 0 50 Z" fill="#F09C1C"/><path d="M50 50 L23.4 50 A26.6 26.6 0 0 0 50 76.6 Z" fill="#D44808"/><circle cx="61.6" cy="40.8" r="6" fill="#EDE6D8"/></g></svg>')
n = 0
for path, html_ in PAGES:
    out = os.path.join(DIST, path.lstrip("/")) if path.endswith(".html") else os.path.join(DIST, path.strip("/"), "index.html")
    os.makedirs(os.path.dirname(out), exist_ok=True); open(out, "w", encoding="utf-8").write(rebase(html_)); n += 1
# ana sayfa: hikâye demosu (nav bağlantıları gerçek sayfalara)
site = re.sub(r'<img[^>]*data-embedded[^>]*>', '', demo)
site = re.sub(r'(<figure class="ph[^"]*?) has(")', r'\1\2', site)
site = re.sub(r'(<img class="wm" data-brand="([a-z0-9_-]+)" alt="" src=")[^"]*(")', r'\1img/brand/\2.png\3', site)
site = re.sub(r'<script id="subeimg" type="application/json">.*?</script>', '<script id="subeimg" type="application/json">{}</script>', site, count=1, flags=re.S)
site = re.sub(r'<script id="menuimg" type="application/json">.*?</script>', '<script id="menuimg" type="application/json">{}</script>', site, count=1, flags=re.S)
site = re.sub(r'(<video[^>]*data-vid="([a-z0-9_-]+)"[^>]*><source src=")[^"]*(")', r'\1video/\2.mp4\3', site)
site = re.sub(r'^<title>.*?</title>\s*', '', site, count=1, flags=re.S)
site = site.replace('<a href="#menu">Menü</a><a href="#subeler">Şubeler</a><a href="#kahvemiz">Kahvemiz</a><a href="#taze">Taze</a><a href="#urunler">Ürünler</a><a href="#kulup">Kulüp</a><a href="#franchise">Franchise</a>',
                    "".join(f'<a href="{h}">{t}</a>' for t,h in NAV))
site = site.replace('<a class="btn amber sm cta" href="#sabah">Ön sipariş</a>','<a class="btn amber sm cta" href="/app/">Ön sipariş</a>')
for sec_id, href, label in [("menu","/menu/","Tüm menü ve ürün sayfaları"),("subeler","/subeler/","Tüm şube sayfaları"),("kahvemiz","/kahvemiz/","Standartların tamamı"),("taze","/taze/","Tüm haberler"),("urunler","/urunler/","Tüm ürünler"),("kulup","/kulup/","Kulüp ve uygulama"),("gece","/etkinlikler/","Etkinlik takvimi"),("franchise","/franchise/","Franchise sayfası ve SSS")]:
    site = re.sub(rf'(<section class="sec[^"]*" id="{sec_id}">.*?<div class="inner">)', rf'\1<p style="margin:0 0 .5rem"><a class="btn ghost sm" href="{href}">{label}</a></p>', site, count=1, flags=re.S)
site = site.replace('<li>Kariyer</li><li>KVKK aydınlatma metni</li><li>Çerez politikası</li><li>Kullanıcı sözleşmesi</li><li>İletişim</li>','<li><a href="/kariyer/">Kariyer</a></li><li><a href="/yasal/kvkk/">KVKK aydınlatma metni</a></li><li><a href="/yasal/cerez/">Çerez politikası</a></li><li><a href="/yasal/kullanici-sozlesmesi/">Kullanıcı sözleşmesi</a></li><li><a href="/iletisim/">İletişim</a></li>')
site = site.replace('<li>Türkçe</li><li>English</li><li>Crnogorski</li>','<li>Türkçe</li><li><a href="/en/">English</a></li><li>Crnogorski · yakında</li>')
home_head = '<!doctype html><html lang="tr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover"><meta name="robots" content="noindex"><meta name="theme-color" content="#004854"><title>Florida Coffee · Boğaz\'da Bir Gün</title><meta name="description" content="Çengelköy\'de doğan, 17 şubeli kahve zinciri. Ön sipariş, FloridaDays Club, franchise."><link rel="icon" href="/favicon.svg" type="image/svg+xml"><link rel="canonical" href="' + SITE + '/"><style>html{color-scheme:dark}body{margin:0}img{max-width:100%}[hidden]{display:none!important}</style>' + \
  '<script type="application/ld+json">' + json.dumps({"@context":"https://schema.org","@type":"Organization","name":"Florida Coffee","alternateName":["Florida Coffee Türkiye","Florida Coffee Co."],"url":SITE,"logo":f"{SITE}/favicon.svg","address":{"@type":"PostalAddress","streetAddress":"Çengelköy Mah. Görgeç Sok. No:6","addressLocality":"Üsküdar","addressRegion":"İstanbul","addressCountry":"TR"}}, ensure_ascii=False) + '</script></head><body>'
open(os.path.join(DIST, "index.html"), "w", encoding="utf-8").write(rebase(home_head + site + '</body></html>')); n += 1
# sitemap + robots + vercel
urls = ["/"] + [p for p,_ in PAGES if not p.endswith(".html")]
open(os.path.join(DIST, "sitemap.xml"), "w", encoding="utf-8").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.w3.org/1999/xhtml" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n' + "".join(f'  <url><loc>{SITE}{u}</loc><lastmod>{TODAY}</lastmod></url>\n' for u in urls) + '</urlset>\n')
open(os.path.join(DIST, "robots.txt"), "w").write(f"User-agent: *\nDisallow: /\n# Demo: yayında 'Allow: /' ve Sitemap satırı açılır\n# Sitemap: {SITE}/sitemap.xml\n")
open(os.path.join(DIST, "vercel.json"), "w").write('{"cleanUrls":true,"trailingSlash":true}\n')
print(f"{n} sayfa yazıldı → {os.path.relpath(DIST, BASE)}/ · {len(BRANCHES)} şube · {sum(len(v) for v in MENU.values())} ürün · {len(NEWS)} haber · sitemap {len(urls)} URL")
