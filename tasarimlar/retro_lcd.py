# -*- coding: utf-8 -*-
"""
Tasarım 4 — "Retro LCD": turuncu plastik çerçeve, yeşilimsi LCD ekran, yedi parçalı rakamlar,
sönük "hayalet" segmentler, Türkçe etiketler. Beş veri: adım, nabız, pil, tarih, gün.
"""
import os
from PIL import Image, ImageDraw
from ortak import *

AD = "retro"
KAT = os.path.join(KOK, "katmanlar_" + AD)
AKTIF, AOD = os.path.join(KAT, "aktif"), os.path.join(KAT, "aod")
ONIZ = os.path.join(KOK, "onizleme")

TURUNCU = (242, 120, 30, 255)
TURUNCU_K = (180, 80, 15, 255)
LCD = (168, 186, 120, 255)
LCD_K = (148, 166, 104, 255)
MUREKKEP = (24, 28, 20, 255)
HAYALET = (152, 170, 108, 255)
AOD_SEG = (90, 110, 60, 255)
AOD_GRI = (110, 110, 110, 255)

EKRAN = (58, 110, 408, 356)        # LCD dikdörtgeni
POS_SAAT = (233, 200)              # HH:MM
POS_GUN = (118, 124)
POS_TARIH = (334, 124)
ALT = [("adim", (112, 300)), ("kalp", (233, 300)), ("pil", (354, 300))]


def arka_plan():
    big, s = ss()
    d = ImageDraw.Draw(big)
    d.ellipse([0, 0, W * s, H * s], fill=TURUNCU)
    # çerçeve dokusu: ince koyu halkalar
    for r in (226, 214):
        d.ellipse([(233 - r) * s, (233 - r) * s, (233 + r) * s, (233 + r) * s], outline=TURUNCU_K, width=int(1.5 * s))
    x0, y0, x1, y1 = [v * s for v in EKRAN]
    d.rounded_rectangle([x0 - 8 * s, y0 - 8 * s, x1 + 8 * s, y1 + 8 * s], radius=16 * s, fill=TURUNCU_K)
    d.rounded_rectangle([x0, y0, x1, y1], radius=10 * s, fill=LCD)
    # LCD üst/alt bölge ayraçları
    d.line([x0 + 14 * s, 146 * s, x1 - 14 * s, 146 * s], fill=LCD_K, width=int(2 * s))
    d.line([x0 + 14 * s, 262 * s, x1 - 14 * s, 262 * s], fill=LCD_K, width=int(2 * s))
    # etiketler
    f = font("bahn", 15 * s)
    for t, x in (("ADIM", 112), ("NABIZ", 233), ("PIL %", 354)):
        d.text((x * s, 338 * s), t, font=f, fill=MUREKKEP, anchor="mm")
    d.text((233 * s, 124 * s), "GÜN · TARİH", font=font("bahn", 13 * s), fill=MUREKKEP, anchor="mm")
    # çerçeve üstünde "marka" tipi kabartma yazı
    d.text((233 * s, 40 * s), "RETRO · GT3", font=font("bahn", 18 * s), fill=TURUNCU_K, anchor="mm")
    d.text((233 * s, 428 * s), "QUARTZ", font=font("bahn", 16 * s), fill=TURUNCU_K, anchor="mm")
    img = down(big)
    for ad, (x, y) in ALT:
        yerlestir(img, simge(ad, MUREKKEP, 20), (x - 40, y))
    return img


def aod_arka_plan():
    img = Image.new("RGBA", (W, H), (0, 0, 0, 255))
    d = ImageDraw.Draw(img)
    x0, y0, x1, y1 = EKRAN
    d.rounded_rectangle([x0, y0, x1, y1], radius=10, outline=AOD_GRI, width=1)
    return img


def onizleme(aktif, saat, dk, sn, adim, nabiz, pil, gun, gunadi):
    base = Image.open(os.path.join(aktif, "00_arka_plan.png")).convert("RGBA")
    rz, rv = os.path.join(aktif, "seg_zaman"), os.path.join(aktif, "seg_veri")
    sayi_yaz(base, rz, f"{saat:02d}:{dk:02d}", POS_SAAT)
    yerlestir(base, gun_ac(os.path.join(aktif, "gun"), gunadi), POS_GUN)
    sayi_yaz(base, rv, f"{gun:02d}", POS_TARIH)
    if aktif == AKTIF:
        sayi_yaz(base, rv, str(adim), (ALT[0][1][0] + 22, ALT[0][1][1]))
        sayi_yaz(base, rv, str(nabiz), (ALT[1][1][0] + 14, ALT[1][1][1]))
        sayi_yaz(base, rv, str(pil), (ALT[2][1][0] + 14, ALT[2][1][1]))
    return base


def main():
    temizle(AKTIF, AOD)
    save(arka_plan(), AKTIF, "00_arka_plan.png")
    segment_seti(os.path.join(AKTIF, "seg_zaman"), 58, 92, MUREKKEP, HAYALET, kal=7)
    segment_seti(os.path.join(AKTIF, "seg_veri"), 20, 40, MUREKKEP, HAYALET, kal=3)
    gun_seti(os.path.join(AKTIF, "gun"), MUREKKEP, "bahn", 26, (70, 34))

    save(aod_arka_plan(), AOD, "00_arka_plan.png")
    segment_seti(os.path.join(AOD, "seg_zaman"), 58, 92, AOD_SEG, None, kal=7)
    segment_seti(os.path.join(AOD, "seg_veri"), 20, 40, AOD_SEG, None, kal=3)
    gun_seti(os.path.join(AOD, "gun"), AOD_GRI, "bahn", 26, (70, 34))

    onizleme(AKTIF, **ORNEK).save(os.path.join(ONIZ, f"{AD}_aktif.png"))
    onizleme(AKTIF, **ORNEK2).save(os.path.join(ONIZ, f"{AD}_aktif_2.png"))
    o = onizleme(AOD, **ORNEK); o.save(os.path.join(ONIZ, f"{AD}_aod.png"))
    rapor(AD, [o, onizleme(AOD, **ORNEK2)], KAT)


if __name__ == "__main__":
    main()
