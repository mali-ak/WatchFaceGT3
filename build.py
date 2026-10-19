# -*- coding: utf-8 -*-
"""
Huawei Watch GT 3 (466x466) — "Gün-Tarih" stili klasik analog kadran, katman üretici.

Güneş ışını (sunburst) kadran, yivli altın çerçeve, altın baton ibreler,
12'de gün adı penceresi, 3'te tarih penceresi, alt yarıda adım / nabız / pil.
Kadran rengi 6 varyant: siyah, sari, mavi, yesil, kirmizi, beyaz.

Çalıştır:  python build.py
Çıktı:     katmanlar/aktif/*  katmanlar/aod/*  onizleme/*.png
Her şey bu dosyadan tekrar üretilir; PNG'leri elle düzenleme, burayı değiştir.
"""
import math
import os
import shutil
import numpy as np
from PIL import Image, ImageDraw, ImageFont

# ---------------------------------------------------------------- sabitler
W = H = 466
C = (233, 233)                    # ibrelerin dönme merkezi
FONT_DIR = r"C:\Windows\Fonts"
F_SERIF = os.path.join(FONT_DIR, "georgia.ttf")       # Roma rakamları
F_SANS_B = os.path.join(FONT_DIR, "segoeuib.ttf")     # sayılar, gün adı
F_SANS = os.path.join(FONT_DIR, "segoeui.ttf")

OUT = os.path.dirname(os.path.abspath(__file__))
AKTIF = os.path.join(OUT, "katmanlar", "aktif")
AOD = os.path.join(OUT, "katmanlar", "aod")
ONIZ = os.path.join(OUT, "onizleme")

TRANSP = (0, 0, 0, 0)
ALTIN = (214, 176, 84, 255)
ALTIN_ACIK = (246, 222, 140, 255)
ALTIN_KOYU = (140, 104, 30, 255)
BEYAZ = (248, 248, 246, 255)
SIYAH = (18, 16, 12, 255)
LUME = (236, 240, 230, 255)
AOD_ALTIN = (120, 98, 44, 255)
AOD_GRI = (105, 105, 105, 255)

# Kadran renkleri: (merkez, kenar)
KADRAN = {
    "yesil":   ((44, 158, 84), (3, 44, 20)),
    "siyah":   ((58, 60, 64), (6, 6, 8)),
    "mavi":    ((46, 98, 196), (5, 20, 68)),
    "kirmizi": ((196, 44, 44), (66, 6, 8)),
    "sari":    ((238, 196, 70), (146, 102, 18)),
    "beyaz":   ((252, 252, 250), (200, 200, 194)),
}
# Açık kadranlarda (sarı, beyaz) alt yarıdaki veri yazıları koyu set ile okunur
KOYU_KADRANLAR = ("sari", "beyaz")

GUNLER = ["Pazar", "Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi"]  # 0 = Pazar
GUN_KISA = ["Paz", "Pzt", "Sal", "Car", "Per", "Cum", "Cmt"]

R_BEZEL_DIS, R_BEZEL_IC = 233, 212      # yivli çerçeve
R_REHAUT = 204                           # iç eğik halka
POS_GUN = (233, 112)                     # gün penceresi merkezi
GUN_BOX = (124, 30)
POS_TARIH = (372, 233)                   # tarih penceresi merkezi
TARIH_BOX = (40, 32)
VERI_Y = 318                             # adım / nabız / pil satırı
VERI_X = (140, 233, 326)


def font(path, size):
    return ImageFont.truetype(path, size)


def polar(r, deg, cx=C[0], cy=C[1]):
    a = math.radians(deg - 90)
    return (cx + r * math.cos(a), cy + r * math.sin(a))


def ss(scale=4):
    return Image.new("RGBA", (W * scale, H * scale), TRANSP), scale


def down(img):
    return img.resize((W, H), Image.LANCZOS)


