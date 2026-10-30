# -*- coding: utf-8 -*-
"""
Huawei Temalar tasarımcı başvurusu için zip paketi üretir:
yalnız PNG, klasörsüz, ≤50 dosya, ≤50 MB.   python tasarimlar/basvuru_paketi.py
Çıktı: tanitim/WatchFaceGT3_basvuru.zip (+ tanitim/zip/ içindeki dosyalar)
"""
import os
import sys
import zipfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw, ImageFont
import ortak

KOK = ortak.KOK
ONIZ = os.path.join(KOK, "onizleme")
ZIPD = os.path.join(KOK, "tanitim", "zip")
os.makedirs(ZIPD, exist_ok=True)
for f in os.listdir(ZIPD):
    os.remove(os.path.join(ZIPD, f))

mask = Image.new("L", (466, 466), 0)
ImageDraw.Draw(mask).ellipse([1, 1, 464, 464], fill=255)


def yuvarlak(name):
    im = Image.open(os.path.join(ONIZ, name + ".png")).convert("RGBA")
    im.putalpha(mask)
    return im


KLASIK = [("Klasik", "aktif_siyah", "aktif_yesil_10_09", "aod_10_09"),
          ("Gece", "gece_aktif", "gece_aktif_2", "gece_aod"),
          ("Porselen", "porselen_aktif", "porselen_aktif_2", "porselen_aod"),
          ("Giyoş", "giyos_aktif", "giyos_aktif_2", "giyos_aod"),
          ("Zarif", "zarif_aktif", "zarif_aktif_2", "zarif_aod")]
RENKLI = [("Mercan", "mercan_aktif", "mercan_aod"), ("Halka", "halka_aktif", "halka_aod"),
          ("Retro", "retro_aktif", "retro_aod"), ("Prizma", "prizma_aktif", "prizma_aod")]

# ---- portfolyo sayfası (1920x1080)
img = Image.new("RGBA", (1920, 1080), (16, 16, 18, 255))
d = ImageDraw.Draw(img)
fb, fr, fl = ortak.font("georgiab", 54), ortak.font("reg", 26), ortak.font("reg", 22)
d.text((80, 56), "WatchFaceGT3  —  Klasik Kadran Koleksiyonu / Classic Watch Face Collection", font=fb, fill=(222, 200, 150))
d.text((80, 128), "Huawei Watch GT 3 · 466×466 · Her kadranda 5 veri: adım, nabız, pil, tarih, gün / 5 data types each · AOD <%4",
       font=fr, fill=(190, 190, 190))
