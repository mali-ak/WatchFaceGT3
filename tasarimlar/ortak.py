# -*- coding: utf-8 -*-
"""Tüm kadran tasarımlarının paylaştığı yardımcılar (466x466, Huawei Watch GT 3)."""
import math
import os
import shutil
from PIL import Image, ImageDraw, ImageFont

W = H = 466
C = (233, 233)
FONT_DIR = r"C:\Windows\Fonts"
FONTS = {
    "bold": os.path.join(FONT_DIR, "segoeuib.ttf"),
    "reg": os.path.join(FONT_DIR, "segoeui.ttf"),
    "bahn": os.path.join(FONT_DIR, "bahnschrift.ttf"),
    "georgia": os.path.join(FONT_DIR, "georgia.ttf"),
    "georgiab": os.path.join(FONT_DIR, "georgiab.ttf"),
    "consola": os.path.join(FONT_DIR, "consolab.ttf"),
    "arialn": os.path.join(FONT_DIR, "ARIALNB.TTF"),
}
TRANSP = (0, 0, 0, 0)
GUNLER = ["Paz", "Pzt", "Sal", "Çar", "Per", "Cum", "Cmt"]      # 0 = Pazar
KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def font(ad, size):
    return ImageFont.truetype(FONTS[ad], size)


def tr_buyuk(t):
    return t.replace("i", "İ").replace("ı", "I").upper()


def polar(r, deg, cx=C[0], cy=C[1]):
    a = math.radians(deg - 90)
    return (cx + r * math.cos(a), cy + r * math.sin(a))


def ss(scale=4):
    return Image.new("RGBA", (W * scale, H * scale), TRANSP), scale


def down(img):
    return img.resize((W, H), Image.LANCZOS)


def temizle(*dirs):
    for d in dirs:
        shutil.rmtree(d, ignore_errors=True)
        os.makedirs(d, exist_ok=True)


def save(img, folder, name):
    os.makedirs(folder, exist_ok=True)
    img.save(os.path.join(folder, name), optimize=True)


def yerlestir(base, img, merkez):
    base.alpha_composite(img, (int(round(merkez[0] - img.width / 2)), int(round(merkez[1] - img.height / 2))))


def dondur(img, deg):
    return img.rotate(-deg, resample=Image.BICUBIC, center=C)


def yanan_oran(img, esik=8):
    g = img.convert("RGB").convert("L").point(lambda v: 255 if v > esik else 0)
    return g.histogram()[255] / (W * H)


# ---------------------------------------------------------------- rakam setleri
def rakam_seti(folder, col, fontad, size, bw, ekstra=(":", "%"), outline=None, ow=0):
    """0-9 (+ ':' '%') eşit genişlikli PNG'ler; Theme Studio Image Number için."""
    f = font(fontad, size)
    h = int(size * 1.25)
    for ch in list("0123456789") + list(ekstra):
        name = {":": "iki_nokta", "%": "yuzde", "/": "bolu", ".": "nokta"}.get(ch, ch)
        w = int(bw * 1.5) if ch == "%" else bw
        img = Image.new("RGBA", (w, h), TRANSP)
        ImageDraw.Draw(img).text((w / 2, h / 2), ch, font=f, fill=col, anchor="mm",
                                 stroke_width=ow, stroke_fill=outline)
        save(img, folder, f"{name}.png")


def sayi_yaz(base, folder, text, merkez, hiza="mm"):
    imgs = []
    for ch in text:
        name = {":": "iki_nokta", "%": "yuzde", "/": "bolu", ".": "nokta"}.get(ch, ch)
        imgs.append(Image.open(os.path.join(folder, f"{name}.png")).convert("RGBA"))
    total = sum(i.width for i in imgs)
    x = merkez[0] - total / 2 if hiza == "mm" else (merkez[0] if hiza == "lm" else merkez[0] - total)
    for i in imgs:
        base.alpha_composite(i, (int(round(x)), int(round(merkez[1] - i.height / 2))))
        x += i.width


