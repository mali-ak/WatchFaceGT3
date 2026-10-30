# -*- coding: utf-8 -*-
"""
Tasarım "Porselen": beyaz emaye kadran, siyah ince Roma rakamları (I-XII), demiryolu dakika rayı,
mavi çelik yaprak ibreler, 6'da tarih penceresi. Veriler küçük siyah yazı. Siyah giyimle kontrast.
"""
import os
from PIL import Image, ImageDraw
from ortak import *

AD = "porselen"
KAT = os.path.join(KOK, "katmanlar_" + AD)
AKTIF, AOD = os.path.join(KAT, "aktif"), os.path.join(KAT, "aod")
ONIZ = os.path.join(KOK, "onizleme")

EMAYE = (247, 245, 240, 255)
EMAYE_G = (232, 229, 222, 255)
SIYAH = (28, 26, 24, 255)
GRI = (105, 102, 98, 255)
MAVI = (28, 62, 150, 255)
MAVI_K = (16, 36, 95, 255)
KIRMIZI = (176, 32, 28, 255)
AOD_G = (120, 120, 120, 255)

ROMA = ["XII", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI"]
POS_TARIH = (233, 330)
POS_GUN = (233, 150)
VERI = [("adim", (138, 268)), ("kalp", (233, 268)), ("pil", (328, 268))]


def arka_plan():
    big, s = ss()
    d = ImageDraw.Draw(big)
    cx, cy = 233 * s, 233 * s
    d.ellipse([0, 0, W * s, H * s], fill=EMAYE)
    # dış kenar: hafif gri (kubbe hissi)
    d.ellipse([cx - 233 * s, cy - 233 * s, cx + 233 * s, cy + 233 * s], fill=(222, 220, 214, 255))
    d.ellipse([cx - 220 * s, cy - 220 * s, cx + 220 * s, cy + 220 * s], fill=EMAYE)
    # demiryolu dakika rayı
    for r in (212, 203):
        d.ellipse([cx - r * s, cy - r * s, cx + r * s, cy + r * s], outline=SIYAH, width=int(1.2 * s))
    for i in range(60):
        deg = i * 6
        p0, p1 = polar(203 * s, deg, cx, cy), polar(212 * s, deg, cx, cy)
        d.line([*p0, *p1], fill=SIYAH, width=int((2.2 if i % 5 == 0 else 1) * s))
    # Roma rakamları
    f = font("georgia", 34 * s)
    for h, t in enumerate(ROMA):
        p = polar(172 * s, h * 30, cx, cy)
        d.text(p, t, font=f, fill=KIRMIZI if h == 0 else SIYAH, anchor="mm")
    # iç ince halka
    d.ellipse([cx - 130 * s, cy - 130 * s, cx + 130 * s, cy + 130 * s], outline=EMAYE_G, width=int(1.5 * s))
    # tarih penceresi
    x, y = POS_TARIH
    d.rectangle([(x - 22) * s, (y - 16) * s, (x + 22) * s, (y + 16) * s], fill=SIYAH)
    d.rectangle([(x - 20) * s, (y - 14) * s, (x + 20) * s, (y + 14) * s], fill=EMAYE)
    # veri satırı ayraçları
    for x in (186, 280):
        d.line([x * s, 258 * s, x * s, 278 * s], fill=EMAYE_G, width=int(1.5 * s))
    img = down(big)
    for ad, (x, y) in VERI:
        yerlestir(img, simge(ad, GRI, 16), (x - 30, y))
    return img


def yaprak(uz, gen, col, aod=False):
    """Mavi çelik yaprak (leaf) ibre."""
    big, s = ss()
    d = ImageDraw.Draw(big)
    cx, cy = 233 * s, 233 * s
    L, Wd = uz * s, gen * s
    pts = []
    import math
    n = 24
    for i in range(n + 1):           # sağ kenar, aşağıdan yukarı
        t = i / n
        y = cy + 14 * s - t * (L + 14 * s)
        w = Wd / 2 * math.sin(math.pi * (0.1 + 0.9 * t)) ** 0.9 if t < 0.97 else 0
        pts.append((cx + w, y))
    for i in range(n, -1, -1):       # sol kenar
        t = i / n
        y = cy + 14 * s - t * (L + 14 * s)
        w = Wd / 2 * math.sin(math.pi * (0.1 + 0.9 * t)) ** 0.9 if t < 0.97 else 0
        pts.append((cx - w, y))
    if aod:
        d.polygon(pts, outline=col, width=int(1.4 * s))
    else:
        d.polygon(pts, fill=col)
        d.line([cx, cy, cx, cy - L * 0.9], fill=MAVI_K, width=int(0.9 * s))
    return down(big)


def saniye():
    big, s = ss()
    d = ImageDraw.Draw(big)
    cx, cy = 233 * s, 233 * s
    d.line([cx, cy + 40 * s, cx, cy - 190 * s], fill=MAVI, width=int(1.6 * s))
    d.ellipse([cx - 5 * s, cy + 28 * s, cx + 5 * s, cy + 38 * s], fill=MAVI)
    return down(big)


def kapak(aod=False):
    big, s = ss()
    d = ImageDraw.Draw(big)
    cx, cy = 233 * s, 233 * s
    col = AOD_G if aod else MAVI
    if aod:
        d.ellipse([cx - 4 * s, cy - 4 * s, cx + 4 * s, cy + 4 * s], outline=col, width=int(1.2 * s))
    else:
        d.ellipse([cx - 6 * s, cy - 6 * s, cx + 6 * s, cy + 6 * s], fill=col)
    return down(big)


def aod_arka_plan():
    big, s = ss()
    d = ImageDraw.Draw(big)
    cx, cy = 233 * s, 233 * s
    f = font("georgia", 30 * s)
    for h, t in enumerate(ROMA):
        if h % 3 == 0:
            d.text(polar(172 * s, h * 30, cx, cy), t, font=f, fill=AOD_G, anchor="mm")
        else:
            p0, p1 = polar(203 * s, h * 30, cx, cy), polar(212 * s, h * 30, cx, cy)
            d.line([*p0, *p1], fill=AOD_G, width=int(2 * s))
    x, y = POS_TARIH
    d.rectangle([(x - 22) * s, (y - 16) * s, (x + 22) * s, (y + 16) * s], outline=AOD_G, width=s)
    img = Image.new("RGBA", (W, H), (0, 0, 0, 255))
    img.alpha_composite(down(big))
    return img


def onizleme(aktif, saat, dk, sn, adim, nabiz, pil, gun, gunadi):
    base = Image.open(os.path.join(aktif, "00_arka_plan.png")).convert("RGBA")
    sayi_yaz(base, os.path.join(aktif, "rakam_tarih"), f"{gun:02d}", POS_TARIH)
    yerlestir(base, gun_ac(os.path.join(aktif, "gun"), gunadi), POS_GUN)
    if aktif == AKTIF:
        rv = os.path.join(aktif, "rakam_veri")
        sayi_yaz(base, rv, str(adim), (VERI[0][1][0] + 10, VERI[0][1][1]))
        sayi_yaz(base, rv, str(nabiz), (VERI[1][1][0] + 6, VERI[1][1][1]))
        sayi_yaz(base, rv, f"{pil}%", (VERI[2][1][0] + 10, VERI[2][1][1]))
    base.alpha_composite(dondur(Image.open(os.path.join(aktif, "ibre_saat.png")), (saat % 12) * 30 + dk * 0.5))
    base.alpha_composite(dondur(Image.open(os.path.join(aktif, "ibre_dakika.png")), dk * 6 + sn * 0.1))
    if aktif == AKTIF:
        base.alpha_composite(dondur(Image.open(os.path.join(aktif, "ibre_saniye.png")), sn * 6))
    base.alpha_composite(Image.open(os.path.join(aktif, "merkez_kapak.png")))
    return base


def main():
    temizle(AKTIF, AOD)
    save(arka_plan(), AKTIF, "00_arka_plan.png")
    save(yaprak(118, 16, MAVI), AKTIF, "ibre_saat.png")
    save(yaprak(176, 13, MAVI), AKTIF, "ibre_dakika.png")
    save(saniye(), AKTIF, "ibre_saniye.png")
    save(kapak(), AKTIF, "merkez_kapak.png")
    rakam_seti(os.path.join(AKTIF, "rakam_tarih"), SIYAH, "georgia", 24, 14, ekstra=())
    rakam_seti(os.path.join(AKTIF, "rakam_veri"), SIYAH, "bahn", 18, 10)
    gun_seti(os.path.join(AKTIF, "gun"), GRI, "georgia", 17, (70, 24))

    save(aod_arka_plan(), AOD, "00_arka_plan.png")
    save(yaprak(118, 16, AOD_G, aod=True), AOD, "ibre_saat.png")
    save(yaprak(176, 13, AOD_G, aod=True), AOD, "ibre_dakika.png")
    save(kapak(aod=True), AOD, "merkez_kapak.png")
    rakam_seti(os.path.join(AOD, "rakam_tarih"), AOD_G, "georgia", 24, 14, ekstra=())
    gun_seti(os.path.join(AOD, "gun"), AOD_G, "georgia", 17, (70, 24))

    onizleme(AKTIF, **ORNEK).save(os.path.join(ONIZ, f"{AD}_aktif.png"))
    onizleme(AKTIF, **ORNEK2).save(os.path.join(ONIZ, f"{AD}_aktif_2.png"))
    o = onizleme(AOD, **ORNEK); o.save(os.path.join(ONIZ, f"{AD}_aod.png"))
    rapor(AD, [o, onizleme(AOD, **ORNEK2)], KAT)


if __name__ == "__main__":
    main()