def save(img, folder, name):
    os.makedirs(folder, exist_ok=True)
    img.save(os.path.join(folder, name), optimize=True)


def tr_buyuk(t):
    return t.replace("i", "İ").replace("ı", "I").upper()


# ---------------------------------------------------------------- güneş ışını kadran
def sunburst(merkez, kenar):
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    dx, dy = xx - C[0], yy - C[1]
    r = np.sqrt(dx * dx + dy * dy) / R_REHAUT
    r = np.clip(r, 0, 1)
    ang = np.arctan2(dy, dx)
    # radyal geçiş + ince açısal "fırça" çizgileri + hafif üst-sol parlama
    t = r ** 1.15
    isin = 1 + 0.03 * np.cos(ang * 72) + 0.015 * np.cos(ang * 7)
    parlama = 1 + 0.10 * np.clip(np.cos(ang + math.radians(135)), 0, 1) * (1 - r)
    m = np.array(merkez, np.float32)[None, None, :]
    k = np.array(kenar, np.float32)[None, None, :]
    rgb = (m * (1 - t[..., None]) + k * t[..., None]) * (isin * parlama)[..., None]
    rgb = np.clip(rgb, 0, 255).astype(np.uint8)
    a = (r < 1).astype(np.uint8) * 255
    img = Image.fromarray(np.dstack([rgb, a]), "RGBA")
    return img


