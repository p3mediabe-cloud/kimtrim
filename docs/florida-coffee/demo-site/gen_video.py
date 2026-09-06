#!/usr/bin/env python3
"""Veo 3.1 ile marka videoları: img/<kare>.jpg ilk kare olarak verilir (görüntü→video).
Anahtar yalnız GEMINI_API_KEY ortam değişkeninden okunur; dosyaya yazılmaz.
Kullanım: GEMINI_API_KEY=... python3 gen_video.py [ad ...]   (varsayılan: hepsi, mevcut .mp4 atlanır)
"""
import os, sys, json, time, base64, io, urllib.request
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
KEY = os.environ.get("GEMINI_API_KEY") or sys.exit("GEMINI_API_KEY yok")
MODEL = "veo-3.1-fast-generate-preview"
API = "https://generativelanguage.googleapis.com/v1beta"
BRAND = ("Brand: Florida Coffee, Istanbul. Palette petrol teal #004854, amber #F09C1C, rust #D44808, cream. "
         "One continuous shot, no cuts, no scene changes, loopable. Photoreal, cinematic, natural light, shallow depth of field, no text, no logos, no captions, no talking, no people looking at camera.")
SHOTS = {
  # ad: (ilk kare, prompt, oran)
  "hero":  ("hero", "Slow cinematic push-in on a cream takeaway cup with a teal band on a terrace rail above the Bosphorus at golden hour. Steam curls gently from the lid, water glitters, a ferry drifts in the far distance, light wind moves a napkin slightly. Calm, warm, premium.", "16:9"),
  "hero2": ("hero_end", "Continuation of the same shot, same cup on the same terrace rail above the Bosphorus. The camera drifts slowly to the right and pulls back a little as golden hour fades into blue dusk: the bridge lights and the far shore light up one by one, a ferry glides past with its lights on, steam keeps rising from the cup. Ends on a calm, wide, glowing evening frame.", "16:9"),
  "pour":  ("pour", "Macro slow motion: espresso streams from a portafilter into a small cup, tiger-striped crema forming, tiny bubbles. Warm amber light, teal-tiled wall softly out of focus. Steady camera, gentle rack focus.", "16:9"),
  "night": ("night", "Vertical: a Florida Coffee shop window glows amber at night on a Bosphorus street, rain-wet pavement reflects the light, a person in a coat walks past carrying a cream cup, cars pass with soft bokeh. Slow lateral dolly.", "9:16"),
}

def call(url, data=None):
    req = urllib.request.Request(url, data=json.dumps(data).encode() if data is not None else None,
                                 headers={"x-goog-api-key": KEY, "Content-Type": "application/json"})
    return json.load(urllib.request.urlopen(req, timeout=120))

def gen(name):
    frame, prompt, ar = SHOTS[name]
    out = os.path.join(HERE, "video", f"{name}.mp4")
    if os.path.exists(out): print("var, atlandı:", name); return
    # ilk kare hedef orana merkezden kırpılır; aksi hâlde Veo siyah bantla başlar
    im = Image.open(os.path.join(HERE, "img", f"{frame}.jpg")).convert("RGB"); w, h = im.size
    tw, th = map(int, ar.split(":")); t = tw / th
    if w / h > t: nw = round(h * t); im = im.crop(((w - nw) // 2, 0, (w - nw) // 2 + nw, h))
    else: nh = round(w / t); im = im.crop((0, (h - nh) // 2, w, (h - nh) // 2 + nh))
    buf = io.BytesIO(); im.save(buf, "JPEG", quality=92); img = buf.getvalue()
    body = {"instances": [{"prompt": prompt + " " + BRAND,
                           "image": {"bytesBase64Encoded": base64.b64encode(img).decode(), "mimeType": "image/jpeg"}}],
            "parameters": {"aspectRatio": ar, "resolution": "720p", "durationSeconds": 8,
                           "negativePrompt": "text, watermark, logo, subtitles, distorted hands, cartoon, oversaturated"}}
    op = call(f"{API}/models/{MODEL}:predictLongRunning", body)
    print(name, "başladı:", op["name"], flush=True)
    for _ in range(90):
        time.sleep(10)
        st = call(f"{API}/{op['name']}")
        if st.get("done"):
            if "error" in st: print(name, "HATA:", st["error"]); return
            r = st["response"]
            samples = r.get("generateVideoResponse", r).get("generatedSamples") or r.get("videos") or []
            if not samples: print(name, "örnek yok:", json.dumps(r)[:500]); return
            uri = samples[0]["video"]["uri"]
            req = urllib.request.Request(uri, headers={"x-goog-api-key": KEY})
            data = urllib.request.urlopen(req, timeout=300).read()
            os.makedirs(os.path.dirname(out), exist_ok=True); open(out, "wb").write(data)
            print(name, "kaydedildi", len(data)//1024, "KB", flush=True); return
    print(name, "zaman aşımı")

if __name__ == "__main__":
    names = sys.argv[1:] or list(SHOTS)
    for n in names: gen(n)
