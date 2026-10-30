# WatchFaceGT3 — Huawei Watch GT 3 için "Gün-Tarih" stili klasik analog kadran

Güneş ışını (sunburst) kadran, yivli altın çerçeve, altın baton ibreler, 12'de **M** monogramı, 3'te tarih penceresi, alt yarıda adım / nabız / pil. Kadran rengi altı seçenek: **siyah, sarı, mavi, yeşil, kırmızı, beyaz**. Sade bir AOD (sürekli açık ekran) varyantı vardır. Tüm katmanlar `build.py` ile üretilir; PNG'ler elle düzenlenmez. Marka logosu veya yazısı yoktur.

| Aktif (yeşil) | Renkler + AOD |
|---|---|
| ![aktif](onizleme/aktif_yesil_10_09.png) | ![renkler](onizleme/renkler_ve_aod.png) |

## Teknik sınırlar (GT 3, HarmonyOS 4 lite)

- Çözünürlük **466 × 466** (46 mm ve 42 mm modellerin ikisi de).
- Kadran paket sürümü **2.1.z** zorunlu ("WATCH + GT series" modu).
- Metin kontrolünde yalnız sistem fontları (Roboto) var; bu yüzden rakamlar ve M logosu **PNG** olarak üretildi.
- AOD'de siyah olmayan piksel oranı **%10 altı ideal, %20 üstü reddedilir**. Bu tasarımda en kötü durumda **≈%4**. `build.py` çalışınca oranı yazdırır.
- Tek görsel ≤ 750 KB (en büyük katman ≈ 210 KB, sarı arka plan).
- Dokunma kısayolları yalnız saatin yerleşik uygulamalarını açabilir.

## Üretim

Gereksinim: Python 3 + Pillow + NumPy (`pip install pillow numpy`). Fontlar Windows'tan okunur (Georgia, Segoe UI).

```bash
python build.py
```

Çıktı:

```
katmanlar/aktif/
  00_arka_plan_{siyah,sari,mavi,yesil,kirmizi,beyaz}.png   kadran + çerçeve + indeksler + pencereler
  ibre_saat.png  ibre_dakika.png  ibre_saniye.png  merkez_kapak.png   (466x466, pivot 233,233, saat 12)
  simge_{adim,kalp,pil}_altin.png   koyu kadranlar için (24x24)
  simge_{adim,kalp,pil}_koyu.png    sarı/beyaz kadran için
  rakam_veri_altin/  rakam_veri_koyu/   0-9 + yuzde + iki_nokta  (13x28)
  rakam_tarih/       0-9 siyah (15x32) — tarih penceresi
  logo_m.png         M monogramı (72x72; arka plana zaten işlenmiş, ayrı katman istenirse)
katmanlar/aod/
  00_arka_plan.png  ibre_saat.png  ibre_dakika.png  merkez_kapak.png  rakam_tarih/
onizleme/
  aktif_yesil_10_09.png  aod_10_09.png  renkler_ve_aod.png
```

Renkler `KADRAN` sözlüğünde (merkez, kenar) olarak; konumlar `POS_LOGO`, `POS_TARIH`, `VERI_X/VERI_Y` sabitlerinde. Değiştir → tekrar çalıştır.

## Theme Studio'da birleştirme (.hwt üretimi)

Resmi araç: **Huawei Theme Studio 11.x** (Windows/macOS), <https://developer.huawei.com/consumer/en/doc/development/Tools-Guides/theme-studio-0000001075536553>. Eski "Watch Face Designer" adı artık kullanılmıyor.

Koordinatlar aşağıda **merkez** olarak verilir; Theme Studio sol-üst köşe ister, merkezden genişlik/2 ve yükseklik/2 çıkar.

