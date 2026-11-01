# Derin Öğrenme — Regresyon Probleminde Ağ Metaparametreleri (Tek Ödev)

Bu proje, hocanın **tahtaya yazdığı aktivasyon fonksiyonları konusu** ile gönderilen **Ödev 1.docx** yönergesini **tek bir çalışma** olarak ele alır. Önceden tamamlanmış `ikili_siniflandirici.py` ödeviyle **aynı ödev değildir**.

## Ödevin resmi şartları

- Keras ile **1 girişli, 1 çıkışlı regresyon modeli**.
- Temel ağ: **1 gizli katmanda 2 ReLU nöron**, çıktı katmanında **1 lineer nöron**.
- Her model **300 epoch**.
- Rastgelelik tohumu = okul numarasının son **iki** hanesi = **21**.
- Giriş: **-2 ≤ p ≤ 2**.
- Aktivasyon: Lineer, Sigmoid, Hiperbolik Tanjant, ReLU, LeakyReLU, ELU, SiLU.
- Öğrenme hızı: **0.1 / 0.01 / 0.001**.
- Optimize edici: **SGD / RMSProp / ADAM**.
- Ağırlık başlatma: **normal / uniform**.
- Gizli katman: **1 / 2 / 5 / 10 / 20**.
- Gizli nöron sayısı: **2 / 5 / 10 / 20 / 50**.
- MSE, RMSE, R² ve süre tabloları; yalnızca iyi sonuç veren ayarlara ait grafikler.

**UYARI — Belgede bir yazım belirsizliği var.** Resmî DOCX belgesinde hedef `y = 1 + sin(pi * y / 4)` olarak belirtiliyor. Bu ifade çıktı `y`'yi tekrar kullandığından giriş `p`'ye bağlı hedef fonksiyonunu tanımlamıyor. Fotoğraftaki regresyon ifadesi, `-2 ≤ p ≤ 2` girişi ve örnek hedef eğrisi doğrultusunda **`y(p) = 1 + sin(pi * p / 4)` varsayıldı**. Bu, hoca tarafından **teyit edilmelidir**; belge sessizce değiştirilmedi.

## Çalıştırma

Python 3.11+:

```bash
pip install -r requirements.txt
python 821_regresyon.py
```

Keras 3, TensorFlow olmadan PyTorch backend ile çalışır. Script her modeli ayrı süreçte çalıştırır; dolayısıyla yavaş bilgisayarda ilk çalıştırma sürebilir. Kesilen deneyler tekrar çalıştırılmadan devam ettirilir; sıfırdan hesaplamak için `python 821_regresyon.py --rebuild`.

Script sonunda oluşturulur:
- `sonuclar/821_karsilastirmalar.csv`: Altı deney grubu, toplam 25 model.
- `sonuclar/821_ozet.json`: Gruplardaki en iyi modeller.
- `grafikler/`: En başarılı model için epoch/MSE (log), epoch/R², hedef-çıkış ve farklı epoch anları.
- `.xlsx` dosyası: Deney tabloları, sıralamalar ve grafik (ayrı hazırlanmış çalışma kitabı).
- `.docx` dosyası: **Doldurulabilir rapor taslağı**; sonuçların yorum bölümleri öğrenci tarafından yazılmalı.

## Karşılaştırma kuralı

Bir seferde yalnızca **tek parametre değiştirilir**, diğerleri hocanın örnek tablosundaki değerlerde (ReLU, SGD, LR 0.1, normal dağılım, tek gizli katman, iki nöron) tutulur. Bu yüzden bazı deneylerin parametreleri birbiriyle çakışır; tabloda özellikle korunmuştur. Böylece hoca istediği altı karşılaştırma ayrı ayrı görülebilir.

**Ölçüm sınırı:** Resmî yönergede ayrılmış test verisi veya test başarımı istenmiyor. Verilerin tamamıyla eğitim yapılıp aynı gridde MSE/RMSE/R² ölçülüyor; bunlar genelleme testi olarak yorumlanmamalı. MSE küçük, R² büyük oldukça örnekleme noktalarına uyum iyileşir. Sayısal kararsızlık oluşursa ilgili satır durum sütununda açıklanır.

## Rapor kullanım kuralı

Öğretmen yönergesinde, **yapay zekânın kod için kullanılabileceği fakat rapor ile yorumların bizzat öğrenci tarafından yazılması gerektiği** açıkça belirtilmiş. Bu nedenle rapor dosyası bir **taslak**tır; yorum bölümleri doldurulmadan teslim edilmemelidir. Grafikleri ve deney sonuçlarını gözlemleyerek kendi cümlelerini yazmalısın.

## Teslim

Yönergede belirtilen son tarih: **1 Kasım 2026**. Dosyanın ilk sayfasındaki tarih ayrı bir hazırlama tarihi olabilir. Teslim takvimi için BYS ve hocanın güncel duyurusu belirleyici olur.

## Kaynak

- `Ödev 1.docx` (öğretmenin yüklediği belge)
- Dersteki tahtanın fotoğrafı (aktivasyon fonksiyonları)
- https://keras.io/api/layers/activations/
- https://keras.io/api/optimizers/