# ---------------------------------------------------------------- çerçeve, halka, indeksler
def bezel_ve_indeksler(koyu_yazi=False):
    """Yivli altın çerçeve + rehaut + baton indeksler + pencere çerçeveleri."""
    big, s = ss()
    d = ImageDraw.Draw(big)
    cx, cy = C[0] * s, C[1] * s

    # yivli çerçeve: 72 yiv, dönüşümlü açık/koyu altın üçgenler
    n = 96
    for i in range(n):
        a0, a1 = i * 360 / n, (i + 1) * 360 / n
        am = (a0 + a1) / 2
        col = ALTIN_ACIK if i % 2 == 0 else ALTIN_KOYU
        p = [polar(R_BEZEL_DIS * s, a0, cx, cy), polar(R_BEZEL_DIS * s, a1, cx, cy),
             polar(R_BEZEL_IC * s, am, cx, cy)]
        d.polygon(p, fill=col)
        col2 = ALTIN if i % 2 == 0 else ALTIN_ACIK
        p2 = [polar(R_BEZEL_IC * s, a0, cx, cy), polar(R_BEZEL_IC * s, a1, cx, cy),
              polar(R_BEZEL_DIS * s, am, cx, cy)]
        d.polygon(p2, fill=col2)
    # çerçeve kenar çizgileri
    for rr, col, w in ((R_BEZEL_DIS - 1, ALTIN_KOYU, 2), (R_BEZEL_IC, ALTIN_KOYU, 2)):
        d.ellipse([cx - rr * s, cy - rr * s, cx + rr * s, cy + rr * s], outline=col, width=w * s)

    # rehaut (eğik iç halka) + dakika çizgileri
    d.ellipse([cx - R_BEZEL_IC * s, cy - R_BEZEL_IC * s, cx + R_BEZEL_IC * s, cy + R_BEZEL_IC * s],
              fill=ALTIN_KOYU)
    d.ellipse([cx - R_REHAUT * s, cy - R_REHAUT * s, cx + R_REHAUT * s, cy + R_REHAUT * s],
              fill=(0, 0, 0, 0))
    # rehaut'u delmek için ayrı katmanda çiz
    reh = Image.new("RGBA", big.size, TRANSP)
    rd = ImageDraw.Draw(reh)
    rd.ellipse([cx - R_BEZEL_IC * s, cy - R_BEZEL_IC * s, cx + R_BEZEL_IC * s, cy + R_BEZEL_IC * s],
               fill=(120, 92, 28, 255))
    rd.ellipse([cx - R_REHAUT * s, cy - R_REHAUT * s, cx + R_REHAUT * s, cy + R_REHAUT * s],
               fill=TRANSP)
    for i in range(60):
        deg = i * 6
        r0 = R_REHAUT if i % 5 else R_REHAUT - 2
        p0, p1 = polar(r0 * s, deg, cx, cy), polar((R_BEZEL_IC - 1) * s, deg, cx, cy)
        rd.line([*p0, *p1], fill=ALTIN_ACIK if i % 5 == 0 else (190, 150, 60, 255),
                width=int((2.2 if i % 5 == 0 else 1.2) * s))
    big = Image.alpha_composite(big, reh)
    d = ImageDraw.Draw(big)

    # baton indeksler (12, 3, 6, 9 hariç) + lume çizgisi
    for h in range(12):
        if h in (0, 3, 6, 9):
            continue
        deg = h * 30
        r0, r1, w = 160, 196, 9
        pts = [polar(r0 * s, deg - 0.9, cx, cy), polar(r1 * s, deg - 0.9, cx, cy),
               polar(r1 * s, deg + 0.9, cx, cy), polar(r0 * s, deg + 0.9, cx, cy)]
        d.polygon(pts, fill=ALTIN)
        d.line([*polar(r0 * s, deg, cx, cy), *polar(r1 * s, deg, cx, cy)], fill=ALTIN_KOYU, width=int(1.2 * s))
        d.line([*polar((r0 + 6) * s, deg, cx, cy), *polar((r1 - 6) * s, deg, cx, cy)], fill=LUME, width=int(3 * s))
    # VI ve IX Roma rakamları
    f = font(F_SERIF, 40 * s)
    for txt, deg in (("VI", 180), ("IX", 270)):
        p = polar(176 * s, deg, cx, cy)
        d.text(p, txt, font=f, fill=ALTIN, anchor="mm", stroke_width=int(0.8 * s), stroke_fill=ALTIN_KOYU)
    # 12'de üçgen/çift baton
    for off in (-7, 7):
        pts = [((cx + off * s) - 3.5 * s, cy - 196 * s), ((cx + off * s) + 3.5 * s, cy - 196 * s),
               ((cx + off * s) + 3.5 * s, cy - 134 * s), ((cx + off * s) - 3.5 * s, cy - 134 * s)]
        d.polygon(pts, fill=ALTIN)
        d.line([cx + off * s, cy - 190 * s, cx + off * s, cy - 140 * s], fill=LUME, width=int(2.2 * s))

    # gün penceresi (12) ve tarih penceresi (3): beyaz zemin, altın çerçeve
    for pos, box in ((POS_GUN, GUN_BOX), (POS_TARIH, TARIH_BOX)):
        x0, y0 = (pos[0] - box[0] / 2) * s, (pos[1] - box[1] / 2) * s
        x1, y1 = (pos[0] + box[0] / 2) * s, (pos[1] + box[1] / 2) * s
        d.rounded_rectangle([x0 - 3 * s, y0 - 3 * s, x1 + 3 * s, y1 + 3 * s], radius=3 * s, fill=ALTIN)
        d.rounded_rectangle([x0 - 1 * s, y0 - 1 * s, x1 + 1 * s, y1 + 1 * s], radius=2 * s, fill=ALTIN_KOYU)
        d.rounded_rectangle([x0, y0, x1, y1], radius=1.5 * s, fill=BEYAZ)

    # veri satırı ayraçları
    col = SIYAH if koyu_yazi else ALTIN
    for x in (186, 280):
        d.line([x * s, (VERI_Y - 12) * s, x * s, (VERI_Y + 12) * s], fill=col, width=int(1 * s))
    return down(big)


def arka_plan(renk):
    merkez, kenar = KADRAN[renk]
    img = Image.new("RGBA", (W, H), (0, 0, 0, 255))
    img.alpha_composite(sunburst(merkez, kenar))
    img.alpha_composite(bezel_ve_indeksler(koyu_yazi=renk in KOYU_KADRANLAR))
    return img


