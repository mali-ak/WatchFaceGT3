# -*- coding: utf-8 -*-
"""
Tasarım "Gece": mat siyah kadran, gümüş (rodyum) baton indeksler, dauphine ibreler,
6'da küçük saniye alt kadranı, 3'te tarih penceresi. Veriler çok küçük ve gri: sade "dress watch".
"""
import os
from PIL import Image, ImageDraw
from ortak import *

AD = "gece"
KAT = os.path.join(KOK, "katmanlar_" + AD)
AKTIF, AOD = os.path.join(KAT, "aktif"), os.path.join(KAT, "aod")
ONIZ = os.path.join(KOK, "onizleme")

SIYAH = (14, 14, 16, 255)
SIYAH_K = (8, 8, 9, 255)
GUMUS = (208, 212, 218, 255)
GUMUS_K = (120, 124, 132, 255)
GRI = (128, 130, 136, 255)
BEYAZ = (240, 240, 242, 255)
AOD_G = (120, 120, 124, 255)

SUB = (233, 322)            # küçük saniye merkezi
SUB_R = 44
POS_TARIH = (372, 233)
POS_GUN = (233, 128)
POS_ADIM = (108, 233)
POS_NABIZ = (128, 330)
POS_PIL = (338, 330)


def arka_plan():
    big, s = ss()
    d = ImageDraw.Draw(big)
    cx, cy = 233 * s, 233 * s
    d.ellipse([0, 0, W * s, H * s], fill=SIYAH)
    # dış halka: koyu füme
    d.ellipse([cx - 233 * s, cy - 233 * s, cx + 233 * s, cy + 233 * s], fill=(22, 22, 25, 255))
    d.ellipse([cx - 218 * s, cy - 218 * s, cx + 218 * s, cy + 218 * s], fill=SIYAH, outline=GUMUS_K, width=int(1 * s))
    # dakika rayı
    for i in range(60):
        deg = i * 6
        r0 = 206 if i % 5 else 200
        p0, p1 = polar(r0 * s, deg, cx, cy), polar(214 * s, deg, cx, cy)
        d.line([*p0, *p1], fill=GUMUS if i % 5 == 0 else GUMUS_K, width=int((2 if i % 5 == 0 else 1) * s))
    # baton indeksler (12 çift)
    for h in range(12):
        deg = h * 30
        offs = (-5, 5) if h == 0 else (0,)
        for off in offs:
            pts = []
            for r, w in ((196, 3.2), (160, 2.4)):
                p = polar(r * s, deg, cx, cy)
                pts.append((p, w))
            (p0, w0), (p1, w1) = pts
            # dikdörtgen baton: deg yönünde
            import math
            ang = math.radians(deg)
            nx, ny = math.cos(ang) * s, math.sin(ang) * s  # dik yön
            ox, oy = nx * off, ny * off
            poly = [(p0[0] - nx * w0 + ox, p0[1] - ny * w0 + oy), (p0[0] + nx * w0 + ox, p0[1] + ny * w0 + oy),
                    (p1[0] + nx * w1 + ox, p1[1] + ny * w1 + oy), (p1[0] - nx * w1 + ox, p1[1] - ny * w1 + oy)]
            d.polygon(poly, fill=GUMUS)
            d.line([p0[0] + ox, p0[1] + oy, p1[0] + ox, p1[1] + oy], fill=GUMUS_K, width=int(0.8 * s))
    # küçük saniye alt kadranı
    d.ellipse([(SUB[0] - SUB_R) * s, (SUB[1] - SUB_R) * s, (SUB[0] + SUB_R) * s, (SUB[1] + SUB_R) * s],
              fill=SIYAH_K, outline=GUMUS_K, width=int(1.2 * s))
    for i in range(60):
        r0 = SUB_R - (6 if i % 15 == 0 else 3)
        p0, p1 = polar(r0 * s, i * 6, SUB[0] * s, SUB[1] * s), polar((SUB_R - 1) * s, i * 6, SUB[0] * s, SUB[1] * s)
        d.line([*p0, *p1], fill=GUMUS if i % 15 == 0 else GUMUS_K, width=int((1.6 if i % 15 == 0 else 0.8) * s))
    # tarih penceresi
    x, y = POS_TARIH
    d.rectangle([(x - 20) * s, (y - 15) * s, (x + 20) * s, (y + 15) * s], fill=GUMUS_K)
    d.rectangle([(x - 18) * s, (y - 13) * s, (x + 18) * s, (y + 13) * s], fill=SIYAH_K)
    img = down(big)
    yerlestir(img, simge("adim", GRI, 18), (POS_ADIM[0], POS_ADIM[1] - 18))
    yerlestir(img, simge("kalp", GRI, 16), (POS_NABIZ[0] - 26, POS_NABIZ[1]))
    yerlestir(img, simge("pil", GRI, 16), (POS_PIL[0] - 28, POS_PIL[1]))
    return img


def dauphine(uz, gen, col, aod=False):
    big, s = ss()
    d = ImageDraw.Draw(big)
    cx, cy = 233 * s, 233 * s
    L, Wd = uz * s, gen * s
    sol = [(cx, cy - L), (cx - Wd / 2, cy - L * 0.18), (cx, cy + 16 * s)]
    sag = [(cx, cy - L), (cx + Wd / 2, cy - L * 0.18), (cx, cy + 16 * s)]
    if aod:
        d.polygon([(cx, cy - L), (cx - Wd / 2, cy - L * 0.18), (cx, cy + 16 * s), (cx + Wd / 2, cy - L * 0.18)],
                  outline=col, width=int(1.4 * s))
    else:
        d.polygon(sol, fill=col)
        d.polygon(sag, fill=tuple(int(c * 0.62) for c in col[:3]) + (255,))
    return down(big)


