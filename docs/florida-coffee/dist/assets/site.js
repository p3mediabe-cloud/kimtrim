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
// hero: tek klip, yumuşak döngü — sona yaklaşırken koyu marka rengine kararır, baştan karanlıktan açılır; hafif yavaşlatılmış
document.querySelectorAll("video[data-fadeloop]").forEach(v => {
  if (reduce) return;
  const veil = document.createElement("span"); veil.className = "veil"; veil.setAttribute("aria-hidden", "true"); v.after(veil);
  const rate = +v.dataset.rate || 1, FADE = .9; let arming = false;
  const applyRate = () => { try { v.playbackRate = rate; } catch (e) {} };
  v.addEventListener("loadedmetadata", applyRate); v.addEventListener("play", applyRate); applyRate();
  veil.classList.add("on"); v.addEventListener("playing", () => requestAnimationFrame(() => veil.classList.remove("on")), {once:true});
  v.addEventListener("timeupdate", () => {
    if (arming || !v.duration || v.currentTime < v.duration - FADE * rate) return;
    arming = true; veil.classList.add("on");
  });
  v.addEventListener("ended", () => {
    v.currentTime = 0;
    v.play().then(() => { setTimeout(() => { veil.classList.remove("on"); arming = false; }, 150); })
            .catch(() => { veil.classList.remove("on"); arming = false; });
  });
});
// hero işareti: boş dururken sağa sola bakar, daha sık kırpar, başını hafif eğer
(() => { const hm = document.querySelector(".heromark .mark"); if (!hm || reduce) return; let lastP = 0;
  addEventListener("pointermove", () => { lastP = Date.now(); hm.style.setProperty("--tilt", "0deg"); }, {passive:true});
  (function idle(){ if (Date.now() - lastP > 1800 && !document.hidden) { const ex = (Math.random() * 2 - 1) * 4.2, ey = (Math.random() * 2 - 1) * 2.2; hm.style.setProperty("--ex", ex.toFixed(2)); hm.style.setProperty("--ey", ey.toFixed(2)); hm.style.setProperty("--tilt", (ex * 1.4).toFixed(1) + "deg"); } setTimeout(idle, 700 + Math.random() * 1600); })(); })();
// header: kaydırınca daralır; mobil menü
(() => { const nav = document.querySelector(".nav"); if (!nav) return; let last = -1;
  const onS = () => { const s = scrollY > 40; if (s !== last) { nav.classList.toggle("scrolled", s); last = s; } }; addEventListener("scroll", onS, {passive:true}); onS();
  const bg = document.getElementById("burger"), mn = document.getElementById("mnav"); if (!bg || !mn) return;
  const set = open => { bg.setAttribute("aria-expanded", String(open)); bg.setAttribute("aria-label", open ? "Menüyü kapat" : "Menüyü aç"); mn.hidden = !open; document.body.classList.toggle("menu-open", open); };
  bg.addEventListener("click", () => set(mn.hidden)); mn.querySelectorAll("a").forEach(a => a.addEventListener("click", () => set(false)));
  addEventListener("keydown", e => { if (e.key === "Escape" && !mn.hidden) set(false); });
  addEventListener("resize", () => { if (innerWidth > 720 && !mn.hidden) set(false); });
  if (typeof showToast !== "function") window.showToast = msg => { let t = document.getElementById("toastv7"); if (!t) { t = document.createElement("div"); t.id = "toastv7"; t.className = "toastv7"; t.setAttribute("role","status"); document.body.appendChild(t); } t.textContent = msg; t.classList.add("on"); clearTimeout(t._h); t._h = setTimeout(() => t.classList.remove("on"), 2800); };
})();
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
// hero: tek klip, yumuşak döngü — sona yaklaşırken koyu marka rengine kararır, baştan karanlıktan açılır; hafif yavaşlatılmış
document.querySelectorAll("video[data-fadeloop]").forEach(v => {
  if (reduce) return;
  const veil = document.createElement("span"); veil.className = "veil"; veil.setAttribute("aria-hidden", "true"); v.after(veil);
  const rate = +v.dataset.rate || 1, FADE = .9; let arming = false;
  const applyRate = () => { try { v.playbackRate = rate; } catch (e) {} };
  v.addEventListener("loadedmetadata", applyRate); v.addEventListener("play", applyRate); applyRate();
  veil.classList.add("on"); v.addEventListener("playing", () => requestAnimationFrame(() => veil.classList.remove("on")), {once:true});
  v.addEventListener("timeupdate", () => {
    if (arming || !v.duration || v.currentTime < v.duration - FADE * rate) return;
    arming = true; veil.classList.add("on");
  });
  v.addEventListener("ended", () => {
    v.currentTime = 0;
    v.play().then(() => { setTimeout(() => { veil.classList.remove("on"); arming = false; }, 150); })
            .catch(() => { veil.classList.remove("on"); arming = false; });
  });
});
// hero işareti: boş dururken sağa sola bakar, daha sık kırpar, başını hafif eğer
(() => { const hm = document.querySelector(".heromark .mark"); if (!hm || reduce) return; let lastP = 0;
  addEventListener("pointermove", () => { lastP = Date.now(); hm.style.setProperty("--tilt", "0deg"); }, {passive:true});
  (function idle(){ if (Date.now() - lastP > 1800 && !document.hidden) { const ex = (Math.random() * 2 - 1) * 4.2, ey = (Math.random() * 2 - 1) * 2.2; hm.style.setProperty("--ex", ex.toFixed(2)); hm.style.setProperty("--ey", ey.toFixed(2)); hm.style.setProperty("--tilt", (ex * 1.4).toFixed(1) + "deg"); } setTimeout(idle, 700 + Math.random() * 1600); })(); })();
// header: kaydırınca daralır; mobil menü
(() => { const nav = document.querySelector(".nav"); if (!nav) return; let last = -1;
  const onS = () => { const s = scrollY > 40; if (s !== last) { nav.classList.toggle("scrolled", s); last = s; } }; addEventListener("scroll", onS, {passive:true}); onS();
  const bg = document.getElementById("burger"), mn = document.getElementById("mnav"); if (!bg || !mn) return;
  const set = open => { bg.setAttribute("aria-expanded", String(open)); bg.setAttribute("aria-label", open ? "Menüyü kapat" : "Menüyü aç"); mn.hidden = !open; document.body.classList.toggle("menu-open", open); };
  bg.addEventListener("click", () => set(mn.hidden)); mn.querySelectorAll("a").forEach(a => a.addEventListener("click", () => set(false)));
  addEventListener("keydown", e => { if (e.key === "Escape" && !mn.hidden) set(false); });
  addEventListener("resize", () => { if (innerWidth > 720 && !mn.hidden) set(false); });
  if (typeof showToast !== "function") window.showToast = msg => { let t = document.getElementById("toastv7"); if (!t) { t = document.createElement("div"); t.id = "toastv7"; t.className = "toastv7"; t.setAttribute("role","status"); document.body.appendChild(t); } t.textContent = msg; t.classList.add("on"); clearTimeout(t._h); t._h = setTimeout(() => t.classList.remove("on"), 2800); };
})();


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