# ---------------------------------------------------------------- ibreler
def baton_ibre(uzunluk, genislik, kuyruk, aod=False):
    """Altın baton ibre, ortasında lume şeridi. Saat 12'yi gösterir, pivot (233,233)."""
    big, s = ss()
    d = ImageDraw.Draw(big)
    cx, cy = C[0] * s, C[1] * s
    L, Wd, T = uzunluk * s, genislik * s, kuyruk * s
    pts = [(cx - Wd * 0.35, cy + T), (cx - Wd / 2, cy - L * 0.25), (cx - Wd / 2, cy - L + Wd * 0.8),
           (cx, cy - L), (cx + Wd / 2, cy - L + Wd * 0.8), (cx + Wd / 2, cy - L * 0.25), (cx + Wd * 0.35, cy + T)]
    if aod:
        d.polygon(pts, outline=AOD_ALTIN, width=int(1.6 * s))
        return down(big)
    d.polygon(pts, fill=ALTIN)
    d.polygon(pts, outline=ALTIN_KOYU, width=int(1.2 * s))
    d.line([cx, cy - L * 0.2, cx, cy - L + Wd * 1.2], fill=LUME, width=int(Wd * 0.42))
    return down(big)


def saniye_ibresi():
    big, s = ss()
    d = ImageDraw.Draw(big)
    cx, cy = C[0] * s, C[1] * s
    d.line([cx, cy + 50 * s, cx, cy - 198 * s], fill=ALTIN, width=int(2.2 * s))
    d.ellipse([cx - 6 * s, cy + 36 * s, cx + 6 * s, cy + 48 * s], fill=ALTIN)
    return down(big)


def merkez_kapak(aod=False):
    big, s = ss()
    d = ImageDraw.Draw(big)
    cx, cy = C[0] * s, C[1] * s
    if aod:
        d.ellipse([cx - 5 * s, cy - 5 * s, cx + 5 * s, cy + 5 * s], outline=AOD_ALTIN, width=int(1.5 * s))
    else:
        d.ellipse([cx - 9 * s, cy - 9 * s, cx + 9 * s, cy + 9 * s], fill=ALTIN, outline=ALTIN_KOYU, width=s)
        d.ellipse([cx - 3 * s, cy - 3 * s, cx + 3 * s, cy + 3 * s], fill=ALTIN_ACIK)
    return down(big)


# ---------------------------------------------------------------- simgeler (24x24)
def crop_box(img, size):
    x0, y0 = C[0] - size // 2, C[1] - size // 2
    return img.crop((x0, y0, x0 + size, y0 + size))


def simge_adim(col):
    big, s = ss()
    d = ImageDraw.Draw(big)
    for dx, dy in ((-4.5, 1), (4.5, -5)):
        x, y = (233 + dx) * s, (233 + dy) * s
        d.ellipse([x - 2.6 * s, y - 1 * s, x + 2.6 * s, y + 7 * s], fill=col)
        d.ellipse([x - 2.3 * s, y - 6.5 * s, x + 2.3 * s, y - 2 * s], fill=col)
    return crop_box(down(big), 24)


def simge_kalp(col):
    big, s = ss()
    d = ImageDraw.Draw(big)
    cx, cy = 233 * s, 233 * s
    r = 4.4 * s
    d.ellipse([cx - 2 * r, cy - r - 3 * s, cx, cy + r - 3 * s], fill=col)
    d.ellipse([cx, cy - r - 3 * s, cx + 2 * r, cy + r - 3 * s], fill=col)
    d.polygon([(cx - 2 * r + 0.6 * s, cy - 1 * s), (cx + 2 * r - 0.6 * s, cy - 1 * s), (cx, cy + 9 * s)], fill=col)
    return crop_box(down(big), 24)