def gun_seti(folder, col, fontad, size, box, prefix="gun", buyuk=True):
    f = font(fontad, size)
    for i, t in enumerate(GUNLER):
        img = Image.new("RGBA", box, TRANSP)
        ImageDraw.Draw(img).text((box[0] / 2, box[1] / 2), tr_buyuk(t) if buyuk else t, font=f, fill=col, anchor="mm")
        save(img, folder, f"{prefix}_{i:02d}_{t.replace('Ç', 'C')}.png")


def gun_ac(folder, i, prefix="gun"):
    t = GUNLER[i].replace("Ç", "C")
    return Image.open(os.path.join(folder, f"{prefix}_{i:02d}_{t}.png")).convert("RGBA")


# ---------------------------------------------------------------- yay kareleri (ilerleme)
def yay_kareleri(folder, prefix, merkez, r, kalinlik, col_on, col_off, start=-90, span=360,
                 adim=10, yuvarlak=True):
    """0..100 arası (adım 10) ilerleme yayı; tam tuval boyutunda PNG'ler."""
    for y in range(0, 101, adim):
        big, s = ss()
        d = ImageDraw.Draw(big)
        box = [(merkez[0] - r) * s, (merkez[1] - r) * s, (merkez[0] + r) * s, (merkez[1] + r) * s]
        if col_off:
            d.arc(box, start, start + span, fill=col_off, width=int(kalinlik * s))
        if y > 0:
            end = start + span * y / 100
            d.arc(box, start, end, fill=col_on, width=int(kalinlik * s))
            if yuvarlak:
                for a in (start, end):
                    p = polar(r * s, a + 90, merkez[0] * s, merkez[1] * s)
                    rr = kalinlik * s / 2
                    d.ellipse([p[0] - rr, p[1] - rr, p[0] + rr, p[1] + rr], fill=col_on)
        save(down(big), folder, f"{prefix}_{y:03d}.png")


def yay_ac(folder, prefix, yuzde, adim=10):
    y = int(round(yuzde / adim) * adim)
    return Image.open(os.path.join(folder, f"{prefix}_{y:03d}.png")).convert("RGBA")


# ---------------------------------------------------------------- yedi parçalı (LCD) rakam
SEG = {  # a b c d e f g
    "0": "abcdef", "1": "bc", "2": "abdeg", "3": "abcdg", "4": "bcfg",
    "5": "acdfg", "6": "acdefg", "7": "abc", "8": "abcdefg", "9": "abcdfg", " ": "",
}