/* ---------- v9: aday başvurusu, eşleştirme ve CRM önizlemesi ---------- */
(() => {
  const f = document.getElementById("applyForm"); if (!f || typeof B === "undefined") return;
  const T = m => (typeof showToast === "function") && showToast(m);
  const q = new URLSearchParams(location.search); const pos = q.get("pos"); if (pos) { const sel = f.querySelector("#aPos"); if (sel) [...sel.options].forEach(o => { if (o.textContent === pos) sel.value = pos; }); }
  // şube tercih çipleri (veriden)
  const bp = document.getElementById("aBranches"); bp.innerHTML = B.map(b => `<button type="button" class="pill" data-multi data-id="${b.id}" aria-pressed="false">${b.n}</button>`).join("");
  f.querySelectorAll("[data-multi]").forEach(p => p.addEventListener("click", () => { p.setAttribute("aria-pressed", String(p.getAttribute("aria-pressed") !== "true")); meter(); }));
  f.querySelectorAll("[data-one] .pill").forEach(p => p.addEventListener("click", () => { p.closest("[data-one]").querySelectorAll(".pill").forEach(x => x.setAttribute("aria-pressed", "false")); p.setAttribute("aria-pressed", "true"); meter(); }));
  f.querySelectorAll(".skill input").forEach(r => { const out = r.closest(".skill").querySelector("b"); const u = () => out.textContent = r.value; r.addEventListener("input", () => { u(); meter(); }); u(); });
  const MSG = [[0,"Başlayalım: adınızı yazın, gerisi kolay."],[25,"İyi gidiyor. Tercihleriniz eşleştirmeyi %40 daha isabetli yapar."],[50,"Yarısı bitti. Beceri puanları vardiya liderinin ilk baktığı şey."],[75,"Neredeyse tamam. Tam profil 10 gün içinde deneme vardiyası şansını artırır."],[100,"Profil tam. Gönderin; eşleştirme anında hazır."]];
  function meter(){ const fields = [...f.querySelectorAll("input:not([type=range]):not([type=checkbox]), select, textarea")]; let filled = fields.filter(x => x.value.trim()).length, total = fields.length + 3;
    if (f.querySelectorAll("[data-multi][aria-pressed=true]").length) filled++; if (f.querySelectorAll("[data-one] .pill[aria-pressed=true]").length >= 2) filled++; if (f.querySelector("#aKvkk")?.checked) filled++;
    const p = Math.round(filled / total * 100); document.getElementById("mBar").style.width = p + "%"; document.getElementById("mPct").textContent = p + "%"; document.getElementById("mMsg").textContent = MSG.filter(m => p >= m[0]).slice(-1)[0][1]; }
  f.addEventListener("input", meter); meter();
  f.addEventListener("submit", e => { e.preventDefault();
    const name = f.querySelector("#aName").value.trim().split(" ")[0] || "Aday", city = f.querySelector("#aCity").value, shifts = [...f.querySelectorAll("#aShifts .pill[aria-pressed=true]")].map(x => x.dataset.v), start = f.querySelector("#aStart .pill[aria-pressed=true]")?.dataset.v || "hemen", pref = new Set([...f.querySelectorAll("[data-multi][aria-pressed=true]")].map(x => x.dataset.id)), position = f.querySelector("#aPos").value;
    const skills = Object.fromEntries([...f.querySelectorAll(".skill input")].map(r => [r.dataset.k, +r.value]));
    const scored = B.map(b => { let sc = 20, why = []; if (pref.has(b.id)) { sc += 35; why.push("tercihiniz"); } if (b.c.includes(city)) { sc += 20; why.push(city); } if (shifts.includes("gece") && b.f.includes("gece")) { sc += 12; why.push("gece vardiyası"); } if (shifts.includes("sabah") && b.f.includes("kahvalti")) { sc += 10; why.push("kahvaltı servisi"); } if (shifts.includes("haftasonu") && b.f.includes("manzara")) { sc += 6; why.push("hafta sonu yoğun"); } if (position === "Şube Müdürü" && b.f.includes("calisma")) { sc += 5; } if (skills.espresso >= 4) sc += 4; return { b, sc: Math.min(98, sc), why }; }).sort((x, y) => y.sc - x.sc).slice(0, 3);
    document.getElementById("mName").textContent = name; document.getElementById("mPos").textContent = position;
    document.getElementById("matchList").innerHTML = scored.map(m => `<a href="/subeler/${m.b.id}/"><img src="/img/subeler/${m.b.id}.jpg" alt="" onerror="this.remove()"><div><h3>${m.b.n}</h3><p>${m.b.c} · ${m.why.length ? m.why.join(", ") : "genel uygunluk"} · ${hourStr(m.b.o)}–${hourStr(m.b.k)}</p></div><span class="pct">%${m.sc}</span></a>`).join("");
    const startTxt = { hemen: "Hemen", "2hafta": "2 hafta sonra", "1ay": "1 ay sonra" }[start];
    const top = scored[0].b, second = scored[1]?.b || top;
    const inbox = [{ from: "Flo · İK", when: "bugün 10:12", q: `${name}, ${top.n} şubesinde ${shifts.includes("gece") ? "Perşembe 16:00–00:00" : "Cumartesi 09:00–17:00"} bir deneme vardiyası açıldı. Gelebilir misin?` },
                   { from: "Flo · İK", when: "yarın 09:00", q: `${second.n} için ${position.toLowerCase()} ihtiyacı doğdu; ${startTxt.toLowerCase()} başlayabilir misin?` },
                   { from: "Flo · İK", when: "haftaya", q: "Müsaitlik durumun hâlâ geçerli mi? 'Evet' dersen havuzda öncelikli kalırsın." }];
    let answered = 0; const ib = document.getElementById("inbox"); ib.innerHTML = inbox.map((m, i) => `<div class="msg" data-i="${i}"><div class="from">${m.from}<span>${m.when}</span></div><div class="q">${m.q}</div><div class="acts"><button type="button" class="btn amber sm" data-a="Evet, uygun">Evet</button><button type="button" class="btn ghost sm" data-a="Bu sefer değil">Hayır</button><button type="button" class="btn ghost sm" data-a="2 hafta sonra">2 hafta sonra</button></div><div class="ans" hidden></div></div>`).join("");
    ib.querySelectorAll("[data-a]").forEach(bt => bt.addEventListener("click", () => { const msg = bt.closest(".msg"); msg.classList.add("done"); const a = msg.querySelector(".ans"); a.hidden = false; a.textContent = "Yanıtın: " + bt.dataset.a + " · kayıt altına alındı, şube müdürüne iletildi."; answered++; document.getElementById("kAns").textContent = Math.round(answered / inbox.length * 100) + "%"; document.getElementById("kTime").textContent = "0:" + String(8 + answered * 3).padStart(2, "0"); if (bt.dataset.a.startsWith("Evet")) { T("Şube müdürü bilgilendirildi · takvimine eklendi"); setStatus("busy", "Vardiyaya atandı · " + top.n); } else if (bt.dataset.a.startsWith("2")) setStatus("soon", "2 hafta sonra müsait"); }));
    const setStatus = (k, t) => { const el = document.getElementById("cStatus"); el.className = "cstatus " + k; el.querySelector("span").textContent = t; };
    document.querySelectorAll("[data-status]").forEach(bt => bt.addEventListener("click", () => setStatus(bt.dataset.status, bt.textContent)));
    setStatus(start === "hemen" ? "" : "soon", start === "hemen" ? "Havuzda · müsait" : "Havuzda · " + startTxt.toLowerCase() + " müsait");
    document.getElementById("applyWrap").hidden = true; const done = document.getElementById("applyDone"); done.hidden = false; done.scrollIntoView({ behavior: "smooth", block: "start" }); T("Başvurun alındı, " + name + ". Eşleştirme hazır.");
  });
})();


/* v10: mobilde ürün ızgaralarını daralt/genişlet; filtre veya arama yapılınca hepsi açılır */
(() => { const grids = [...document.querySelectorAll("[data-collapse]")]; if (!grids.length) return;
  const mq = matchMedia("(max-width:640px)");
  grids.forEach(g => { const n = g.children.length, lim = +g.dataset.collapse || 6; if (n <= lim) return; g.classList.add("collapsed"); if (lim === 4) g.classList.add("c4");
    const b = document.createElement("button"); b.type = "button"; b.className = "mmore"; const unit = g.classList.contains("pgrid") ? " ürün" : ""; b.textContent = "Tamamını göster · " + n + unit; g.after(b);
    b.addEventListener("click", () => { const c = g.classList.toggle("collapsed"); b.textContent = c ? "Tamamını göster · " + n + unit : "Daha az göster"; if (c) g.scrollIntoView({block:"start"}); }); });
  const openAll = () => { grids.forEach(g => g.classList.remove("collapsed")); document.querySelectorAll(".mmore").forEach(b => b.hidden = true); };
  const si = document.getElementById("msearch"); if (si) si.addEventListener("input", openAll, {once:true});
  document.querySelectorAll("#dietF .mcat").forEach(b => b.addEventListener("click", openAll, {once:true}));
  const clk = document.querySelectorAll("[data-clock]"); if (clk.length) { const t = () => { const d = new Date(); clk.forEach(e => e.textContent = String(d.getHours()).padStart(2,"0") + ":" + String(d.getMinutes()).padStart(2,"0")); }; t(); setInterval(t, 30000); }
  void mq; })();

(() => { const ns = document.getElementById("navStatus"); if (!ns || typeof B === "undefined") return;
  const paint = () => { const b = B[0], now = new Date(), o = isOpen(b, now); const t = b.n + " · " + (o ? "açık" : "kapalı") + " · gün batımı " + zhm(sunTimes(now, b.lat, b.lng).set, tzOf(b)); ns.querySelector("span").textContent = t; ns.classList.toggle("off", !o); const m = document.getElementById("mnavStatus"); if (m) m.textContent = t; };
  paint(); setInterval(paint, 60000); })();
