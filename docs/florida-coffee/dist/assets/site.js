"use strict";
const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;
const fmt = n => n.toLocaleString("tr-TR");
const pad = n => String(n).padStart(2,"0");
const hhmm = d => pad(d.getHours()) + ":" + pad(d.getMinutes());
/* Şubeler kendi saat dilimlerinde okunur; ziyaretçi nerede olursa olsun doğru. */
const TZ_TR = "Europe/Istanbul", TZ_ME = "Europe/Podgorica";
const tzOf = b => b.c.includes("Karadağ") ? TZ_ME : TZ_TR;
const zhm = (d, tz) => new Intl.DateTimeFormat("tr-TR", {timeZone:tz, hourCycle:"h23", hour:"2-digit", minute:"2-digit"}).format(d);
const zhours = (d, tz) => { const [h,m] = zhm(d,tz).split(":").map(Number); return h + m/60; };
const zday = (d, tz) => ["Sun","Mon","Tue","Wed","Thu","Fri","Sat"]
  .indexOf(new Intl.DateTimeFormat("en-US", {timeZone:tz, weekday:"short"}).format(d));

/* ---------------- sun times (NOAA / SunCalc core) ---------------- */
function sunTimes(date, lat, lng){
  const rad = Math.PI/180, dayMs = 864e5, J1970 = 2440588, J2000 = 2451545;
  const toJulian = d => d.valueOf()/dayMs - 0.5 + J1970;
  const fromJulian = j => new Date((j + 0.5 - J1970) * dayMs);
  const toDays = d => toJulian(d) - J2000;
  const e = rad * 23.4397;
  const M = d => rad * (357.5291 + 0.98560028 * d);
  const L = m => { const C = rad*(1.9148*Math.sin(m) + 0.02*Math.sin(2*m) + 0.0003*Math.sin(3*m)); return m + C + rad*102.9372 + Math.PI; };
  const dec = l => Math.asin(Math.sin(e) * Math.sin(l));
  const lw = rad * -lng, phi = rad * lat, d = toDays(date);
  const n = Math.round(d - 0.0009 - lw/(2*Math.PI));
  const ds = 0.0009 + lw/(2*Math.PI) + n;
  const m = M(ds), l = L(m), dc = dec(l);
  const Jnoon = J2000 + ds + 0.0053*Math.sin(m) - 0.0069*Math.sin(2*l);
  const h = rad * -0.833;
  const w = Math.acos((Math.sin(h) - Math.sin(phi)*Math.sin(dc)) / (Math.cos(phi)*Math.cos(dc)));
  const dsSet = 0.0009 + (w + lw)/(2*Math.PI) + n;
  const Jset = J2000 + dsSet + 0.0053*Math.sin(m) - 0.0069*Math.sin(2*l);
  return { set: fromJulian(Jset), rise: fromJulian(Jnoon - (Jset - Jnoon)) };
}

/* ---------------- branches ---------------- */
const F = { manzara:"Manzara", gece:"Gece açık", calisma:"Çalışma alanı", otopark:"Otopark", kahvalti:"Kahvaltı", evcil:"Evcil dostu" };
const B = [
 {id:"kavacik", n:"Kavacık", c:"Beykoz, İstanbul", lat:41.105, lng:29.085, o:8, k:26, f:["manzara","gece","otopark","evcil"], r:"4,8", rev:312, note:"Üst kat terası tam gün batımına bakar. Hafta içi 09:00–11:00 en sakin saat."},
 {id:"beykoz", n:"Beykoz Kelle İbrahim", c:"Beykoz, İstanbul", lat:41.1265, lng:29.087, o:9, k:26, f:["manzara","gece","kahvalti","evcil"], r:"4,6", rev:198, note:"Sahil hattında, geç saatlere kadar açık. Hafta sonu kahvaltı 09:00–13:00."},
 {id:"cengelkoy", n:"Çengelköy", c:"Üsküdar, İstanbul · merkez", lat:41.0533, lng:29.0553, o:8, k:23, f:["manzara","kahvalti"], r:"4,7", rev:540, note:"İlk şubemiz. Cupping akşamları burada yapılır."},
 {id:"kadikoy", n:"Kadıköy", c:"Kadıköy, İstanbul", lat:40.99, lng:29.027, o:8, k:25, f:["calisma","gece"], r:"4,5", rev:421, note:"Her masada priz, üst katta sessiz çalışma bölgesi."},
 {id:"talimhane", n:"Taksim Talimhane", c:"Beyoğlu, İstanbul", lat:41.038, lng:28.982, o:7.5, k:25, f:["gece"], r:"4,4", rev:260, note:"Otellere yakın; sabah 07:30'da açılır."},
 {id:"taksim", n:"Taksim Meydan", c:"Beyoğlu, İstanbul", lat:41.037, lng:28.986, o:7.5, k:26, f:["gece"], r:"4,3", rev:305, note:"Gece ikiye kadar açık; ayaküstü servis hızlıdır."},
 {id:"bahcesehir", n:"Bahçeşehir", c:"Başakşehir, İstanbul", lat:41.07, lng:28.67, o:8, k:23, f:["calisma","otopark","kahvalti"], r:"4,6", rev:150, note:"Geniş otopark, aile masaları ve çocuk köşesi."},
 {id:"umraniye", n:"Ümraniye", c:"Ümraniye, İstanbul", lat:41.023, lng:29.116, o:8, k:23, f:["calisma","otopark"], r:"4,5", rev:98, note:"Ofis bölgesinde; öğle arası 12:30–13:30 yoğun."},
 {id:"esenyurt", n:"Esenyurt", c:"Esenyurt, İstanbul", lat:41.029, lng:28.67, o:8.5, k:23, f:["otopark"], r:"4,2", rev:77, note:"Cadde üstü, hızlı servis odaklı."},
 {id:"izmit", n:"İzmit Yahyakaptan", c:"Kocaeli", lat:40.772, lng:29.94, o:8, k:23.5, f:["calisma","otopark"], r:"4,4", rev:210, note:"Parkın karşısında; hafta sonu terası açık."},
 {id:"sakarya", n:"Sakarya Çark Caddesi", c:"Adapazarı", lat:40.78, lng:30.4, o:8, k:24, f:["calisma","kahvalti"], r:"4,6", rev:132, note:"Üniversiteye yakın; sınav dönemi gece yarısına kadar açık."},
 {id:"bursa", n:"Bursa Nilüfer", c:"Bursa", lat:40.21, lng:28.96, o:8, k:23, f:["calisma","otopark"], r:"4,5", rev:88, note:"Bulvar üstü, geniş iç mekân."},
 {id:"samsun", n:"Samsun Marina", c:"Atakum", lat:41.34, lng:36.24, o:8, k:24, f:["manzara","kahvalti","otopark"], r:"4,6", rev:140, note:"Marinaya bakar; gün batımı denizin üstünde."},
 {id:"rize", n:"Rize", c:"Rize merkez", lat:41.02, lng:40.52, o:8, k:23, f:["manzara"], r:"4,7", rev:54, note:"Sahil yolunda; çay ile kahveyi aynı menüde tutuyoruz."},
 {id:"erzincan", n:"Erzincan", c:"Erzincan merkez", lat:39.75, lng:39.5, o:8.5, k:22.5, f:["calisma"], r:"4,5", rev:41, note:"Şehrin ilk üçüncü dalga kahvecisi."},
 {id:"podgorica", n:"Podgorica", c:"Karadağ", lat:42.44, lng:19.26, o:8, k:22, f:["calisma"], r:"4,7", rev:66, note:"Karadağ'daki ilk şubemiz. Menü EN/ME."},
 {id:"budva", n:"Budva", c:"Karadağ · sahil", lat:42.29, lng:18.84, o:8, k:25, f:["manzara","gece"], r:"4,8", rev:120, note:"Adriyatik kıyısında; yaz aylarında gece bire kadar."}
];
const DAYS = ["Pazar","Pazartesi","Salı","Çarşamba","Perşembe","Cuma","Cumartesi"];
const hourStr = h => pad(Math.floor(h)%24) + ":" + pad(Math.round((h%1)*60));
function isOpen(b, now){
  const h = zhours(now, tzOf(b));
  const close = b.k;                       // may exceed 24 (past midnight)
  if (h >= b.o && h < Math.min(close,24)) return true;
  if (close > 24 && h < close - 24) return true;   // early morning tail
  return false;
}


