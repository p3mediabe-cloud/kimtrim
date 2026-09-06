#!/usr/bin/env python3
"""Florida Coffee demo görselleri — Gemini (Nano Banana Pro) ile üretim.
Kullanım:  GEMINI_API_KEY=... python3 gen_images.py [--model gemini-3-pro-image] [--only hero,cup]
Çıktı:     img/<ad>.png  (mevcut dosyalar atlanır)
"""
import os, sys, json, base64, time, urllib.request, urllib.error, argparse

BRAND = ("Brand palette: deep petrol teal #004854, warm amber #F09C1C, burnt orange #D44808, "
         "soft cream #EDE6D8. Cups are cream paper with a petrol teal lower band and a small toucan-head "
         "emblem made of an amber upper quadrant and burnt-orange lower quadrant. No readable text, no letters, "
         "no watermark. Photorealistic editorial photography, natural light, shallow depth of field, "
         "Fujifilm-like color, subtle film grain, no HDR, no oversaturation, no AI gloss.")

SHOTS = {
 "hero":      ("16:9", "Sunrise over the Bosphorus seen from a café terrace in Kavacık, Istanbul. Foreground: a cream paper coffee cup with petrol-teal band on a wooden rail, steam rising, sea and ferry lights softly blurred behind. Golden-hour amber light meeting cool teal water."),
 "sunset":    ("16:9", "Golden hour on a waterfront café terrace in Beykoz, Istanbul, Bosphorus bridge far in the haze. Two people at a table, faces turned away, two cream cups with teal band. Amber sun flare, long shadows, teal water."),
 "night":     ("16:9", "Late night café terrace on the Bosphorus, 1 a.m., string lights, opposite shore lights reflecting on black water, a single cream cup with teal band on the table, warm amber lamp glow against deep petrol night."),
 "barista":   ("4:3",  "A barista's hands weighing 14 grams of ground coffee on a small scale beside an espresso machine portafilter, close-up, cream and petrol-teal café interior, amber accent light, shallow focus."),
 "pour":      ("4:3",  "Close-up of espresso extracting into a cream ceramic cup, honey-thick stream, chrome group head, petrol-teal tiled bar behind, amber pendant light reflection."),
 "latteart":  ("1:1",  "Top-down flat lay of a flat white with rosetta latte art in a cream cup with petrol-teal band, on a light oak table, one amber-colored coffee bean bag corner visible, morning light."),
 "coldbrew":  ("1:1",  "Cold brew with tonic and orange peel in a tall glass, condensation, ice, served on a teal ceramic tray, Bosphorus terrace background out of focus, bright noon light."),
 "beans":     ("4:3",  "Freshly roasted medium-roast arabica beans spilling from a cream paper bag with a petrol-teal band onto a dark walnut counter, single amber pendant light, macro detail, roast oil sheen subtle."),
 "workspace": ("4:3",  "A quiet upstairs work area of a café in Kadıköy: laptops, cream cups with teal band, plants, big windows, petrol-teal accent wall, a young person working, natural daylight."),
 "sakarya":   ("16:9", "Street-front café on a lively pedestrian avenue in a Turkish city at dusk, big glass façade glowing amber, petrol-teal awning, students chatting outside with cream cups with teal band."),
 "cup":       ("1:1",  "Product shot: a single cream paper coffee cup with a petrol-teal lower band and a small amber-and-burnt-orange toucan-head emblem, white lid, on a plain cream background, soft studio light, slight shadow."),
 "franchise": ("16:9", "Warm café interior seen through the front window at blue hour, petrol-teal façade, amber interior light, a chalk-free blank sign, staff in cream aprons, inviting, cinematic."),
 # ---- v15: Instagram yerine üretilen ek sahneler ----
 "ekip":      ("16:9", "Four baristas in cream aprons with a small petrol-teal chest emblem laughing together behind a petrol-teal tiled counter of a café in Istanbul, mid-shift, one holding a cream cup with teal band, warm amber pendant lights, morning light from a big window, candid editorial, genuine expressions, diverse ages 20 to 35."),
 "egitim":    ("4:3",  "Barista training room: a trainer guides a young trainee pouring latte art into a cream cup, both in cream aprons, a row of six practice cups on a petrol-teal counter, a wall-mounted scale and timer, amber accent light, focused calm mood."),
 "akustik":   ("16:9", "Evening acoustic set on a Bosphorus café terrace in Kavacık: a duo with an acoustic guitar and a cajón under warm string lights, a small audience at tables with cream cups with teal band, the bridge lights far behind on dark teal water, amber glow, people seen from behind or in profile."),
 "cupping":   ("4:3",  "Coffee cupping session in a café in Çengelköy: a long light-oak table with a row of white cupping bowls, cupping spoons, small cream cards, six people leaning in from the sides, hands and spoons in focus, faces softly blurred, petrol-teal wall, daylight from the left."),
 "hasat":     ("16:9", "Coffee harvest on a highland farm in Ethiopia at golden hour: a farmer's hands picking ripe red coffee cherries from a branch, woven basket, misty green hills behind, warm amber sun, shallow focus, respectful documentary style."),
 "kavurma":   ("4:3",  "Small-batch coffee roastery: a roast master in a cream apron checks beans on the sample trier of a drum roaster, chaff and warm haze in amber light, petrol-teal painted roaster body, cream paper bags with teal band stacked on a walnut shelf."),
 "acilis":    ("16:9", "Opening day of a new café on a pedestrian street in Sakarya, Turkey: a cheerful queue of students and families outside a glass façade with a petrol-teal awning, amber and cream balloons, staff in cream aprons handing out cream cups with teal band, bright afternoon light, celebratory but tasteful."),
 "kurumsal":  ("16:9", "Corporate coffee delivery in a modern Istanbul office meeting room: a barista in a cream apron places a cream cardboard carrier box of cups with teal band and a thermal jug on a long table, glass walls, city view, petrol-teal and amber details, clean daylight."),
 "gecefiltre": ("4:3",  "Night terrace of a Bosphorus café after 22:00: a person seen from behind in a light jacket reads a paperback at a small table, a cream cup with teal band of filter coffee beside a small amber lantern, opposite shore lights as bokeh on black water, calm, quiet, cinematic."),
 "teslim":    ("4:3",  "Mobile-order pick-up shelf in a café: a petrol-teal wooden shelf with three cream cups with teal band, each with a small handwritten cream label, a phone held in the foreground showing a blurred order screen, amber accent light, shallow focus."),
}