def segment_rakam(ch, w, h, col, ghost=None, kal=None, s=4):
    """Yedi parçalı tek rakam; w x h kutu, kenarlarda boşluk, düz dikdörtgen parçalar."""
    img = Image.new("RGBA", (w * s, h * s), TRANSP)
    d = ImageDraw.Draw(img)
    kal = (kal or max(3, w // 6)) * s
    px, py = int(w * 0.12) * s, int(h * 0.05) * s         # dış boşluk
    gap = max(1, int(0.35 * kal))                         # parçalar arası boşluk
    x0, x1, y0, y1 = px, w * s - px, py, h * s - py
    ym = (y0 + y1) / 2
    segs = {
        "a": [x0 + kal + gap, y0, x1 - kal - gap, y0 + kal],
        "g": [x0 + kal + gap, ym - kal / 2, x1 - kal - gap, ym + kal / 2],
        "d": [x0 + kal + gap, y1 - kal, x1 - kal - gap, y1],
        "f": [x0, y0 + kal + gap, x0 + kal, ym - kal / 2 - gap],
        "b": [x1 - kal, y0 + kal + gap, x1, ym - kal / 2 - gap],
        "e": [x0, ym + kal / 2 + gap, x0 + kal, y1 - kal - gap],
        "c": [x1 - kal, ym + kal / 2 + gap, x1, y1 - kal - gap],
    }
    on = SEG.get(ch, "")
    for k, box in segs.items():
        if k in on:
            d.rectangle(box, fill=col)
        elif ghost:
            d.rectangle(box, fill=ghost)
    return img.resize((w, h), Image.LANCZOS)


def segment_seti(folder, w, h, col, ghost=None, kal=None):
    for ch in "0123456789":
        save(segment_rakam(ch, w, h, col, ghost, kal), folder, f"{ch}.png")
    # iki nokta
    img = Image.new("RGBA", (w // 2, h), TRANSP)
    d = ImageDraw.Draw(img)
    r = max(2, w // 8)
    for yy in (h * 0.32, h * 0.68):
        d.ellipse([w / 4 - r, yy - r, w / 4 + r, yy + r], fill=col)
    save(img, folder, "iki_nokta.png")
    img = Image.new("RGBA", (w, h), TRANSP)
    ImageDraw.Draw(img).text((w / 2, h / 2), "%", font=font("bahn", int(h * 0.6)), fill=col, anchor="mm")
    save(img, folder, "yuzde.png")


# ---------------------------------------------------------------- simgeler (tek renk, boyut n)
def simge(ad, col, n=28):
    big, s = ss()
    d = ImageDraw.Draw(big)
    cx, cy = C[0] * s, C[1] * s
    k = n / 28 * s
    if ad == "adim":
        for dx, dy in ((-5, 1), (5, -6)):
            x, y = cx + dx * k, cy + dy * k
            d.ellipse([x - 3 * k, y - 1 * k, x + 3 * k, y + 8 * k], fill=col)
            d.ellipse([x - 2.6 * k, y - 7.5 * k, x + 2.6 * k, y - 2.5 * k], fill=col)
    elif ad == "kalp":
        r = 5 * k
        d.ellipse([cx - 2 * r, cy - r - 3 * k, cx, cy + r - 3 * k], fill=col)
        d.ellipse([cx, cy - r - 3 * k, cx + 2 * r, cy + r - 3 * k], fill=col)
        d.polygon([(cx - 2 * r + 0.6 * k, cy - 1 * k), (cx + 2 * r - 0.6 * k, cy - 1 * k), (cx, cy + 10.5 * k)], fill=col)
    elif ad == "pil":
        d.rounded_rectangle([cx - 10 * k, cy - 6 * k, cx + 8 * k, cy + 6 * k], radius=2 * k, outline=col, width=int(2 * k))
        d.rounded_rectangle([cx + 9 * k, cy - 2.5 * k, cx + 11.5 * k, cy + 2.5 * k], radius=1 * k, fill=col)
        d.rounded_rectangle([cx - 8 * k, cy - 4 * k, cx + 3 * k, cy + 4 * k], radius=1 * k, fill=col)
    elif ad == "takvim":
        d.rounded_rectangle([cx - 10 * k, cy - 8 * k, cx + 10 * k, cy + 10 * k], radius=2 * k, outline=col, width=int(2 * k))
        d.rectangle([cx - 10 * k, cy - 8 * k, cx + 10 * k, cy - 3 * k], fill=col)
        for dx in (-6, -2, 2):
            d.line([cx + dx * k, cy - 11 * k, cx + dx * k, cy - 6 * k], fill=col, width=int(2 * k))
    out = down(big)
    x0, y0 = C[0] - n // 2, C[1] - n // 2
    return out.crop((x0, y0, x0 + n, y0 + n))


# ---------------------------------------------------------------- önizleme yardımcıları
def rapor(ad, aod_imgs, katman_dir):
    en_kotu = max(yanan_oran(i) for i in aod_imgs)
    en_buyuk = max((os.path.getsize(os.path.join(r, f)), os.path.join(r, f))
                   for r, _, fs in os.walk(katman_dir) for f in fs)
    print(f"[{ad}] AOD yanan piksel oranı (en kötü): %{en_kotu*100:.2f}  (hedef <%10)  |  "
          f"en büyük katman {en_buyuk[0]/1024:.0f} KB")
    return en_kotu


ORNEK = dict(saat=10, dk=9, sn=36, adim=6482, nabiz=72, pil=85, gun=19, gunadi=1)
ORNEK2 = dict(saat=16, dk=42, sn=12, adim=11205, nabiz=118, pil=40, gun=19, gunadi=1)
