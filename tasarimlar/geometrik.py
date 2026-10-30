# -*- coding: utf-8 -*-
"""
Tasarım 5 — "Prizma": geometrik analog. Dilimlere bölünmüş renk blokları (mor / turkuaz / sarı / mercan),
beyaz ince ibreler, saat işaretleri nokta, alt yarıda beş veri. AOD: yalnız dış çizgiler.
"""
import math
import os
from PIL import Image, ImageDraw
from ortak import *

AD = "prizma"
KAT = os.path.join(KOK, "katmanlar_" + AD)
AKTIF, AOD = os.path.join(KAT, "aktif"), os.path.join(KAT, "aod")
ONIZ = os.path.join(KOK, "onizleme")

MOR = (96, 60, 200, 255)
TURKUAZ = (20, 190, 180, 255)
SARI = (255, 200, 40, 255)
MERCAN = (255, 96, 90, 255)
KOYU = (22, 20, 34, 255)
BEYAZ = (250, 250, 250, 255)
AOD_G = (140, 140, 140, 255)

DILIMLER = [(-90, 0, MOR), (0, 90, TURKUAZ), (90, 180, SARI), (180, 270, MERCAN)]
POS_VERI = [("gun", (233, 318)), ("adim", (138, 358)), ("kalp", (233, 358)), ("pil", (322, 358))]


def arka_plan():
    big, s = ss()
    d = ImageDraw.Draw(big)
    cx, cy = 233 * s, 233 * s
    for a0, a1, col in DILIMLER:
        d.pieslice([0, 0, W * s, H * s], a0, a1, fill=col)
    # çeyreklerin ortasına açık üçgen vurgu (prizma hissi)
    for a0, a1, col in DILIMLER:
        am = (a0 + a1) / 2
        lighter = tuple(min(255, int(c * 1.18)) for c in col[:3]) + (255,)
        p1 = (cx + 233 * s * math.cos(math.radians(a0)), cy + 233 * s * math.sin(math.radians(a0)))
        p2 = (cx + 233 * s * math.cos(math.radians(am)), cy + 233 * s * math.sin(math.radians(am)))
        d.polygon([(cx, cy), p1, p2], fill=lighter)
    # koyu iç disk (kadran)
    r = 158
    d.ellipse([cx - r * s, cy - r * s, cx + r * s, cy + r * s], fill=KOYU)
    d.ellipse([cx - (r - 4) * s, cy - (r - 4) * s, cx + (r - 4) * s, cy + (r - 4) * s], outline=(255, 255, 255, 40), width=s)
    # saat noktaları
    for h in range(12):
        p = polar(138 * s, h * 30, cx, cy)
        rr = (5 if h % 3 == 0 else 2.5) * s
        d.ellipse([p[0] - rr, p[1] - rr, p[0] + rr, p[1] + rr], fill=BEYAZ)
    # alt veri bandı
    d.rounded_rectangle([(233 - 132) * s, 296 * s, (233 + 132) * s, 392 * s], radius=22 * s, fill=(40, 38, 58, 255))
    img = down(big)
    for ad, (x, y) in POS_VERI:
        if ad == "gun":
            continue
        yerlestir(img, simge(ad, BEYAZ, 20), (x - 30, y))
    return img


def ibre(uzunluk, genislik, col, aod=False):
    big, s = ss()
    d = ImageDraw.Draw(big)
    cx, cy = 233 * s, 233 * s
    pts = [(cx - genislik / 2 * s, cy + 18 * s), (cx - genislik / 2 * s, cy - uzunluk * s),
           (cx + genislik / 2 * s, cy - uzunluk * s), (cx + genislik / 2 * s, cy + 18 * s)]
    if aod:
        d.polygon(pts, outline=col, width=int(1.5 * s))
    else:
        d.rounded_rectangle([pts[0][0], pts[1][1], pts[2][0], pts[0][1]], radius=genislik / 2 * s, fill=col)
    return down(big)


def saniye():
    big, s = ss()
    d = ImageDraw.Draw(big)
    cx, cy = 233 * s, 233 * s
    d.line([cx, cy + 30 * s, cx, cy - 148 * s], fill=SARI, width=int(2 * s))
    d.ellipse([cx - 6 * s, cy - 148 * s - 6 * s, cx + 6 * s, cy - 148 * s + 6 * s], fill=SARI)
    return down(big)


