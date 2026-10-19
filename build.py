# -*- coding: utf-8 -*-
"""
Huawei Watch GT 3 (466x466) klasik analog kadran — katman üretici.

Çalıştır:  python build.py
Çıktı:     katmanlar/aktif/*  katmanlar/aod/*  onizleme/*.png

Her şey bu dosyadan tekrar üretilir; PNG'leri elle düzenleme, burayı değiştir.
"""
import math
import os
import shutil
from PIL import Image, ImageDraw, ImageFont, ImageFilter

# ---------------------------------------------------------------- sabitler
W = H = 466
C = (W // 2, H // 2)          # (233, 233) — tüm ibrelerin dönme merkezi
FONT_DIR = r"C:\Windows\Fonts"
F_SERIF = os.path.join(FONT_DIR, "georgia.ttf")       # rakamlar (klasik)
F_SANS = os.path.join(FONT_DIR, "segoeuib.ttf")       # veri sayıları
F_SANS_R = os.path.join(FONT_DIR, "segoeui.ttf")      # gün/ay adları

OUT = os.path.dirname(os.path.abspath(__file__))
AKTIF = os.path.join(OUT, "katmanlar", "aktif")
AOD = os.path.join(OUT, "katmanlar", "aod")
ONIZ = os.path.join(OUT, "onizleme")

# Renkler
BG = (12, 14, 18, 255)
DIAL_C = (24, 28, 35, 255)
RING = (46, 52, 62, 255)
WHITE = (236, 236, 236, 255)
GOLD = (212, 168, 83, 255)
GRAY = (138, 143, 153, 255)
DIM = (70, 74, 82, 255)
RED = (200, 55, 45, 255)
AOD_W = (170, 170, 170, 255)
AOD_D = (95, 95, 95, 255)
TRANSP = (0, 0, 0, 0)

GUNLER = ["Paz", "Pzt", "Sal", "Çar", "Per", "Cum", "Cmt"]        # 0 = Pazar
AYLAR = ["Oca", "Şub", "Mar", "Nis", "May", "Haz",
         "Tem", "Ağu", "Eyl", "Eki", "Kas", "Ara"]

# Veri konumları (merkez noktaları)
POS_PIL = (233, 128)      # üst: pil
POS_ADIM = (128, 233)     # sol: adım
POS_NABIZ = (338, 233)    # sağ: nabız
POS_TARIH = (233, 330)    # alt: gün + tarih


def font(path, size):
    return ImageFont.truetype(path, size)


def new():
    return Image.new("RGBA", (W, H), TRANSP)


def polar(r, deg):
    """Saat 12 = 0°, saat yönü. Merkeze göre piksel koordinatı."""
    a = math.radians(deg - 90)
    return (C[0] + r * math.cos(a), C[1] + r * math.sin(a))


def save(img, folder, name):
    os.makedirs(folder, exist_ok=True)
    img.save(os.path.join(folder, name), optimize=True)


def ss(scale=4):
    """Süperörnekleme için büyük tuval."""
    return Image.new("RGBA", (W * scale, H * scale), TRANSP), scale


def down(img, scale):
    return img.resize((W, H), Image.LANCZOS)


# ---------------------------------------------------------------- arka plan
def arka_plan():
    img = Image.new("RGBA", (W, H), BG)
    # yumuşak radyal gradyan
    grad = Image.new("L", (W, H), 0)
    gd = ImageDraw.Draw(grad)
    for r in range(233, 0, -2):
        v = int(255 * (1 - r / 233) ** 1.6)
        gd.ellipse([C[0] - r, C[1] - r, C[0] + r, C[1] + r], fill=v)
    dial = Image.new("RGBA", (W, H), DIAL_C)
    img = Image.composite(dial, img, grad)

    big, s = ss()
    d = ImageDraw.Draw(big)
    cx, cy = C[0] * s, C[1] * s

    # dış halka
    d.ellipse([cx - 232 * s, cy - 232 * s, cx + 232 * s, cy + 232 * s],
              outline=RING, width=3 * s)
    d.ellipse([cx - 224 * s, cy - 224 * s, cx + 224 * s, cy + 224 * s],
              outline=(30, 34, 42, 255), width=1 * s)

    # dakika / saat çizgileri
    for i in range(60):
        deg = i * 6
        if i % 5 == 0:
            r0, r1, w, col = 200, 220, 4, WHITE
            if i % 15 == 0:
                col = GOLD
        else:
            r0, r1, w, col = 210, 220, 1.5, GRAY
        p0 = polar(r0, deg)
        p1 = polar(r1, deg)
        d.line([p0[0] * s, p0[1] * s, p1[0] * s, p1[1] * s],
               fill=col, width=int(w * s))

    # 12 / 3 / 6 / 9 rakamları (Georgia)
    f = font(F_SERIF, 46 * s)
    for n, deg in ((12, 0), (3, 90), (6, 180), (9, 270)):
        p = polar(178, deg)
        d.text((p[0] * s, p[1] * s), str(n), font=f, fill=GOLD, anchor="mm")

    # veri alanları için ince çerçeveli küçük "pencere" halkaları
    for p in (POS_ADIM, POS_NABIZ):
        r = 56
        d.ellipse([(p[0] - r) * s, (p[1] - r) * s, (p[0] + r) * s, (p[1] + r) * s],
                  outline=RING, width=2 * s)

    # tarih penceresi çizgisi
    x, y = POS_TARIH
    d.line([(x - 60) * s, (y - 24) * s, (x + 60) * s, (y - 24) * s], fill=RING, width=1 * s)
    d.line([(x - 60) * s, (y + 24) * s, (x + 60) * s, (y + 24) * s], fill=RING, width=1 * s)

    img.alpha_composite(down(big, s))
    return img


# ---------------------------------------------------------------- ibreler
def ibre(uzunluk, genislik, kuyruk, renk, orta=None, aod=False):
    """Saat 12'yi gösteren ibre; tuval 466x466, pivot (233,233)."""
    big, s = ss()
    d = ImageDraw.Draw(big)
    cx, cy = C[0] * s, C[1] * s
    L, Wd, T = uzunluk * s, genislik * s, kuyruk * s
    if aod:
        # ince dış çizgi, içi boş
        pts = [(cx - Wd / 2, cy + T), (cx - Wd / 2, cy - L + Wd),
               (cx, cy - L), (cx + Wd / 2, cy - L + Wd), (cx + Wd / 2, cy + T)]
        d.polygon(pts, outline=renk, width=int(1.6 * s))
    else:
        # sivri uçlu gövde
        pts = [(cx - Wd / 2, cy + T), (cx - Wd / 2, cy - L + Wd * 1.6),
               (cx, cy - L), (cx + Wd / 2, cy - L + Wd * 1.6), (cx + Wd / 2, cy + T)]
        d.polygon(pts, fill=renk)
        if orta:
            d.line([cx, cy - L + Wd * 2.2, cx, cy - 10 * s], fill=orta, width=int(Wd * 0.35))
    return down(big, s)


def saniye_ibresi():
    big, s = ss()
    d = ImageDraw.Draw(big)
    cx, cy = C[0] * s, C[1] * s
    d.line([cx, cy + 45 * s, cx, cy - 200 * s], fill=RED, width=int(2.4 * s))
    d.ellipse([cx - 7 * s, cy + 30 * s, cx + 7 * s, cy + 44 * s], fill=RED)
    return down(big, s)


def merkez_kapak(aod=False):
    big, s = ss()
    d = ImageDraw.Draw(big)
    cx, cy = C[0] * s, C[1] * s
    if aod:
        d.ellipse([cx - 5 * s, cy - 5 * s, cx + 5 * s, cy + 5 * s], outline=AOD_W, width=int(1.5 * s))
    else:
        d.ellipse([cx - 9 * s, cy - 9 * s, cx + 9 * s, cy + 9 * s], fill=GOLD)
        d.ellipse([cx - 3 * s, cy - 3 * s, cx + 3 * s, cy + 3 * s], fill=BG)
    return down(big, s)


# ---------------------------------------------------------------- simgeler
def simge_adim(col):
    big, s = ss()
    d = ImageDraw.Draw(big)
    # iki ayak izi (basit)
    for dx, dy in ((-7, 0), (7, -9)):
        x, y = (233 + dx) * s, (233 + dy) * s
        d.ellipse([x - 4 * s, y - 2 * s, x + 4 * s, y + 10 * s], fill=col)
        d.ellipse([x - 3.5 * s, y - 10 * s, x + 3.5 * s, y - 3 * s], fill=col)
    return crop_box(down(big, s), 40)


def simge_kalp(col):
    big, s = ss()
    d = ImageDraw.Draw(big)
    cx, cy = 233 * s, 233 * s
    r = 7 * s
    d.ellipse([cx - 2 * r, cy - r - 4 * s, cx, cy + r - 4 * s], fill=col)
    d.ellipse([cx, cy - r - 4 * s, cx + 2 * r, cy + r - 4 * s], fill=col)
    d.polygon([(cx - 2 * r + 1 * s, cy - 1 * s), (cx + 2 * r - 1 * s, cy - 1 * s),
               (cx, cy + 14 * s)], fill=col)
    return crop_box(down(big, s), 40)


def simge_pil(col):
    big, s = ss()
    d = ImageDraw.Draw(big)
    cx, cy = 233 * s, 233 * s
    d.rounded_rectangle([cx - 13 * s, cy - 7 * s, cx + 11 * s, cy + 7 * s],
                        radius=3 * s, outline=col, width=int(2 * s))
    d.rounded_rectangle([cx + 12 * s, cy - 3 * s, cx + 15 * s, cy + 3 * s], radius=1 * s, fill=col)
    d.rounded_rectangle([cx - 10 * s, cy - 4 * s, cx + 4 * s, cy + 4 * s], radius=1 * s, fill=col)
    return crop_box(down(big, s), 40)


def crop_box(img, size):
    """466 tuvalin ortasından size x size kare kırp (simge dosyaları için)."""
    x0, y0 = C[0] - size // 2, C[1] - size // 2
    return img.crop((x0, y0, x0 + size, y0 + size))


# ---------------------------------------------------------------- rakam / metin setleri
def rakam_seti(folder, col, size=27, bw=17):
    """0-9 eşit genişlikli PNG'ler (Theme Studio 'Image Number' için)."""
    f = font(F_SANS, size)
    for n in range(10):
        img = Image.new("RGBA", (bw, size + 6), TRANSP)
        d = ImageDraw.Draw(img)
        d.text((bw / 2, (size + 6) / 2), str(n), font=f, fill=col, anchor="mm")
        save(img, folder, f"{n}.png")
    # yüzde ve iki nokta işaretleri de gerekebilir
    for ch, name in ((":", "iki_nokta"), ("%", "yuzde")):
        img = Image.new("RGBA", (bw, size + 6), TRANSP)
        ImageDraw.Draw(img).text((bw / 2, (size + 6) / 2), ch, font=f, fill=col, anchor="mm")
        save(img, folder, f"{name}.png")


def tr_buyuk(t):
    return t.replace("i", "İ").replace("ı", "I").upper()


def metin_seti(folder, prefix, liste, col, size=24, box=(64, 32)):
    f = font(F_SANS_R, size)
    for i, t in enumerate(liste):
        img = Image.new("RGBA", box, TRANSP)
        ImageDraw.Draw(img).text((box[0] / 2, box[1] / 2), tr_buyuk(t), font=f, fill=col, anchor="mm")
        save(img, folder, f"{prefix}_{i:02d}_{t}.png")


# ---------------------------------------------------------------- pil yayı (11 kare)
def pil_yay(folder, yuzde, col_on, col_off):
    """Pil için 0..100 arası 11 kare; üstte 12 rakamının altında kısa yay."""
    big, s = ss()
    d = ImageDraw.Draw(big)
    r = 36
    box = [(POS_PIL[0] - r) * s, (POS_PIL[1] - r) * s, (POS_PIL[0] + r) * s, (POS_PIL[1] + r) * s]
    start, span = 135, 270           # alt kısım açık, 270° yay
    d.arc(box, start, start + span, fill=col_off, width=int(3 * s))
    if yuzde > 0:
        d.arc(box, start, start + span * yuzde / 100, fill=col_on, width=int(3 * s))
    img = down(big, s)
    save(img, folder, f"pil_yay_{yuzde:03d}.png")
    return img


# ---------------------------------------------------------------- önizleme birleştirme
def yerlestir(base, img, merkez):
    base.alpha_composite(img, (int(merkez[0] - img.width / 2), int(merkez[1] - img.height / 2)))


def sayi_yaz(base, folder, text, merkez):
    imgs = []
    for ch in text:
        name = {":": "iki_nokta", "%": "yuzde"}.get(ch, ch)
        imgs.append(Image.open(os.path.join(folder, f"{name}.png")).convert("RGBA"))
    total = sum(i.width for i in imgs)
    x = merkez[0] - total / 2
    for i in imgs:
        base.alpha_composite(i, (int(x), int(merkez[1] - i.height / 2)))
        x += i.width


def dondur(img, deg):
    return img.rotate(-deg, resample=Image.BICUBIC, center=C)


def onizleme_aktif(saat, dk, sn, adim, nabiz, pil, gun, ay, gunadi):
    base = Image.open(os.path.join(AKTIF, "00_arka_plan.png")).convert("RGBA")
    base.alpha_composite(Image.open(os.path.join(AKTIF, "pil", f"pil_yay_{round(pil/10)*10:03d}.png")))
    # simgeler
    yerlestir(base, Image.open(os.path.join(AKTIF, "simge_pil.png")), (POS_PIL[0], POS_PIL[1] - 16))
    yerlestir(base, Image.open(os.path.join(AKTIF, "simge_adim.png")), (POS_ADIM[0], POS_ADIM[1] - 22))
    yerlestir(base, Image.open(os.path.join(AKTIF, "simge_kalp.png")), (POS_NABIZ[0], POS_NABIZ[1] - 22))
    rk = os.path.join(AKTIF, "rakam")
    sayi_yaz(base, rk, f"{pil}%", (POS_PIL[0], POS_PIL[1] + 10))
    sayi_yaz(base, rk, str(adim), (POS_ADIM[0], POS_ADIM[1] + 14))
    sayi_yaz(base, rk, str(nabiz), (POS_NABIZ[0], POS_NABIZ[1] + 14))
    # tarih: GÜN  13 EKİ
    gimg = Image.open(os.path.join(AKTIF, "gun", f"gun_{gunadi:02d}_{GUNLER[gunadi]}.png"))
    aimg = Image.open(os.path.join(AKTIF, "ay", f"ay_{ay:02d}_{AYLAR[ay]}.png"))
    yerlestir(base, gimg, (POS_TARIH[0] - 48, POS_TARIH[1]))
    sayi_yaz(base, rk, f"{gun:02d}", (POS_TARIH[0] + 6, POS_TARIH[1]))
    yerlestir(base, aimg, (POS_TARIH[0] + 52, POS_TARIH[1]))
    # ibreler
    h_deg = (saat % 12) * 30 + dk * 0.5
    m_deg = dk * 6 + sn * 0.1
    s_deg = sn * 6
    base.alpha_composite(dondur(Image.open(os.path.join(AKTIF, "ibre_saat.png")), h_deg))
    base.alpha_composite(dondur(Image.open(os.path.join(AKTIF, "ibre_dakika.png")), m_deg))
    base.alpha_composite(dondur(Image.open(os.path.join(AKTIF, "ibre_saniye.png")), s_deg))
    base.alpha_composite(Image.open(os.path.join(AKTIF, "merkez_kapak.png")))
    return base


def onizleme_aod(saat, dk, gun, ay, gunadi):
    base = Image.open(os.path.join(AOD, "00_arka_plan.png")).convert("RGBA")
    rk = os.path.join(AOD, "rakam")
    gimg = Image.open(os.path.join(AOD, "gun", f"gun_{gunadi:02d}_{GUNLER[gunadi]}.png"))
    aimg = Image.open(os.path.join(AOD, "ay", f"ay_{ay:02d}_{AYLAR[ay]}.png"))
    yerlestir(base, gimg, (POS_TARIH[0] - 48, POS_TARIH[1]))
    sayi_yaz(base, rk, f"{gun:02d}", (POS_TARIH[0] + 6, POS_TARIH[1]))
    yerlestir(base, aimg, (POS_TARIH[0] + 52, POS_TARIH[1]))
    h_deg = (saat % 12) * 30 + dk * 0.5
    m_deg = dk * 6
    base.alpha_composite(dondur(Image.open(os.path.join(AOD, "ibre_saat.png")), h_deg))
    base.alpha_composite(dondur(Image.open(os.path.join(AOD, "ibre_dakika.png")), m_deg))
    base.alpha_composite(Image.open(os.path.join(AOD, "merkez_kapak.png")))
    return base


def yanan_oran(img, esik=8):
    """Siyah olmayan piksel oranı (AOD kuralı: <%10 ideal, >%20 ret)."""
    g = img.convert("RGB").convert("L").point(lambda v: 255 if v > esik else 0)
    return g.histogram()[255] / (W * H)


# ---------------------------------------------------------------- AOD arka planı
def aod_arka_plan():
    big, s = ss()
    d = ImageDraw.Draw(big)
    for i in range(12):
        deg = i * 30
        p0, p1 = polar(206, deg), polar(220, deg)
        col = AOD_W if i % 3 == 0 else AOD_D
        d.line([p0[0] * s, p0[1] * s, p1[0] * s, p1[1] * s], fill=col, width=int(2 * s))
    f = font(F_SERIF, 40 * s)
    for n, deg in ((12, 0), (3, 90), (6, 180), (9, 270)):
        p = polar(178, deg)
        d.text((p[0] * s, p[1] * s), str(n), font=f, fill=AOD_D, anchor="mm")
    img = Image.new("RGBA", (W, H), (0, 0, 0, 255))
    img.alpha_composite(down(big, s))
    return img


# ---------------------------------------------------------------- ana akış
def main():
    for p in (AKTIF, AOD, ONIZ):
        shutil.rmtree(p, ignore_errors=True)
        os.makedirs(p, exist_ok=True)

    # --- aktif katmanlar
    save(arka_plan(), AKTIF, "00_arka_plan.png")
    save(ibre(118, 11, 22, WHITE, orta=GOLD), AKTIF, "ibre_saat.png")
    save(ibre(172, 8, 26, WHITE, orta=GOLD), AKTIF, "ibre_dakika.png")
    save(saniye_ibresi(), AKTIF, "ibre_saniye.png")
    save(merkez_kapak(), AKTIF, "merkez_kapak.png")
    save(simge_adim(GOLD), AKTIF, "simge_adim.png")
    save(simge_kalp(RED), AKTIF, "simge_kalp.png")
    save(simge_pil(GOLD), AKTIF, "simge_pil.png")
    rakam_seti(os.path.join(AKTIF, "rakam"), WHITE)
    metin_seti(os.path.join(AKTIF, "gun"), "gun", GUNLER, GOLD)
    metin_seti(os.path.join(AKTIF, "ay"), "ay", AYLAR, GOLD)
    for y in range(0, 101, 10):
        pil_yay(os.path.join(AKTIF, "pil"), y, GOLD, RING)

    # --- AOD katmanları
    save(aod_arka_plan(), AOD, "00_arka_plan.png")
    save(ibre(118, 11, 22, AOD_W, aod=True), AOD, "ibre_saat.png")
    save(ibre(172, 8, 26, AOD_W, aod=True), AOD, "ibre_dakika.png")
    save(merkez_kapak(aod=True), AOD, "merkez_kapak.png")
    rakam_seti(os.path.join(AOD, "rakam"), AOD_D)
    metin_seti(os.path.join(AOD, "gun"), "gun", GUNLER, AOD_D)
    metin_seti(os.path.join(AOD, "ay"), "ay", AYLAR, AOD_D)

    # --- önizlemeler
    ornek = dict(gun=19, ay=9, gunadi=1)            # 19 Eki, Pazartesi
    a1 = onizleme_aktif(10, 9, 36, adim=6482, nabiz=72, pil=85, **ornek)
    a1.save(os.path.join(ONIZ, "aktif_10_09.png"))
    a2 = onizleme_aktif(16, 42, 12, adim=11205, nabiz=118, pil=40, **ornek)
    a2.save(os.path.join(ONIZ, "aktif_16_42.png"))
    aod1 = onizleme_aod(10, 9, **ornek)
    aod1.save(os.path.join(ONIZ, "aod_10_09.png"))
    # Theme Studio küçük kapak görseli (kadran listesinde görünen) için 466 kare yeterli;
    # yan yana karşılaştırma:
    yan = Image.new("RGBA", (W * 3 + 40, H), (30, 30, 30, 255))
    yan.alpha_composite(a1, (0, 0)); yan.alpha_composite(a2, (W + 20, 0)); yan.alpha_composite(aod1, (2 * W + 40, 0))
    yan.save(os.path.join(ONIZ, "yan_yana.png"))

    # --- AOD piksel oranı (en kötü durum: ibreler 10:09 + tarih)
    en_kotu = max(yanan_oran(onizleme_aod(h, m, **ornek)) for h, m in ((10, 9), (6, 30), (12, 0), (3, 45)))
    print(f"AOD yanan piksel oranı (en kötü örnek): %{en_kotu*100:.2f}  (hedef <%10, sınır %20)")
    # boyut kontrolü
    en_buyuk = max((os.path.getsize(os.path.join(r, f)), os.path.join(r, f))
                   for r, _, fs in os.walk(os.path.join(OUT, "katmanlar")) for f in fs)
    print(f"En büyük katman: {en_buyuk[0]/1024:.0f} KB  {os.path.relpath(en_buyuk[1], OUT)}  (sınır 750 KB)")
    print("Tamam: katmanlar/ ve onizleme/ üretildi.")


if __name__ == "__main__":
    main()