/* ---------- logo canlandırma ---------- */
(() => {
  const marks = [...document.querySelectorAll(".mark")];
  if (!reduce && matchMedia("(pointer:fine)").matches) {
    let raf = 0, px = 0, py = 0;
    addEventListener("pointermove", e => { px = e.clientX; py = e.clientY; if (!raf) raf = requestAnimationFrame(look); }, {passive:true});
    function look(){ raf = 0; for (const m of marks) { const r = m.getBoundingClientRect(); if (!r.width) continue;
      const cx = r.left + r.width * .616, cy = r.top + r.height * .408, dx = px - cx, dy = py - cy, d = Math.hypot(dx, dy) || 1, k = Math.min(1, d / 240) * 4.2;
      m.style.setProperty("--ex", (dx / d * k).toFixed(2)); m.style.setProperty("--ey", (dy / d * k).toFixed(2)); } }
  }
  // kayan şerit: şube adları
  const mq = document.getElementById("marq");
  if (mq && typeof B !== "undefined") {
    const dot = marks[0] ? marks[0].outerHTML.replace(/class="mark[^"]*"/, 'class="mark"') : "·";
    const seq = B.map(b => `<span>${b.n}${dot}</span>`).join("");
    mq.innerHTML = seq + seq;
  }
  // sayaçlar
  const cnt = [...document.querySelectorAll("[data-count]")];
  if (cnt.length) {
    const run = el => { const to = +el.dataset.count, t0 = performance.now(), dur = reduce ? 0 : 1400;
      const step = t => { const p = Math.min(1, (t - t0) / (dur || 1)), e = 1 - Math.pow(1 - p, 3); el.textContent = Math.round(to * e); if (p < 1) requestAnimationFrame(step); };
      requestAnimationFrame(step); };
    const io = new IntersectionObserver(es => es.forEach(x => { if (x.isIntersecting) { run(x.target); io.unobserve(x.target); } }), {threshold:.4});
    cnt.forEach(el => io.observe(el));
  }
})();
// hero: iki klip, uzun çapraz geçiş — yalnız üstteki katman içeri solar; altta kalan opak kalır ki sabit görsel araya sızmasın
document.querySelectorAll(".ph").forEach(fig => {
  const v = [...fig.querySelectorAll("video")]; if (v.length !== 2 || reduce) return;
  let cur = 0, busy = false;
  const startOf = el => +el.dataset.start || 0;
  const fadeOf = el => Math.min(3, (el.duration || 8) / 2.5);
  v[1].classList.add("out"); v[1].addEventListener("loadedmetadata", () => { v[1].currentTime = startOf(v[1]); }, {once:true});
  const swap = i => {
    if (i !== cur || busy) return;
    busy = true; const el = v[i], n = v[1 - i], FADE = fadeOf(el);
    el.classList.remove("top"); n.classList.add("top", "out");
    if (Math.abs(n.currentTime - startOf(n)) > .3) n.currentTime = startOf(n);
    n.play().then(() => { requestAnimationFrame(() => n.classList.remove("out")); cur = 1 - i;
      setTimeout(() => { el.classList.add("out"); el.pause(); el.currentTime = startOf(el); busy = false; if (n.ended) swap(1 - i); }, FADE * 1000 + 150);
    }).catch(() => { n.classList.remove("top"); el.currentTime = startOf(el); el.play(); busy = false; });
  };
  v.forEach((el, i) => {
    el.addEventListener("timeupdate", () => { if (el.duration && el.currentTime >= el.duration - fadeOf(el)) swap(i); });
    el.addEventListener("ended", () => swap(i));
  });
});
/* ---------- /logo canlandırma ---------- */

