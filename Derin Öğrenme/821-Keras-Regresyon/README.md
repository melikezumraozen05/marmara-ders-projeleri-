# 821 | Keras ile Regresyon Problemlerinde Hiperparametre Analizi

**Ders:** Derin Öğrenme

**Konu:** Keras ile regresyon problemlerinde yapay sinir ağı hiperparametrelerinin ağ performansına etkisinin incelenmesi.

Son üç hanesi **821** olan öğrenci numarasından hareketle 821 rastgele tohumu kullanılarak Keras 3 ile **20 gerçek deney** yapılmıştır. Scikit-learn diabetes regresyon veri kümesindeki 442 gözlem 282 eğitim, 71 doğrulama ve 89 test olarak ayrılmıştır.

## Karşılaştırmalar
- Gizli katman aktivasyonları: **linear, sigmoid, tanh, ReLU**
- Optimizasyonlar: **SGD, Adam, RMSprop**
- Nöron sayısı: **8, 32, 64**
- Gizli katman: **1 ve 2**
- Batch size: **16, 32, 64**
- Öğrenme hızı: **0,001 / 0,005 / 0,01**
- Maksimum epoch: **60 ve 120**
- Çıktı katmanı: Sürekli hedef için her modelde **linear**

## Çalıştırma

Python 3.11+ ortamında:

    pip install -r requirements.txt
    python 821_regresyon.py

Kısa kontrol için: `python 821_regresyon.py --quick`.

Keras 3, **PyTorch backend** kullanır. Kod, bağımsız TensorFlow kurulumu gerektirmez.

## Ölçülen bulgular

| Ölçüt | Ölçülen değer |
|---|---:|
| Deney sayısı | 20 |
| En iyi doğrulama deneyi | V01 / ReLU + Adam / 8 nöron |
| Doğrulama MAE | **43,06** |
| Test MAE | **42,44** |
| Test RMSE | **51,41** |
| Test R² | **0,523** |

Ölçümler **gerçektir**; `sonuclar/821_deney_sonuclari.csv` dosyası tüm 20 deneyi barındırır. Test kümesi hiperparametre seçiminde kullanılmadı, yalnızca seçilen model test edildi.

**Sınırlılık:** Sonuçlar tek veri bölünmesi ve tek tohum içindir; genel model üstünlüğü sonucuna varılmamalıdır.

ChatGPT içinde ayrıca biçimlendirilmiş Word raporu ve grafikli Excel çalışma kitabı hazırlanmıştır. Bunların ikili (.docx/.xlsx) sürümleri bu GitHub dizinine ayrıca yüklenmelidir.

**Kaynaklar:** [Keras aktivasyon API](https://keras.io/api/layers/activations/), [Keras optimizer API](https://keras.io/api/optimizers/), [scikit-learn diabetes verisi](https://scikit-learn.org/stable/modules/generated/sklearn.datasets.load_diabetes.html).

Hocanın ayrıntılı Drive yönergesine erişilmediği için gönderim öncesi resmi görev metniyle karşılaştırma yapılmalıdır.
