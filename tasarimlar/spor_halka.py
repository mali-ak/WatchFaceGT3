# -*- coding: utf-8 -*-
"""
Tasarım 3 — "Halka": spor. Siyah zemin, üç iç içe ilerleme halkası (adım / nabız / pil),
sağ altta büyük saat, üstte gün + tarih. Halkalar 11 kare (0-100) resim dizisi.
"""
import os
from PIL import Image, ImageDraw
from ortak import *

AD = "halka"
KAT = os.path.join(KOK, "katmanlar_" + AD)
AKTIF, AOD = os.path.join(KAT, "aktif"), os.path.join(KAT, "aod")
ONIZ = os.path.join(KOK, "onizleme")

SIYAH = (6, 6, 8, 255)
LIME = (190, 255, 60, 255)
PEMBE = (255, 50, 120, 255)
CYAN = (40, 220, 255, 255)
SONUK = (34, 34, 40, 255)
BEYAZ = (245, 245, 245, 255)
GRI = (150, 150, 160, 255)
AOD_G = (120, 120, 128, 255)

HM = (150, 200)             # halka merkezi
HALKALAR = [("adim", 112, 20, LIME), ("kalp", 88, 20, PEMBE), ("pil", 64, 20, CYAN)]
POS_SAAT = (233, 356)       # HH:MM merkezi (büyük)
POS_GUN = (233, 52)
POS_VERI = [("adim", (342, 160)), ("kalp", (342, 204)), ("pil", (342, 248))]


def arka_plan():
    big, s = ss()
    d = ImageDraw.Draw(big)
    d.ellipse([0, 0, W * s, H * s], fill=SIYAH)
    img = down(big)
    # halka içine simgeler (ortada küçük)
    yerlestir(img, simge("adim", LIME, 20), (HM[0], HM[1] - 12))
    yerlestir(img, simge("kalp", PEMBE, 18), (HM[0] - 11, HM[1] + 11))
    yerlestir(img, simge("pil", CYAN, 18), (HM[0] + 12, HM[1] + 11))
    # sağ veri listesi simgeleri
    for ad, (x, y) in POS_VERI:
        col = {"adim": LIME, "kalp": PEMBE, "pil": CYAN}[ad]
        yerlestir(img, simge(ad, col, 22), (x - 36, y))
    d2 = ImageDraw.Draw(img)
    d2.line([290, 140, 290, 268], fill=SONUK, width=2)
    return img


def aod_arka_plan():
    img = Image.new("RGBA", (W, H), (0, 0, 0, 255))
    d = ImageDraw.Draw(img)
    for ad, r, k, col in HALKALAR:
        d.ellipse([HM[0] - r, HM[1] - r, HM[0] + r, HM[1] + r], outline=AOD_G, width=1)
    return img


def onizleme(aktif, saat, dk, sn, adim, nabiz, pil, gun, gunadi):
    base = Image.open(os.path.join(aktif, "00_arka_plan.png")).convert("RGBA")
    rz, rv = os.path.join(aktif, "rakam_zaman"), os.path.join(aktif, "rakam_veri")
    if aktif == AKTIF:
        hy = os.path.join(aktif, "halka")
        base.alpha_composite(yay_ac(hy, "adim", min(100, adim / 100)))        # hedef 10 000 adım
        base.alpha_composite(yay_ac(hy, "kalp", min(100, nabiz / 1.8)))      # 180 bpm = tam
        base.alpha_composite(yay_ac(hy, "pil", pil))
        sayi_yaz(base, rv, str(adim), (POS_VERI[0][1][0] - 18, POS_VERI[0][1][1]), "lm")
        sayi_yaz(base, rv, str(nabiz), (POS_VERI[1][1][0] - 18, POS_VERI[1][1][1]), "lm")
        sayi_yaz(base, rv, f"{pil}%", (POS_VERI[2][1][0] - 18, POS_VERI[2][1][1]), "lm")
    sayi_yaz(base, rz, f"{saat:02d}:{dk:02d}", POS_SAAT)
    yerlestir(base, gun_ac(os.path.join(aktif, "gun"), gunadi), (POS_GUN[0] - 34, POS_GUN[1]))
    sayi_yaz(base, rv, f"{gun:02d}", (POS_GUN[0] + 30, POS_GUN[1]))
    return base


def main():
    temizle(AKTIF, AOD)
    save(arka_plan(), AKTIF, "00_arka_plan.png")
    for ad, r, k, col in HALKALAR:
        yay_kareleri(os.path.join(AKTIF, "halka"), ad, HM, r, k, col, SONUK)
    rakam_seti(os.path.join(AKTIF, "rakam_zaman"), BEYAZ, "bahn", 84, 42, ekstra=(":",))
    rakam_seti(os.path.join(AKTIF, "rakam_veri"), BEYAZ, "bahn", 30, 17)
    gun_seti(os.path.join(AKTIF, "gun"), GRI, "bahn", 28, (70, 36))

    save(aod_arka_plan(), AOD, "00_arka_plan.png")
    rakam_seti(os.path.join(AOD, "rakam_zaman"), TRANSP, "bahn", 84, 42, ekstra=(":",), outline=BEYAZ, ow=2)
    rakam_seti(os.path.join(AOD, "rakam_veri"), AOD_G, "bahn", 30, 17)
    gun_seti(os.path.join(AOD, "gun"), AOD_G, "bahn", 28, (70, 36))

    onizleme(AKTIF, **ORNEK).save(os.path.join(ONIZ, f"{AD}_aktif.png"))
    onizleme(AKTIF, **ORNEK2).save(os.path.join(ONIZ, f"{AD}_aktif_2.png"))
    o = onizleme(AOD, **ORNEK); o.save(os.path.join(ONIZ, f"{AD}_aod.png"))
    rapor(AD, [o, onizleme(AOD, **ORNEK2)], KAT)


if __name__ == "__main__":
    main()