/* ---------- logo canlandırma ---------- */
(() => {
  const marks = [...document.querySelectorAll(".mark")];
  if (!reduce && matchMedia("(pointer:fine)").matches) {
    let raf = 0, px = 0, py = 0;
    addEventListener("pointermove", e => { px = e.clientX; py = e.clientY; if (!raf) raf = requestAnimationFrame(look); }, {passive:true});
    function look(){ raf = 0; for (const m of marks) { const r = m.getBoundingClientRect(); if (!r.width) continue;
      const cx = r.left + r.width * .616, cy = r.top + r.height * .408, dx = px - cx, dy = py - cy, d = Math.hypot(dx, dy) || 1, k = Math.min(1, d / 240) * 4.2;
      m.style.setProperty("--ex", (dx / d * k).toFixed(2)); m.style.setProperty("--ey", (dy / d * k).toFixed(2)); } }
  }
  // kayan şerit: şube adları
  const mq = document.getElementById("marq");
  if (mq && typeof B !== "undefined") {
    const dot = marks[0] ? marks[0].outerHTML.replace(/class="mark[^"]*"/, 'class="mark"') : "·";
    const seq = B.map(b => `<span>${b.n}${dot}</span>`).join("");
    mq.innerHTML = seq + seq;
  }
  // sayaçlar
  const cnt = [...document.querySelectorAll("[data-count]")];
  if (cnt.length) {
    const run = el => { const to = +el.dataset.count, t0 = performance.now(), dur = reduce ? 0 : 1400;
      const step = t => { const p = Math.min(1, (t - t0) / (dur || 1)), e = 1 - Math.pow(1 - p, 3); el.textContent = Math.round(to * e); if (p < 1) requestAnimationFrame(step); };
      requestAnimationFrame(step); };
    const io = new IntersectionObserver(es => es.forEach(x => { if (x.isIntersecting) { run(x.target); io.unobserve(x.target); } }), {threshold:.4});
    cnt.forEach(el => io.observe(el));
  }
})();
// hero: iki klip, uzun çapraz geçiş — yalnız üstteki katman içeri solar; altta kalan opak kalır ki sabit görsel araya sızmasın
document.querySelectorAll(".ph").forEach(fig => {
  const v = [...fig.querySelectorAll("video")]; if (v.length !== 2 || reduce) return;
  let cur = 0, busy = false;
  const startOf = el => +el.dataset.start || 0;
  const fadeOf = el => Math.min(3, (el.duration || 8) / 2.5);
  v[1].classList.add("out"); v[1].addEventListener("loadedmetadata", () => { v[1].currentTime = startOf(v[1]); }, {once:true});
  const swap = i => {
    if (i !== cur || busy) return;
    busy = true; const el = v[i], n = v[1 - i], FADE = fadeOf(el);
    el.classList.remove("top"); n.classList.add("top", "out");
    if (Math.abs(n.currentTime - startOf(n)) > .3) n.currentTime = startOf(n);
    n.play().then(() => { requestAnimationFrame(() => n.classList.remove("out")); cur = 1 - i;
      setTimeout(() => { el.classList.add("out"); el.pause(); el.currentTime = startOf(el); busy = false; if (n.ended) swap(1 - i); }, FADE * 1000 + 150);
    }).catch(() => { n.classList.remove("top"); el.currentTime = startOf(el); el.play(); busy = false; });
  };
  v.forEach((el, i) => {
    el.addEventListener("timeupdate", () => { if (el.duration && el.currentTime >= el.duration - fadeOf(el)) swap(i); });
    el.addEventListener("ended", () => swap(i));
  });
});

const MENU = {
  sicak: [
    ["Florida Filtre","Günün çekirdeği · filtre","120",["5 kcal","95 mg kafein","sütsüz","vegan"]],
    ["Espresso","14 g double shot · 18–23 sn","95",["3 kcal","85 mg kafein","sütsüz","vegan"]],
    ["Americano","Çift shot, sıcak su","115",["8 kcal","170 mg","sütsüz","vegan"]],
    ["Flat White","Çift shot, ince süt dokusu","150",["140 kcal","180 mg"]],
    ["Cortado","Tek shot, eşit süt","130",["70 kcal","75 mg"]],
    ["Cappuccino","Çift shot, bol köpük","145",["150 kcal","170 mg"]],
    ["Latte","Çift shot, sıcak süt","150",["190 kcal","170 mg"]],
    ["Türk Kahvesi","7 g, közde, lokum ile","95",["25 kcal","65 mg","sütsüz"]]
  ],
  soguk: [
    ["Cold Brew","16 saat demleme","145",["25 kcal","200 mg","sütsüz","vegan"]],
    ["Boğaz Cold Brew","Tonik ve portakal kabuğu ile · Kavacık, Beykoz","165",["60 kcal","200 mg","sütsüz","vegan"]],
    ["Iced Latte","Espresso, soğuk süt, buz","160",["150 kcal","150 mg"]],
    ["Iced Americano","Çift shot, buzlu su","125",["10 kcal","170 mg","sütsüz","vegan"]],
    ["Iced White Mocha","Beyaz çikolata sosu ile","185",["320 kcal","150 mg"]],
    ["Frappe","Blender, kremalı","175",["290 kcal","120 mg"]]
  ],
  diger: [
    ["Matcha Latte","Tören sınıfı matcha","165",["180 kcal","70 mg"]],
    ["Sıcak Çikolata","%55 bitter","150",["280 kcal","kafeinsiz"]],
    ["Chai Latte","Ev yapımı baharat konsantresi","155",["210 kcal","40 mg"]],
    ["Ev Limonatası","Taze sıkım, naneli","110",["90 kcal","kafeinsiz","vegan","sütsüz"]],
    ["Demleme Çay","Rize · bardak","65",["0 kcal","30 mg","vegan","sütsüz"]]
  ],
  yiyecek: [
    ["Kavacık Kahvaltı Tabağı","İki kişilik · 09:00–13:00","690",["kahvaltı"]],
    ["Tereyağlı Kruvasan","Günlük üretim","95",["glüten","süt"]],
    ["San Sebastian","Dilim","185",["yumurta","süt"]],
    ["Fıstıklı Cheesecake","Dilim","195",["fıstık","süt"]],
    ["Avokadolu Ekşi Maya","Yumurta ilaveli","265",["glüten"]],
    ["Glütensiz Brownie","Vegan","145",["vegan","glütensiz"]]
  ]
};
const kcalOf = tags => { const t = tags.find(x => /kcal/.test(x)); return t ? parseInt(t) : 999; };
const cafOf = tags => { if (tags.some(x => /kafeinsiz/.test(x))) return 0; const t = tags.find(x => /mg/.test(x)); return t ? parseInt(t) : 0; };

