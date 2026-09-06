#!/usr/bin/env python3.12
"""Florida Coffee — çok sayfalı statik site üreticisi.
Kaynaklar: demo-site/index.html (ana sayfa hikâye demosu, Flo motoru, şube/menü verisi) + bu dosyadaki içerik.
Çıktı: ../dist/  (Vercel / GitHub Pages'e doğrudan yayınlanır)
Kullanım: python3 build.py
"""
import re, os, json, shutil, html as H
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
    body = body[:end] + f'<main class="{cls}">' + body[end:] + '</main>'
    return head(title, desc, path, jsonld) + f'''<body data-page="{page}">
<header class="nav"><a class="home" href="/" aria-label="Florida Coffee ana sayfa">{LOGO_HTML}</a>
<nav class="navlinks" aria-label="Ana menü">{nav}</nav><a class="btn amber sm cta" href="/app/">Ön sipariş</a></header>
{body}
<footer><div class="wrap"><div class="cols">
<div>{LOGO_FOOT}<span class="sr">Florida Coffee</span><p style="margin:0;color:var(--ink-3);font-size:.85rem">Çengelköy Mah. Görgeç Sok. No:6<br>Üsküdar / İstanbul<br>Taste of Joy</p></div>
<div><h4>Keşfet</h4><ul><li><a href="/menu/">Menü</a></li><li><a href="/subeler/">Şubeler</a></li><li><a href="/kahvemiz/">Kahvemiz</a></li><li><a href="/taze/">Taze</a></li><li><a href="/urunler/">Ürünler</a></li><li><a href="/etkinlikler/">Etkinlikler</a></li></ul></div>
<div><h4>Kulüp ve uygulama</h4><ul><li><a href="/kulup/">FloridaDays Club</a></li><li><a href="/uygulama/">Uygulama</a></li><li><a href="/app/">Uygulama demosu</a></li><li><a href="/hikayemiz/">Hikâyemiz</a></li></ul></div>
<div><h4>Kurumsal</h4><ul><li><a href="/franchise/">Franchise</a></li><li><a href="/kurumsal/">Kurumsal satış</a></li><li><a href="/kariyer/">Kariyer</a></li><li><a href="/sss/">SSS</a></li><li><a href="/iletisim/">İletişim</a></li></ul></div>
<div><h4>Yasal</h4><ul><li><a href="/yasal/kvkk/">KVKK aydınlatma</a></li><li><a href="/yasal/cerez/">Çerez politikası</a></li><li><a href="/yasal/kullanici-sozlesmesi/">Kullanıcı sözleşmesi</a></li><li><a href="/yasal/mesafeli-satis/">Mesafeli satış</a></li><li><a href="/en/">English</a></li></ul></div>
</div><div class="end"><span>© 2026 Florida Coffee Kahve Gıda San. ve Tic. A.Ş. · Demo, P3Media</span><span><a href="/platform/">Platform prototipi</a> · <a href="/sunum/">Sunum</a></span></div></div></footer>
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

# ---------- KAHVEMİZ ----------
page("/kahvemiz/", shell(hero("Bölüm 10:00 · Standart","Aynı fincan,<br>on yedi şubede.","Kavacık'taki latte, Bursa'dakiyle aynı olmak zorunda. Bunu sağlayan iyi niyet değil, ölçülebilir standart. Reçetelerimiz kişisel yoruma açık değildir.",[("Kahvemiz",None)],"barista") +
  '''<section class="sec"><div class="wrap two"><div class="panel"><h2 style="font-size:1.4rem;margin-bottom:.8rem">Espresso standardımız</h2><dl class="kv"><dt>Doz</dt><dd>14 g · double shot, tartı ile</dd><dt>Su sıcaklığı</dt><dd>90–96 °C</dd><dt>Basınç</dt><dd>9 bar</dd><dt>Shot süresi</dt><dd>18–23 saniye</dd><dt>Çıktı</dt><dd>30–60 g</dd><dt>Süt</dt><dd>60–65 °C mikro köpük</dd><dt>Fincan</dt><dd>Önceden ısıtılır</dd><dt>Kavurma</dt><dd>Orta 215–220 °C · Koyu 220–225 °C</dd></dl></div>
  <div><h2 style="font-size:1.4rem;margin-bottom:.8rem">Shot öncesi zorunlu 5 adım</h2><ol style="padding-left:1.2rem;color:var(--ink-2);display:grid;gap:.5rem"><li><b style="color:var(--ink)">Grup başlığı flush</b> — 2–3 sn su, kalıntı temizlenir, sıcaklık dengelenir</li><li><b style="color:var(--ink)">Portafiltre temizlenir</b> — sepet kuru, partikül yok</li><li><b style="color:var(--ink)">Gramaj tartılır</b> — 14 g, göz kararı kabul edilmez</li><li><b style="color:var(--ink)">Tamp</b> — eşit basınç, düz yüzey</li><li><b style="color:var(--ink)">Süre</b> — kronometre, 18–23 sn</li></ol><p style="margin-top:1rem;font-size:.9rem">Birinin atlanması zincir standardına aykırıdır. Kaynak: barista operasyon el kitabı.</p></div></div></section>
  <section class="sec" style="padding-top:0"><div class="wrap"><h2 style="margin-bottom:1rem">Kahve kuşağı: çekirdek nereden geliyor</h2><div class="grid g3">
  <div class="cell"><h3>Latin Amerika</h3><p><b>Denge.</b> Fındık, badem, kakao, sütlü çikolata, karamel, narenciye. Orta asidite, temiz bitiş. Brezilya, Kolombiya, Guatemala. Espresso için en stabil profil.</p></div>
  <div class="cell"><h3>Afrika</h3><p><b>Aroma ve asidite.</b> Çiçeksi, kırmızı ve tropikal meyveler, çay benzeri yapı. Canlı, parlak. Etiyopya, Kenya, Tanzanya. Filtre ve üçüncü dalga için.</p></div>
  <div class="cell"><h3>Asya-Pasifik</h3><p><b>Gövde.</b> Topraksı, baharatsı, bitter çikolata, tütün, odunsu. Düşük asidite, yoğun ve kalıcı. Endonezya, Vietnam, Hindistan. Sert içim için.</p></div></div>
  <p style="margin-top:1.2rem">Harmanımız: Etiyopya Yirgacheffe %60 + Brezilya Cerrado %40. <a href="/urunler/">Eve götürün →</a></p></div></section>''',
  "kahvemiz","Kahvemiz ve Standartlarımız · Florida Coffee","Florida Coffee espresso standardı: 14 g doz, 90–96 °C, 9 bar, 18–23 sn, süt 60–65 °C. Shot öncesi 5 adım, kahve kuşağı profilleri.","/kahvemiz/"))

# ---------- TAZE ----------
newsitems = "".join(f'<a class="cell" data-t="{n["t"]}" href="/taze/{slug(n["h"])}/"><div class="lbl" style="display:flex;justify-content:space-between"><span style="color:var(--amber)">{TL[n["t"]]}</span><span>{n["d"]}</span></div><h3>{n["h"]}</h3><p>{n["p"]}</p><span class="more">Devamı →</span></a>' for n in NEWS)
tf = "".join(f'<button class="fbtn" aria-pressed="{"true" if k=="hepsi" else "false"}" data-t="{k}">{v}</button>' for k,v in [("hepsi","Hepsi"),("sube","Şube"),("urun","Ürün"),("kampanya","Kampanya"),("etkinlik","Etkinlik")])
page("/taze/", shell(hero("Bölüm 11:30 · Taze","Yeni ne var,<br>ilk siz duyun.","Yeni şube, sezon ürünü, kampanya ve etkinlikler. Uygulamada bildirim olarak da gelir.",[("Taze",None)]) +
  f'<section class="sec"><div class="wrap"><div class="filters" id="tazeF">{tf}</div><div class="grid g3" id="news">{newsitems}</div><form class="f panel" style="margin-top:1.4rem;grid-template-columns:1fr auto;align-items:end"><label>Haber al · ayda en fazla iki e-posta<input type="email" required placeholder="e-posta adresiniz"></label><button class="btn amber" type="submit">Kaydol</button><div class="ok" hidden style="grid-column:1/-1">Kaydedildi. İlk haber Sakarya açılışı olacak.</div></form></div></section>',
  "taze","Taze · Haberler ve Yenilikler · Florida Coffee","Florida Coffee'den yeni şubeler, sezon ürünleri, kampanyalar ve etkinlikler.","/taze/"))
for n in NEWS:
    sl = slug(n["h"]); ld = {"@context":"https://schema.org","@type":"NewsArticle","headline":n["h"],"description":n["p"],"image":f"{SITE}/img/{n['img']}.jpg","publisher":{"@type":"Organization","name":"Florida Coffee"}}
    page(f"/taze/{sl}/", shell(hero(f'{TL[n["t"]]} · {n["d"]}', n["h"], n["p"], [("Taze","/taze/"),(n["h"],None)], n["img"]) +
      f'<section class="sec"><div class="wrap two"><div class="prose"><p>{n["body"]}</p><div style="display:flex;gap:.5rem;flex-wrap:wrap;margin-top:1.2rem"><a class="btn amber" href="/app/">Uygulama</a><a class="btn ghost" href="/taze/">Tüm haberler</a></div></div><div class="grid" style="grid-template-columns:1fr">{"".join(f'<a class="cell" href="/taze/{slug(o["h"])}/"><div class="lbl" style="color:var(--amber)">{TL[o["t"]]}</div><h3>{o["h"]}</h3><span class="more">Devamı →</span></a>' for o in NEWS if o is not n)[:3000]}</div></div></section>',
      "taze", f"{n['h']} · Florida Coffee", n["p"], f"/taze/{sl}/", ld))

# ---------- ÜRÜNLER ----------
prods = "".join(f'<a class="cell" href="/urunler/{slug(p["n"])}/">{f"<img src=\"/img/{p['img']}.jpg\" alt=\"\" style=\"aspect-ratio:4/3;object-fit:cover;width:100%;display:block;margin:-1.1rem -1.2rem .4rem;width:calc(100% + 2.4rem);max-width:none\">" if p["img"] else ""}<div style="display:flex;justify-content:space-between;gap:.6rem;align-items:baseline"><h3>{p["n"]}</h3><b style="font-family:var(--disp);white-space:nowrap">{p["p"]}</b></div><p>{p["d"]}</p><div style="display:flex;gap:.3rem;flex-wrap:wrap">{"".join(f"<span class=chip>{t}</span>" for t in p["tags"])}</div><span class="more">Ürün sayfası →</span></a>' for p in PRODUCTS)
page("/urunler/", shell(hero("Bölüm 17:00 · Ürünler","Aynı çekirdek,<br>sizin mutfağınızda.","Şubede içtiğiniz harman, aynı kavurma tarihiyle. Uygulamadan ön sipariş, şubeden teslim; kargo yakında.",[("Ürünler",None)],"beans") +
  f'<section class="sec"><div class="wrap"><div class="grid g3">{prods}</div><p style="font-size:.8rem;margin-top:1rem;color:var(--ink-3)">Fiyatlar örnektir; katalog merkezden yönetilir.</p></div></section>',
  "urunler","Ürünler · Çekirdek, Set, Termos, Hediye Kartı · Florida Coffee","Florida Coffee ürünleri: Sonbahar Harmanı 250 g, Ev Espresso Seti, Florida Termos, dijital hediye kartı.","/urunler/"))
for p in PRODUCTS:
    sl = slug(p["n"]); ld = {"@context":"https://schema.org","@type":"Product","name":p["n"],"description":p["d"],"brand":{"@type":"Brand","name":"Florida Coffee"},"offers":{"@type":"Offer","priceCurrency":"TRY","price":re.sub(r"[^\d]","",p["p"].split("–")[0]),"availability":"https://schema.org/InStoreOnly"}}
    if p["img"]: ld["image"] = f"{SITE}/img/{p['img']}.jpg"
    page(f"/urunler/{sl}/", shell(hero("Ürün", p["n"], p["d"], [("Ürünler","/urunler/"),(p["n"],None)], p["img"]) +
      f'<section class="sec"><div class="wrap two"><div class="prose"><p>{p["body"]}</p><div class="panel" style="margin-top:1rem"><dl class="kv"><dt>Fiyat</dt><dd><b>{p["p"]}</b></dd><dt>Teslim</dt><dd>Uygulamadan ön sipariş, şubeden teslim · kargo yakında</dd><dt>Etiketler</dt><dd>{" · ".join(p["tags"])}</dd></dl><div style="display:flex;gap:.5rem;flex-wrap:wrap;margin-top:1rem"><a class="btn amber" href="/app/">Ön sipariş</a><a class="btn ghost" href="/urunler/">Tüm ürünler</a></div></div></div><div>{f"<div class=imgband><img src=\"/img/{p['img']}.jpg\" alt=\"{p['n']}\"></div>" if p["img"] else "<div class=panel><h3>Dijital hediye</h3><p>Telefona anında gider; bakiye FloridaDays cüzdanına aktarılır.</p></div>"}</div></div></section>',
      "urunler", f"{p['n']} · Florida Coffee", p["d"], f"/urunler/{sl}/", ld))

# ---------- KULÜP / UYGULAMA / ETKİNLİKLER ----------
page("/kulup/", shell(hero("Bölüm 21:00 · FloridaDays Club","Sadakat kartınız<br>cüzdanınızda kaybolmasın.","Her harcama 1 ₺ = 1 çekirdek; 10 içecekte biri bizden. Seviye son 6 ayın harcamasıyla belirlenir. Ödeme ve puan tek QR.",[("Kulüp",None)],"cup") +
  '''<section class="sec"><div class="wrap"><div class="grid g3">
  <div class="cell"><div class="lbl">0–2.500 ₺</div><h3>Classic</h3><p>Doğum günü içeceği · kampanyalara erişim · çekirdek biriktirme</p></div>
  <div class="cell" style="border-top:3px solid var(--amber)"><div class="lbl">2.500–7.500 ₺</div><h3>Plus</h3><p>Ayda 2 boy yükseltme · erken sezon menüsü · etkinliklerde öncelik</p></div>
  <div class="cell"><div class="lbl">7.500 ₺ +</div><h3>Premium</h3><p>Ücretsiz ekstra shot · gün batımında manzaralı masa önceliği · özel cupping</p></div></div>
  <div class="two" style="margin-top:2rem"><div class="panel"><h3>Fiziksel karttan uygulamaya</h3><p style="margin:.5rem 0 0;color:var(--ink-2)">Uygulamada Kart → Kartımı tara. Karttaki kodu okutun; damgalar ve bakiye anında geçer. Kart sonra da çalışır; ikisi tek hesaptır. Aktarımı tamamlayanlara ilk kahve bizden.</p></div>
  <div class="panel"><h3>Cüzdan</h3><p style="margin:.5rem 0 0;color:var(--ink-2)">Kredi kartı, Multinet, Sodexo, Setcard ile yükleme; 500 ₺ yüklemeye 25 ₺ bonus. Arkadaşınıza kahve veya bakiye gönderin.</p></div></div>
  <div style="display:flex;gap:.5rem;flex-wrap:wrap;margin-top:1.6rem"><a class="btn amber" href="/app/">Uygulama demosunu aç</a><a class="btn ghost" href="/uygulama/">Uygulama hakkında</a></div></div></section>''',
  "kulup","FloridaDays Club · Sadakat Programı · Florida Coffee","Florida Coffee sadakat programı: 1 ₺ = 1 çekirdek, 10 içecekte biri hediye, Classic/Plus/Premium seviyeleri, cüzdan ve kart aktarımı.","/kulup/"))
page("/uygulama/", shell(hero("Uygulama","Sıra sizi bekletmesin.<br>Kahve sizi beklesin.","Ön sipariş, \"Geldim\", cüzdan, sadakat ve kampanyalar tek uygulamada. iOS ve Android.",[("Uygulama",None)],"workspace") +
  '''<section class="sec"><div class="wrap"><div class="grid g4">
  <div class="cell"><h3>Ön sipariş</h3><p>Şube ve içecek seçin, ödeyin; hazırlık "Geldim" deyince ya da 200 m yaklaşınca başlar.</p></div>
  <div class="cell"><h3>Süt tercihi profilde</h3><p>Laktozsuz, yulaf, badem — bir kez seçin, barista ekranında etiketli görünür.</p></div>
  <div class="cell"><h3>Tek QR</h3><p>Ödeme ve puan aynı kodla. Yemek kartlarıyla yükleme, bonuslu bakiye.</p></div>
  <div class="cell"><h3>Kampanyalar</h3><p>Şube, seviye ve saat bazlı; ölü saatlerde otomatik indirim.</p></div></div>
  <div class="badges" style="margin-top:1.6rem"><span class="badge">App Store · yakında güncelleme</span><span class="badge">Google Play · yakında güncelleme</span><a class="btn amber" href="/app/">Tarayıcıda dene</a></div></div></section>''',
  "kulup","Florida Coffee Uygulaması · Ön Sipariş ve Sadakat","Florida Coffee mobil uygulaması: ön sipariş, Geldim, cüzdan, FloridaDays Club.","/uygulama/",
  {"@context":"https://schema.org","@type":"MobileApplication","name":"Florida Coffee","operatingSystem":"iOS, Android","applicationCategory":"FoodApplication","offers":{"@type":"Offer","price":"0","priceCurrency":"TRY"}}))
page("/etkinlikler/", shell(hero("Bölüm 23:30 · Etkinlikler","Şehir susunca<br>Boğaz konuşur.","Kavacık ve Beykoz ikiye kadar açık. Akustik akşamlar, cupping ve gece filtresi.",[("Etkinlikler",None)],"night") +
  '''<section class="sec"><div class="wrap"><div class="grid g3">
  <div class="cell"><div class="lbl" style="color:var(--amber)">Her Perşembe · 21:00</div><h3>Akustik set · Kavacık terası</h3><p>İki kişilik akustik, gün batımından sonra. Yer ayırma uygulamadan; Plus ve Premium öncelikli.</p><a class="more" href="/subeler/kavacik/">Kavacık →</a></div>
  <div class="cell"><div class="lbl" style="color:var(--amber)">Ayın ilk Cumartesi'si</div><h3>Cupping · Çengelköy</h3><p>Sezon harmanını birlikte tadıyoruz. 12 kişilik, ücretsiz.</p><a class="more" href="/subeler/cengelkoy/">Çengelköy →</a></div>
  <div class="cell"><div class="lbl" style="color:var(--amber)">Her gün 22:00 sonrası</div><h3>Gece filtresi</h3><p>Kafeinsiz seçenekle aynı fiyat. Uykunuzu bozmadan oturmaya devam.</p><a class="more" href="/menu/">Menü →</a></div></div></div></section>''',
  "gece","Etkinlikler · Florida Coffee","Florida Coffee etkinlikleri: akustik akşamlar, cupping, gece filtresi.","/etkinlikler/",
  {"@context":"https://schema.org","@type":"Event","name":"Akustik akşamlar · Kavacık terası","eventSchedule":{"@type":"Schedule","byDay":"https://schema.org/Thursday","startTime":"21:00"},"location":{"@type":"Place","name":"Florida Coffee Kavacık"}}))

# ---------- FRANCHISE ----------
calc = '''<div class="panel"><label class="lbl" for="fCity">Konum tipi</label><select id="fCity" style="width:100%;margin:.4rem 0 1rem;background:rgba(9,14,19,.6);border:1px solid var(--hair-2);color:var(--ink);padding:.6rem"><option value="1.15">İstanbul cadde</option><option value="1" selected>Büyükşehir cadde (Bursa, Sakarya, Samsun)</option><option value="0.85">İlçe / üniversite çevresi</option></select>
<label class="lbl" for="fM2">Mağaza alanı: <b id="fM2v">110</b> m²</label><input type="range" id="fM2" min="60" max="220" step="5" value="110" style="width:100%;accent-color:var(--amber)">
<label class="lbl" for="fRev" style="display:block;margin-top:.8rem">Tahmini aylık ciro: <b id="fRevv">1.400.000</b> ₺</label><input type="range" id="fRev" min="500000" max="4000000" step="50000" value="1400000" style="width:100%;accent-color:var(--amber)">
<div class="grid g2" style="margin-top:1rem"><div class="cell"><div class="lbl">Kuruluş yatırımı</div><b id="oInv" style="font-family:var(--disp);font-size:1.4rem">—</b></div><div class="cell"><div class="lbl">Aylık royalty (%5 + KDV)</div><b id="oRoy" style="font-family:var(--disp);font-size:1.4rem">—</b></div><div class="cell"><div class="lbl">Ulusal reklam (≤ %1)</div><b id="oAd" style="font-family:var(--disp);font-size:1.4rem">—</b></div><div class="cell"><div class="lbl">Örnek geri dönüş</div><b id="oPb" style="font-family:var(--disp);font-size:1.4rem">—</b></div></div>
<p style="font-size:.8rem;color:var(--ink-3);margin:.9rem 0 0">Örnek hesaplamadır, teklif değildir. Giriş bedeli ve platform lisansı merkez tarafından belirlenir.</p></div>'''
page("/franchise/", shell(hero("Bölüm 02:00 · Franchise","Bu günü kendi<br>şehrinizde kurun.","3 km bölge koruması, 45 gün eğitim, merkezi tedarik ve dijital altyapının tamamı. Hesaplayıcı örnek bir yatırım tablosu çıkarır.",[("Franchise",None)],"franchise") +
  f'''<section class="sec"><div class="wrap two">{calc}<div><div class="grid g2">
  <div class="cell"><h3>3 km bölge koruması</h3><p>Sözleşme süresince aynı bölgede ikinci Florida açılmaz.</p></div>
  <div class="cell"><h3>45 gün eğitim</h3><p>30 gün işletme yönetimi, 15 gün barista; açılışta merkez ekibi şubede.</p></div>
  <div class="cell"><h3>Merkezi tedarik</h3><p>Çekirdek, ambalaj ve ekipman tek kaynaktan; 40 gün vade.</p></div>
  <div class="cell"><h3>Dijital altyapı dahil</h3><p>Şube sayfanız, uygulamada yeriniz, sadakat, raporlama paneli.</p></div></div>
  <div class="panel" style="margin-top:1rem"><h3 style="margin-bottom:.5rem">Açılmasını istediğimiz bölgeler</h3><div style="display:flex;gap:.3rem;flex-wrap:wrap">{"".join(f'<span class="chip water">{c}</span>' for c in ["Eskişehir","Ankara Çayyolu","İzmir Alsancak","Antalya Lara","Trabzon","Konya"])}<span class="chip copper">Saraybosna</span><span class="chip copper">Tiran</span></div>
  <div style="display:flex;gap:.5rem;flex-wrap:wrap;margin-top:1.1rem"><a class="btn amber" href="/franchise/basvuru/">Başvuru formu</a><a class="btn ghost" href="/franchise/sss/">Franchise SSS</a></div></div></div></div></section>''',
  "franchise","Franchise · Florida Coffee","Florida Coffee franchise: 3 km bölge koruması, 45 gün eğitim, merkezi tedarik, royalty %5. Yatırım hesaplayıcı ve başvuru.","/franchise/"))
page("/franchise/basvuru/", shell(hero("Franchise · Başvuru","Ön başvuru.<br>İki dakika.","Formu doldurun; franchise ekibimiz 24 saat içinde arar. Flo ile sohbet ederek de bırakabilirsiniz.",[("Franchise","/franchise/"),("Başvuru",None)]) +
  '''<section class="sec"><div class="wrap two"><form class="f panel"><label>Ad Soyad<input required></label><label>Telefon<input type="tel" required placeholder="05xx xxx xx xx"></label><label>E-posta<input type="email" required></label><label>Hedef şehir / ilçe<input required></label><label>Bütçe<select><option>2 M ₺ altı</option><option>2–4 M ₺</option><option>4–6 M ₺</option><option>6 M ₺ üstü</option></select></label><label>Deneyim<select><option>Yok</option><option>Perakende</option><option>Kafe / restoran işlettim</option><option>Franchise sahibiyim</option></select></label><label>Lokasyon durumu<select><option>Henüz yok</option><option>Adayım var</option><option>Kira sözleşmem hazır</option></select></label><label>Not<textarea rows="3"></textarea></label><label style="grid-template-columns:auto 1fr;align-items:start;gap:.6rem;display:grid;font-weight:400"><input type="checkbox" required style="width:auto"> <span>KVKK aydınlatma metnini okudum; bilgilerimin franchise değerlendirmesi için işlenmesini kabul ediyorum.</span></label><button class="btn amber" type="submit">Başvuruyu gönder</button><div class="ok" hidden>Başvurunuz alındı. Franchise ekibimiz 24 saat içinde arayacak; e-postanıza yatırım özeti gidecek.</div></form>
  <div><div class="panel"><h3>Süreç</h3><ol style="padding-left:1.2rem;color:var(--ink-2);display:grid;gap:.5rem;margin:.6rem 0 0"><li>Ön başvuru ve 24 saat içinde arama</li><li>Keşif görüşmesi: bölge, bütçe, lokasyon</li><li>3 km çakışma kontrolü ve lokasyon onayı</li><li>Sözleşme, 45 gün eğitim, açılış</li></ol></div><p style="margin-top:1rem;font-size:.9rem">Sorunuz mu var? Sağ alttaki Flo, franchise şartlarını anlatır ve başvurunuzu sohbetle alır.</p></div></div></section>''',
  "franchise","Franchise Başvurusu · Florida Coffee","Florida Coffee franchise ön başvuru formu.","/franchise/basvuru/"))
ffaq = [("Yatırım ne kadar?","Konuma ve metrekareye göre değişir; büyükşehir caddesinde 100–120 m² için örnek hesap 3,5–4,5 M ₺ bandında. Kesin rakam keşif görüşmesinde."),("Royalty ve reklam payı?","Aylık ciro üzerinden %5 + KDV royalty; ulusal reklam bütçesi en fazla %1. Her ikisi sözleşmede yazılıdır."),("Bölge koruması var mı?","Evet, 3 km. Sözleşme süresince aynı bölgede ikinci Florida açılmaz."),("Eğitim nasıl?","Toplam 45 gün: 30 gün işletme yönetimi, 15 gün barista. Açılışta merkez ekibi şubede."),("Tedarik nasıl işler?","Çekirdek, ambalaj ve ekipman merkezden; 40 gün vade. FIFO zorunlu."),("Dijital altyapı dahil mi?","Evet: şube sayfası, uygulamada yer, sadakat programı, raporlama paneli, ciro bildirimi otomasyonu."),("Sözleşme süresi?","10 yıl."),("Deneyim şart mı?","Şart değil; işletme deneyimi başvuru puanını yükseltir. Eğitim programı sıfırdan başlayanlar için tasarlanmıştır.")]
page("/franchise/sss/", shell(hero("Franchise · SSS","Sık sorulan<br>franchise soruları.","Kısa ve net. Daha fazlası için başvuru sonrası keşif görüşmesi.",[("Franchise","/franchise/"),("SSS",None)]) +
  f'<section class="sec"><div class="wrap"><div class="faq">{"".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q,a in ffaq)}</div><div style="margin-top:1.4rem"><a class="btn amber" href="/franchise/basvuru/">Başvuru formu</a></div></div></section>',
  "franchise","Franchise SSS · Florida Coffee","Florida Coffee franchise sık sorulan sorular: yatırım, royalty, bölge koruması, eğitim, tedarik.","/franchise/sss/",
  {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in ffaq]}))

# ---------- HİKÂYE / KURUMSAL / KARİYER / SSS / İLETİŞİM ----------
page("/hikayemiz/", shell(hero("Hikâyemiz","Çengelköy'de bir sabah<br>başladı.","Boğaz'a bakan bir köşede, aynı fincanı her gün aynı standartla verme sözüyle. Bugün 17 nokta, iki ülke; söz aynı.",[("Hikâyemiz",None)],"hero") +
  '''<section class="sec"><div class="wrap two"><div class="prose"><h2>Çengelköy</h2><p>İlk şubemiz Çengelköy'de, Boğaz'ın sabah ışığını en iyi gören sokaklardan birinde açıldı. Kahveyi bir ürün olarak değil, günün ritmi olarak düşündük: şafakta ilk filtre, öğle arasında hızlı bir espresso, gün batımında terasta uzun bir cold brew.</p><h2>Standart</h2><p>Büyürken bir şeyi kural yaptık: Kavacık'taki latte Bursa'dakiyle aynı olacak. Bunun için barista operasyon el kitabını yazdık — 14 g doz, 90–96 °C, 18–23 sn, süt 60–65 °C. Reçete kişisel yoruma açık değildir; standardı barista üretir.</p><h2>Boğaz'dan Adriyatik'e</h2><p>İstanbul, Kocaeli, Sakarya, Bursa, Samsun, Rize, Erzincan… ve Karadağ'da Podgorica ile Budva. Her şubede farklı bir manzara, aynı fincan.</p><h2>Mutluluğun tadı</h2><p>Taste of Joy bir slogan değil, ölçüt: müşteri hangi şubeye girerse girsin aynı tadı, aynı sunumu ve aynı sıcaklığı bulmalı.</p></div>
  <div class="grid" style="grid-template-columns:1fr"><div class="cell"><div class="lbl">17</div><h3>şube, 2 ülke</h3></div><div class="cell"><div class="lbl">45 gün</div><h3>barista ve işletme eğitimi</h3></div><div class="cell"><div class="lbl">14 g · 18–23 sn</div><h3>espresso standardı</h3></div><div class="cell"><div class="lbl">02:00</div><h3>Boğaz şubelerinde kapanış</h3></div></div></div></section>''',
  "safak","Hikâyemiz · Florida Coffee","Florida Coffee'nin hikâyesi: Çengelköy'den 17 şubeye, İstanbul'dan Karadağ'a; her fincanda aynı standart.","/hikayemiz/",
  {"@context":"https://schema.org","@type":"Organization","name":"Florida Coffee","alternateName":["Florida Coffee Türkiye","Florida Coffee Co."],"url":SITE,"logo":f"{SITE}/favicon.svg","address":{"@type":"PostalAddress","streetAddress":"Çengelköy Mah. Görgeç Sok. No:6","addressLocality":"Üsküdar","addressRegion":"İstanbul","addressCountry":"TR"},"sameAs":["https://www.instagram.com/floridacoffeetr/","https://www.tiktok.com/@floridacoffee_","https://www.facebook.com/floridacoffeetr/"]}))
page("/kurumsal/", shell(hero("Kurumsal","Toplantınıza kahve,<br>etkinliğinize bar.","Ofis ikramı, etkinlik kahve barı, toplu hediye kartı. Talebinizi bırakın; 1 iş günü içinde dönüş.",[("Kurumsal",None)],"pour") +
  '''<section class="sec"><div class="wrap two"><div class="grid" style="grid-template-columns:1fr"><div class="cell"><h3>Ofis ikramı</h3><p>Haftalık çekirdek ve filtre teslimi; barista eğitimi opsiyonu.</p></div><div class="cell"><h3>Etkinlik kahve barı</h3><p>Mobil espresso barı, 2 barista, 4 saat; 100–400 kişilik etkinlikler.</p></div><div class="cell"><h3>Toplu hediye kartı</h3><p>Çalışan ve müşteri hediyesi için dijital kartlar; kurumsal fatura.</p></div></div>
  <form class="f panel"><label>Kurum<input required></label><label>Ad Soyad<input required></label><label>E-posta<input type="email" required></label><label>İhtiyaç<select><option>Ofis ikramı</option><option>Etkinlik kahve barı</option><option>Toplu hediye kartı</option><option>Diğer</option></select></label><label>Not<textarea rows="3"></textarea></label><button class="btn amber" type="submit">Talep gönder</button><div class="ok" hidden>Talebiniz alındı; 1 iş günü içinde dönüş yapacağız.</div></form></div></section>''',
  "kulup","Kurumsal Satış · Florida Coffee","Florida Coffee kurumsal: ofis ikramı, etkinlik kahve barı, toplu hediye kartı.","/kurumsal/"))
jobs = "".join(f'<div class="cell"><div class="lbl">{j["loc"]} · {j["type"]}</div><h3>{j["t"]}</h3><p>{j["d"]}</p><a class="more" href="#basvur">Başvur →</a></div>' for j in JOBS)
page("/kariyer/", shell(hero("Kariyer","Barista standardı üretir.<br>Siz de üretin.","Her barista hazırladığı her fincanla markayı temsil eder. Deneyim şart değil; 45 günlük eğitimimiz var.",[("Kariyer",None)],"barista") +
  f'''<section class="sec"><div class="wrap"><div class="grid g3">{jobs}</div><div class="two" style="margin-top:2rem" id="basvur"><form class="f panel"><label>Ad Soyad<input required></label><label>Telefon<input type="tel" required></label><label>E-posta<input type="email" required></label><label>Pozisyon<select>{"".join(f"<option>{j['t']}</option>" for j in JOBS)}</select></label><label>Şehir<input></label><label>Kısaca siz<textarea rows="3"></textarea></label><button class="btn amber" type="submit">Başvur</button><div class="ok" hidden>Başvurunuz alındı. İnsan kaynakları 5 iş günü içinde dönüş yapar.</div></form>
  <div class="panel"><h3>Nasıl çalışıyoruz</h3><ul style="padding-left:1.2rem;color:var(--ink-2);margin:.6rem 0 0;display:grid;gap:.4rem"><li>15 gün barista eğitimi: ekstraksiyon, süt dokusu, latte art, hijyen</li><li>Front bar / back bar net görev ayrımı; FIFO zorunlu</li><li>Haftalık kalibrasyon, aylık kalite denetimi</li><li>Şube müdürlüğüne iç terfi yolu</li></ul></div></div></div></section>''',
  "kahvemiz","Kariyer · Florida Coffee","Florida Coffee'de barista, şube müdürü ve kalite uzmanı pozisyonları.","/kariyer/",
  [{"@context":"https://schema.org","@type":"JobPosting","title":j["t"],"description":j["d"],"datePosted":TODAY,"employmentType":"FULL_TIME","hiringOrganization":{"@type":"Organization","name":"Florida Coffee"},"jobLocation":{"@type":"Place","address":{"@type":"PostalAddress","addressLocality":j["loc"].split("·")[0].strip(),"addressCountry":"TR"}}} for j in JOBS]))
page("/sss/", shell(hero("SSS","Sık sorulanlar.","Ön sipariş, süt seçenekleri, sadakat, şubeler, franchise. Cevabı bulamazsanız Flo'ya sorun.",[("SSS",None)]) +
  f'<section class="sec"><div class="wrap"><div class="faq">{"".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q,a in FAQ)}</div></div></section>',
  "safak","Sık Sorulan Sorular · Florida Coffee","Florida Coffee SSS: ön sipariş, süt seçenekleri, FloridaDays Club, şube saatleri, franchise.","/sss/",
  {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in FAQ]}))
page("/iletisim/", shell(hero("İletişim","Yazın, arayın,<br>ya da gelin.","Merkez Çengelköy'de. Şube telefonları şube sayfalarında. Franchise ve kurumsal için ilgili formlar.",[("İletişim",None)]) +
  '''<section class="sec"><div class="wrap two"><div class="panel"><dl class="kv"><dt>Merkez</dt><dd>Florida Coffee Kahve Gıda San. ve Tic. A.Ş.<br>Çengelköy Mah. Görgeç Sok. No:6, Üsküdar / İstanbul</dd><dt>Franchise</dt><dd><a href="/franchise/basvuru/">Başvuru formu</a> ya da Flo</dd><dt>Kurumsal</dt><dd><a href="/kurumsal/">Talep formu</a></dd><dt>Basın</dt><dd>basin@ (örnek)</dd><dt>Sosyal</dt><dd><a href="https://www.instagram.com/floridacoffeetr/" rel="noopener">Instagram</a> · <a href="https://www.tiktok.com/@floridacoffee_" rel="noopener">TikTok</a></dd></dl></div>
  <form class="f panel"><label>Ad Soyad<input required></label><label>E-posta<input type="email" required></label><label>Konu<select><option>Genel</option><option>Şube geri bildirimi</option><option>Uygulama</option><option>Basın</option></select></label><label>Mesaj<textarea rows="4" required></textarea></label><button class="btn amber" type="submit">Gönder</button><div class="ok" hidden>Mesajınız alındı; 1 iş günü içinde dönüş yapacağız.</div></form></div></section>''',
  "safak","İletişim · Florida Coffee","Florida Coffee iletişim: merkez adresi, franchise ve kurumsal formlar, sosyal medya.","/iletisim/"))

# ---------- YASAL ----------
LEGAL = {
 "kvkk": ("KVKK Aydınlatma Metni", ["<h2>Veri sorumlusu</h2><p>Florida Coffee Kahve Gıda San. ve Tic. A.Ş., Çengelköy Mah. Görgeç Sok. No:6, Üsküdar / İstanbul.</p>","<h2>İşlenen veriler ve amaçlar</h2><ul><li>Uygulama üyeliği: ad, telefon, e-posta, doğum tarihi (isteğe bağlı) — hesap oluşturma, sadakat programı</li><li>Sipariş ve ödeme verileri — siparişin yerine getirilmesi, muhasebe</li><li>Konum (izinle) — en yakın şube, \"Geldim\" tetikleme</li><li>Süt ve alerjen tercihleri — sipariş doğruluğu</li><li>Franchise başvuru bilgileri — değerlendirme ve iletişim</li></ul>","<h2>Hukuki sebepler</h2><p>Sözleşmenin kurulması ve ifası, meşru menfaat, açık rıza (pazarlama izni, kişiselleştirme).</p>","<h2>Aktarım</h2><p>Ödeme kuruluşları, SMS/e-posta altyapısı, bulut barındırma (Türkiye veri lokasyonu tercih edilir). Yurt dışına aktarımda KVKK m.9 şartları uygulanır.</p>","<h2>Haklarınız</h2><p>KVKK m.11 kapsamında bilgi talep etme, düzeltme, silme, itiraz. Uygulamada Profil → Hesabımı sil ile 30 gün içinde anonimleştirme; mali kayıtlar mevzuat süresince saklanır.</p>"]),
 "cerez": ("Çerez Politikası", ["<h2>Kullanılan çerezler</h2><ul><li>Zorunlu: oturum, güvenlik, dil</li><li>Tercih: son seçilen şube ve filtreler (localStorage)</li><li>Analitik: anonimleştirilmiş kullanım istatistikleri (rıza ile)</li><li>Pazarlama: kampanya ölçümü (rıza ile)</li></ul>","<h2>Yönetim</h2><p>Tarayıcı ayarlarından çerezleri silebilir ve engelleyebilirsiniz. Zorunlu çerezler dışındakiler için açık rıza alınır; rıza her zaman geri alınabilir.</p>"]),
 "kullanici-sozlesmesi": ("Kullanıcı Sözleşmesi", ["<h2>Konu</h2><p>Bu sözleşme Florida Coffee web sitesi ve mobil uygulamasının kullanım şartlarını düzenler.</p>","<h2>Üyelik ve sadakat</h2><p>FloridaDays Club puanları nakde çevrilemez, 12 ay geçerlidir, devredilemez. Seviye son 6 aylık harcamayla belirlenir.</p>","<h2>Ön sipariş</h2><p>Ödeme anında sipariş kesinleşir. Şube kaynaklı iptallerde bedel cüzdana iade edilir. Teslim alınmayan siparişler 15 dakika hatırlatma sonrası sonlandırılır.</p>","<h2>Cüzdan</h2><p>Bakiye yalnızca Florida Coffee şubelerinde ve uygulamada kullanılır; bonus bakiyeler iade kapsamı dışındadır.</p>"]),
 "mesafeli-satis": ("Mesafeli Satış Sözleşmesi", ["<h2>Taraflar</h2><p>Satıcı: Florida Coffee Kahve Gıda San. ve Tic. A.Ş. Alıcı: uygulama üzerinden sipariş veren kullanıcı.</p>","<h2>Konu</h2><p>Uygulama üzerinden ön sipariş edilen içecek, yiyecek ve ürünlerin satışı; şubeden teslim.</p>","<h2>Cayma hakkı</h2><p>Kişiye özel hazırlanan ve çabuk bozulan gıda ürünlerinde cayma hakkı kullanılamaz. Paketli ürünlerde (çekirdek, termos, set) teslimden itibaren 14 gün içinde ambalajı açılmamış ürünler için cayma hakkı vardır.</p>","<h2>Uyuşmazlık</h2><p>Tüketici hakem heyetleri ve tüketici mahkemeleri yetkilidir.</p>"]),
}
for k,(t,secs) in LEGAL.items():
    page(f"/yasal/{k}/", shell(hero("Yasal", t, "Bu metin demo amaçlı taslaktır.", [("Yasal",None),(t,None)]) +
      f'<section class="sec"><div class="wrap prose"><div class="notice">Taslak — yayın öncesi hukuk müşaviri onayı gerekir. Şirket bilgileri sözleşme özetinden alınmıştır.</div>{"".join(secs)}<p style="margin-top:2rem;font-size:.85rem">Son güncelleme: {TODAY}</p></div></section>',
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