(() => { const f = document.getElementById("fnews"); if (f) f.addEventListener("submit", e => { e.preventDefault(); showToast("Kaydedildi. Ayda en fazla iki e-posta."); f.reset(); }); })();
const MENU = {
  sicak: [
    ["Florida Filtre","Günün çekirdeği · filtre","120",["5 kcal", "95 mg kafein", "sütsüz", "vegan"]],
    ["V60","Elde demleme · 250 ml · günün çekirdeği","140",["5 kcal", "120 mg kafein", "sütsüz", "vegan"]],
    ["Chemex","İki kişilik · 500 ml","220",["5 kcal", "120 mg kafein", "sütsüz", "vegan"]],
    ["Espresso","14 g double shot · 18–23 sn","95",["3 kcal", "85 mg kafein", "sütsüz", "vegan"]],
    ["Americano","Çift shot, sıcak su","115",["8 kcal", "170 mg", "sütsüz", "vegan"]],
    ["Cortado","Tek shot, eşit süt","130",["70 kcal", "75 mg"]],
    ["Flat White","Çift shot, ince süt dokusu","150",["140 kcal", "180 mg"]],
    ["Cappuccino","Çift shot, bol köpük","145",["150 kcal", "170 mg"]],
    ["Latte","Çift shot, sıcak süt","150",["190 kcal", "170 mg"]],
    ["Caramel Latte","Ev yapımı karamel şurubu","170",["260 kcal", "170 mg"]],
    ["Vanilla Latte","Madagaskar vanilya","170",["240 kcal", "170 mg"]],
    ["Mocha","%55 bitter çikolata, espresso, süt","175",["300 kcal", "170 mg"]],
    ["White Mocha","Beyaz çikolata, espresso, süt","180",["330 kcal", "170 mg"]],
    ["Caramel Macchiato","Vanilya, süt, espresso üstte, karamel","180",["270 kcal", "170 mg"]],
    ["Türk Kahvesi","7 g, közde, lokum ile","95",["25 kcal", "65 mg", "sütsüz"]],
    ["Sütlü Türk Kahvesi","Sütle pişirilmiş","105",["70 kcal", "65 mg"]]
  ],
  soguk: [
    ["Cold Brew","16 saat demleme","145",["25 kcal", "200 mg", "sütsüz", "vegan"]],
    ["Boğaz Cold Brew","Tonik ve portakal kabuğu ile · Kavacık, Beykoz","165",["60 kcal", "200 mg", "sütsüz", "vegan"]],
    ["Iced Filtre","Günün çekirdeği · buz üstüne","130",["5 kcal", "95 mg", "sütsüz", "vegan"]],
    ["Iced Americano","Çift shot, buzlu su","125",["10 kcal", "170 mg", "sütsüz", "vegan"]],
    ["Iced Latte","Espresso, soğuk süt, buz","160",["150 kcal", "150 mg"]],
    ["Iced Caramel Latte","Karamel şurubu, süt, buz","175",["250 kcal", "150 mg"]],
    ["Iced Mocha","Bitter çikolata sosu, espresso, süt, buz","180",["300 kcal", "150 mg"]],
    ["Iced White Mocha","Beyaz çikolata sosu ile","185",["320 kcal", "150 mg"]],
    ["Frappe","Blender, kremalı","175",["290 kcal", "120 mg"]],
    ["Çikolatalı Frappe","Bitter çikolata, blender","180",["330 kcal", "100 mg"]],
    ["Affogato","Vanilyalı dondurma üstüne espresso","165",["220 kcal", "85 mg"]]
  ],
  diger: [
    ["Sıcak Çikolata","%55 bitter","150",["280 kcal", "kafeinsiz"]],
    ["Salep","Kış mevsimi · tarçınlı","140",["230 kcal", "kafeinsiz"]],
    ["Chai Latte","Ev yapımı baharat konsantresi","155",["210 kcal", "40 mg"]],
    ["Matcha Latte","Tören sınıfı matcha","165",["180 kcal", "70 mg"]],
    ["Iced Matcha Latte","Matcha, süt, buz","170",["170 kcal", "70 mg"]],
    ["Demleme Çay","Rize · bardak","65",["0 kcal", "30 mg", "vegan", "sütsüz"]],
    ["Bitki Çayı","Ihlamur · nane-limon · papatya","95",["0 kcal", "kafeinsiz", "vegan", "sütsüz"]],
    ["Ev Limonatası","Taze sıkım, naneli","110",["90 kcal", "kafeinsiz", "vegan", "sütsüz"]],
    ["Hibiskus Soğuk Çay","Taze meyve ve hibiskus çiçeği · soğuk","120",["70 kcal", "kafeinsiz", "vegan", "sütsüz"]],
    ["Çilekli Smoothie","Çilek, muz, yoğurt","160",["210 kcal", "kafeinsiz"]],
    ["Çikolatalı Milkshake","Dondurma, süt, bitter çikolata","175",["380 kcal", "kafeinsiz"]],
    ["Meyveli Soda","Şeftali · yeşil elma · nar","95",["60 kcal", "kafeinsiz", "vegan", "sütsüz"]]
  ],
  yiyecek: [
    ["Kavacık Kahvaltı Tabağı","İki kişilik · 09:00–13:00","690",["kahvaltı"]],
    ["Tereyağlı Kruvasan","Günlük üretim","95",["glüten", "süt"]],
    ["Çikolatalı Kruvasan","Bitter çikolata dolgulu","110",["glüten", "süt"]],
    ["San Sebastian","Dilim","185",["yumurta", "süt"]],
    ["Fıstıklı Cheesecake","Dilim","195",["fıstık", "süt"]],
    ["Frambuazlı Cheesecake","Dilim","190",["süt", "yumurta"]],
    ["Glütensiz Brownie","Vegan","145",["vegan", "glütensiz"]],
    ["Havuçlu Kek","Cevizli, krem peynir kaplı","150",["ceviz", "süt", "glüten"]],
    ["Limonlu Kek","Dilim · haşhaşlı","135",["glüten", "yumurta"]],
    ["Cookie","Bitter çikolata parçalı","85",["glüten", "süt"]],
    ["Avokadolu Ekşi Maya","Yumurta ilaveli","265",["glüten"]],
    ["Kaşarlı Tost","Ekşi maya, eski kaşar","165",["glüten", "süt"]],
    ["Tavuklu Sandviç","Izgara tavuk, roka, pesto","235",["glüten"]],
    ["Granola Kasesi","Yoğurt, mevsim meyvesi, bal","175",["süt", "ceviz"]]
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
  const render = () => { const items = MENU[cat].filter(([,,,t]) => passDiet(t)); ml.innerHTML = items.length ? items.map(([n,d,p,t]) => `<a class="mitem" href="/menu/${slug(n)}/"><span class="thumb"><img src="/img/menu/${slug(n)}.jpg" alt="" loading="lazy" decoding="async" onerror="this.parentNode.remove()"></span><span class="n">${n}</span><span class="p">${p} ₺</span><span class="d">${d}</span><span class="tags">${t.filter(x=>x!=="sütsüz"||diet==="sutsuz").map(x=>`<span class="tg ${/vegan|glütensiz|kafeinsiz/.test(x)?"v":/kafein|mg/.test(x)?"c":""}">${x}</span>`).join("")}</span></a>`).join("") : `<p style="padding:1rem 0">Bu filtrede ürün yok.</p>`; };
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
    bl.innerHTML = list.map(b => { const open = isOpen(b,now); return `<a class="cell" href="/subeler/${b.id}/"><figure class="bimg"><img src="/img/subeler/${b.id}.jpg" alt="" loading="lazy" decoding="async" onerror="this.parentNode.remove()"></figure><div style="display:flex;justify-content:space-between;gap:.5rem"><h3>${b.n}</h3><span style="font-size:.78rem;color:${open?"var(--ok)":"var(--ink-3)"}">${open?"Açık":"Kapalı"}</span></div><p>${b.c} · ${hourStr(b.o)}–${hourStr(b.k)} · ★ ${b.r}</p>${b.f.includes("manzara")?`<p style="color:var(--amber)">Gün batımı ${zhm(sunTimes(now,b.lat,b.lng).set,tzOf(b))}</p>`:""}<div style="display:flex;gap:.3rem;flex-wrap:wrap">${b.f.map(f=>`<span class="chip">${F2[f]}</span>`).join("")}</div><span class="more">Şube sayfası →</span></a>`; }).join(""); };
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
/* ================= FLO — Florida Coffee'nin tukanı · v2 (bağlam, görev akışları, hafıza, kartlar) ================= */
const floEl = document.getElementById("flo"), fab = document.getElementById("floFab"), msgs = document.getElementById("floMsgs"),
      quick = document.getElementById("floQuick"), floIn = document.getElementById("floIn"), floHint = document.getElementById("floHint"),
      floCtx = document.getElementById("floCtx");
const fold = s => s.toLowerCase().replace(/i̇/g,"i").replace(/[çğıöşüâîû]/g, c => ({"ç":"c","ğ":"g","ı":"i","ö":"o","ş":"s","ü":"u","â":"a","î":"i","û":"u"})[c]);
const norm = t => fold(t).replace(/[^a-z0-9 ]/g," ").replace(/\s+/g," ").trim();
const hit = (t, k) => { k = fold(k); return k.length <= 4 && !k.includes(" ") ? (" " + t + " ").includes(" " + k + " ") : t.includes(k); };
const has = (t, ...ws) => ws.some(w => hit(t, w));
const esc = s => String(s).replace(/[&<>"]/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"})[c]);
const fmtTL = n => n.toLocaleString("tr-TR") + " ₺";
const store = { get(k){ try{ return JSON.parse(localStorage.getItem("flo:"+k)); }catch(e){ return null; } }, set(k,v){ try{ localStorage.setItem("flo:"+k, JSON.stringify(v)); }catch(e){} } };
const mem = Object.assign({ name:"", branch:"", milk:"", lastOrder:null, visits:0, seen:[] }, store.get("mem") || {});
const remember = () => store.set("mem", mem);
const stat = id => { const s = store.get("stats") || {}; s[id] = (s[id] || 0) + 1; store.set("stats", s); };
let flow = null, pending = null;   // aktif görev akışı · bekleyen evet/hayır

/* --- bağlam: sayfa, saat, şube --- */
const PAGE = document.body.dataset.page || "safak", PATH = location.pathname;
let ctxSection = PAGE;
const IMG = typeof MENUIMG !== "undefined" ? MENUIMG : {};
const slugOf = s => norm(s).replace(/ /g,"-");
const pimg = s => IMG[s] ? `<img src="${IMG[s]}" alt="" loading="lazy">` : `<img src="/img/menu/${s}.jpg" alt="" loading="lazy" onerror="this.remove()">`;
const bimg = id => (typeof SUBEIMG !== "undefined" && SUBEIMG[id]) ? `<img src="${SUBEIMG[id]}" alt="" loading="lazy">` : `<img src="/img/subeler/${id}.jpg" alt="" loading="lazy" onerror="this.remove()">`;
const hourNow = () => new Date().getHours();
const daypart = () => { const h = hourNow(); return h < 11 ? "sabah" : h < 15 ? "ogle" : h < 19 ? "ikindi" : h < 23 ? "aksam" : "gece"; };
const greetWord = () => ({sabah:"Günaydın", ogle:"İyi günler", ikindi:"İyi günler", aksam:"İyi akşamlar", gece:"İyi geceler"})[daypart()];
const homeBranch = () => B.find(b => b.id === mem.branch) || B[0];
const sunsetOf = b => zhm(sunTimes(new Date(), b.lat, b.lng).set, tzOf(b));
const openNow = () => B.filter(b => isOpen(b, new Date()));

