#!/usr/bin/env python3
"""img/<ad>.(jpg|png|webp) dosyalarını index.html içindeki .ph[data-img=<ad>] yuvalarına data-URI olarak gömer.
Artifact tek HTML dosyası olduğu için harici görsel yükleyemez; yayın öncesi bu betik çalıştırılır. Yeniden çalıştırmak güvenlidir."""
import re, io, os, base64, sys
from PIL import Image
here = os.path.dirname(os.path.abspath(__file__))
html_path = os.path.join(here, "index.html")
s = open(html_path, encoding="utf-8").read()
MAXW = {"hero":1800, "sunset":1600, "night":1600, "franchise":1600, "sakarya":1600}
def load(name):
    for ext in ("jpg","jpeg","png","webp"):
        p = os.path.join(here, "img", f"{name}.{ext}")
        if os.path.exists(p): return p
def to_data_uri(path, maxw):
    im = Image.open(path).convert("RGB")
    if im.width > maxw: im = im.resize((maxw, round(im.height*maxw/im.width)), Image.LANCZOS)
    buf = io.BytesIO(); im.save(buf, "JPEG", quality=82, optimize=True, progressive=True)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode(), len(buf.getvalue())
total = 0; done = []
# önceki gömmeleri temizle
s = re.sub(r'<img class="emb"[^>]*>', '', s)
s = re.sub(r'(<figure class="ph)( has)?', r'\1', s)
for m in list(re.finditer(r'<figure class="ph([^"]*)"([^>]*)data-img="([^"]+)"([^>]*)>', s)):
    name = m.group(3); path = load(name)
    if not path: continue
    uri, n = to_data_uri(path, MAXW.get(name, 1200)); total += n
    tag = f'<figure class="ph has{m.group(1)}"{m.group(2)}data-img="{name}"{m.group(4)}><img class="emb" src="{uri}" alt="">'
    s = s.replace(m.group(0), tag, 1); done.append(f"{name}:{n//1024}KB")
open(html_path, "w", encoding="utf-8").write(s)
print("gömüldü:", ", ".join(done) or "hiç (img/ boş)", "| toplam", total//1024, "KB")
