#!/usr/bin/env python3
"""Menü araçları — tek kaynak menu.json.
  python3 menu_tools.py sync     → index.html içindeki `const MENU = {...}` bloğunu menu.json'dan yeniden yazar
  GEMINI_API_KEY=... python3 menu_tools.py images [--threads 3] [--only slug,slug]
                                 → her ürün için img/menu/<slug>.jpg üretir (Nano Banana Pro, 1:1); mevcutlar atlanır
Anahtar yalnız ortam değişkeninden okunur, dosyaya yazılmaz.
"""
import os, sys, re, io, json, base64, time, argparse, urllib.request, urllib.error
from concurrent.futures import ThreadPoolExecutor, as_completed

HERE = os.path.dirname(os.path.abspath(__file__))
MENU = json.load(open(os.path.join(HERE, "menu.json"), encoding="utf-8"))
slug = lambda s: re.sub(r'[^a-z0-9]+', '-', s.lower().translate(str.maketrans("çğıöşüâî", "cgiosuai"))).strip("-")

# Rakip ürün fotoğraflarının ortak dili (Espressolab, Kahve Dünyası, Coffy vitrinleri): tek açı, tek zemin, tek ışık,
# ürün merkezde, arka plan sade. Bunu marka renklerimizle sabitliyoruz.
STYLE = ("Menu product photograph for a specialty coffee chain, part of one consistent series. Camera at 40 degrees, "
         "subject centered and filling most of the frame, on a light cream stone tabletop. Soft diffused window light from the "
         "left, one gentle shadow. Background: softly blurred petrol-teal (#004854) tiled wall with a faint warm amber bokeh. "
         "Hot drinks in cream ceramic cups with a small toucan emblem (amber upper quadrant, burnt-orange lower quadrant); "
         "cold drinks in clear tall glasses with a cream paper straw; food on cream ceramic plates. No hands, no people, no text, "
         "no letters, no logos other than the small toucan emblem, no extra props beyond those described. Square 1:1. "
         "Photorealistic, natural colors, no HDR, no oversaturation, subtle film grain.")

def sync():
    p = os.path.join(HERE, "index.html"); h = open(p, encoding="utf-8").read()
    i = h.index("const MENU = {"); j = h.index("\nlet curCat")
    cats = list(MENU["kategoriler"])
    lines = ["const MENU = {"]
    for ci, c in enumerate(cats):
        lines.append(f"  {c}: [")
        rows = [u for u in MENU["urunler"] if u["cat"] == c]
        for ri, u in enumerate(rows):
            tags = json.dumps(u["tags"], ensure_ascii=False)
            lines.append(f'    [{json.dumps(u["name"], ensure_ascii=False)},{json.dumps(u["desc"], ensure_ascii=False)},"{u["price"]}",{tags}]' + ("," if ri < len(rows) - 1 else ""))
        lines.append("  ]" + ("," if ci < len(cats) - 1 else ""))
    lines.append("};")
    h = h[:i] + "\n".join(lines) + h[j:]
    open(p, "w", encoding="utf-8").write(h)
    print(f"MENU bloğu yazıldı: {len(MENU['urunler'])} ürün, {len(cats)} kategori")

def gen_one(key, model, u, out):
    prompt = f"{u['shot'][0].upper() + u['shot'][1:]}. Item: {u['name']} ({u['desc']}).\n\n{STYLE}"
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
    body = {"contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"responseModalities": ["IMAGE"], "imageConfig": {"aspectRatio": "1:1"}}}
    req = urllib.request.Request(url, data=json.dumps(body).encode(), headers={"Content-Type": "application/json", "x-goog-api-key": key})
    for i in range(4):
        try:
            with urllib.request.urlopen(req, timeout=240) as r: data = json.load(r)
            for part in data.get("candidates", [{}])[0].get("content", {}).get("parts", []):
                if "inlineData" in part:
                    from PIL import Image
                    im = Image.open(io.BytesIO(base64.b64decode(part["inlineData"]["data"]))).convert("RGB")
                    if max(im.size) > 1200: im = im.resize((1200, 1200), Image.LANCZOS)
                    im.save(out, "JPEG", quality=86, optimize=True, progressive=True)
                    return os.path.getsize(out)
            raise RuntimeError("yanıtta görsel yok")
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 503) and i < 3: time.sleep(10 * (i + 1)); continue
            raise RuntimeError(f"HTTP {e.code}: {e.read().decode()[:200]}")

def images(threads, only, model):
    key = os.environ.get("GEMINI_API_KEY") or sys.exit("GEMINI_API_KEY yok")
    outdir = os.path.join(HERE, "img", "menu"); os.makedirs(outdir, exist_ok=True)
    todo = []
    for u in MENU["urunler"]:
        s = slug(u["name"])
        if only and s not in only: continue
        out = os.path.join(outdir, s + ".jpg")
        if os.path.exists(out): continue
        todo.append((u, out))
    print(f"{len(todo)} görsel üretilecek ({threads} paralel)", flush=True)
    with ThreadPoolExecutor(threads) as ex:
        futs = {ex.submit(gen_one, key, model, u, out): (u, out) for u, out in todo}
        for f in as_completed(futs):
            u, out = futs[f]
            try: print("✓", os.path.basename(out), f.result() // 1024, "KB", flush=True)
            except Exception as e: print("✗", os.path.basename(out), e, flush=True)

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("cmd", choices=["sync", "images"])
    ap.add_argument("--threads", type=int, default=3); ap.add_argument("--only", default=""); ap.add_argument("--model", default="gemini-3-pro-image")
    a = ap.parse_args()
    if a.cmd == "sync": sync()
    else: images(a.threads, set(filter(None, a.only.split(","))), a.model)