/* --- bilgi tabanı --- */
const MENU_ALL = Object.entries(MENU).flatMap(([cat, arr]) => arr.map(([n,d,p,tags]) => ({cat, n, d, p:+p, tags, slug: slugOf(n)})));
const findProduct = t => MENU_ALL.filter(x => t.includes(norm(x.n))).sort((a, b) => b.n.length - a.n.length)[0] || MENU_ALL.find(x => norm(x.n).split(" ").some(w => w.length > 4 && hit(t, w)));
const findBranch = t => B.filter(b => t.includes(norm(b.n))).sort((a, b) => b.n.length - a.n.length)[0] || B.find(b => norm(b.n).split(" ").some(w => w.length > 4 && t.includes(w))) || B.find(b => norm(b.c).split(/[ ,·]+/).some(w => w.length > 4 && t.includes(w)));
const pathProduct = () => { const m = PATH.match(/\/menu\/([a-z0-9-]+)\//); return m ? MENU_ALL.find(x => x.slug === m[1]) : null; };
const FLO_EVENTS = [
  {d:4, h:"Akustik set", w:"Kavacık terası · Perşembe 21:00", b:"kavacik"},
  {d:6, h:"Cupping", w:"Çengelköy · ayın ilk Cumartesi'si 11:00", b:"cengelkoy"},
  {d:3, h:"Latte art atölyesi", w:"Kadıköy · Çarşamba 19:00 · 8 kişi", b:"kadikoy"},
  {d:0, h:"Kahvaltı sofrası", w:"Beykoz · Bahçeşehir · Samsun · Pazar 09:00", b:"beykoz"},
];
const FAQ = [
  ["laktozsuz sut var mi bitkisel yulaf badem", "Evet. Laktozsuz +10 ₺, yulaf ve badem +15 ₺; her şubede. Tercihinizi uygulama profilinize kaydederseniz bir daha söylemeniz gerekmez, barista ekranında etiketli görünür."],
  ["wifi internet sifre", "Tüm şubelerde ücretsiz Wi-Fi var; şifre fişte ve tezgâhta. Kadıköy, Sakarya ve Bahçeşehir'de uzun çalışmaya uygun priz düzeni var."],
  ["priz calisma alani laptop", "Çalışma alanı olan şubeler: Kadıköy (üst kat), Sakarya Çark Caddesi, Bahçeşehir, Ümraniye. Hafta içi 10–12 en sakin saatler."],
  ["otopark park", "Şubeye ait otopark: Kavacık, Bahçeşehir, İzmit, Bursa Nilüfer, Samsun Marina. Diğerlerinde çevrede ücretli otopark."],
  ["evcil kopek kedi", "Bahçeli ve teraslı şubelerimiz evcil dostu: Kavacık, Beykoz, Çengelköy, Podgorica, Budva. İç mekânda kucak boyu kabul."],
  ["kahvalti", "Kahvaltı: Beykoz, Bahçeşehir ve Samsun'da hafta sonu 09:00–13:00 iki kişilik kahvaltı sofrası; hafta içi tüm şubelerde tost, kruvasan, granola."],
  ["dogum gunu", "Classic üyeler dahil herkese doğum gününde bir içecek bizden; uygulamada doğum tarihinizi ekleyin, o gün otomatik tanımlanır."],
  ["ogrenci indirim", "Sakarya, Kadıköy ve Erzincan'da öğrenci kimliğiyle hafta içi 14–16 filtre kahve %20 indirimli; uygulamada öğrenci profili açın."],
  ["fatura e fatura kurumsal", "Şubede fiş, uygulamada e-arşiv fatura otomatik; kurumsal siparişlerde şirket bilgilerinizi bir kez kaydedin."],
  ["gluten glutensiz alerjen", "Glütensiz: Glütensiz Brownie, granola kâsesi (yulafı sertifikalı). Alerjen etiketleri her üründe; emin değilseniz baristaya sorun."],
  ["cocuk bebek mama sandalye", "Bahçeşehir ve Beykoz'da çocuk köşesi ve mama sandalyesi var; sıcak çikolata ve milkshake çocuk boyu servis edilir."],
  ["uygulama indir ios android", "Uygulama iOS ve Android'de. Ön sipariş, Geldim, cüzdan, sadakat tek yerde; kurulum bir dakika."],
  ["kapali gun bayram tatil", "Bayramın ilk günü öğleden sonra açılıyoruz; diğer günler normal saatler. Şube sayfasında bayram saatleri güncellenir."],
  ["ingilizce english menu", "English menu is available in every branch; Podgorica and Budva teams speak English and Montenegrin."],
];

/* --- mesaj ve kartlar --- */
function bubble(html, dir="in", chips){
  const d = document.createElement("div"); d.className = "msg " + dir; d.innerHTML = html; msgs.appendChild(d); msgs.scrollTop = msgs.scrollHeight;
  if (chips) setQuick(chips); if (dir === "in" && floEl.hidden) badge(true); return d;
}
function setQuick(list){ quick.innerHTML = ""; (list || []).forEach(([label, send]) => { const b = document.createElement("button"); b.type = "button"; b.textContent = label; b.onclick = () => userSays(send || label); quick.appendChild(b); }); }
function say(html, chips){ return new Promise(r => { const t = document.createElement("div"); t.className = "typing"; t.innerHTML = "<i></i><i></i><i></i>"; msgs.appendChild(t); msgs.scrollTop = msgs.scrollHeight;
  setTimeout(() => { t.remove(); bubble(html, "in", chips); r(); }, reduce ? 100 : 380 + Math.min(800, html.replace(/<[^>]+>/g,"").length * 5)); }); }
const card = (inner, cls="") => `<div class="fcard-msg ${cls}">${inner}</div>`;
function productCard(p, note){
  const facts = p.tags.filter(x => /kcal|mg|kafeinsiz|vegan|glütensiz/.test(x)).slice(0,3).map(x => `<span>${x}</span>`).join("");
  return card(`${pimg(p.slug)}<div><b>${p.n}</b><small>${p.d}</small><em>${fmtTL(p.p)} <span>orta boy</span></em><div class="ff">${facts}</div>${note ? `<p>${note}</p>` : ""}
    <div class="fa"><button type="button" data-send="sipariş: ${p.n}">Sipariş ver</button><a href="/menu/${p.slug}/">Ürün sayfası</a></div></div>`, "prod");
}
function branchCard(b){
  const now = new Date(), open = isOpen(b, now);
  return card(`${bimg(b.id)}<div><b>${b.n}</b><small>${b.c}</small><em class="${open ? "ok" : "off"}">${open ? "Şu an açık" : "Şu an kapalı"} · ${hourStr(b.o)}–${hourStr(b.k)}</em>${b.f.includes("manzara") ? `<small>Gün batımı ${sunsetOf(b)}</small>` : ""}<p>${b.note}</p>
    <div class="fa"><button type="button" data-send="sipariş şube: ${b.n}">Buradan sipariş</button><a href="https://www.google.com/maps/search/?api=1&query=${b.lat},${b.lng}" target="_blank" rel="noopener">Yol tarifi</a><a href="/subeler/${b.id}/">Şube sayfası</a></div></div>`, "branch");
}
msgs.addEventListener("click", e => { const b = e.target.closest("[data-send]"); if (b) userSays(b.dataset.send); });

/* --- öneri motoru: ruh hâli + saat + diyet --- */
function recommend(t){
  const pick = names => names.map(n => MENU_ALL.find(x => x.n === n)).filter(Boolean);
  if (has(t,"uyan","enerji","yorgun","uyku","uykusuz","sert")) return ["Uyanmanız lazım; sert ama mideyi yormayan üçlü:", pick(["Flat White","Espresso","Cold Brew"])];
  if (has(t,"odak","calis","ders","sinav","uzun sure","toplanti")) return ["Uzun odak için kafeini yavaş salanlar:", pick(["Florida Filtre","V60","Americano"])];
  if (has(t,"sicak hava","serin","bunal","buz","soguk bir","yaz")) return ["Serinleten seçenekler:", pick(["Boğaz Cold Brew","Iced Latte","Hibiskus Soğuk Çay"])];
  if (has(t,"tatli","seker","canim ceker","cikolata")) return ["Tatlı krizi için:", pick(["Iced White Mocha","San Sebastian","Caramel Latte"])];
  if (has(t,"hafif","az kafein","kafeinsiz","aksam","gece","uyumadan")) return ["Akşam içilir, uykuyu bozmaz:", pick(["Cortado","Bitki Çayı","Sıcak Çikolata"])];
  if (has(t,"sutsuz","laktoz","vegan")) return ["Sütsüz ve vegan seçenekler:", pick(["Americano","Cold Brew","Florida Filtre"])];
  if (has(t,"kahvalti","ac","yemek","atistir")) return ["Yanına bir şeyler:", pick(["Kavacık Kahvaltı Tabağı","Avokadolu Ekşi Maya","Tereyağlı Kruvasan"])];
  const dp = daypart();
  if (dp === "sabah") return ["Sabah için en çok sipariş edilenler:", pick(["Flat White","Florida Filtre","Iced Latte"])];
  if (dp === "ogle" || dp === "ikindi") return ["Öğleden sonra en iyi giden üçlü:", pick(["Iced Latte","Cold Brew","Cappuccino"])];
  return ["Bu saatte hafif olsun:", pick(["Cortado","Türk Kahvesi","Sıcak Çikolata"])];
}

/* --- görev akışları (slot doldurma) --- */
const SIZES = {"kucuk":["Küçük",-15],"orta":["Orta",0],"buyuk":["Büyük",20]}, MILKS = {"inek":["İnek sütü",0],"laktozsuz":["Laktozsuz",10],"yulaf":["Yulaf",15],"badem":["Badem",15]};
const FLOWS = {
  order: {
    start(d){ flow = {id:"order", step:0, data:d || {}}; return next(); },
    steps: [
      { ask: d => d.drink ? null : ["Ne içiyorsunuz? Ürün adı yazın ya da seçin.", [["Iced Latte"],["Flat White"],["Florida Filtre"],["Cold Brew"],["Ne önerirsin?","öner"]]],
        take: (d, t) => { if (has(t,"oner","onerir","oneri","ne icsem","tavsiye","karar")) { const [l, list] = recommend(t); return l + list.map(p => productCard(p)).join("") + "Hangisi olsun?"; } const p = findProduct(t); if (!p) return "Menüde bulamadım; başka bir ad deneyin (örn. Flat White)."; d.drink = p; if (p.tags.includes("sütsüz") || p.cat === "yiyecek" || p.cat === "diger") d.milk = ["—",0]; } },
      { ask: d => d.size ? null : [`<b>${d.drink.n}</b>, hangi boy?`, [["Küçük · −15 ₺","küçük"],["Orta","orta"],["Büyük · +20 ₺","büyük"]]],
        take: (d, t) => { const k = Object.keys(SIZES).find(k => t.includes(k)); if (!k) return "Küçük, orta ya da büyük?"; d.size = SIZES[k]; } },
      { ask: d => d.milk ? null : [mem.milk ? `Süt tercihiniz <b>${mem.milk}</b> kayıtlı; öyle mi kalsın?` : "Süt?", mem.milk ? [["Evet, "+mem.milk, mem.milk],["İnek"],["Yulaf"],["Badem"]] : [["İnek"],["Laktozsuz · +10 ₺","laktozsuz"],["Yulaf · +15 ₺","yulaf"],["Badem · +15 ₺","badem"]]],
        take: (d, t) => { const k = Object.keys(MILKS).find(k => t.includes(k)) || (has(t,"evet","olur","kalsin") && mem.milk ? Object.keys(MILKS).find(k => fold(mem.milk).includes(k)) : null); if (!k) return "İnek, laktozsuz, yulaf ya da badem?"; d.milk = MILKS[k]; mem.milk = MILKS[k][0]; remember(); } },
      { ask: d => d.branch ? null : [`Hangi şubeden? Size en yakın <b>${homeBranch().n}</b> görünüyor.`, [[homeBranch().n],["Kadıköy"],["Kavacık"],["Başka şube","şube listesi"]]],
        take: (d, t) => { if (has(t,"sube listesi")) return "Şubeler: " + B.map(b => b.n).join(", ") + ". Hangisi?"; const b = findBranch(t); if (!b) return "Şube adını yazar mısınız? (örn. Kadıköy)"; d.branch = b; mem.branch = b.id; remember(); } },
      { ask: d => d.when ? null : ["Ne zaman hazır olsun?", [["Geldiğimde"],["10 dk sonra"],["Şimdi"]]],
        take: (d, t) => { d.when = t.includes("geld") ? "Geldiğimde" : has(t,"10") ? "10 dk sonra" : has(t,"simdi","hemen") ? "Şimdi" : null; if (!d.when) return "Geldiğimde, 10 dk sonra ya da şimdi?"; } },
      { ask: d => { const total = d.drink.p + d.size[1] + d.milk[1]; d.total = total;
          return [card(`${pimg(d.drink.slug)}<div><b>${d.drink.n}</b><small>${d.size[0]}${d.milk[1] !== undefined && d.milk[0] !== "—" ? " · " + d.milk[0] : ""} · ${d.branch.n} · ${d.when}</small><em>${fmtTL(total)} <span>+${total} çekirdek</span></em><p>Ödeme cüzdandan (412 ₺). Onaylıyor musunuz?</p></div>`, "prod"), [["Onayla"],["Boyu değiştir","boy değiştir"],["Vazgeç"]]]; },
        take: (d, t) => { if (has(t,"boy degistir")) { d.size = null; flow.step = 0; return ""; } if (!(t.startsWith("onay") || has(t,"evet","tamam","olur","onayliyorum"))) return "Onaylamak için \"Onayla\" yazın ya da vazgeçin."; d.ok = true; } },
    ],
    done(d){
      const code = "FC·" + Math.floor(4800 + Math.random() * 200); mem.lastOrder = {drink:d.drink.n, size:d.size[0], milk:d.milk[0], branch:d.branch.id, when:d.when}; remember(); stat("order_done");
      const panel = document.getElementById("drinks");
      if (panel) { const click = (id, n) => { const b = document.querySelector(`#${id} .opt[data-n="${n}"]`); if (b && b.getAttribute("aria-pressed") !== "true") b.click(); };
        click("drinks", d.drink.n); click("sizes", d.size[0]); if (d.milk[0] !== "—") click("milks", d.milk[0]); click("whens", d.when === "Geldiğimde" ? "geldigimde" : d.when === "Şimdi" ? "simdi" : "10dk");
        const sel = document.getElementById("oBranch"); if (sel && [...sel.options].some(o => o.value === d.branch.n)) { sel.value = d.branch.n; sel.dispatchEvent(new Event("change")); }
        const act = document.getElementById("tAct"); if (act) act.click(); }
      return [`Sipariş <b>${code}</b> ${d.branch.n} şubesine iletildi. ${d.when === "Geldiğimde" ? "Kapıya 200 m kala ya da \"Geldim\" deyince hazırlanmaya başlar." : "Hazırlanıyor; tezgâhta kodunuzu gösterin."}${panel ? " Sipariş panelinde de görüyorsunuz." : ""}`,
        panel ? [["Paneli göster","#sabah"],["Şube yolu","yol tarifi " + d.branch.n],["Başka bir şey"]] : [["Uygulamada aç","/app/"],["Şube yolu","yol tarifi " + d.branch.n],["Başka bir şey"]]];
    }
  },
  lead: {
    start(){ flow = {id:"lead", step:0, data:{}}; return next(); },
    steps: [
      { ask: () => ["Süper. Dört kısa soru. <b>Adınız ve soyadınız?</b>", []], take: (d, t, raw) => { if (raw.length < 3) return "Adınızı yazar mısınız?"; d.name = raw.split(" ").map(w => w ? w[0].toLocaleUpperCase("tr") + w.slice(1) : w).join(" "); mem.name = d.name.split(" ")[0]; remember(); } },
      { ask: d => [`Teşekkürler ${d.name.split(" ")[0]}. <b>Telefon numaranız?</b>`, []], take: (d, t) => { const digits = t.replace(/\D/g,""); if (digits.length < 10) return "Numarayı 05xx xxx xx xx biçiminde yazabilir misiniz?"; d.phone = digits; } },
      { ask: () => ["<b>Hangi şehir veya ilçe</b> için düşünüyorsunuz?", [["Eskişehir"],["Ankara"],["İzmir"],["Antalya"]]], take: (d, t, raw) => { d.city = raw; } },
      { ask: () => ["<b>Yatırım bütçeniz</b> hangi aralıkta?", [["2 M ₺ altı"],["2–4 M ₺"],["4–6 M ₺"],["6 M ₺ üstü"]]], take: (d, t, raw) => { d.budget = raw; } },
      { ask: () => ["Son soru: <b>işletme deneyiminiz</b> var mı?", [["Yok"],["Perakende"],["Kafe / restoran işlettim"],["Franchise sahibiyim"]]], take: (d, t, raw) => { d.exp = raw; } },
    ],
    done(d){
      const bIdx = has(norm(d.budget),"alti") ? 0 : has(norm(d.budget),"ustu") ? 3 : has(norm(d.budget),"4 6","4-6") ? 2 : 1;
      const eIdx = ["yok","perakende","kafe","franchise"].findIndex(k => norm(d.exp).includes(k));
      const near = B.find(b => norm(d.city).split(" ").some(w => w.length > 3 && norm(b.n + " " + b.c).includes(w)));
      d.score = Math.min(97, 40 + bIdx * 12 + Math.max(0, eIdx) * 9 + (near ? 2 : 14)); d.at = new Date().toISOString(); store.set("lead", d); stat("lead_done");
      return [`Başvurunuz alındı, ${d.name.split(" ")[0]}. Kayıt <b>#L-${Math.floor(1000 + Math.random() * 9000)}</b>.\n• Bölge: ${esc(d.city)}${near ? ` — ${near.n} şubemize yakın, 3 km kontrolü yapılır` : " — bölge açık görünüyor"}\n• Ön değerlendirme: <b>${d.score}/100</b>\n\nFranchise ekibimiz <b>24 saat içinde</b> ${d.phone.replace(/(\d{4})(\d{3})(\d{2})(\d{2})/, "$1 $2 $3 $4")} numarasını arayacak.`, [["Yatırım hesaplayıcı","/franchise/"],["Franchise SSS","/franchise/sss/"],["Başka bir şey"]]];
    }
  },
  career: {
    start(){ flow = {id:"career", step:0, data:{}}; return next(); },
    steps: [
      { ask: () => ["Barista olmak için deneyim şart değil; 45 günlük eğitimimiz var. <b>Adınız?</b>", []], take: (d, t, raw) => { if (raw.length < 2) return "Adınızı yazar mısınız?"; d.name = raw.split(" ").map(w => w ? w[0].toLocaleUpperCase("tr") + w.slice(1) : w).join(" "); mem.name = d.name.split(" ")[0]; remember(); } },
      { ask: () => ["<b>Hangi şehirde</b> çalışmak istersiniz?", [["İstanbul"],["Sakarya"],["Bursa"],["Samsun"]]], take: (d, t, raw) => { d.city = raw; } },
      { ask: () => ["<b>Pozisyon?</b>", [["Barista"],["Şube müdürü"],["Mutfak"],["Kalite uzmanı"]]], take: (d, t, raw) => { d.role = raw; } },
      { ask: () => ["<b>Ne zaman başlayabilirsiniz?</b>", [["Hemen"],["2 hafta içinde"],["1 ay sonra"]]], take: (d, t, raw) => { d.avail = raw; } },
    ],
    done(d){ store.set("career", d); stat("career_done");
      const branches = B.filter(b => norm(b.c + " " + b.n).includes(norm(d.city))).slice(0,3);
      return [`Ön kaydınız açıldı, ${d.name.split(" ")[0]}. ${branches.length ? "Size uygun şubeler: <b>" + branches.map(b => b.n).join(", ") + "</b>." : "Şube eşleştirmesi şehir bazında yapılacak."} Açık vardiya doğduğunda yapay zekâ size sorar, yanıtınızı kayda alır; "Hemen" diyen adaylar aynı gün başlar.\nTam profil için 4 adımlı başvuruyu tamamlayın (3 dakika).`, [["Başvuruyu tamamla","/kariyer/basvuru/"],["Barista eğitimi nasıl?","eğitim"],["Başka bir şey"]]]; }
  },
  corporate: {
    start(){ flow = {id:"corporate", step:0, data:{}}; return next(); },
    steps: [
      { ask: () => ["Ofis ikramı, etkinlik kahve barı ya da toplu hediye kartı; hepsinde 1 iş günü içinde teklif. <b>Hangisi?</b>", [["Ofis ikramı"],["Etkinlik barı"],["Toplu hediye kartı"]]], take: (d, t, raw) => { d.type = raw; } },
      { ask: () => ["<b>Kaç kişi</b> için?", [["10–25"],["25–100"],["100+"]]], take: (d, t, raw) => { d.people = raw; } },
      { ask: () => ["<b>Şirket adı ve telefon?</b>", []], take: (d, t, raw) => { if (raw.replace(/\D/g,"").length < 10) return "Telefonu da ekler misiniz? (05xx…)"; d.contact = raw; } },
    ],
    done(d){ store.set("corporate", d); stat("corporate_done"); return [`Talebiniz alındı: <b>${esc(d.type)}</b>, ${esc(d.people)} kişi. Kurumsal ekibimiz 1 iş günü içinde teklifle döner. Bütçe fikri için hesaplayıcı kurumsal sayfada.`, [["Kurumsal sayfa","/kurumsal/"],["Başka bir şey"]]]; }
  },
  feedback: {
    start(d){ flow = {id:"feedback", step:0, data:d || {}}; return next(); },
    steps: [
      { ask: d => d.branch ? null : ["Üzgünüm. <b>Hangi şubede</b> oldu?", B.slice(0,4).map(b => [b.n])], take: (d, t, raw) => { const b = findBranch(t); if (!b) return "Şube adını yazar mısınız?"; d.branch = b; } },
      { ask: d => d.text ? null : ["<b>Ne oldu?</b> Kısaca anlatın; yazdıklarınız kayıt numarasıyla şube müdürüne ve kalite ekibine gider.", []], take: (d, t, raw) => { if (raw.length < 6) return "Biraz daha detay verebilir misiniz?"; d.text = raw; } },
      { ask: () => ["Sizi arayalım mı? <b>Telefon</b> yazın ya da geçin.", [["Geç"]]], take: (d, t, raw) => { d.phone = has(t,"gec") ? "" : raw.replace(/\D/g,""); } },
    ],
    done(d){ const id = "K-" + Math.floor(10000 + Math.random() * 90000); store.set("feedback", Object.assign(d, {id})); stat("feedback_done");
      return [`Kayıt <b>#${id}</b> açıldı: ${d.branch.n}. ${d.phone ? "Şube müdürü <b>1 saat içinde</b> arayacak." : "Yanıt uygulama bildirimi olarak gelecek."} Bir sonraki ziyaretinizde bir içecek bizden; uygulamanıza tanımlandı.`, [["Bir insanla konuş","insan"],["Başka bir şey"]]]; }
  },
  reserve: {
    start(d){ flow = {id:"reserve", step:0, data:d || {}}; return next(); },
    steps: [
      { ask: d => d.ev ? null : ["Hangi etkinlik?", FLO_EVENTS.map(e => [e.h])], take: (d, t) => { const e = FLO_EVENTS.find(e => t.includes(norm(e.h).split(" ")[0])); if (!e) return "Etkinlik adını seçer misiniz?"; d.ev = e; } },
      { ask: () => ["<b>Kaç kişi?</b>", [["1"],["2"],["3–4"],["5+"]]], take: (d, t, raw) => { d.people = raw; } },
      { ask: () => ["<b>Telefon numaranız?</b> Hatırlatmayı oraya gönderelim.", []], take: (d, t) => { const digits = t.replace(/\D/g,""); if (digits.length < 10) return "05xx ile başlayan numara?"; d.phone = digits; } },
    ],
    done(d){ stat("reserve_done"); return [`Yeriniz ayrıldı: <b>${d.ev.h}</b>, ${d.ev.w}, ${esc(d.people)} kişi. Etkinlikten 3 saat önce hatırlatma gelir; Plus ve Premium üyelere öncelikli masa.`, [["Takvime ekle","/etkinlikler/"],["Başka bir şey"]]]; }
  },
};
async function next(){
  const F = FLOWS[flow.id];
  while (flow.step < F.steps.length) { const q = F.steps[flow.step].ask(flow.data); if (q) return say(q[0], q[1]); flow.step++; }
  const [txt, chips] = F.done(flow.data); flow = null; return say(txt, chips);
}
async function flowStep(raw){
  const t = norm(raw);
  if (has(t,"vazgec","iptal","bosver","cikis")) { flow = null; return say("Tamam, iptal ettim. Başka ne yapabilirim?", defaultChips()); }
  const F = FLOWS[flow.id]; const err = F.steps[flow.step].take(flow.data, t, raw.trim());
  if (err) { flow.miss = (flow.miss || 0) + 1; return say(err, flow.miss >= 2 ? [["Vazgeç"]] : undefined); }
  flow.step++; return next();
}

/* --- niyetler: anahtar kelime puanı, en yüksek kazanır --- */
const defaultChips = () => [
  mem.lastOrder ? ["Her zamanki · " + mem.lastOrder.drink, "her zamanki"] : ["Sipariş ver","sipariş"],
  ["En yakın şube"], ["Ne içsem?","öner"], ["Franchise","franchise"], ["Bir insanla konuş","insan"]];
const INTENTS = [
 { id:"selam", kw:["merhaba","selam","hey","gunaydin","iyi aksamlar","naber","iyi gunler"], w:3,
   reply:() => [`${greetWord()}${mem.name ? " " + mem.name : ""}! Ben <b>Flo</b>. Sipariş, şube, menü, sadakat, franchise, kariyer; ne lazımsa buradayım.`, defaultChips()] },
 { id:"usual", kw:["her zamanki","yine ayni","ayni siparis","son siparis"], w:4,
   reply:() => { const o = mem.lastOrder; if (!o) return ["Henüz kayıtlı bir siparişiniz yok; ilkini birlikte verelim mi?", [["Sipariş ver","sipariş"]]];
     const p = MENU_ALL.find(x => x.n === o.drink), b = B.find(x => x.id === o.branch) || B[0]; return FLOWS.order.start({drink:p, size:SIZES[Object.keys(SIZES).find(k => fold(o.size).includes(k))], milk:MILKS[Object.keys(MILKS).find(k => fold(o.milk).includes(k))] || ["—",0], branch:b, when:o.when}), null; } },
 { id:"order", kw:["siparis","on siparis","siparis ver","siparis: ","geldim","sira","beklemek"], w:4,
   reply:t => { const m = t.match(/siparis sube (.+)/); if (m) return FLOWS.order.start({branch: findBranch(m[1]) || B[0]}), null;
     const p = (t.includes("siparis") ? findProduct(t.replace(/^siparis\s*/, "")) : null) || pathProduct(); return FLOWS.order.start(p ? {drink:p} : {}), null; } },
 { id:"oner", kw:["oner","ne icsem","ne icmeli","tavsiye","karar veremedim","onerir misin","hangisini","ne alsam"], w:3,
   reply:t => { const [lead, list] = recommend(t); return [lead + list.map(p => productCard(p)).join(""), [["Sipariş ver","sipariş"],["Başka öner","öner tatlı"],["Menüye git","/menu/"]]]; } },
 { id:"mood", kw:["uyan","uykusuz","yorgun","odaklan","ders calis","sicaktan","bunal","tatli bir sey","canim ceker","kafein az","gece kahve","serin"], w:2,
   reply:t => INTENTS.find(i => i.id === "oner").reply(t) },
 { id:"franchise", kw:["franchise","bayilik","bayi","yatirim","sube acmak","dukkan acmak","isletme acmak","ortak olmak","kendi sehrim"], w:3,
   reply:() => ["Kendi şehrinizde bir Florida; kısa özet:\n• <b>3 km bölge koruması</b>, 10 yıl sözleşme\n• <b>45 gün eğitim</b>: 30 gün işletme + 15 gün barista\n• Merkezi tedarik, 40 gün vade · royalty %5 + KDV\n• Web, uygulama ve raporlama paneli dahil\n\n2 dakikada ön başvurunuzu alayım; ekibimiz 24 saat içinde arar.",
     [["Başvuruyu başlat","lead"],["Yatırım ne kadar?","yatırım tutarı"],["Hangi şehirler açık?","açık şehirler"],["Franchise sayfası","/franchise/"]]] },
 { id:"yatirim", kw:["yatirim tutari","ne kadar yatirim","maliyet","butce ne","kac para","giris bedeli","geri donus"], w:3,
   reply:() => ["Kuruluş yatırımı konuma ve metrekareye göre değişir; büyükşehir caddesinde 100–120 m² için örnek hesap <b>3,5–4,5 M ₺</b>. Hesaplayıcı canlı tablo verir; kesin rakam keşif görüşmesinde.", [["Hesaplayıcı","/franchise/"],["Başvuruyu başlat","lead"]]] },
 { id:"sehirler", kw:["acik sehir","hangi sehir","nereler acik","bolge","hangi iller"], w:3,
   reply:() => ["Öncelikli bölgeler: <b>Eskişehir, Ankara Çayyolu, İzmir Alsancak, Antalya Lara, Trabzon, Konya</b>; yurt dışında Saraybosna ve Tiran. Mevcut 17 şubenin 3 km çevresi korumalı; çakışma kontrolü başvuruda otomatik.", [["Başvuruyu başlat","lead"],["Bölge kontrolü","/franchise/"]]] },
 { id:"lead", kw:["lead","basvuruyu baslat","basvurmak istiyorum","kaydimi al","aramanizi istiyorum","on basvuru"], w:5, reply:() => (FLOWS.lead.start(), null) },
 { id:"career", kw:["is basvurusu","barista olmak","calismak istiyorum","is ariyorum","kariyer","eleman","personel","staj","ise alim","is ilani","cv"], w:4, reply:() => (FLOWS.career.start(), null) },
 { id:"egitim", kw:["egitim","barista egitimi","45 gun","sertifika"], w:2,
   reply:() => ["Barista yolculuğu 45 gün: 15 gün akademi (doz, shot, süt dokusu, 5 adım), 30 gün şubede usta barista yanında. Sonunda sınav ve sertifika; sertifikalılar 6 ayda vardiya lideri olabilir.", [["Başvur","kariyer"],["Kariyer sayfası","/kariyer/"]]] },
 { id:"corporate", kw:["kurumsal","ofis","toplu","etkinlik bari","catering","ikram","sirket","toplanti icin"], w:3, reply:() => (FLOWS.corporate.start(), null) },
 { id:"sikayet", kw:["sikayet","sorun yasadim","kotu","berbat","soguk geldi","yanlis","bekledim","ilgilenmedi","rezalet","memnun degilim","iade","bozuk"], w:4, reply:() => (FLOWS.feedback.start(), null) },
 { id:"ovgu", kw:["cok iyiydi","harikaydi","bayildim","tebrik","ellerine saglik","muhtesem"], w:3,
   reply:() => ["Bunu duymak çok güzel; hangi şubeydi? Ekibe ileteyim, sizin adınıza bir teşekkür notu gitsin.", B.slice(0,4).map(b => [b.n, "övgü şube " + b.n])] },
 { id:"ovgu2", kw:["ovgu sube"], w:5, reply:t => { const b = findBranch(t); stat("praise"); return [`${b ? b.n : "Şube"} ekibine iletildi. Google'da da paylaşırsanız ekibin primine yansıyor.`, [["Google'da değerlendir","https://www.google.com/maps/search/?api=1&query=Florida+Coffee"],["Başka bir şey"]]]; } },
 { id:"insan", kw:["insan","yetkili","gercek biri","musteri hizmet","temsilci","canli destek","whatsapp","arayin beni"], w:4,
   reply:() => ["Sizi bir insana aktarıyorum. WhatsApp'tan yazabilir ya da numaranızı bırakabilirsiniz; mesai içinde 1 saatte dönüş.", [["WhatsApp'tan yaz","https://wa.me/905000000000"],["Numaramı bırak","numaramı bırakacağım"],["Sorunumu anlatacağım","şikayet"]]] },
 { id:"numara", kw:["numarami birakacagim"], w:5, reply:() => (FLOWS.feedback.start({branch: homeBranch(), text:"Geri arama talebi"}), null) },
 { id:"yakin", kw:["en yakin","yakinimda","yakin sube","konum","neresi yakin","nerede siz"], w:3,
   reply:() => { const b = homeBranch(); return [`Konum izni olmadan tahminim <b>${b.n}</b>:` + branchCard(b) + "Başka bir semt söyleyin, oradaki şubeyi göstereyim.", [["Kadıköy"],["Taksim"],["Sakarya"],["Tüm şubeler","/subeler/"]]]; } },
 { id:"acik", kw:["acik mi","kacta acil","kaca kadar","saat kac","kapali mi","su an acik","gece acik","calisma saat"], w:3,
   reply:t => { const b = findBranch(t); if (b) return [branchCard(b), [["Buradan sipariş","sipariş şube: " + b.n],["Başka şube"]]];
     const o = openNow(); const late = B.filter(x => x.k >= 25).map(x => x.n).join(", "); return [`Şu an <b>${o.length}/${B.length}</b> şube açık. Gece 02:00'a kadar açık olanlar: <b>${late}</b>. Hangi şubeyi soruyorsunuz?`, [["Kavacık"],["Kadıköy"],["Taksim"],["Tüm şubeler","/subeler/"]]]; } },
 { id:"sube", kw:["sube","subeler","subeniz","nerede","adres"], w:2,
   reply:t => { const b = findBranch(t); if (b) return [branchCard(b), [["Buradan sipariş","sipariş şube: " + b.n],["Yol tarifi","yol tarifi " + b.n],["Başka şube"]]];
     return [`${B.length} şube, iki ülke: ${B.map(x => x.n).join(", ")}. Hangisi?`, [["Kavacık"],["Kadıköy"],["Budva"],["Harita","/subeler/"]]]; } },
 { id:"yol", kw:["yol tarifi","nasil giderim","harita","navigasyon"], w:4,
   reply:t => { const b = findBranch(t) || homeBranch(); return [`<b>${b.n}</b> için yol tarifi hazır.`, [["Google Maps'te aç", `https://www.google.com/maps/search/?api=1&query=${b.lat},${b.lng}`],["Şube sayfası", `/subeler/${b.id}/`]]]; } },
 { id:"manzara", kw:["manzara","bogaz","teras","gun batimi","gunbatimi","deniz"], w:3,
   reply:() => { const now = new Date(); const v = B.filter(b => b.f.includes("manzara")).map(b => `• <b>${b.n}</b> — gün batımı ${sunsetOf(b)}${isOpen(b, now) ? "" : " (şu an kapalı)"}`).join("\n");
     return [`Manzaralı şubeler ve bugünkü gün batımı:\n${v}\n\nPremium üyeler gün batımı için masa ayırabilir.`, [["Kavacık'ı göster","kavacık"],["Masa ayır","yer ayır"],["Kulüp seviyeleri","sadakat"]]]; } },
 { id:"fiyat", kw:["fiyat","kac lira","ne kadar","menu","icecek","kahve cesit","kalori","kac kalori","kafein","alerjen","icinde ne var"], w:2,
   reply:t => { const p = findProduct(t); if (p) return [productCard(p, "Süt: inek dahil, laktozsuz +10 ₺, yulaf/badem +15 ₺. Boy: küçük −15, büyük +20 ₺."), [["Sipariş ver","sipariş: " + p.n],["Benzer öner","öner"],["Menü","/menu/"]]];
     return ["Menüde 4 kategori: sıcak kahveler (95–150 ₺), soğuk kahveler (125–185 ₺), kahve dışı ve yiyecek. Ürün adı söyleyin; fiyat, kalori ve alerjeni göstereyim.", [["Flat White"],["Cold Brew"],["San Sebastian"],["Menüye git","/menu/"]]]; } },
 { id:"hafif", kw:["hafif","diyet","sekersiz","vegan","laktoz","sutsuz","gluten","kafeinsiz","az kafein","dusuk kalori"], w:3,
   reply:t => { let list = MENU_ALL; if (has(t,"vegan")) list = list.filter(x => x.tags.includes("vegan")); else if (has(t,"kafeinsiz","az kafein")) list = list.filter(x => cafOf(x.tags) < 80); else if (has(t,"gluten")) list = list.filter(x => x.tags.includes("glütensiz")); else if (has(t,"laktoz","sutsuz")) list = list.filter(x => x.tags.includes("sütsüz")); else list = list.filter(x => kcalOf(x.tags) < 100);
     return [(has(t,"laktoz","sutsuz") ? "Laktozsuz, yulaf ve badem sütü her şubede (+10 / +15 ₺); tercihiniz profile kaydedilir. Sütsüz içilenler:" : "Size uyanlar:") + list.slice(0,3).map(p => productCard(p)).join("") + (list.length > 3 ? `<small>+${list.length - 3} ürün daha menüde filtrelenebilir.</small>` : ""), [["Menüde filtrele","/menu/"],["Sipariş ver","sipariş"]]]; } },
 { id:"standart", kw:["standart","ayni","kalite","doz","gram","shot","sut sicakligi","bar","kavurma","cekirdek","nereden","neden tartilir","14 g"], w:2,
   reply:() => ["Her şubede aynı fincan; reçete kişisel yoruma açık değil:\n• Doz <b>14 g</b> double shot, tartıyla (1 g sapma shot'ı 2–3 sn kaydırır)\n• Su <b>90–96 °C</b>, basınç <b>9 bar</b>\n• Shot <b>18–23 sn</b>, çıktı 30–60 g\n• Süt <b>60–65 °C</b> mikro köpük\nHarman: Etiyopya Yirgacheffe %60, Brezilya Cerrado %40, orta kavurma.", [["5 adım nedir?","beş adım"],["Shot simülatörü","/kahvemiz/"],["Bu standartla ne içsem?","öner uyan"]]] },
 { id:"besadim", kw:["bes adim","5 adim"], w:4,
   reply:() => ["Shot öncesi zorunlu 5 adım:\n1. Grup başlığı flush, 2–3 sn su\n2. Portafiltre temiz, sepet kuru\n3. Gramaj tartılır, 14 g\n4. Tamp: eşit basınç, düz yüzey\n5. Süre: kronometre, 18–23 sn\nBirini atlamak zincir standardına aykırı.", [["Kahvemiz sayfası","/kahvemiz/"],["Sipariş ver","sipariş"]]] },
 { id:"sadakat", kw:["sadakat","kart","puan","cekirdek kazan","kulup","club","seviye","premium","plus","damga","ucretsiz kahve","bedava","floridadays"], w:2,
   reply:() => ["<b>FloridaDays Club</b>:\n• 1 ₺ = 1 çekirdek, 10 içecekte biri bizden\n• Seviye son 6 ay harcamayla: Classic, Plus (2.500 ₺+), Premium (7.500 ₺+)\n• Plus: ayda 2 boy yükseltme · Premium: ücretsiz ekstra shot, gün batımı masası\n• Ödeme + puan tek QR", [["Kartımı aktar","kart aktar"],["Ne kadar kazanırım?","hesapla"],["Kulüp sayfası","/kulup/"]]] },
 { id:"hesapla", kw:["hesapla","ne kadar kazanirim","kac cekirdek","haftada"], w:3,
   reply:t => { const w = parseInt((t.match(/(\d+)/) || [])[1]) || 5; const yearly = w * 52 * 150; const tier = yearly / 2 >= 7500 ? "Premium" : yearly / 2 >= 2500 ? "Plus" : "Classic";
     return [`Haftada ${w} kahve (ortalama 150 ₺) ile yılda <b>${yearly.toLocaleString("tr-TR")} çekirdek</b>, <b>${Math.floor(w * 52 / 10)} hediye içecek</b> ve <b>${tier}</b> seviyesi. Farklı bir sayı yazın, yeniden hesaplayayım.`, [["Haftada 3","hesapla 3"],["Haftada 10","hesapla 10"],["Hesaplayıcı","/kulup/"]]]; } },
 { id:"kartaktar", kw:["kart aktar","aktar","tasi","fiziksel kart","damgalarim"], w:4,
   reply:() => (pending = {yes: () => say("1/3 · Uygulamada <b>Kart</b> sekmesine girin.", [["Sonraki","aktar 2"]]) },
     ["Fiziksel kartınızı 3 adımda uygulamaya taşıyalım; damgalar ve bakiye anında geçer. Başlayalım mı?", [["Evet, başlayalım","evet"],["Uygulamayı indir","/uygulama/"]]]) },
 { id:"aktar2", kw:["aktar 2"], w:6, reply:() => ["2/3 · <b>Kartımı tara</b>'ya dokunun, karttaki kodu kameraya gösterin.", [["Sonraki","aktar 3"]]] },
 { id:"aktar3", kw:["aktar 3"], w:6, reply:() => ["3/3 · Damgalar ve bakiye hesabınıza yazıldı; kart da çalışmaya devam eder. Aktarımı tamamlayanlara <b>ilk sipariş küçük boy kahve bizden</b>.", [["Sipariş ver","sipariş"],["Kulüp sayfası","/kulup/"]]] },
 { id:"etkinlik", kw:["etkinlik","akustik","cupping","konser","muzik","atolye","latte art","program"], w:3,
   reply:() => ["Bu hafta:\n" + FLO_EVENTS.map(e => `• <b>${e.h}</b> — ${e.w}`).join("\n"), [["Yer ayır","yer ayır"],["Etkinlik takvimi","/etkinlikler/"]]] },
 { id:"reserve", kw:["yer ayir","rezervasyon","masa ayir","masa istiyorum","kayit ol"], w:4, reply:() => (FLOWS.reserve.start(), null) },
 { id:"urun", kw:["satin","eve","paket","termos","hediye karti","hediye","urun","kapsul","kargo","harman","cekirdek al"], w:2,
   reply:() => ["Eve götürebilecekleriniz: <b>Sonbahar Harmanı 250 g</b> (420 ₺), <b>Ev Espresso Seti</b> (1.150 ₺), <b>Florida Termos</b> (650 ₺; kendi bardağınızla %10 indirim), <b>dijital hediye kartı</b> (250–2.000 ₺). Uygulamadan ön sipariş, şubeden teslim; kargo yakında.", [["Ürünler","/urunler/"],["Hediye gönder","/urunler/hediye-karti/"]]] },
 { id:"yeni", kw:["yeni","haber","yenilik","kampanya","indirim","acilis","olu saat"], w:2,
   reply:() => { const late = hourNow() >= 14 && hourNow() < 16; return [`${late ? "<b>Şu an ölü saat kampanyası aktif:</b> yoğunluğu düşük şubelerde soğuk kahveler %20 indirimli.\n" : ""}Taze olanlar: Sakarya'da yeni adres, Boğaz Cold Brew sezonu, kart → uygulama kampanyası (ilk kahve bizden), hafta içi 14–16 soğuk kahvelerde %20.`, [["Haberler","/taze/"],["Sipariş ver","sipariş"]]]; } },
 { id:"uygulama", kw:["uygulama","app","indir","ios","android","telefonuma"], w:2,
   reply:() => ["Uygulama iOS ve Android'de: ön sipariş, \"Geldim\", cüzdan, sadakat, kampanyalar. Kurulum bir dakika; kartını aktaran herkese ilk sipariş küçük boy kahve bizden.", [["Uygulama sayfası","/uygulama/"],["Tarayıcıda dene","/app/"]]] },
 { id:"iletisim", kw:["iletisim","telefon","mail","e posta","merkez","genel mudurluk","basin","is birligi","sponsor"], w:2,
   reply:() => ["Merkez: Çengelköy Mah. Görgeç Sok. No:6, Üsküdar / İstanbul · merhaba@floridacoffee.com.tr · +90 216 000 00 00. Şube telefonları şube sayfalarında; basın ve iş birliği için iletişim formu.", [["İletişim sayfası","/iletisim/"],["Bir insanla konuş","insan"]]] },
 { id:"kim", kw:["kimsin","nesin","sen kim","flo","tukan","adin ne","robot"], w:2,
   reply:() => ["Ben Flo, logodaki tukan. Şubeleri, menüyü, standartları ve kampanyaları bilirim; sipariş alır, franchise ve iş başvurusu açar, şikâyeti kayda geçirir, gerektiğinde bir insana aktarırım. Canlıda Claude API ile konuşuyorum; burada kural tabanlı demo.", defaultChips()] },
 { id:"isim", kw:["benim adim","adim"], w:3,
   reply:(t, raw) => { const m = raw.match(/(?:benim adım|adım)\s+([A-Za-zÇĞİÖŞÜçğıöşü]{2,})/i); if (!m) return ["Adınızı nasıl yazayım?", []]; mem.name = m[1][0].toUpperCase() + m[1].slice(1); remember(); return [`Memnun oldum, ${mem.name}. Bir dahaki sefere adınla karşılarım.`, defaultChips()]; } },
 { id:"tesekkur", kw:["tesekkur","sagol","eyvallah","super","harika","tamamdir","iyi bayram"], w:2,
   reply:() => ["Ben teşekkür ederim. Mutluluğun tadıyla kalın ☕", defaultChips()] },
 { id:"evet", kw:["evet","olur","tamam","hadi","baslayalim","istiyorum","aynen"], w:1,
   reply:() => { if (pending) { const p = pending; pending = null; p.yes(); return null; } return ["Neye evet dediğinizi anlayamadım; şunlardan biriyle devam edelim mi?", defaultChips()]; } },
 { id:"hayir", kw:["hayir","yok","istemiyorum","gerek yok","kalsin"], w:1,
   reply:() => { pending = null; return ["Tamam. Başka bir şey?", defaultChips()]; } },
 { id:"baska", kw:["baska bir sey","baska","menu basa","ana menu"], w:1, reply:() => ["Buyurun, ne lazım?", defaultChips()] },
];
const EN_WORDS = ["where","menu","price","open","hours","franchise","how","what","order","nearest","location","thanks","hello","hi "];
function matchIntent(t){
  let best = null, bestScore = 0;
  for (const it of INTENTS) { let s = 0; for (const k of it.kw) if (hit(t, k)) s += it.w + k.length / 8; if (s > bestScore) { best = it; bestScore = s; } }
  return bestScore >= 1.5 ? best : null;
}
const STOP = new Set(["var","mi","mu","ne","bir","icin","nasil","nerede","ile","den","dan","olur","misiniz","misin","bana","ben","siz","ama","her","cok","daha"]);
function faqLookup(t){
  let best = null, bs = 0; const words = t.split(" ").filter(w => w.length > 2 && !STOP.has(w));
  for (const [k, a] of FAQ) { const s = words.filter(w => k.includes(w)).length; if (s > bs) { bs = s; best = a; } }
  return bs >= 1 ? best : null;
}
async function userSays(text){
  const raw = String(text).trim(); if (!raw) return;
  if (raw.startsWith("#")){ closeFlo(); document.querySelector(raw)?.scrollIntoView({behavior: reduce ? "auto" : "smooth"}); return; }
  if (raw.startsWith("/") || raw.startsWith("http")){ location.href = raw; return; }
  bubble(esc(raw), "out"); floIn.value = "";
  const t = norm(raw);
  if (flow) return flowStep(raw);
  if (EN_WORDS.some(w => t.includes(w)) && !has(t,"sube","menu ve")) { stat("en"); return say("I can help in English too: 17 locations in Türkiye and Montenegro, same recipe everywhere (14 g dose, 18–23 s shot). Locations, menu and the app are on the English page.", [["English page","/en/"],["Nearest location","en yakın"],["Menu","/menu/"]]); }
  const p = findProduct(t), b = findBranch(t);
  const it = matchIntent(t);
  if (it) { stat(it.id); const r = it.reply(t, raw); if (r === null || r === undefined) return; return say(r[0], r[1]); }
  if (p) { stat("product"); return say(productCard(p, "Süt: inek dahil, laktozsuz +10 ₺, yulaf/badem +15 ₺."), [["Sipariş ver","sipariş: " + p.n],["Benzer öner","öner"]]); }
  if (b) { stat("branch"); return say(branchCard(b), [["Buradan sipariş","sipariş şube: " + b.n],["Başka şube"]]); }
  const f = faqLookup(t); if (f) { stat("faq"); return say(f, defaultChips()); }
  stat("fallback");
  return say("Bunu tam anlayamadım. Şunlardan biri mi?", [["Sipariş ver","sipariş"],["En yakın şube"],["Ne içsem?","öner"],["Franchise","franchise"],["Bir insanla konuş","insan"]]);
}

/* --- panel, rozet, favicon --- */
function paintCtx(){ if (!floCtx) return; const b = homeBranch(), open = isOpen(b, new Date()); floCtx.innerHTML = `<span class="dot-s ${open ? "g" : "r"}"></span>${b.n} · ${open ? "açık" : "kapalı"} · gün batımı ${sunsetOf(b)}`; }
function greet(){
  const b = homeBranch(), dp = daypart(); mem.visits++; remember(); paintCtx();
  const hello = mem.name ? `${greetWord()}, ${mem.name}!` : `${greetWord()}! Ben <b>Flo</b>, Florida Coffee'nin tukanı.`;
  const line = dp === "sabah" ? `Sıra beklemeden kahve için sipariş alabilirim; ${b.n} ${isOpen(b, new Date()) ? "açık" : "birazdan açılıyor"}.` : dp === "aksam" ? `${b.n}'ta gün batımı <b>${sunsetOf(b)}</b>; manzaralı masa ister misiniz?` : dp === "gece" ? "Gece 02:00'a kadar açık şubelerimiz var; kafeinsiz filtre aynı fiyat." : `Şu an ${openNow().length} şube açık. Ne lazım?`;
  bubble(`${hello} ${line}`, "in", defaultChips());
  const lead = store.get("lead"); if (lead && !mem.seen.includes("lead")) { bubble(`Not: franchise ön başvurunuz kayıtlı (${esc(lead.city)}, puan ${lead.score}). Ekibimiz arayacak.`, "sys"); mem.seen.push("lead"); remember(); }
}
function openFlo(){ floEl.hidden = false; fab.setAttribute("aria-expanded","true"); floHint.classList.remove("on"); badge(false); if (!msgs.children.length) greet(); setTimeout(() => floIn.focus(), 50); }
function closeFlo(){ floEl.hidden = true; fab.setAttribute("aria-expanded","false"); }
fab.addEventListener("click", () => floEl.hidden ? openFlo() : closeFlo());
document.getElementById("floClose").addEventListener("click", closeFlo);
document.getElementById("floForm").addEventListener("submit", e => { e.preventDefault(); userSays(floIn.value); });
addEventListener("keydown", e => { if (e.key === "Escape" && !floEl.hidden) closeFlo(); });
function badge(on){ fab.classList.toggle("has-new", !!on); setFavicon(false, !!on); }
/* favicon: başlıktaki tukan, göz kırpar; yeni mesajda amber nokta */
const favLink = (() => { let l = document.querySelector('link[rel="icon"]'); if (!l) { l = document.createElement("link"); l.rel = "icon"; document.head.appendChild(l); } l.type = "image/svg+xml"; return l; })();
function favSVG(closed, dot){ return "data:image/svg+xml," + encodeURIComponent(`<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><rect width="100" height="100" rx="18" fill="#004854"/><g transform="translate(10 10) scale(.8)"><circle cx="50" cy="50" r="38.3" fill="none" stroke="#EDE6D8" stroke-width="23.4"/><path d="M50 50 L50 0 A50 50 0 0 0 0 50 Z" fill="#F09C1C"/><path d="M50 50 L23.4 50 A26.6 26.6 0 0 0 50 76.6 Z" fill="#D44808"/>${closed ? '<rect x="55" y="39.5" width="13" height="2.6" rx="1.3" fill="#004854"/>' : '<circle cx="61.6" cy="40.8" r="6" fill="#004854"/>'}</g>${dot ? '<circle cx="84" cy="16" r="11" fill="#F09C1C" stroke="#004854" stroke-width="4"/>' : ""}</svg>`); }
let favDot = false;
function setFavicon(closed, dot){ if (dot !== undefined) favDot = dot; favLink.href = favSVG(closed, favDot); }
setFavicon(false, false);
if (!reduce) setInterval(() => { if (document.hidden) return; setFavicon(true); setTimeout(() => setFavicon(false), 140); }, 6000 + Math.random() * 3000);
/* fab: göz, ipucu gösterilince ona bakar */
const fabEye = fab.querySelector(".eyeg");
function glance(x, y, ms){ if (!fabEye || reduce) return; fabEye.style.setProperty("--ex", x); fabEye.style.setProperty("--ey", y); setTimeout(() => { fabEye.style.setProperty("--ex", 0); fabEye.style.setProperty("--ey", 0); }, ms || 1400); }
if (!reduce) setInterval(() => { if (!document.hidden && Math.random() < .5) glance((Math.random() * 6 - 3).toFixed(1), (Math.random() * 3 - 1.5).toFixed(1), 900); }, 5000);


/* bölüm bazlı ipucu balonu: hikâyenin anlatıcısı Flo · tıklanınca o soruyu yanıtlar */
const HINTS = {
  safak:    {t:"{selam} Gün batımı {ss}. Sıra beklemeden kahve ister misin?", s:"sipariş"},
  sabah:    {t:"Sıra beklemeden nasıl olur? Siparişi ben alayım.", s:"sipariş"},
  kahvemiz: {t:"14 g neden tartılır? Anlatayım.", s:"14 g neden tartılır"},
  taze:     {t:"Sakarya'da yeni adres var; kampanyaları da söyleyeyim.", s:"yenilikler"},
  secim:    {t:"Karar veremedin mi? Nasıl hissettiğini söyle, ben seçeyim.", s:"ne içsem"},
  menu:     {t:"Kalori, kafein, alerjen; hangi ürünü soruyorsun?", s:"menü ve fiyatlar"},
  urunler:  {t:"Harmanı eve götürmek ister misin?", s:"eve götür"},
  subeler:  {t:"Sana en yakın şubeyi söyleyeyim mi?", s:"en yakın şube"},
  kulup:    {t:"Kartını uygulamaya aktarmayı anlatayım.", s:"kart aktar"},
  gece:     {t:"Perşembe Kavacık'ta akustik var; yer ayırayım mı?", s:"etkinlikler"},
  franchise:{t:"Kendi şehrinde Florida? 2 dakikada ön başvuru.", s:"franchise"},
  basvuru:  {t:"Franchise başvurusu için buradayım.", s:"franchise"},
  kariyer:  {t:"Barista olmak deneyim istemez; ön kaydını 1 dakikada alayım.", s:"kariyer"},
  kurumsal: {t:"Ofis ikramı mı, etkinlik barı mı? Teklif 1 iş günü.", s:"kurumsal"},
  iletisim: {t:"Bir insanla konuşmak istersen aktarırım.", s:"bir insanla konuş"},
  sss:      {t:"Soruyu bana yaz, SSS'de aramana gerek yok.", s:"laktozsuz süt var mı"},
  uygulama: {t:"Uygulamada neler var, göstereyim mi?", s:"uygulama"},
  app:      {t:"Demo siparişi birlikte verelim mi?", s:"sipariş"},
  etkinlikler:{t:"Bu haftanın programı bende; yer ayırayım mı?", s:"etkinlikler"},
  product:  {t:"{p} hakkında ne sormak istersin? Fiyat, kalori, süt.", s:"{p}"},
  branch:   {t:"{b} şu an {open}. Buradan sipariş vereyim mi?", s:"sipariş şube: {b}"},
};
function pageHint(){
  const m = PATH.match(/\/menu\/([a-z0-9-]+)\//); if (m) { const p = MENU_ALL.find(x => x.slug === m[1]); if (p) return Object.assign({}, HINTS.product, {t: HINTS.product.t.replace("{p}", p.n), s: p.n}); }
  const mb = PATH.match(/\/subeler\/([a-z0-9-]+)\//); if (mb) { const b = B.find(x => x.id === mb[1]); if (b) return {t: HINTS.branch.t.replace("{b}", b.n).replace("{open}", isOpen(b, new Date()) ? "açık" : "kapalı"), s: HINTS.branch.s.replace("{b}", b.n)}; }
  const seg = PATH.split("/").filter(Boolean); const key = seg.find(x => HINTS[x] && x !== "basvuru") || (seg.includes("basvuru") ? "franchise" : null);
  return HINTS[key] || HINTS[PAGE] || HINTS.safak;
}
let lastHint = "", hintTimer, hintSend = "";
function showHint(id){ if (id === lastHint || !floEl.hidden) return; lastHint = id; ctxSection = id;
  const h = document.body.dataset.page ? pageHint() : (HINTS[id] || HINTS.safak);
  const ss = sunsetOf(homeBranch()); hintSend = h.s;
  floHint.textContent = h.t.replace("{ss}", ss).replace("{selam}", mem.name ? `${greetWord()} ${mem.name}!` : `${greetWord()}!`);
  floHint.classList.add("on"); glance(-4, 0, 1600); clearTimeout(hintTimer); hintTimer = setTimeout(() => floHint.classList.remove("on"), 6500); }
floHint.addEventListener("click", e => { e.stopPropagation(); floHint.classList.remove("on"); openFlo(); if (hintSend) userSays(hintSend); });

showHint(document.body.dataset.page || "safak");
