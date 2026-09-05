#!/usr/bin/env python3
"""img/<ad>.(jpg|png) dosyalarını index.html içindeki .ph[data-img=<ad>] yuvalarına
JPEG data-URI olarak gömer (artifact harici dosya yükleyemez). Tekrar çalıştırılabilir:
önceki gömülü <img data-embedded> etiketlerini temizleyip yeniden yazar.
Kullanım: python3 embed_images.py [--max 1600] [--q 82] [--out index.html]
"""
import os, re, io, base64, argparse
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))

def to_jpeg_data_uri(path, max_side, q):
    im = Image.open(path).convert("RGB")
    w, h = im.size
    if max(w, h) > max_side:
        r = max_side / max(w, h); im = im.resize((round(w*r), round(h*r)), Image.LANCZOS)
    buf = io.BytesIO(); im.save(buf, "JPEG", quality=q, optimize=True, progressive=True)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode(), len(buf.getvalue())

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--max", type=int, default=1600)
    ap.add_argument("--q", type=int, default=82)
    ap.add_argument("--src", default="index.html")
    ap.add_argument("--out", default="index.html")
    ap.add_argument("--videos", default="hero", help="data-URI olarak gömülecek videolar (virgülle); boyut için yalnız hero varsayılan")
    a = ap.parse_args()
    html = open(os.path.join(HERE, a.src), encoding="utf-8").read()
    # önceki gömmeleri temizle
    html = re.sub(r'<img[^>]*data-embedded[^>]*>', '', html)
    html = re.sub(r'(<figure class="ph)([^"]*?) has(")', r'\1\2\3', html)
    total = 0; done = []
    def sub(m):
        nonlocal total
        cls, rest, name = m.group(1), m.group(2), m.group(3)
        src = None
        for ext in ("jpg", "png", "webp"):
            p = os.path.join(HERE, "img", f"{name}.{ext}")
            if os.path.exists(p): src = p; break
        if not src: return m.group(0)
        uri, n = to_jpeg_data_uri(src, a.max, a.q); total += n; done.append(name)
        # hero-bg de dahil: sınıfa ' has' ekle ve img'yi figure'ün başına koy
        tail = m.group(4)
        return f'<figure class="ph{cls} has"{rest}data-img="{name}"{tail}><img data-embedded alt="" src="{uri}">'
    html = re.sub(r'<figure class="ph([^"]*)"([^>]*?)data-img="([a-z0-9_-]+)"([^>]*)>', sub, html)
    # marka görselleri (nav/footer kelime işareti) → data-URI
    def brand(m):
        p = os.path.join(HERE, "brand", m.group(2) + ".png")
        if not os.path.exists(p): return m.group(0)
        return m.group(1) + "data:image/png;base64," + base64.b64encode(open(p, "rb").read()).decode() + m.group(3)
    html, nb = re.subn(r'(<img class="wm" data-brand="([a-z0-9_-]+)" alt="" src=")[^"]*(")', brand, html)
    # videolar: seçilenler data-URI, diğerleri video/<ad>.mp4 (artifact'ta yüklenmez, alttaki görsel kalır)
    vids = set(filter(None, a.videos.split(",")))
    def vid(m):
        name = m.group(2); p = os.path.join(HERE, "video", name + ".mp4")
        if name in vids and os.path.exists(p):
            return m.group(1) + "data:video/mp4;base64," + base64.b64encode(open(p, "rb").read()).decode() + m.group(3)
        return m.group(1) + f"video/{name}.mp4" + m.group(3)
    html, nv = re.subn(r'(<video[^>]*data-vid="([a-z0-9_-]+)"[^>]*><source src=")[^"]*(")', vid, html)
    open(os.path.join(HERE, a.out), "w", encoding="utf-8").write(html)
    print(f"marka görseli: {nb}, video etiketi: {nv} (gömülü: {', '.join(sorted(vids))})")
    print(f"gömüldü: {len(done)} görsel, toplam {total//1024} KB → {a.out}")
    print(", ".join(done))

if __name__ == "__main__": main()