def simge_pil(col):
    big, s = ss()
    d = ImageDraw.Draw(big)
    cx, cy = 233 * s, 233 * s
    d.rounded_rectangle([cx - 9 * s, cy - 5 * s, cx + 7 * s, cy + 5 * s], radius=2 * s, outline=col, width=int(1.6 * s))
    d.rounded_rectangle([cx + 8 * s, cy - 2 * s, cx + 10 * s, cy + 2 * s], radius=1 * s, fill=col)
    d.rounded_rectangle([cx - 7 * s, cy - 3 * s, cx + 2 * s, cy + 3 * s], radius=1 * s, fill=col)
    return crop_box(down(big), 24)


# ---------------------------------------------------------------- rakam / metin setleri
def rakam_seti(folder, col, size, bw, ekstra=True):
    f = font(F_SANS_B, size)
    h = size + 6
    for n in range(10):
        img = Image.new("RGBA", (bw, h), TRANSP)
        ImageDraw.Draw(img).text((bw / 2, h / 2), str(n), font=f, fill=col, anchor="mm")
        save(img, folder, f"{n}.png")
    if ekstra:
        for ch, name in ((":", "iki_nokta"), ("%", "yuzde")):
            img = Image.new("RGBA", (bw, h), TRANSP)
            ImageDraw.Draw(img).text((bw / 2, h / 2), ch, font=f, fill=col, anchor="mm")
            save(img, folder, f"{name}.png")


def gun_seti(folder, col, size=17, box=GUN_BOX):
    f = font(F_SANS_B, size)
    for i, t in enumerate(GUNLER):
        img = Image.new("RGBA", box, TRANSP)
        ImageDraw.Draw(img).text((box[0] / 2, box[1] / 2 + 1), tr_buyuk(t), font=f, fill=col, anchor="mm")
        save(img, folder, f"gun_{i:02d}_{GUN_KISA[i]}.png")


# ---------------------------------------------------------------- önizleme birleştirme
def yerlestir(base, img, merkez):
    base.alpha_composite(img, (int(round(merkez[0] - img.width / 2)), int(round(merkez[1] - img.height / 2))))


def sayi_yaz(base, folder, text, merkez):
    imgs = [Image.open(os.path.join(folder, f"{ {':': 'iki_nokta', '%': 'yuzde'}.get(ch, ch)}.png")).convert("RGBA")
            for ch in text]
    total = sum(i.width for i in imgs)
    x = merkez[0] - total / 2
    for i in imgs:
        base.alpha_composite(i, (int(round(x)), int(round(merkez[1] - i.height / 2))))
        x += i.width


def dondur(img, deg):
    return img.rotate(-deg, resample=Image.BICUBIC, center=C)


def onizleme_aktif(renk, saat, dk, sn, adim, nabiz, pil, gun, gunadi):
    base = Image.open(os.path.join(AKTIF, f"00_arka_plan_{renk}.png")).convert("RGBA")
    set_ = "koyu" if renk in KOYU_KADRANLAR else "altin"
    rk = os.path.join(AKTIF, "rakam_veri_" + set_)
    yerlestir(base, Image.open(os.path.join(AKTIF, f"simge_adim_{set_}.png")), (VERI_X[0] - 30, VERI_Y))
    sayi_yaz(base, rk, str(adim), (VERI_X[0] + 6, VERI_Y))
    yerlestir(base, Image.open(os.path.join(AKTIF, f"simge_kalp_{set_}.png")), (VERI_X[1] - 24, VERI_Y))
    sayi_yaz(base, rk, str(nabiz), (VERI_X[1] + 6, VERI_Y))
    yerlestir(base, Image.open(os.path.join(AKTIF, f"simge_pil_{set_}.png")), (VERI_X[2] - 24, VERI_Y))
    sayi_yaz(base, rk, f"{pil}%", (VERI_X[2] + 8, VERI_Y))
    yerlestir(base, Image.open(os.path.join(AKTIF, "gun", f"gun_{gunadi:02d}_{GUN_KISA[gunadi]}.png")), POS_GUN)
    sayi_yaz(base, os.path.join(AKTIF, "rakam_tarih"), f"{gun:02d}", POS_TARIH)
    h_deg = (saat % 12) * 30 + dk * 0.5
    base.alpha_composite(dondur(Image.open(os.path.join(AKTIF, "ibre_saat.png")), h_deg))
    base.alpha_composite(dondur(Image.open(os.path.join(AKTIF, "ibre_dakika.png")), dk * 6 + sn * 0.1))
    base.alpha_composite(dondur(Image.open(os.path.join(AKTIF, "ibre_saniye.png")), sn * 6))
    base.alpha_composite(Image.open(os.path.join(AKTIF, "merkez_kapak.png")))
    return base


