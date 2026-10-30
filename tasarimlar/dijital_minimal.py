# -*- coding: utf-8 -*-
"""
Tasarım 2 — "Mercan": dijital minimal. Lacivert zemin, sağ-altta büyük mercan daire,
sol tarafta dev saat/dakika rakamları alt alta, mercan alanda beş veri.
"""
import os
from PIL import Image, ImageDraw
from ortak import *

AD = "mercan"
KAT = os.path.join(KOK, "katmanlar_" + AD)
AKTIF, AOD = os.path.join(KAT, "aktif"), os.path.join(KAT, "aod")
ONIZ = os.path.join(KOK, "onizleme")

LACIVERT = (11, 16, 38, 255)
MERCAN = (255, 79, 63, 255)
MERCAN_K = (214, 54, 42, 255)
BEYAZ = (250, 247, 242, 255)
AOD_G = (150, 150, 150, 255)

POS_SAAT = (142, 140)       # saat rakamları merkezi
POS_DK = (142, 300)
VERI = [("gun", (330, 232)), ("adim", (352, 286)), ("kalp", (360, 338)), ("pil", (346, 390))]
DAIRE = ((432, 404), 228)   # merkez, yarıçap


def arka_plan():
    big, s = ss()
    d = ImageDraw.Draw(big)
    d.ellipse([0, 0, W * s, H * s], fill=LACIVERT)
    (cx, cy), r = DAIRE
    d.ellipse([(cx - r) * s, (cy - r) * s, (cx + r) * s, (cy + r) * s], fill=MERCAN)
    # mercan dairede ince koyu halka (derinlik)
    d.ellipse([(cx - r + 14) * s, (cy - r + 14) * s, (cx + r - 14) * s, (cy + r - 14) * s],
              outline=MERCAN_K, width=int(1.5 * s))
    # simgeler (beyaz) mercan alana
    img = down(big)
    for ad, (x, y) in VERI:
        if ad == "gun":
            continue
        yerlestir(img, simge(ad, BEYAZ, 26), (x - 58, y))
    yerlestir(img, simge("takvim", BEYAZ, 26), (VERI[0][1][0] - 62, VERI[0][1][1]))
    # saat/dakika ayırıcı ince çizgi
    d2 = ImageDraw.Draw(img)
    d2.line([70, 220, 215, 220], fill=(255, 255, 255, 60), width=2)
    return img


def aod_arka_plan():
    img = Image.new("RGBA", (W, H), (0, 0, 0, 255))
    d = ImageDraw.Draw(img)
    (cx, cy), r = DAIRE
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=MERCAN_K, width=2)
    d.line([70, 220, 215, 220], fill=AOD_G, width=1)
    return img


def onizleme(aktif, saat, dk, sn, adim, nabiz, pil, gun, gunadi):
    base = Image.open(os.path.join(aktif, "00_arka_plan.png")).convert("RGBA")
    rz = os.path.join(aktif, "rakam_zaman")
    rv = os.path.join(aktif, "rakam_veri")
    sayi_yaz(base, rz, f"{saat:02d}", POS_SAAT)
    sayi_yaz(base, rz, f"{dk:02d}", POS_DK)
    if aktif == AKTIF:
        g = gun_ac(os.path.join(aktif, "gun"), gunadi)
        yerlestir(base, g, (VERI[0][1][0] - 14, VERI[0][1][1]))
        sayi_yaz(base, rv, f"{gun:02d}", (VERI[0][1][0] + 40, VERI[0][1][1]))
        sayi_yaz(base, rv, str(adim), VERI[1][1])
        sayi_yaz(base, rv, str(nabiz), VERI[2][1])
        sayi_yaz(base, rv, f"{pil}%", VERI[3][1])
    else:
        g = gun_ac(os.path.join(aktif, "gun"), gunadi)
        yerlestir(base, g, (VERI[0][1][0] - 14, VERI[0][1][1]))
        sayi_yaz(base, rv, f"{gun:02d}", (VERI[0][1][0] + 40, VERI[0][1][1]))
    return base


def main():
    temizle(AKTIF, AOD)
    save(arka_plan(), AKTIF, "00_arka_plan.png")
    rakam_seti(os.path.join(AKTIF, "rakam_zaman"), BEYAZ, "bahn", 150, 78, ekstra=())
    rakam_seti(os.path.join(AKTIF, "rakam_veri"), BEYAZ, "bold", 28, 17)
    gun_seti(os.path.join(AKTIF, "gun"), BEYAZ, "bold", 26, (66, 34))

    save(aod_arka_plan(), AOD, "00_arka_plan.png")
    rakam_seti(os.path.join(AOD, "rakam_zaman"), TRANSP, "bahn", 150, 78, ekstra=(), outline=AOD_G, ow=2)
    rakam_seti(os.path.join(AOD, "rakam_veri"), AOD_G, "bold", 28, 17)
    gun_seti(os.path.join(AOD, "gun"), AOD_G, "bold", 26, (66, 34))

    a = onizleme(AKTIF, **ORNEK); a.save(os.path.join(ONIZ, f"{AD}_aktif.png"))
    onizleme(AKTIF, **ORNEK2).save(os.path.join(ONIZ, f"{AD}_aktif_2.png"))
    o = onizleme(AOD, **ORNEK); o.save(os.path.join(ONIZ, f"{AD}_aod.png"))
    rapor(AD, [o, onizleme(AOD, **ORNEK2)], KAT)


if __name__ == "__main__":
    main()