def kucuk_saniye():
    big, s = ss()
    d = ImageDraw.Draw(big)
    cx, cy = SUB[0] * s, SUB[1] * s
    d.line([cx, cy + 12 * s, cx, cy - (SUB_R - 6) * s], fill=GUMUS, width=int(1.5 * s))
    d.ellipse([cx - 3 * s, cy - 3 * s, cx + 3 * s, cy + 3 * s], fill=GUMUS)
    return down(big)


def kapak(aod=False):
    big, s = ss()
    d = ImageDraw.Draw(big)
    cx, cy = 233 * s, 233 * s
    if aod:
        d.ellipse([cx - 4 * s, cy - 4 * s, cx + 4 * s, cy + 4 * s], outline=AOD_G, width=int(1.2 * s))
    else:
        d.ellipse([cx - 6 * s, cy - 6 * s, cx + 6 * s, cy + 6 * s], fill=GUMUS)
        d.ellipse([cx - 2 * s, cy - 2 * s, cx + 2 * s, cy + 2 * s], fill=SIYAH_K)
    return down(big)


def aod_arka_plan():
    big, s = ss()
    d = ImageDraw.Draw(big)
    cx, cy = 233 * s, 233 * s
    for h in range(12):
        deg = h * 30
        p0, p1 = polar(196 * s, deg, cx, cy), polar(166 * s, deg, cx, cy)
        d.line([*p0, *p1], fill=AOD_G, width=int(2 * s))
    x, y = POS_TARIH
    d.rectangle([(x - 20) * s, (y - 15) * s, (x + 20) * s, (y + 15) * s], outline=AOD_G, width=s)
    img = Image.new("RGBA", (W, H), (0, 0, 0, 255))
    img.alpha_composite(down(big))
    return img


def onizleme(aktif, saat, dk, sn, adim, nabiz, pil, gun, gunadi):
    base = Image.open(os.path.join(aktif, "00_arka_plan.png")).convert("RGBA")
    rt = os.path.join(aktif, "rakam_tarih")
    sayi_yaz(base, rt, f"{gun:02d}", POS_TARIH)
    yerlestir(base, gun_ac(os.path.join(aktif, "gun"), gunadi), POS_GUN)
    if aktif == AKTIF:
        rv = os.path.join(aktif, "rakam_veri")
        sayi_yaz(base, rv, str(adim), (POS_ADIM[0], POS_ADIM[1] + 4))
        sayi_yaz(base, rv, str(nabiz), (POS_NABIZ[0] + 6, POS_NABIZ[1]))
        sayi_yaz(base, rv, f"{pil}%", (POS_PIL[0] + 8, POS_PIL[1]))
        base.alpha_composite(Image.open(os.path.join(aktif, "ibre_kucuk_saniye.png")).rotate(-sn * 6, resample=Image.BICUBIC, center=SUB))
    base.alpha_composite(dondur(Image.open(os.path.join(aktif, "ibre_saat.png")), (saat % 12) * 30 + dk * 0.5))
    base.alpha_composite(dondur(Image.open(os.path.join(aktif, "ibre_dakika.png")), dk * 6 + sn * 0.1))
    base.alpha_composite(Image.open(os.path.join(aktif, "merkez_kapak.png")))
    return base


def main():
    temizle(AKTIF, AOD)
    save(arka_plan(), AKTIF, "00_arka_plan.png")
    save(dauphine(118, 14, GUMUS), AKTIF, "ibre_saat.png")
    save(dauphine(178, 11, GUMUS), AKTIF, "ibre_dakika.png")
    save(kucuk_saniye(), AKTIF, "ibre_kucuk_saniye.png")
    save(kapak(), AKTIF, "merkez_kapak.png")
    rakam_seti(os.path.join(AKTIF, "rakam_tarih"), BEYAZ, "bahn", 22, 13, ekstra=())
    rakam_seti(os.path.join(AKTIF, "rakam_veri"), GRI, "bahn", 19, 11)
    gun_seti(os.path.join(AKTIF, "gun"), GRI, "bahn", 18, (60, 26))

    save(aod_arka_plan(), AOD, "00_arka_plan.png")
    save(dauphine(118, 14, AOD_G, aod=True), AOD, "ibre_saat.png")
    save(dauphine(178, 11, AOD_G, aod=True), AOD, "ibre_dakika.png")
    save(kapak(aod=True), AOD, "merkez_kapak.png")
    rakam_seti(os.path.join(AOD, "rakam_tarih"), AOD_G, "bahn", 22, 13, ekstra=())
    gun_seti(os.path.join(AOD, "gun"), AOD_G, "bahn", 18, (60, 26))

    onizleme(AKTIF, **ORNEK).save(os.path.join(ONIZ, f"{AD}_aktif.png"))
    onizleme(AKTIF, **ORNEK2).save(os.path.join(ONIZ, f"{AD}_aktif_2.png"))
    o = onizleme(AOD, **ORNEK); o.save(os.path.join(ONIZ, f"{AD}_aod.png"))
    rapor(AD, [o, onizleme(AOD, **ORNEK2)], KAT)


if __name__ == "__main__":
    main()