def onizleme_aod(saat, dk, gun, gunadi):
    base = Image.open(os.path.join(AOD, "00_arka_plan.png")).convert("RGBA")
    yerlestir(base, Image.open(os.path.join(AOD, "gun", f"gun_{gunadi:02d}_{GUN_KISA[gunadi]}.png")), POS_GUN)
    sayi_yaz(base, os.path.join(AOD, "rakam_tarih"), f"{gun:02d}", POS_TARIH)
    base.alpha_composite(dondur(Image.open(os.path.join(AOD, "ibre_saat.png")), (saat % 12) * 30 + dk * 0.5))
    base.alpha_composite(dondur(Image.open(os.path.join(AOD, "ibre_dakika.png")), dk * 6))
    base.alpha_composite(Image.open(os.path.join(AOD, "merkez_kapak.png")))
    return base


def yanan_oran(img, esik=8):
    g = img.convert("RGB").convert("L").point(lambda v: 255 if v > esik else 0)
    return g.histogram()[255] / (W * H)


# ---------------------------------------------------------------- AOD arka planı
def aod_arka_plan():
    big, s = ss()
    d = ImageDraw.Draw(big)
    cx, cy = C[0] * s, C[1] * s
    d.ellipse([cx - R_BEZEL_IC * s, cy - R_BEZEL_IC * s, cx + R_BEZEL_IC * s, cy + R_BEZEL_IC * s],
              outline=AOD_ALTIN, width=int(1.5 * s))
    for h in range(12):
        deg = h * 30
        if h in (0, 3, 6, 9):
            continue
        pts = [polar(166 * s, deg - 0.8, cx, cy), polar(196 * s, deg - 0.8, cx, cy),
               polar(196 * s, deg + 0.8, cx, cy), polar(166 * s, deg + 0.8, cx, cy)]
        d.polygon(pts, outline=AOD_ALTIN, width=int(1.3 * s))
    f = font(F_SERIF, 36 * s)
    for txt, deg in (("VI", 180), ("IX", 270)):
        d.text(polar(176 * s, deg, cx, cy), txt, font=f, fill=AOD_ALTIN, anchor="mm")
    for off in (-7, 7):
        d.rectangle([(cx + off * s) - 3 * s, cy - 196 * s, (cx + off * s) + 3 * s, cy - 140 * s],
                    outline=AOD_ALTIN, width=int(1.3 * s))
    for pos, box in ((POS_GUN, GUN_BOX), (POS_TARIH, TARIH_BOX)):
        d.rounded_rectangle([(pos[0] - box[0] / 2) * s, (pos[1] - box[1] / 2) * s,
                             (pos[0] + box[0] / 2) * s, (pos[1] + box[1] / 2) * s],
                            radius=2 * s, outline=AOD_ALTIN, width=int(1.3 * s))
    img = Image.new("RGBA", (W, H), (0, 0, 0, 255))
    img.alpha_composite(down(big))
    return img