/* nav aktif */
document.querySelectorAll(".navlinks a").forEach(a => { if (location.pathname.startsWith(a.getAttribute("href")) && a.getAttribute("href") !== "/") a.setAttribute("aria-current","page"); });
/* şube canlı durumu */
document.querySelectorAll("[data-branch]").forEach(el => { const b = B.find(x => x.id === el.dataset.branch); if (!b) return; const now = new Date(), open = isOpen(b, now);
  el.innerHTML = `<span class="dot-s ${open?"g":"r"}"></span> ${open ? "Şu an açık" : "Şu an kapalı"}` + (b.f.includes("manzara") ? ` · gün batımı ${zhm(sunTimes(now,b.lat,b.lng).set, tzOf(b))}` : ""); });
/* formlar (demo) */
document.querySelectorAll("form.f").forEach(f => f.addEventListener("submit", e => { e.preventDefault(); const ok = f.querySelector(".ok"); if (ok) ok.hidden = false; f.querySelectorAll("input,textarea").forEach(i => i.value = ""); }));
/* menü filtreleri */
const ml = document.getElementById("mlist");
if (ml) {
  let cat = document.querySelector("#mcats [aria-pressed=true]")?.dataset.c || "sicak", diet = "";
  const passDiet = tags => !diet || (diet==="hafif" ? kcalOf(tags)<100 : diet==="vegan" ? tags.includes("vegan") : diet==="sutsuz" ? (tags.includes("sütsüz")||tags.includes("vegan")) : diet==="azkafein" ? cafOf(tags)<80 : diet==="glutensiz" ? !tags.includes("glüten") : true);
  const slug = s => s.toLowerCase().replace(/[çğıöşüâî]/g, c => ({"ç":"c","ğ":"g","ı":"i","ö":"o","ş":"s","ü":"u","â":"a","î":"i"})[c]).replace(/[^a-z0-9]+/g,"-").replace(/^-|-$/g,"");
  const render = () => { const items = MENU[cat].filter(([,,,t]) => passDiet(t)); ml.innerHTML = items.length ? items.map(([n,d,p,t]) => `<a class="mitem" href="/menu/${slug(n)}/"><span class="n">${n}</span><span class="p">${p} ₺</span><span class="d">${d}</span><span class="tags">${t.filter(x=>x!=="sütsüz"||diet==="sutsuz").map(x=>`<span class="tg ${/vegan|glütensiz|kafeinsiz/.test(x)?"v":/kafein|mg/.test(x)?"c":""}">${x}</span>`).join("")}</span></a>`).join("") : `<p style="padding:1rem 0">Bu filtrede ürün yok.</p>`; };
  document.querySelectorAll("#mcats .mcat").forEach(b => b.addEventListener("click", () => { document.querySelectorAll("#mcats .mcat").forEach(x=>x.setAttribute("aria-pressed","false")); b.setAttribute("aria-pressed","true"); cat = b.dataset.c; render(); }));
  document.querySelectorAll("#dietF .mcat").forEach(b => b.addEventListener("click", () => { document.querySelectorAll("#dietF .mcat").forEach(x=>x.setAttribute("aria-pressed","false")); b.setAttribute("aria-pressed","true"); diet = b.dataset.d; render(); }));
  render();
}
/* şube bulucu */
const bl = document.getElementById("branches");
if (bl) {
  const F2 = {manzara:"Manzara",gece:"Gece açık",calisma:"Çalışma alanı",otopark:"Otopark",kahvalti:"Kahvaltı",evcil:"Evcil dostu"};
  const active = new Set();
  const render = () => { const now = new Date(); const list = B.filter(b => [...active].every(f => f==="acik" ? isOpen(b,now) : b.f.includes(f)));
    document.getElementById("fcount").textContent = list.length + " / " + B.length + " şube";
    bl.innerHTML = list.map(b => { const open = isOpen(b,now); return `<a class="cell" href="/subeler/${b.id}/"><div style="display:flex;justify-content:space-between;gap:.5rem"><h3>${b.n}</h3><span style="font-size:.78rem;color:${open?"var(--ok)":"var(--ink-3)"}">${open?"Açık":"Kapalı"}</span></div><p>${b.c} · ${hourStr(b.o)}–${hourStr(b.k)} · ★ ${b.r}</p>${b.f.includes("manzara")?`<p style="color:var(--amber)">Gün batımı ${zhm(sunTimes(now,b.lat,b.lng).set,tzOf(b))}</p>`:""}<div style="display:flex;gap:.3rem;flex-wrap:wrap">${b.f.map(f=>`<span class="chip">${F2[f]}</span>`).join("")}</div><span class="more">Şube sayfası →</span></a>`; }).join(""); };
  document.querySelectorAll("#filters .fbtn").forEach(btn => btn.addEventListener("click", () => { const f = btn.dataset.f, on = btn.getAttribute("aria-pressed")==="true"; btn.setAttribute("aria-pressed", String(!on)); on ? active.delete(f) : active.add(f); render(); }));
  render();
}
/* haber filtreleri */
const nl = document.getElementById("news");
if (nl) { document.querySelectorAll("#tazeF .fbtn").forEach(b => b.addEventListener("click", () => { document.querySelectorAll("#tazeF .fbtn").forEach(x=>x.setAttribute("aria-pressed","false")); b.setAttribute("aria-pressed","true"); const t = b.dataset.t; nl.querySelectorAll("[data-t]").forEach(el => el.hidden = !(t==="hepsi" || el.dataset.t===t)); })); }
/* franchise hesaplayıcı */
const fC = document.getElementById("fCity");
if (fC) { const fmt = n => n.toLocaleString("tr-TR"); const calc = () => { const city=+fC.value, m2=+document.getElementById("fM2").value, rev=+document.getElementById("fRev").value;
  document.getElementById("fM2v").textContent=m2; document.getElementById("fRevv").textContent=fmt(rev);
  const inv=Math.round((m2*28000*city+900000)/50000)*50000, roy=rev*0.05*1.2, ad=rev*0.01, margin=rev*0.22-roy-ad;
  document.getElementById("oInv").textContent=fmt(inv)+" ₺"; document.getElementById("oRoy").textContent=fmt(Math.round(roy))+" ₺"; document.getElementById("oAd").textContent="≤ "+fmt(Math.round(ad))+" ₺"; document.getElementById("oPb").textContent=margin>0?Math.round(inv/margin)+"–"+Math.round(inv/margin*1.4)+" ay":"—"; };
  ["fCity","fM2","fRev"].forEach(id => document.getElementById(id).addEventListener("input", calc)); calc(); }