def call(model, key, prompt, aspect, retries=3):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={key}"
    body = {"contents":[{"parts":[{"text": prompt + "\n\n" + BRAND}]}],
            "generationConfig":{"responseModalities":["IMAGE"],"imageConfig":{"aspectRatio":aspect}}}
    req = urllib.request.Request(url, data=json.dumps(body).encode(), headers={"Content-Type":"application/json"})
    for i in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=180) as r:
                data = json.load(r)
            for part in data.get("candidates",[{}])[0].get("content",{}).get("parts",[]):
                if "inlineData" in part:
                    return base64.b64decode(part["inlineData"]["data"]), part["inlineData"].get("mimeType","image/png")
            raise RuntimeError("yanıtta görsel yok: " + json.dumps(data)[:300])
        except urllib.error.HTTPError as e:
            msg = e.read().decode()[:300]
            if e.code in (429,500,503) and i < retries-1:
                time.sleep(8*(i+1)); continue
            raise RuntimeError(f"HTTP {e.code}: {msg}")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="gemini-3-pro-image")
    ap.add_argument("--only", default="")
    a = ap.parse_args()
    key = os.environ.get("GEMINI_API_KEY")
    if not key: sys.exit("GEMINI_API_KEY ortam değişkeni yok.")
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "img")
    os.makedirs(out, exist_ok=True)
    wanted = [s.strip() for s in a.only.split(",") if s.strip()] or list(SHOTS)
    for name in wanted:
        aspect, prompt = SHOTS[name]
        path = os.path.join(out, name + ".png")
        if any(os.path.exists(os.path.join(out, name + e)) for e in (".png",".jpg",".webp")): print("atla  ", name); continue
        try:
            img, mime = call(a.model, key, prompt, aspect)
            if "jpeg" in mime: path = path[:-4] + ".jpg"
            open(path, "wb").write(img); print("tamam ", name, len(img)//1024, "KB")
        except Exception as e:
            print("HATA  ", name, e)

if __name__ == "__main__": main()
