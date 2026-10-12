# Gemini API ile Akıllı E-Ticaret Ürün ve Stok Yönetim Sistemi

**Ders:** Yapay Zeka ile Programlama — Ödev 2  
**Öğrenci:** Melike Zümra Özen

Kullanıcının girdiği ürün açıklamasından Gemini API ile ürün adı, kategori, üç SEO etiketi ve iki cümlelik satış açıklaması üreten Python konsol uygulamasıdır. Fiyat ve stok kullanıcıdan alınır. Ürünler `urunler.json` dosyasında kalıcı olarak saklanır.

## Kurulum ve çalıştırma (Windows)

1. Python kurulu olmalıdır (3.10 veya üzeri).
2. Bu dosyaların bulunduğu klasörü açın. Klasörün boş bir yerine Shift + sağ tıklayıp terminali/PowerShell'i açın.
3. Gerekli paketi kurun:

```powershell
py -m pip install -r requirements.txt
```

4. [Google AI Studio](https://aistudio.google.com/apikey) üzerinden kendi Gemini API anahtarınızı alın. Aynı PowerShell penceresinde aşağıdaki örnekteki yazıyı kendi anahtarınızla değiştirin:

```powershell
$env:GEMINI_API_KEY="BURAYA_KENDI_API_ANAHTARINIZ"
py main.py
```

`py` komutu bulunamazsa komutlarda `python` kullanın. Anahtar terminal oturumu kapanınca yeniden ayarlanmalıdır. Anahtarı kod dosyalarına veya GitHub'a eklemeyin.

Varsayılan model `gemini-3.5-flash-lite` olarak ayarlanmıştır. Hesabınızda başka model kullanmanız gerekiyorsa çalıştırmadan önce:

```powershell
$env:GEMINI_MODEL="HESABINIZDA_KULLANILABILEN_MODEL_ADI"
```

Mac/Linux için `python3` komutunu, anahtar ayarlamak için `export GEMINI_API_KEY="anahtarınız"` kullanın.

## Menü ve örnek kullanım

- **1 — Yeni Ürün Ekle:** Açıklama, fiyat ve stok ister; Gemini yanıtını doğruladıktan sonra kaydeder.
- **2 — Ürünleri Listele:** Kayıtları ve stok uyarılarını gösterir.
- **3 — Ürün Ara:** Ad veya kodun bir kısmını girerek büyük/küçük harf duyarsız arama yapar.
- **4 — Stok Güncelle:** Ürün kodunu ve yeni stok miktarını alır, dosyaya kaydeder.
- **5 — Çıkış:** Uygulamayı kapatır.

Örneğin `1` seçip açıklamaya `Mavi 50 litre su geçirmez kamp çantası`, fiyata `2499`, stoğa `3` yazın. İlk ürün `URN-0001` koduyla kaydedilir ve `KRİTİK STOK` uyarısı gösterilir. `3` seçerek `kamp` aratın. `4` seçip `URN-0001` ürününün stoğunu `15` yapın. Uygulamayı kapatıp açınca kayıt korunur. Gemini'nin oluşturduğu ürün adı değişebilir.

## Dosyalar

| Dosya | Görevi |
| --- | --- |
| main.py | Menü, Gemini bağlantısı, kayıt, arama ve stok işlemleri |
| urunler.json | Ürün kayıtları; başlangıçta boş JSON listesi |
| requirements.txt | Gerekli Python paketi |
| .gitignore | Geçici dosyaları ve yerel gizli ayar dosyasını Git dışında bırakır |
| README.md | Kurulum ve açıklamalar |

## Kodun kısa açıklaması

`e_ticaret_api_simulasyonu()` gerçek Gemini API çağrısı yapar ve doğrulanmış bir Python sözlüğü döndürür. Fonksiyon adı ödev yönergesine uygundur. Önceki dersin kaynak kodu sağlanmadığı için bağlantı Google GenAI SDK ile yeniden oluşturulmuştur.

`analiz_dogrula()` zorunlu metin alanlarını, üç etiketi ve iki cümleyi denetler. Cümle sayımı basit noktalama kuralına dayanır; modelden kısaltmasız kısa cümleler istenir. `urunleri_oku()` kayıtları yükler. `urunleri_kaydet()` önce geçici dosyaya yazıp başarılı olduğunda asıl dosyayı değiştirir. Yeni ürün kodu, mevcut en büyük numaranın bir fazlasıdır. `sayi_al()` negatif ve geçersiz sayıları reddeder; stok tam sayı olmalıdır.

Stok sıfırsa `STOKTA YOK`, 1–4 arasındaysa `KRİTİK STOK` gösterilir. Bozuk JSON dosyası otomatik olarak silinmez veya üzerine yazılmaz; kullanıcı dosyayı düzeltene kadar kayıt işlemleri durdurulur, menü çalışmaya devam eder. Boş dosya boş liste kabul edilir. API hatası veya eksik yanıt durumunda ürün kaydedilmez. Listeleme, arama ve stok güncelleme için API anahtarı gerekmez.

## Doğrulama

Kayıt, yeniden okuma, kod üretimi, arama, stok güncelleme, hatalı sayılar, bozuk JSON ve eksik API yanıtı yerel olarak kontrol edilmiştir. Ürün ekleme akışı sahte API yanıtıyla denenmiştir. Kullanıcının bilgisayarında gerçek Gemini API ile ürün ekleme başarıyla denenmiştir (gemini-3.5-flash-lite). URN-0001 kodlu ürün, fiyat 2499 TL ve stok 3 ile kaydedilmiş; kritik stok uyarısı gösterilmiştir.

Tek kullanıcıyla aynı anda tek uygulama çalıştırılması için hazırlanmıştır.

## Teknik kaynak

Gemini bağlantısı için Google'ın resmi SDK dokümantasyonu: https://googleapis.github.io/python-genai/