/* ================= FLO — Florida Coffee'nin tukanı (kural tabanlı demo motoru) ================= */
const floEl = document.getElementById("flo"), fab = document.getElementById("floFab"), msgs = document.getElementById("floMsgs"),
      quick = document.getElementById("floQuick"), floIn = document.getElementById("floIn"), floHint = document.getElementById("floHint");
const norm = t => t.toLowerCase().replace(/i̇/g,"i").replace(/[^a-zçğıöşü0-9 ]/g," ").replace(/\s+/g," ").trim();
const has = (t, ...ws) => ws.some(w => t.includes(w));
const fmtTL = n => n.toLocaleString("tr-TR") + " ₺";
const store = { get(k){ try{ return JSON.parse(localStorage.getItem("flo:"+k)); }catch(e){ return null; } }, set(k,v){ try{ localStorage.setItem("flo:"+k, JSON.stringify(v)); }catch(e){} } };
let lead = null;  // aktif lead akışı

function bubble(text, dir="in", chips){
  const d = document.createElement("div"); d.className = "msg " + dir; d.innerHTML = text; msgs.appendChild(d); msgs.scrollTop = msgs.scrollHeight;
  setQuick(chips || []); return d;
}
function setQuick(list){ quick.innerHTML = ""; list.forEach(([label, send]) => { const b = document.createElement("button"); b.type = "button"; b.textContent = label; b.onclick = () => userSays(send || label); quick.appendChild(b); }); }
function say(text, chips){ return new Promise(r => { const t = document.createElement("div"); t.className = "typing"; t.textContent = "Flo yazıyor…"; msgs.appendChild(t); msgs.scrollTop = msgs.scrollHeight;
  setTimeout(() => { t.remove(); bubble(text, "in", chips); r(); }, reduce ? 120 : 420 + Math.min(900, text.length * 6)); }); }

/* --- bilgi tabanı --- */
const MENU_ALL = Object.entries(MENU).flatMap(([cat, arr]) => arr.map(([n,d,p,tags]) => ({cat, n, d, p:+p, tags})));
const findProduct = t => MENU_ALL.find(x => t.includes(norm(x.n))) || MENU_ALL.find(x => norm(x.n).split(" ").some(w => w.length > 3 && t.includes(w)));
const findBranch = t => B.find(b => t.includes(norm(b.n))) || B.find(b => norm(b.n).split(" ").some(w => w.length > 4 && t.includes(w)));
const branchLine = b => { const now = new Date(), open = isOpen(b, now), ss = zhm(sunTimes(now, b.lat, b.lng).set, tzOf(b));
  return `<b>${b.n}</b> · ${b.c}\n${open ? "Şu an açık" : "Şu an kapalı"} · ${hourStr(b.o)}–${hourStr(b.k)}${b.f.includes("manzara") ? ` · gün batımı ${ss}` : ""}\n${b.note}`; };
const DEFAULT_CHIPS = [["En yakın şube"],["Menü ve fiyatlar"],["Franchise almak istiyorum","franchise"],["Kahveniz neden aynı?","standart"],["Sadakat kartı"]];

