# -*- coding: utf-8 -*-
"""
Tasarım "Zarif": siyah zemin, ince serif (Georgia) büyük saat, şampanya rengi ince çizgiler,
altında küçük büyük-harf gün + tarih, en altta çok küçük gri adım / nabız / pil. Dijital ama "dress".
"""
import os
from PIL import Image, ImageDraw
from ortak import *

AD = "zarif"
KAT = os.path.join(KOK, "katmanlar_" + AD)
AKTIF, AOD = os.path.join(KAT, "aktif"), os.path.join(KAT, "aod")
ONIZ = os.path.join(KOK, "onizleme")

SIYAH = (10, 10, 11, 255)
SAMPANYA = (222, 200, 150, 255)
FILDISI = (242, 236, 224, 255)
GRI = (120, 118, 112, 255)
AOD_G = (120, 118, 112, 255)

POS_SAAT = (233, 212)
POS_GUN = (233, 300)
VERI = [("adim", (128, 372)), ("kalp", (233, 372)), ("pil", (338, 372))]


def arka_plan():
    big, s = ss()
    d = ImageDraw.Draw(big)
    cx, cy = 233 * s, 233 * s
    d.ellipse([0, 0, W * s, H * s], fill=SIYAH)
    # ince dış halka + 12 nokta
    d.ellipse([cx - 220 * s, cy - 220 * s, cx + 220 * s, cy + 220 * s], outline=(40, 38, 34, 255), width=int(1 * s))
    for h in range(12):
        p = polar(220 * s, h * 30, cx, cy)
        rr = 2.2 * s
        d.ellipse([p[0] - rr, p[1] - rr, p[0] + rr, p[1] + rr], fill=SAMPANYA)
    # şampanya hairline çizgiler (saatin üstü ve altı)
    d.line([(233 - 120) * s, 136 * s, (233 + 120) * s, 136 * s], fill=SAMPANYA, width=int(1 * s))
    d.line([(233 - 120) * s, 272 * s, (233 + 120) * s, 272 * s], fill=SAMPANYA, width=int(1 * s))
    for x in (233 - 120, 233 + 120):
        for y in (136, 272):
            d.ellipse([(x - 2) * s, (y - 2) * s, (x + 2) * s, (y + 2) * s], fill=SAMPANYA)
    # alt ayraç noktaları
    for x in (180, 286):
        d.ellipse([(x - 1.5) * s, (372 - 1.5) * s, (x + 1.5) * s, (372 + 1.5) * s], fill=GRI)
    img = down(big)
    for ad, (x, y) in VERI:
        yerlestir(img, simge(ad, GRI, 16), (x - 30, y))
    return img


def aod_arka_plan():
    img = Image.new("RGBA", (W, H), (0, 0, 0, 255))
    d = ImageDraw.Draw(img)
    d.line([233 - 120, 136, 233 + 120, 136], fill=AOD_G, width=1)
    d.line([233 - 120, 272, 233 + 120, 272], fill=AOD_G, width=1)
    return img


def onizleme(aktif, saat, dk, sn, adim, nabiz, pil, gun, gunadi):
    base = Image.open(os.path.join(aktif, "00_arka_plan.png")).convert("RGBA")
    sayi_yaz(base, os.path.join(aktif, "rakam_zaman"), f"{saat:02d}:{dk:02d}", POS_SAAT)
    yerlestir(base, gun_ac(os.path.join(aktif, "gun"), gunadi), (POS_GUN[0] - 36, POS_GUN[1]))
    sayi_yaz(base, os.path.join(aktif, "rakam_tarih"), f"{gun:02d}", (POS_GUN[0] + 38, POS_GUN[1]))
    if aktif == AKTIF:
        rv = os.path.join(aktif, "rakam_veri")
        sayi_yaz(base, rv, str(adim), (VERI[0][1][0] + 10, VERI[0][1][1]))
        sayi_yaz(base, rv, str(nabiz), (VERI[1][1][0] + 6, VERI[1][1][1]))
        sayi_yaz(base, rv, f"{pil}%", (VERI[2][1][0] + 10, VERI[2][1][1]))
    return base


def main():
    temizle(AKTIF, AOD)
    save(arka_plan(), AKTIF, "00_arka_plan.png")
    rakam_seti(os.path.join(AKTIF, "rakam_zaman"), FILDISI, "georgia", 118, 62, ekstra=(":",))
    rakam_seti(os.path.join(AKTIF, "rakam_tarih"), SAMPANYA, "georgia", 24, 14, ekstra=())
    rakam_seti(os.path.join(AKTIF, "rakam_veri"), GRI, "bahn", 18, 10)
    gun_seti(os.path.join(AKTIF, "gun"), SAMPANYA, "georgia", 22, (70, 30))

    save(aod_arka_plan(), AOD, "00_arka_plan.png")
    rakam_seti(os.path.join(AOD, "rakam_zaman"), TRANSP, "georgia", 118, 62, ekstra=(":",), outline=AOD_G, ow=1)
    rakam_seti(os.path.join(AOD, "rakam_tarih"), AOD_G, "georgia", 24, 14, ekstra=())
    gun_seti(os.path.join(AOD, "gun"), AOD_G, "georgia", 22, (70, 30))

    onizleme(AKTIF, **ORNEK).save(os.path.join(ONIZ, f"{AD}_aktif.png"))
    onizleme(AKTIF, **ORNEK2).save(os.path.join(ONIZ, f"{AD}_aktif_2.png"))
    o = onizleme(AOD, **ORNEK); o.save(os.path.join(ONIZ, f"{AD}_aod.png"))
    rapor(AD, [o, onizleme(AOD, **ORNEK2)], KAT)


if __name__ == "__main__":
    main()
