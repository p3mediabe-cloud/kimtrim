#!/usr/bin/env python3
"""Şube fotoğrafları — her şube için karakterine (şehir, manzara, gece, çalışma, kahvaltı) göre markalı 16:9 kare.
Kaynak: index.html içindeki `const B` şube verisi. Çıktı: img/subeler/<id>.jpg (mevcutlar atlanır).
GEMINI_API_KEY=... python3 gen_branches.py [--threads 3] [--only kavacik,budva]
"""
import os, sys, re, io, json, base64, time, argparse, urllib.request, urllib.error
from concurrent.futures import ThreadPoolExecutor, as_completed

HERE = os.path.dirname(os.path.abspath(__file__))
STYLE = ("Editorial architectural photograph of a specialty coffee shop, part of one consistent brand series. "
         "The shop is unmistakably one brand: petrol-teal (#004854) façade or awning, cream interior walls, warm amber (#F09C1C) "
         "pendant lights, light oak tables, a cream paper cup with a teal band and a tiny toucan emblem visible somewhere. "
         "No readable signage text, no letters, no logos other than the tiny toucan emblem, no visible faces (people only from behind or far away). "
         "16:9, natural light, photorealistic, subtle film grain, no HDR, no oversaturation.")

# şube kimliğine göre sahne (özellik etiketleri + not)
SCENES = {
 "kavacik":   "Upper-floor terrace of a café in Kavacık, Istanbul at golden hour: wooden rail, cream cups on tables, the Bosphorus and the Fatih Sultan Mehmet bridge in warm haze below.",
 "beykoz":    "Waterfront café on the Beykoz shore at dusk, string lights just switched on, a few tables outside by the water, Bosphorus ferry lights in the distance.",
 "cengelkoy": "The original flagship café in historic Çengelköy: a small stone-and-wood building with a petrol-teal awning on a narrow street near the water, morning light, a cupping table visible through the window.",
 "kadikoy":   "Bright upstairs work floor of a café in Kadıköy: long oak tables, people working on laptops seen from behind, big windows onto a lively street, plants, sockets on tables.",
 "talimhane": "Compact corner café in Taksim Talimhane at 07:30, early morning light on wet pavement, hotels behind, a barista seen from behind opening the counter.",
 "taksim":    "Busy street-front café near Taksim square late at night, amber interior glow, quick takeaway counter, people passing with cream cups, city lights.",
 "bahcesehir": "Spacious family café in Bahçeşehir with a wide parking lot outside, big glass façade, a children's reading corner and large family tables inside, afternoon light.",
 "umraniye":  "Modern café on an office avenue in Ümraniye at lunch hour, glass façade reflecting office buildings, a short queue seen from behind, clean lines.",
 "esenyurt":  "Street-front café in Esenyurt on a broad avenue, fast takeaway window, petrol-teal façade, midday light, cars blurred in front.",
 "izmit":     "Café across from a green park in İzmit, weekend terrace with cream cups, trees, families walking in the park seen from afar.",
 "sakarya":   "Café near the university on Çark Caddesi in Sakarya at midnight during exam season, warm light inside, students studying seen from behind through the window.",
 "bursa":     "Large boulevard café in Nilüfer, Bursa: wide interior with high ceiling, long counter, oak tables, mountains faint through the window, afternoon light.",
 "samsun":    "Café overlooking the marina in Atakum, Samsun at sunset, sailboats and masts, the sun setting over the Black Sea, terrace tables with cream cups.",
 "rize":      "Small café on the coastal road in Rize with tea gardens on the green hills behind, a Turkish tea glass and a cream coffee cup side by side on a wooden table, soft overcast light.",
 "erzincan":  "The first third-wave coffee shop in Erzincan: a cozy modern café interior with snowy mountains outside the window, winter morning light, one cream cup on the counter.",
 "podgorica": "Modern café in Podgorica, Montenegro: stone façade with petrol-teal awning on a sunny Mediterranean street, outdoor tables, cream cups, bright light.",
 "budva":     "Café on the Adriatic promenade in Budva, Montenegro at night in summer: turquoise sea and old town walls behind, string lights, terrace tables, cream cups.",
}

def branches():
    h = open(os.path.join(HERE, "index.html"), encoding="utf-8").read()
    raw = re.search(r'const B = \[(.*?)\n\];', h, re.S).group(1)
    return [(m.group(1), m.group(2), m.group(3)) for m in re.finditer(r'\{id:"([^"]+)", n:"([^"]+)", c:"([^"]+)"', raw)]

def gen_one(key, model, bid, name, city, out):
    prompt = f"{SCENES.get(bid, f'A café in {city}.')} Location: {name}, {city}.\n\n{STYLE}"
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
    body = {"contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"responseModalities": ["IMAGE"], "imageConfig": {"aspectRatio": "16:9"}}}
    req = urllib.request.Request(url, data=json.dumps(body).encode(), headers={"Content-Type": "application/json", "x-goog-api-key": key})
    for i in range(4):
        try:
            with urllib.request.urlopen(req, timeout=240) as r: data = json.load(r)
            for part in data.get("candidates", [{}])[0].get("content", {}).get("parts", []):
                if "inlineData" in part:
                    from PIL import Image
                    im = Image.open(io.BytesIO(base64.b64decode(part["inlineData"]["data"]))).convert("RGB")
                    if im.width > 1600: im = im.resize((1600, round(im.height * 1600 / im.width)), Image.LANCZOS)
                    im.save(out, "JPEG", quality=84, optimize=True, progressive=True)
                    return os.path.getsize(out)
            raise RuntimeError("yanıtta görsel yok")
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 503) and i < 3: time.sleep(10 * (i + 1)); continue
            raise RuntimeError(f"HTTP {e.code}: {e.read().decode()[:200]}")

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--threads", type=int, default=3); ap.add_argument("--only", default=""); ap.add_argument("--model", default="gemini-3-pro-image")
    a = ap.parse_args(); only = set(filter(None, a.only.split(",")))
    key = os.environ.get("GEMINI_API_KEY") or sys.exit("GEMINI_API_KEY yok")
    outdir = os.path.join(HERE, "img", "subeler"); os.makedirs(outdir, exist_ok=True)
    todo = [(b, os.path.join(outdir, b[0] + ".jpg")) for b in branches() if (not only or b[0] in only) and not os.path.exists(os.path.join(outdir, b[0] + ".jpg"))]
    print(f"{len(todo)} şube görseli üretilecek", flush=True)
    with ThreadPoolExecutor(a.threads) as ex:
        futs = {ex.submit(gen_one, key, a.model, *b, out): (b, out) for b, out in todo}
        for f in as_completed(futs):
            (b, out) = futs[f]
            try: print("✓", os.path.basename(out), f.result() // 1024, "KB", flush=True)
            except Exception as e: print("✗", os.path.basename(out), e, flush=True)
