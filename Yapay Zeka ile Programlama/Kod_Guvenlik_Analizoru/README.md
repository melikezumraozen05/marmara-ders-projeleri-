# Gemini 3.8 Flash - Kod Güvenlik Analizörü

**Ders:** Yapay Zeka ile Programlama  
**Konu:** Yapay Zeka Destekli Statik Kod Güvenlik Analizi (SAST)

Bu proje Google Gemini 3.8 Flash modelini kullanarak üç örnek Python kodunu **çalıştırmadan** analiz eder. Yanıtlar Türkçedir.

## Testler

1. SQL Injection: Parametreleştirilmemiş sorgu.
2. Sabit Parola Kullanımı: Kaynak koda yazılmış parola.
3. Komut Enjeksiyonu: Kullanıcı girdisinin kabuk komutuna eklenmesi.

## Windows kurulum

Python 3.10 veya üzeri gerekir.

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

[Google AI Studio](https://aistudio.google.com/apikey) üzerinden alınan API anahtarını .env içindeki GEMINI_API_KEY karşısına yazın. **.env dosyasını GitHub'a yüklemeyin.**

## Çalıştırma

```powershell
python security_analyzer.py
```

Her test için güvenlik açığı, nedenleri, etkileri ve güvenli örnek kod önerisi gösterilir. Üç API isteği sorunsuz yanıtlanırsa son satırda `TÜM GÜVENLİK TESTLERİ TAMAMLANDI` görünür.

**Not:** Bu bir eğitim örneğidir. Güvenlik açığı içeren örnekler gerçek sistemlerde kullanılmamalıdır. Gemini analizi güvenlik garantisi değildir. API anahtarı, ağ erişimi ve kullanılabilir kota olmadan canlı analiz yapılamaz.