# ---------------------------------------------------------------- ana akış
def main():
    for p in (AKTIF, AOD, ONIZ):
        shutil.rmtree(p, ignore_errors=True)
        os.makedirs(p, exist_ok=True)

    # --- aktif katmanlar
    for renk in KADRAN:
        save(arka_plan(renk), AKTIF, f"00_arka_plan_{renk}.png")
    save(baton_ibre(128, 13, 24), AKTIF, "ibre_saat.png")
    save(baton_ibre(188, 11, 28), AKTIF, "ibre_dakika.png")
    save(saniye_ibresi(), AKTIF, "ibre_saniye.png")
    save(merkez_kapak(), AKTIF, "merkez_kapak.png")
    for ad, col in (("altin", ALTIN), ("koyu", SIYAH)):
        save(simge_adim(col), AKTIF, f"simge_adim_{ad}.png")
        save(simge_kalp(col), AKTIF, f"simge_kalp_{ad}.png")
        save(simge_pil(col), AKTIF, f"simge_pil_{ad}.png")
        rakam_seti(os.path.join(AKTIF, f"rakam_veri_{ad}"), col, size=22, bw=13)
    rakam_seti(os.path.join(AKTIF, "rakam_tarih"), SIYAH, size=26, bw=15, ekstra=False)
    gun_seti(os.path.join(AKTIF, "gun"), SIYAH)

    # --- AOD katmanları
    save(aod_arka_plan(), AOD, "00_arka_plan.png")
    save(baton_ibre(128, 13, 24, aod=True), AOD, "ibre_saat.png")
    save(baton_ibre(188, 11, 28, aod=True), AOD, "ibre_dakika.png")
    save(merkez_kapak(aod=True), AOD, "merkez_kapak.png")
    rakam_seti(os.path.join(AOD, "rakam_tarih"), AOD_GRI, size=26, bw=15, ekstra=False)
    gun_seti(os.path.join(AOD, "gun"), AOD_GRI)

    # --- önizlemeler
    ornek = dict(gun=19, gunadi=1)                      # 19, Pazartesi
    a1 = onizleme_aktif("yesil", 10, 9, 36, adim=6482, nabiz=72, pil=85, **ornek)
    a1.save(os.path.join(ONIZ, "aktif_yesil_10_09.png"))
    aod1 = onizleme_aod(10, 9, **ornek)
    aod1.save(os.path.join(ONIZ, "aod_10_09.png"))
    # 6 renk + AOD: 3x3 ızgara yarım boyutta
    hucre = W // 2 + 8
    izg = Image.new("RGBA", (hucre * 4, hucre * 2), (28, 28, 28, 255))
    kareler = [onizleme_aktif(r, 10, 9, 36, adim=11205, nabiz=118, pil=40, **ornek) for r in KADRAN] + [aod1]
    for i, k in enumerate(kareler):
        izg.alpha_composite(k.resize((W // 2, H // 2), Image.LANCZOS), ((i % 4) * hucre + 4, (i // 4) * hucre + 4))
    izg.save(os.path.join(ONIZ, "renkler_ve_aod.png"))

    # --- AOD piksel oranı
    en_kotu = max(yanan_oran(onizleme_aod(h, m, **ornek)) for h, m in ((10, 9), (6, 30), (12, 0), (3, 45)))
    print(f"AOD yanan piksel oranı (en kötü örnek): %{en_kotu*100:.2f}  (hedef <%10, sınır %20)")
    en_buyuk = max((os.path.getsize(os.path.join(r, f)), os.path.join(r, f))
                   for r, _, fs in os.walk(os.path.join(OUT, "katmanlar")) for f in fs)
    print(f"En büyük katman: {en_buyuk[0]/1024:.0f} KB  {os.path.relpath(en_buyuk[1], OUT)}  (sınır 750 KB)")
    print("Tamam: katmanlar/ ve onizleme/ üretildi.")


if __name__ == "__main__":
    main()