const INTENTS = [
 { id:"selam", test:t => has(t,"merhaba","selam","hey","günaydın","iyi akşamlar","naber"),
   reply:() => ["Merhaba! Ben <b>Flo</b>, Florida Coffee'nin tukanı. Şube, menü, sadakat ve franchise konularında yanınızdayım. Ne lazım?", DEFAULT_CHIPS] },
 { id:"franchise", test:t => has(t,"franchise","bayilik","bayi","yatırım","şube açmak","dükkan açmak","işletme açmak","ortak olmak"),
   reply:() => ["Kendi şehrinizde bir Florida — harika. Kısa özet:\n• <b>3 km bölge koruması</b>, 10 yıl sözleşme\n• <b>45 gün eğitim</b>: 30 gün işletme + 15 gün barista\n• Merkezi tedarik, 40 gün vade\n• Royalty ciro %5 + KDV, ulusal reklam en fazla %1\n• Web sitesi, uygulama ve raporlama paneli dahil\n\nİsterseniz 2 dakikada ön başvurunuzu alayım; ekibimiz 24 saat içinde arar.",
     [["Başvuruyu başlat","lead"],["Yatırım ne kadar?","yatırım tutarı"],["Hangi şehirler açık?","açık şehirler"]]] },
 { id:"yatirim", test:t => has(t,"yatırım tutarı","ne kadar yatırım","maliyet","bütçe ne","kaç para","giriş bedeli"),
   reply:() => ["Kuruluş yatırımı konuma ve metrekareye göre değişir; büyükşehir caddesinde 100–120 m² için örnek hesap <b>3,5–4,5 M ₺</b> bandında çıkıyor. Sayfadaki hesaplayıcı canlı bir tablo verir; kesin rakam keşif görüşmesinde.",
     [["Hesaplayıcıya git","#franchise"],["Başvuruyu başlat","lead"]]] },
 { id:"sehirler", test:t => has(t,"açık şehir","hangi şehir","nereler açık","bölge"),
   reply:() => ["Öncelikli bölgelerimiz: <b>Eskişehir, Ankara Çayyolu, İzmir Alsancak, Antalya Lara, Trabzon, Konya</b>; yurt dışında Saraybosna ve Tiran. Mevcut 17 şubemizin 3 km çevresi korumalı, o yüzden çakışma kontrolünü başvuruda otomatik yapıyoruz.",
     [["Başvuruyu başlat","lead"],["Şubeleri gör","#subeler"]]] },
 { id:"lead", test:t => t === "lead" || has(t,"başvur","başvuru","kaydımı al","aramanızı istiyorum"),
   reply:() => { lead = {step:0, data:{}}; return ["Süper. Dört kısa soru. <b>Adınız ve soyadınız?</b>", []]; } },
 { id:"insan", test:t => has(t,"insan","yetkili","gerçek biri","müşteri hizmet","şikayet","sorun yaşadım"),
   reply:() => ["Anlıyorum. Sizi bir insana aktarıyorum; telefon numaranızı yazarsanız 1 saat içinde ararız. İsterseniz burada da anlatın, kaydı açıp şube müdürüne iletirim.", [["Numaramı bırakayım","lead"],["Burada anlatacağım","şikayetimi yazacağım"]]] },
 { id:"sikayet2", test:t => has(t,"şikayetimi yazacağım"), reply:() => ["Dinliyorum. Hangi şube ve ne oldu? Yazdığınız her şey kayıt numarasıyla HQ kalite ekibine gider.", []] },
 { id:"yakin", test:t => has(t,"en yakın","yakınımda","nerede","yakın şube","konum"),
   reply:() => { const b = B[0]; return [`Konum izni olmadan tahminim <b>${b.n}</b>:\n${branchLine(b)}\n\nBaşka bir semt söyleyin, oradaki şubeyi anlatayım.`, [["Beykoz"],["Kadıköy"],["Sakarya"],["Tüm şubeler","#subeler"]]]; } },
 { id:"sube", test:t => !!findBranch(t) || has(t,"şube","saat","kaça kadar","açık mı","kapalı mı","gün batımı"),
   reply:t => { const b = findBranch(t); if (b) return [branchLine(b), [["Yol tarifi","#subeler"],["Ön sipariş","#sabah"],["Başka şube"]]];
     const now = new Date(), open = B.filter(x => isOpen(x, now)).length; return [`Şu an <b>${open}/${B.length}</b> şubemiz açık. Hangi semtteydiniz? Kavacık, Beykoz, Çengelköy, Kadıköy, Taksim, Bahçeşehir, Ümraniye, Esenyurt, İzmit, Sakarya, Bursa, Samsun, Rize, Erzincan, Podgorica, Budva.`, [["Kavacık"],["Kadıköy"],["Sakarya"]]]; } },
 { id:"manzara", test:t => has(t,"manzara","boğaz","teras","gün batımı"),
   reply:() => { const now = new Date(); const v = B.filter(b => b.f.includes("manzara")).map(b => `• <b>${b.n}</b> — gün batımı ${zhm(sunTimes(now,b.lat,b.lng).set, tzOf(b))}${isOpen(b,now) ? "" : " (şu an kapalı)"}`).join("\n");
     return [`Manzaralı şubelerimiz ve bugünkü gün batımı saatleri:\n${v}\n\nPremium üyeler gün batımı için masa ayırabilir.`, [["Kavacık'ı anlat","kavacık"],["Kulüp seviyeleri","sadakat"]]]; } },
 { id:"fiyat", test:t => !!findProduct(t) || has(t,"fiyat","kaç lira","ne kadar","menü","içecek","kahve çeşit"),
   reply:t => { const p = findProduct(t); if (p) return [`<b>${p.n}</b> — ${fmtTL(p.p)} (İstanbul, orta boy)\n${p.d}\n${p.tags.filter(x=>/kcal|mg|kafeinsiz/.test(x)).join(" · ")}\nSüt: inek dahil, laktozsuz +10 ₺, yulaf/badem +15 ₺.`, [["Sipariş ver","#sabah"],["Başka ürün","menü"],["Hafif seçenekler","hafif"]]];
     return ["Menüde 4 kategori var: sıcak kahveler (95–150 ₺), soğuk kahveler (125–185 ₺), kahve dışı ve yiyecek. Bir ürün adı söyleyin, fiyat ve kaloriyi vereyim.", [["Flat White"],["Cold Brew"],["Iced Latte"],["Menüye git","#menu"]]]; } },
 { id:"hafif", test:t => has(t,"hafif","kalori","diyet","şekersiz","vegan","laktoz","sütsüz","glüten","kafeinsiz","az kafein"),
   reply:t => { let list = MENU_ALL; if (has(t,"vegan")) list = list.filter(x=>x.tags.includes("vegan")); else if (has(t,"kafeinsiz","az kafein")) list = list.filter(x=>cafOf(x.tags) < 80); else if (has(t,"glüten")) list = list.filter(x=>!x.tags.includes("glüten")); else if (has(t,"laktoz","sütsüz")) list = list.filter(x=>x.tags.includes("sütsüz")); else list = list.filter(x=>kcalOf(x.tags) < 100);
     const v = list.slice(0,6).map(x=>`• ${x.n} — ${fmtTL(x.p)} · ${x.tags.filter(y=>/kcal/.test(y))[0]||""}`).join("\n"); return [`Size uyanlar:\n${v}\n\nLaktoz için laktozsuz, yulaf ve badem sütü her şubede var; tercihiniz uygulama profilinize kaydedilir.`, [["Menüde filtrele","#menu"],["Sipariş ver","#sabah"]]]; } },
 { id:"standart", test:t => has(t,"standart","aynı","kalite","neden","doz","gram","shot","süt sıcaklığı","bar","kavurma","çekirdek","nereden"),
   reply:() => ["Her şubede aynı fincan, çünkü reçete kişisel yoruma açık değil:\n• Doz <b>14 g</b> double shot, tartıyla\n• Su <b>90–96 °C</b>, basınç <b>9 bar</b>\n• Shot <b>18–23 sn</b>, çıktı 30–60 g\n• Süt <b>60–65 °C</b> mikro köpük\n• Shot öncesi zorunlu 5 adım\nHarman: Etiyopya Yirgacheffe %60, Brezilya Cerrado %40, orta kavurma.", [["5 adım nedir?","beş adım"],["Kahve kuşağı","kuşak"],["Bölüme git","#kahvemiz"]]] },
 { id:"besadim", test:t => has(t,"beş adım","5 adım"),
   reply:() => ["Shot öncesi zorunlu 5 adım:\n1. Grup başlığı flush — 2–3 sn su, kalıntı temizlenir\n2. Portafiltre temizlenir, sepet kuru\n3. Gramaj tartılır — 14 g, göz kararı yok\n4. Tamp — eşit basınç, düz yüzey\n5. Süre — kronometre, 18–23 sn\nBirini atlamak zincir standardına aykırı.", [["Kavurma","kavurma"],["Menü","menü"]]] },
 { id:"kusak", test:t => has(t,"kuşak","etiyopya","brezilya","afrika","latin","asya","asidite"),
   reply:() => ["Kahve kuşağı üç karakter verir:\n• <b>Latin Amerika</b> — denge, fındık, kakao, karamel; espresso için en stabil\n• <b>Afrika</b> — aroma ve canlı asidite, çiçeksi, meyvemsi; filtre için\n• <b>Asya-Pasifik</b> — gövde, topraksı, bitter çikolata; sert içim\nHarmanımız Latin Amerika + Afrika.", [["Standartlar","standart"],["Ürünler","#urunler"]]] },
 { id:"sadakat", test:t => has(t,"sadakat","kart","puan","çekirdek kazan","kulüp","club","seviye","premium","plus","damga","ücretsiz kahve","bedava"),
   reply:() => ["<b>FloridaDays Club</b>:\n• 1 ₺ = 1 çekirdek, 10 içecekte biri bizden\n• Seviye son 6 ay harcamayla: Classic (0–2.500 ₺), Plus (2.500–7.500 ₺), Premium (7.500 ₺+)\n• Plus: ayda 2 boy yükseltme · Premium: ücretsiz ekstra shot, gün batımında masa önceliği\n• Fiziksel kartınızı tek taramayla uygulamaya aktarın\nÖdeme + puan tek QR.", [["Kartı nasıl aktarırım?","kart aktar"],["Uygulama","#kulup"]]] },
 { id:"kartaktar", test:t => has(t,"kart aktar","aktar","taşı"),
   reply:() => ["Uygulamada <b>Kart → Kartımı tara</b>: karttaki kodu okutun, damgalar ve bakiye anında hesabınıza geçer. Kart sonra da çalışır; ikisi tek hesaptır.", [["Uygulamayı indir","#kulup"]]] },
 { id:"siparis", test:t => has(t,"sipariş","ön sipariş","geldim","sıra","beklemek","teslim","kurye","yemeksepeti","getir"),
   reply:() => ["Ön sipariş şöyle çalışır: şube ve içeceği seçin, ödeyin; hazırlık siz <b>\"Geldim\"</b> deyince ya da şubeye 200 m yaklaşınca başlar — kahve soğumaz. Teslimat için Yemeksepeti'ndeyiz; kendi kuryemiz yakında.", [["Nasıl görünüyor?","#sabah"],["En yakın şube","en yakın"]]] },
 { id:"etkinlik", test:t => has(t,"etkinlik","akustik","cupping","konser","müzik","rezervasyon","masa"),
   reply:() => ["Bu hafta:\n• <b>Perşembe 21:00</b> — Akustik set, Kavacık terası (yer ayırma uygulamadan)\n• <b>Ayın ilk Cumartesi'si</b> — Cupping, Çengelköy, 12 kişi, ücretsiz\n• Her gün 22:00 sonrası kafeinsiz filtre aynı fiyat", [["Yer ayır","#gece"],["Premium masa önceliği","sadakat"]]] },
 { id:"urun", test:t => has(t,"satın","eve","paket","termos","hediye kartı","hediye","ürün","kapsül","kargo"),
   reply:() => ["Eve götürebilecekleriniz: <b>Sonbahar Harmanı 250 g</b> (420 ₺), <b>Ev Espresso Seti</b> (1.150 ₺), <b>Florida Termos</b> (650 ₺, kendi bardağınızla %10 indirim) ve <b>dijital hediye kartı</b>. Şu an uygulamadan ön sipariş, şubeden teslim; kargo yakında.", [["Ürünlere git","#urunler"],["Hediye gönder","#kulup"]]] },
 { id:"yeni", test:t => has(t,"yeni","haber","yenilik","kampanya","indirim","açılış"),
   reply:() => ["Taze olanlar: Sakarya'da yeni adres (Şal Sokak), Boğaz Cold Brew sezonu, kart → uygulama kampanyası (ilk kahve bizden), hafta içi 14–16 soğuk kahvelerde %20. Hepsi \"Taze\" bölümünde.", [["Taze bölümü","#taze"],["Haber al","#taze"]]] },
 { id:"iletisim", test:t => has(t,"iletişim","telefon","mail","e-posta","adres","merkez","nerede merkez"),
   reply:() => ["Merkez: Çengelköy Mah. Görgeç Sok. No:6, Üsküdar / İstanbul. Şube telefonları şube kartlarında; franchise için buradan ön başvuru alabilirim.", [["Şubeler","#subeler"],["Franchise","franchise"]]] },
 { id:"kim", test:t => has(t,"kimsin","nesin","flo","tukan","adın"),
   reply:() => ["Ben Flo — logodaki tukan. Florida Coffee'nin şubelerini, menüsünü ve standartlarını bilirim; franchise başvurunuzu da alırım. Gerçek bir insana ihtiyaç olursa aktarırım.", DEFAULT_CHIPS] },
 { id:"tesekkur", test:t => has(t,"teşekkür","sağol","eyvallah","süper","harika"),
   reply:() => ["Ben teşekkür ederim. Mutluluğun tadıyla kalın ☕", DEFAULT_CHIPS] },
];

