# -*- coding: utf-8 -*-
"""
Tasarım "Giyoş": siyah kadran, merkezde giyoş (iç içe halka) dokusu, rose gold indeks ve ibreler,
kronograf görünümlü iki alt kadran: 9'da adım (0-10 000), 3'te pil; 6'da nabız; 4:30'da tarih; 12'de gün.
Alt kadran ibreleri 11 kare resim dizisi olarak üretilir.
"""
import math
import os
from PIL import Image, ImageDraw
from ortak import *

AD = "giyos"
KAT = os.path.join(KOK, "katmanlar_" + AD)
AKTIF, AOD = os.path.join(KAT, "aktif"), os.path.join(KAT, "aod")
ONIZ = os.path.join(KOK, "onizleme")

SIYAH = (12, 11, 12, 255)
DOKU = (255, 255, 255, 22)
ROSE = (218, 165, 135, 255)
ROSE_K = (150, 105, 80, 255)
GRI = (150, 146, 142, 255)
BEYAZ = (240, 236, 232, 255)
AOD_G = (118, 110, 104, 255)

SUB_ADIM = (118, 233)
SUB_PIL = (348, 233)
SUB_R = 50
POS_NABIZ = (233, 330)
POS_TARIH = (318, 318)
POS_GUN = (233, 128)


def alt_kadran(d, s, m, r, etiket_col):
    cx, cy = m[0] * s, m[1] * s
    d.ellipse([cx - r * s, cy - r * s, cx + r * s, cy + r * s], fill=(20, 19, 20, 255), outline=ROSE_K, width=int(1.2 * s))
    for i in range(40):
        a = -135 + i * 270 / 40            # 270° ölçek
        r0 = r - (7 if i % 10 == 0 else 3)
        p0, p1 = polar(r0 * s, a, cx, cy), polar((r - 1) * s, a, cx, cy)
        d.line([*p0, *p1], fill=ROSE if i % 10 == 0 else ROSE_K, width=int((1.6 if i % 10 == 0 else 0.8) * s))
    p = polar((r - 1) * s, 135, cx, cy)
    d.line([*p, *polar((r - 7) * s, 135, cx, cy)], fill=ROSE, width=int(1.6 * s))


def arka_plan():
    big, s = ss()
    d = ImageDraw.Draw(big)
    cx, cy = 233 * s, 233 * s
    d.ellipse([0, 0, W * s, H * s], fill=SIYAH)
    # giyoş: iç içe ince halkalar + ışınsal çizgiler, ayrı katmanda (alfa doğru karışsın)
    doku = Image.new("RGBA", big.size, TRANSP)
    dd = ImageDraw.Draw(doku)
    for r in range(4, 150, 3):
        dd.ellipse([cx - r * s, cy - r * s, cx + r * s, cy + r * s], outline=DOKU, width=int(0.9 * s))
    for i in range(0, 360, 5):
        p0, p1 = polar(20 * s, i, cx, cy), polar(150 * s, i, cx, cy)
        dd.line([*p0, *p1], fill=(255, 255, 255, 9), width=int(0.7 * s))
    big = Image.alpha_composite(big, doku)
    d = ImageDraw.Draw(big)
    d.ellipse([cx - 150 * s, cy - 150 * s, cx + 150 * s, cy + 150 * s], outline=ROSE_K, width=int(1.2 * s))
    # dakika rayı ve indeksler
    for i in range(60):
        deg = i * 6
        p0, p1 = polar(206 * s, deg, cx, cy), polar(214 * s, deg, cx, cy)
        d.line([*p0, *p1], fill=ROSE_K, width=int(1 * s))
    for h in range(12):
        deg = h * 30
        if h in (3, 9):
            continue
        p0, p1 = polar(200 * s, deg, cx, cy), polar(176 * s, deg, cx, cy)
        d.line([*p0, *p1], fill=ROSE, width=int(5 * s))
        d.line([*p0, *p1], fill=ROSE_K, width=int(1 * s))
    # tachymeter benzeri dış yazı yok; sade
    alt_kadran(d, s, SUB_ADIM, SUB_R, ROSE)
    alt_kadran(d, s, SUB_PIL, SUB_R, ROSE)
    # tarih penceresi (4:30)
    x, y = POS_TARIH
    d.rectangle([(x - 19) * s, (y - 14) * s, (x + 19) * s, (y + 14) * s], fill=ROSE_K)
    d.rectangle([(x - 17) * s, (y - 12) * s, (x + 17) * s, (y + 12) * s], fill=SIYAH)
    img = down(big)
    yerlestir(img, simge("adim", GRI, 16), (SUB_ADIM[0], SUB_ADIM[1] + 24))
    yerlestir(img, simge("pil", GRI, 16), (SUB_PIL[0], SUB_PIL[1] + 24))
    yerlestir(img, simge("kalp", GRI, 16), (POS_NABIZ[0] - 26, POS_NABIZ[1]))
    return img