def kapak(aod=False):
    big, s = ss()
    d = ImageDraw.Draw(big)
    cx, cy = 233 * s, 233 * s
    if aod:
        d.ellipse([cx - 5 * s, cy - 5 * s, cx + 5 * s, cy + 5 * s], outline=AOD_G, width=int(1.5 * s))
    else:
        d.ellipse([cx - 8 * s, cy - 8 * s, cx + 8 * s, cy + 8 * s], fill=BEYAZ)
        d.ellipse([cx - 3 * s, cy - 3 * s, cx + 3 * s, cy + 3 * s], fill=KOYU)
    return down(big)


def aod_arka_plan():
    img = Image.new("RGBA", (W, H), (0, 0, 0, 255))
    d = ImageDraw.Draw(img)
    for a0, a1, col in DILIMLER:
        p = polar(233, a0 + 90)
        d.line([233, 233, p[0], p[1]], fill=(60, 60, 60, 255), width=1)
    d.ellipse([233 - 158, 233 - 158, 233 + 158, 233 + 158], outline=AOD_G, width=1)
    for h in range(12):
        p = polar(138, h * 30)
        rr = 4 if h % 3 == 0 else 2
        d.ellipse([p[0] - rr, p[1] - rr, p[0] + rr, p[1] + rr], fill=AOD_G)
    return img


def onizleme(aktif, saat, dk, sn, adim, nabiz, pil, gun, gunadi):
    base = Image.open(os.path.join(aktif, "00_arka_plan.png")).convert("RGBA")
    rv = os.path.join(aktif, "rakam_veri")
    yerlestir(base, gun_ac(os.path.join(aktif, "gun"), gunadi), (POS_VERI[0][1][0] - 26, POS_VERI[0][1][1]))
    sayi_yaz(base, rv, f"{gun:02d}", (POS_VERI[0][1][0] + 34, POS_VERI[0][1][1]))
    if aktif == AKTIF:
        sayi_yaz(base, rv, str(adim), (POS_VERI[1][1][0] + 20, POS_VERI[1][1][1]))
        sayi_yaz(base, rv, str(nabiz), (POS_VERI[2][1][0] + 14, POS_VERI[2][1][1]))
        sayi_yaz(base, rv, f"{pil}%", (POS_VERI[3][1][0] + 20, POS_VERI[3][1][1]))
    base.alpha_composite(dondur(Image.open(os.path.join(aktif, "ibre_saat.png")), (saat % 12) * 30 + dk * 0.5))
    base.alpha_composite(dondur(Image.open(os.path.join(aktif, "ibre_dakika.png")), dk * 6 + sn * 0.1))
    if aktif == AKTIF:
        base.alpha_composite(dondur(Image.open(os.path.join(aktif, "ibre_saniye.png")), sn * 6))
    base.alpha_composite(Image.open(os.path.join(aktif, "merkez_kapak.png")))
    return base


def main():
    temizle(AKTIF, AOD)
    save(arka_plan(), AKTIF, "00_arka_plan.png")
    save(ibre(92, 10, BEYAZ), AKTIF, "ibre_saat.png")
    save(ibre(134, 7, BEYAZ), AKTIF, "ibre_dakika.png")
    save(saniye(), AKTIF, "ibre_saniye.png")
    save(kapak(), AKTIF, "merkez_kapak.png")
    rakam_seti(os.path.join(AKTIF, "rakam_veri"), BEYAZ, "bahn", 24, 14)
    gun_seti(os.path.join(AKTIF, "gun"), SARI, "bahn", 22, (52, 28))

    save(aod_arka_plan(), AOD, "00_arka_plan.png")
    save(ibre(92, 10, AOD_G, aod=True), AOD, "ibre_saat.png")
    save(ibre(134, 7, AOD_G, aod=True), AOD, "ibre_dakika.png")
    save(kapak(aod=True), AOD, "merkez_kapak.png")
    rakam_seti(os.path.join(AOD, "rakam_veri"), AOD_G, "bahn", 24, 14)
    gun_seti(os.path.join(AOD, "gun"), AOD_G, "bahn", 22, (52, 28))

    onizleme(AKTIF, **ORNEK).save(os.path.join(ONIZ, f"{AD}_aktif.png"))
    onizleme(AKTIF, **ORNEK2).save(os.path.join(ONIZ, f"{AD}_aktif_2.png"))
    o = onizleme(AOD, **ORNEK); o.save(os.path.join(ONIZ, f"{AD}_aod.png"))
    rapor(AD, [o, onizleme(AOD, **ORNEK2)], KAT)


if __name__ == "__main__":
    main()