async function leadStep(t){
  const d = lead.data; const raw = floIn.value || t;
  if (lead.step === 0){ d.name = t.replace(/\b\w/g, c => c.toUpperCase()); lead.step = 1; return say(`Teşekkürler ${d.name.split(" ")[0]}. <b>Telefon numaranız?</b>`); }
  if (lead.step === 1){ const digits = t.replace(/\D/g,""); if (digits.length < 10) return say("Numarayı 05xx xxx xx xx biçiminde yazabilir misiniz?"); d.phone = digits; lead.step = 2; return say("<b>Hangi şehir veya ilçe</b> için düşünüyorsunuz?"); }
  if (lead.step === 2){ d.city = t; lead.step = 3; return say("<b>Yatırım bütçeniz</b> hangi aralıkta?", [["2 M ₺ altı"],["2–4 M ₺"],["4–6 M ₺"],["6 M ₺ üstü"]]); }
  if (lead.step === 3){ d.budget = t; lead.step = 4; return say("Son soru: <b>işletme deneyiminiz</b> var mı?", [["Yok"],["Perakende"],["Kafe / restoran işlettim"],["Franchise sahibiyim"]]); }
  if (lead.step === 4){ d.exp = t;
    const bIdx = ["2 m altı","2 4","4 6","6 m üstü"].findIndex(k => norm(d.budget).includes(k.split(" ")[0]) && (k==="2 m altı"?norm(d.budget).includes("altı"):k==="6 m üstü"?norm(d.budget).includes("üstü"):true));
    const eIdx = ["yok","perakende","kafe","franchise"].findIndex(k => norm(d.exp).includes(k));
    const near = B.find(b => norm(d.city).split(" ").some(w => w.length>3 && norm(b.n+" "+b.c).includes(w)));
    const score = Math.min(97, 40 + Math.max(0,bIdx)*12 + Math.max(0,eIdx)*9 + (near ? 2 : 14));
    d.score = score; d.at = new Date().toISOString(); store.set("lead", d); lead = null;
    return say(`Başvurunuz alındı, ${d.name.split(" ")[0]}. Kayıt <b>#L-${String(Math.floor(1000+Math.random()*9000))}</b>.\n• Bölge: ${d.city}${near ? ` — dikkat: ${near.n} şubemize yakın, 3 km kontrolü yapılır` : " — bölge açık görünüyor"}\n• Ön değerlendirme puanı: <b>${score}/100</b>\n\nFranchise ekibimiz <b>24 saat içinde</b> ${d.phone.replace(/(\d{4})(\d{3})(\d{2})(\d{2})/,"$1 $2 $3 $4")} numarasından arayacak. E-postanıza yatırım özeti ve \"Neden Florida\" videosu gidecek.`, [["Yatırım hesaplayıcı","#franchise"],["Teşekkürler"]]); }
}