def ibre(uz, gen, col, aod=False):
    """Rose gold, ortası boş (açık işlemeli) ibre."""
    big, s = ss()
    d = ImageDraw.Draw(big)
    cx, cy = 233 * s, 233 * s
    L, Wd = uz * s, gen * s
    pts = [(cx - Wd * 0.3, cy + 18 * s), (cx - Wd / 2, cy - L * 0.55), (cx, cy - L), (cx + Wd / 2, cy - L * 0.55), (cx + Wd * 0.3, cy + 18 * s)]
    if aod:
        d.polygon(pts, outline=col, width=int(1.3 * s))
    else:
        d.polygon(pts, fill=col)
        d.polygon([(cx - Wd * 0.18, cy - 10 * s), (cx - Wd * 0.25, cy - L * 0.5), (cx + Wd * 0.25, cy - L * 0.5), (cx + Wd * 0.18, cy - 10 * s)], fill=SIYAH)
    return down(big)


def saniye():
    big, s = ss()
    d = ImageDraw.Draw(big)
    cx, cy = 233 * s, 233 * s
    d.line([cx, cy + 44 * s, cx, cy - 196 * s], fill=ROSE, width=int(1.6 * s))
    d.ellipse([cx - 5 * s, cy + 30 * s, cx + 5 * s, cy + 40 * s], fill=ROSE)
    return down(big)


def alt_ibre_kareleri(folder, prefix, m):
    """0..100 → -135°..+135° arası küçük ibre, 11 kare."""
    for y in range(0, 101, 10):
        big, s = ss()
        d = ImageDraw.Draw(big)
        cx, cy = m[0] * s, m[1] * s
        a = -135 + 270 * y / 100
        p = polar((SUB_R - 9) * s, a, cx, cy)
        q = polar(8 * s, a + 180, cx, cy)
        d.line([*q, *p], fill=BEYAZ, width=int(1.6 * s))
        d.ellipse([cx - 3 * s, cy - 3 * s, cx + 3 * s, cy + 3 * s], fill=ROSE)
        save(down(big), folder, f"{prefix}_{y:03d}.png")


def kapak(aod=False):
    big, s = ss()
    d = ImageDraw.Draw(big)
    cx, cy = 233 * s, 233 * s
    if aod:
        d.ellipse([cx - 4 * s, cy - 4 * s, cx + 4 * s, cy + 4 * s], outline=AOD_G, width=int(1.2 * s))
    else:
        d.ellipse([cx - 7 * s, cy - 7 * s, cx + 7 * s, cy + 7 * s], fill=ROSE)
        d.ellipse([cx - 2.5 * s, cy - 2.5 * s, cx + 2.5 * s, cy + 2.5 * s], fill=SIYAH)
    return down(big)


