# -*- coding: utf-8 -*-
"""Tüm tasarımları üretir ve yan yana karşılaştırma görseli çıkarır.  python tasarimlar/hepsi.py"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw
import ortak
import dijital_minimal, spor_halka, retro_lcd, geometrik

for m in (dijital_minimal, spor_halka, retro_lcd, geometrik):
    m.main()

ONIZ = os.path.join(ortak.KOK, "onizleme")
adlar = ["aktif_yesil_10_09", "mercan_aktif", "halka_aktif", "retro_aktif", "prizma_aktif"]
aodlar = ["aod_10_09", "mercan_aod", "halka_aod", "retro_aod", "prizma_aod"]
h = 240
sheet = Image.new("RGB", (h * 5 + 60, h * 2 + 30), (28, 28, 30))
for i, (a, o) in enumerate(zip(adlar, aodlar)):
    for row, n in ((0, a), (1, o)):
        im = Image.open(os.path.join(ONIZ, n + ".png")).convert("RGB").resize((h - 10, h - 10), Image.LANCZOS)
        sheet.paste(im, (10 + i * (h + 10), 10 + row * (h + 10)))
sheet.save(os.path.join(ONIZ, "tum_tasarimlar.png"))
print("onizleme/tum_tasarimlar.png yazıldı")