async function userSays(text){
  const t0 = text.trim(); if (!t0) return;
  if (t0.startsWith("#")){ closeFlo(); document.querySelector(t0)?.scrollIntoView({behavior: reduce ? "auto" : "smooth"}); return; }
  bubble(t0.replace(/</g,"&lt;"), "out"); floIn.value = "";
  const t = norm(t0);
  if (lead) return leadStep(t0);
  const it = INTENTS.find(i => i.test(t));
  if (it){ const [txt, chips] = it.reply(t); return say(txt, chips); }
  return say("Bunu tam anlayamadım. Şunlardan biri mi?", [["En yakın şube"],["Menü ve fiyatlar"],["Franchise","franchise"],["Sadakat kartı"],["Bir insanla konuşmak istiyorum","insan"]]);
}
function openFlo(){ floEl.hidden = false; fab.setAttribute("aria-expanded","true"); if (!msgs.children.length){
  const now = new Date(), ss = zhm(sunTimes(now, B[0].lat, B[0].lng).set, tzOf(B[0]));
  bubble(`Merhaba! Ben <b>Flo</b>, Florida Coffee'nin tukanı. Bugün Kavacık'ta gün batımı <b>${ss}</b>. Şube, menü, sadakat ya da franchise — ne lazım?`, "in", DEFAULT_CHIPS);
  const prev = store.get("lead"); if (prev) bubble(`Not: daha önce bir franchise ön başvurusu bırakmışsınız (${prev.city}, puan ${prev.score}). Ekibimiz iletişime geçecek.`, "sys"); }
  setTimeout(() => floIn.focus(), 50); }
function closeFlo(){ floEl.hidden = true; fab.setAttribute("aria-expanded","false"); }
fab.addEventListener("click", () => floEl.hidden ? openFlo() : closeFlo());
document.getElementById("floClose").addEventListener("click", closeFlo);
document.getElementById("floForm").addEventListener("submit", e => { e.preventDefault(); userSays(floIn.value); });
addEventListener("keydown", e => { if (e.key === "Escape" && !floEl.hidden) closeFlo(); });


/* bölüm bazlı ipucu balonu: hikâyenin anlatıcısı Flo */
const HINTS = { safak:"Günaydın! Gün batımı {ss}. Sor bana.", sabah:"Sıra beklemeden nasıl olur, anlatayım mı?", kahvemiz:"14 g neden tartılır? Sor.", taze:"Sakarya'da yeni adres var. Detay?", secim:"Karar veremedin mi? Bana söyle.", menu:"Kalori ve alerjen sorabilirsin.", urunler:"Harmanı eve götürmek ister misin?", subeler:"Sana en yakın şubeyi söyleyeyim.", kulup:"Kartını uygulamaya aktarmayı anlatayım.", gece:"Perşembe Kavacık'ta akustik var.", franchise:"Kendi şehrinde Florida? 2 dakikada başvuru.", basvuru:"Franchise başvurusu için buradayım." };
let lastHint = "", hintTimer;
function showHint(id){ if (id === lastHint || !floEl.hidden) return; lastHint = id; const ss = zhm(sunTimes(new Date(), B[0].lat, B[0].lng).set, tzOf(B[0]));
  floHint.textContent = (HINTS[id] || HINTS.safak).replace("{ss}", ss); floHint.classList.add("on"); clearTimeout(hintTimer); hintTimer = setTimeout(() => floHint.classList.remove("on"), 5200); }

showHint(document.body.dataset.page || "safak");