def aod_arka_plan():
    big, s = ss()
    d = ImageDraw.Draw(big)
    cx, cy = 233 * s, 233 * s
    for h in range(12):
        if h in (3, 9):
            continue
        p0, p1 = polar(200 * s, h * 30, cx, cy), polar(176 * s, h * 30, cx, cy)
        d.line([*p0, *p1], fill=AOD_G, width=int(2 * s))
    for m in (SUB_ADIM, SUB_PIL):
        d.ellipse([(m[0] - SUB_R) * s, (m[1] - SUB_R) * s, (m[0] + SUB_R) * s, (m[1] + SUB_R) * s], outline=AOD_G, width=s)
    x, y = POS_TARIH
    d.rectangle([(x - 19) * s, (y - 14) * s, (x + 19) * s, (y + 14) * s], outline=AOD_G, width=s)
    img = Image.new("RGBA", (W, H), (0, 0, 0, 255))
    img.alpha_composite(down(big))
    return img


def onizleme(aktif, saat, dk, sn, adim, nabiz, pil, gun, gunadi):
    base = Image.open(os.path.join(aktif, "00_arka_plan.png")).convert("RGBA")
    sayi_yaz(base, os.path.join(aktif, "rakam_tarih"), f"{gun:02d}", POS_TARIH)
    yerlestir(base, gun_ac(os.path.join(aktif, "gun"), gunadi), POS_GUN)
    if aktif == AKTIF:
        rv = os.path.join(aktif, "rakam_veri")
        base.alpha_composite(yay_ac(os.path.join(aktif, "alt_ibre"), "adim", min(100, adim / 100)))
        base.alpha_composite(yay_ac(os.path.join(aktif, "alt_ibre"), "pil", pil))
        sayi_yaz(base, rv, str(nabiz), (POS_NABIZ[0] + 6, POS_NABIZ[1]))
    base.alpha_composite(dondur(Image.open(os.path.join(aktif, "ibre_saat.png")), (saat % 12) * 30 + dk * 0.5))
    base.alpha_composite(dondur(Image.open(os.path.join(aktif, "ibre_dakika.png")), dk * 6 + sn * 0.1))
    if aktif == AKTIF:
        base.alpha_composite(dondur(Image.open(os.path.join(aktif, "ibre_saniye.png")), sn * 6))
    base.alpha_composite(Image.open(os.path.join(aktif, "merkez_kapak.png")))
    return base


def main():
    temizle(AKTIF, AOD)
    save(arka_plan(), AKTIF, "00_arka_plan.png")
    save(ibre(120, 13, ROSE), AKTIF, "ibre_saat.png")
    save(ibre(180, 11, ROSE), AKTIF, "ibre_dakika.png")
    save(saniye(), AKTIF, "ibre_saniye.png")
    save(kapak(), AKTIF, "merkez_kapak.png")
    alt_ibre_kareleri(os.path.join(AKTIF, "alt_ibre"), "adim", SUB_ADIM)
    alt_ibre_kareleri(os.path.join(AKTIF, "alt_ibre"), "pil", SUB_PIL)
    rakam_seti(os.path.join(AKTIF, "rakam_tarih"), BEYAZ, "bahn", 21, 12, ekstra=())
    rakam_seti(os.path.join(AKTIF, "rakam_veri"), GRI, "bahn", 19, 11)
    gun_seti(os.path.join(AKTIF, "gun"), ROSE, "georgia", 17, (60, 24))

    save(aod_arka_plan(), AOD, "00_arka_plan.png")
    save(ibre(120, 13, AOD_G, aod=True), AOD, "ibre_saat.png")
    save(ibre(180, 11, AOD_G, aod=True), AOD, "ibre_dakika.png")
    save(kapak(aod=True), AOD, "merkez_kapak.png")
    rakam_seti(os.path.join(AOD, "rakam_tarih"), AOD_G, "bahn", 21, 12, ekstra=())
    gun_seti(os.path.join(AOD, "gun"), AOD_G, "georgia", 17, (60, 24))

    onizleme(AKTIF, **ORNEK).save(os.path.join(ONIZ, f"{AD}_aktif.png"))
    onizleme(AKTIF, **ORNEK2).save(os.path.join(ONIZ, f"{AD}_aktif_2.png"))
    o = onizleme(AOD, **ORNEK); o.save(os.path.join(ONIZ, f"{AD}_aod.png"))
    rapor(AD, [o, onizleme(AOD, **ORNEK2)], KAT)


if __name__ == "__main__":
    main()