x0, y0, cell = 80, 200, 340
for i, (ad, a, _, o) in enumerate(KLASIK):
    x = x0 + i * (cell + 20)
    img.alpha_composite(yuvarlak(a).resize((cell, cell), Image.LANCZOS), (x, y0))
    img.alpha_composite(yuvarlak(o).resize((cell // 2, cell // 2), Image.LANCZOS), (x + cell // 4, y0 + cell + 24))
    d.text((x + cell // 2, y0 + cell + 24 + cell // 2 + 28), ad + "  ·  AOD", font=fl, fill=(200, 200, 200), anchor="mm")
d.text((80, 1030), "Tüm katmanlar Python/Pillow ile üretilir (Theme Studio 2.1.z, WATCH + GT series).  github.com/mali-ak/WatchFaceGT3",
       font=fl, fill=(130, 130, 130))
img.convert("RGB").save(os.path.join(ZIPD, "00_portfolyo_klasik.png"), optimize=True)

# ikinci sayfa: renkli set
img = Image.new("RGBA", (1920, 1080), (16, 16, 18, 255))
d = ImageDraw.Draw(img)
d.text((80, 56), "WatchFaceGT3  —  Renkli Set / Colour Set", font=fb, fill=(222, 200, 150))
d.text((80, 128), "Dijital minimal · Spor halkalar · Retro LCD · Geometrik analog", font=fr, fill=(190, 190, 190))
cell = 380
for i, (ad, a, o) in enumerate(RENKLI):
    x = 80 + i * (cell + 60)
    img.alpha_composite(yuvarlak(a).resize((cell, cell), Image.LANCZOS), (x, 200))
    img.alpha_composite(yuvarlak(o).resize((cell // 2, cell // 2), Image.LANCZOS), (x + cell // 4, 200 + cell + 24))
    d.text((x + cell // 2, 200 + cell + 24 + cell // 2 + 28), ad + "  ·  AOD", font=fl, fill=(200, 200, 200), anchor="mm")
img.convert("RGB").save(os.path.join(ZIPD, "01_portfolyo_renkli.png"), optimize=True)

# ---- tek tek önizlemeler
for i, (ad, a, a2, o) in enumerate(KLASIK, 1):
    for suffix, n in (("onizleme", a), ("onizleme2", a2), ("aod", o)):
        Image.open(os.path.join(ONIZ, n + ".png")).convert("RGB").save(
            os.path.join(ZIPD, f"{i:02d}_{ad.replace('ş', 's')}_{suffix}.png"), optimize=True)
for i, (ad, a, o) in enumerate(RENKLI, 6):
    for suffix, n in (("onizleme", a), ("aod", o)):
        Image.open(os.path.join(ONIZ, n + ".png")).convert("RGB").save(
            os.path.join(ZIPD, f"{i:02d}_{ad}_{suffix}.png"), optimize=True)

# ---- kaynak dosya ekran görüntüleri (kod + katman klasörü)
fc = ortak.font("consola", 15)
for name, path in (("build_py", os.path.join(KOK, "build.py")), ("gece_py", os.path.join(KOK, "tasarimlar", "gece.py"))):
    src = open(path, encoding="utf-8").read().splitlines()[:70]
    im = Image.new("RGB", (1600, 1180), (30, 30, 30))
    dd = ImageDraw.Draw(im)
    dd.text((20, 12), f"{os.path.basename(path)}  — kaynak dosya / source file (ilk 70 satır)", font=fc, fill=(222, 200, 150))
    for j, l in enumerate(src):
        dd.text((20, 40 + j * 16), f"{j+1:4d}  {l[:150]}", font=fc, fill=(220, 220, 220))
    im.save(os.path.join(ZIPD, f"90_kaynak_{name}.png"), optimize=True)

for name, folder in (("klasik", "katmanlar/aktif"), ("gece", "katmanlar_gece/aktif"), ("giyos", "katmanlar_giyos/aktif")):
    base = os.path.join(KOK, folder)
    files = []
    for r, _, fs in os.walk(base):
        for f in sorted(fs):
            files.append(os.path.join(r, f))
    im = Image.new("RGB", (1600, 900), (30, 30, 30))
    dd = ImageDraw.Draw(im)
    dd.text((20, 12), f"{folder}  — Theme Studio'ya yüklenen katmanlar / layer files", font=fc, fill=(222, 200, 150))
    x, y = 20, 50
    for p in files[:35]:
        t = Image.open(p).convert("RGBA")
        t.thumbnail((150, 150))
        bgc = Image.new("RGBA", (150, 150), (60, 60, 60, 255))
        bgc.alpha_composite(t, ((150 - t.width) // 2, (150 - t.height) // 2))
        im.paste(bgc.convert("RGB"), (x, y))
        dd.text((x, y + 154), os.path.relpath(p, base)[:20], font=fc, fill=(200, 200, 200))
        x += 170
        if x > 1420:
            x, y = 20, y + 190
    im.save(os.path.join(ZIPD, f"91_katmanlar_{name}.png"), optimize=True)

# ---- zip
out = os.path.join(KOK, "tanitim", "WatchFaceGT3_basvuru.zip")
with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
    for n in sorted(os.listdir(ZIPD)):
        z.write(os.path.join(ZIPD, n), n)
n = len(os.listdir(ZIPD))
print(f"{out}: {n} dosya, {os.path.getsize(out)/1024/1024:.1f} MB")
assert n <= 50 and os.path.getsize(out) < 50 * 1024 * 1024