1. **New Project → Watch Face**. Device: *WATCH + GT series*, Resolution **466 × 466**, Version **2.1.z**. Proje adı: WatchFaceGT3.
2. **Arka plan (renk seçimi)**: `Background` kontrolüne `00_arka_plan_yesil.png` yükle. Kullanıcının saatte rengi değiştirebilmesi için Theme Studio'nun **Style (stil değiştirme)** özelliğini kullan: arka plan kontrolünde *Style* ekle, her stile bir renk dosyasını ata (6 stil). Saatte kadrana uzun basınca *Stil* seçeneğinden renk değişir. Not: sarı ve beyaz stillerde veri simgeleri/rakamları için `_koyu` setini, diğerlerinde `_altin` setini aynı stil gruplarına bağla (simgeler ve veri sayıları da *Style*'a dahil edilir).
3. **M logosu**: arka plan PNG'lerine işlenmiştir, ayrıca katman gerekmez. (Değiştirmek istersen `logo_m.png` 72 × 72, merkez (233,118).)
4. **Tarih**: `Image Number` kontrolü, `rakam_tarih/0-9`, veri *Day*, iki hane, hizalama *center*, merkez **(372,233)**.
5. **Veri satırı** (y = 318): `Image` + `Image Number` (`rakam_veri_altin/`, hizalama center):
   - Adım: simge `simge_adim_*.png` merkez (110,318); sayı veri *Steps*, merkez (146,318). 5 haneye kadar sığar.
   - Nabız: simge `simge_kalp_*.png` (209,318); sayı veri *Heart rate*, merkez (239,318).
   - Pil: simge `simge_pil_*.png` (302,318); sayı veri *Battery*, merkez (334,318), son ek `yuzde.png`.
6. **İbreler**: `Pointer` kontrolleri. Üç ibre PNG'si tam tuval (466 × 466), **saat 12'yi gösterir**, dönme merkezi **(233,233)**. `ibre_saat.png` (Hour), `ibre_dakika.png` (Minute), `ibre_saniye.png` (Second). En üste `merkez_kapak.png` `Image` olarak (0,0).
7. **AOD**: Sol panelde *AOD* sekmesine geç; `katmanlar/aod/` dosyalarıyla arka plan, tarih, saat ve dakika ibresi, merkez kapağı ekle (saniye ibresi ve veri satırı **yok**). Theme Studio'nun "AOD pixel ratio" uyarısı çıkmamalı (ölçüm ≈%4).
8. **Kapak görseli**: `onizleme/aktif_yesil_10_09.png`.
9. **Build → Export** ile `.hwt` dosyasını üret.

### Saate önizleme göndermek

1. Telefonda **Huawei Health** açık, saat bağlı olsun.
2. Theme Studio'da **Preview on device**: telefon ve bilgisayar aynı Wi-Fi ağında olmalı; Theme Studio'nun gösterdiği QR kodu Huawei Health ile tarat. Kadran geçici olarak saate yüklenir.
3. Resmi olmayan yükleme yolları (modlu Health APK, Gadgetbridge) lisans ve güvenlik riski taşır; bu projede kullanılmadı.

### Huawei Temalar'a yayınlama

1. Huawei ID ile <https://developer.huawei.com> → **Theme** hizmetine kayıt; kimlik doğrulaması (*Qualification application*) gerekir.
2. **Merchant Service** kaydı ve *Publisher Agreement* onayı (ücretli kadran için).
3. Theme Studio'da **Publish** → ad (Türkçe + İngilizce), açıklama, kapak görseli, fiyat (ücretsiz veya kademe; 3+ veri türü için en az Tier 4 isteniyor).
4. Durum *Pending Review* olur; inceleme süresi resmi olarak açıklanmıyor.
5. Onaylanınca Huawei Health → Kadranlar → Daha fazla'da görünür.

## Dosya yapısı

```
build.py        tüm katmanları ve önizlemeleri üreten script
katmanlar/      üretilen PNG katmanları (aktif + aod)
onizleme/       birleştirilmiş örnek görüntüler
README.md       bu dosya
```

## Diğer tasarımlar (tasarimlar/)

Huawei tasarımcı başvurusu için birbirinden farklı beş kadran gerekir. Klasik kadrana ek olarak dört tasarım daha `tasarimlar/` altında, hepsi beş veri türü (adım, nabız, pil, tarih, haftanın günü) ve AOD ile:

| Ad | Script | Stil | Katman klasörü |
|---|---|---|---|
| Klasik (M) | `build.py` | Sunburst analog, yivli altın çerçeve, 6 renk | `katmanlar/` |
| Mercan | `tasarimlar/dijital_minimal.py` | Lacivert + mercan daire, dev dijital rakamlar | `katmanlar_mercan/` |
| Halka | `tasarimlar/spor_halka.py` | Üç ilerleme halkası (adım/nabız/pil), spor | `katmanlar_halka/` |
| Retro | `tasarimlar/retro_lcd.py` | Turuncu çerçeve, yeşil LCD, yedi parçalı rakam | `katmanlar_retro/` |
| Prizma | `tasarimlar/geometrik.py` | Dört renkli dilim, koyu disk, beyaz ibreler | `katmanlar_prizma/` |
| Gece | `tasarimlar/gece.py` | Mat siyah, gümüş baton, dauphine ibre, 6'da küçük saniye | `katmanlar_gece/` |
| Porselen | `tasarimlar/porselen.py` | Beyaz emaye, Roma rakamları, demiryolu ray, mavi çelik yaprak ibre | `katmanlar_porselen/` |
| Giyoş | `tasarimlar/giyos.py` | Siyah giyoş doku, rose gold, kronograf tipi alt kadranlar (adım, pil) | `katmanlar_giyos/` |
| Zarif | `tasarimlar/zarif_dijital.py` | İnce serif dijital saat, şampanya hairline çizgiler | `katmanlar_zarif/` |

**Siyah ceket / siyah gömlek için set (klasik giyim):** Klasik (siyah varyant), Gece, Porselen, Giyoş, Zarif → karşılaştırma `onizleme/klasik_tasarimlar.png`. Renkli set (Mercan, Halka, Retro, Prizma) → `onizleme/tum_tasarimlar.png`.

Hepsini üretmek için:

```bash
python tasarimlar/hepsi.py
```

Çıktı `onizleme/<ad>_aktif.png`, `<ad>_aod.png` ve karşılaştırma `onizleme/tum_tasarimlar.png`. Ortak yardımcılar `tasarimlar/ortak.py` içinde (rakam setleri, gün adı setleri, ilerleme yayı kareleri, yedi parçalı rakam, simgeler, AOD oranı).

Theme Studio'da kullanım, klasik kadranla aynı mantıkta:

- `00_arka_plan.png` → Background.
- `rakam_zaman/` → saat ve dakika için iki ayrı Image Number kontrolü (Mercan: alt alta; Halka, Retro: `iki_nokta.png` ile yan yana). Retro'da `seg_zaman/`, `seg_veri/`.
- `rakam_veri/` → adım (Steps), nabız (Heart rate), pil (Battery, son ek `yuzde.png`), gün numarası (Day).
- `gun/` → Image Sequence, veri Week day, 0 = Pazar.
- `halka/<ad>_000..100.png` (Halka) ve `alt_ibre/<ad>_000..100.png` (Giyoş) → Progress / Image Sequence, 11 kare; adım hedefi 10 000, nabız 180 bpm = tam, pil %.
- `ibre_kucuk_saniye.png` (Gece) → Pointer, veri Second, pivot **(233,322)** (küçük saniye alt kadranının merkezi).
- `ibre_*.png`, `merkez_kapak.png` (Prizma) → Pointer kontrolleri, pivot (233,233).
- Konumlar her scriptin başındaki `POS_*` sabitlerinde merkez koordinatı olarak yazılıdır.

### Başvuru notu

İlk tasarımcı başvurusu (21 Ekim 2026) reddedildi: tek kadranın renk varyantları "benzer tasarımlar" sayıldı ve en az beş farklı, özgün tasarım istendi. Yeni başvuru paketi `tanitim/` altında üretilir (yalnız JPG/PNG/MP4, klasörsüz zip, ≤50 dosya, ≤50 MB).
