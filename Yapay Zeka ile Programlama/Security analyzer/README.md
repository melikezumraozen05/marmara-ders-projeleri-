# Security analyzer — Yapay Zekâ ile Kod Güvenlik Analizi

**Ders:** Yapay Zeka ile Programlama

Bu Python projesi, Gemini API yardımıyla örnek Python kodlarında statik güvenlik analizi yapar. Kod örnekleri çalıştırılmaz.

## Analiz edilen açıklar

1. SQL Injection — parametreleştirilmemiş SQL sorgusu.
2. Sabit Parola Kullanımı — kaynak kodda parola saklanması.
3. Komut Enjeksiyonu — kullanıcı girdisinin kabuk komutlarına eklenmesi.

Her analizde risk, nedeni, olası etkiler ve güvenli kod önerisi Türkçe raporlanır.

## Kurulum

Python 3.10+ gereklidir.

```powershell
py -m pip install -r requirements.txt
Copy-Item .env.example .env
```

`.env` dosyasındaki `GEMINI_API_KEY` alanına kendi anahtarınızı yazın. **Anahtarı GitHub'a yüklemeyin.** Modeli `GEMINI_MODEL` ile değiştirebilirsiniz.

```powershell
py security_analyzer.py
```

## Test kayıtları ve model notu

`test_ciktisi.txt` dosyasında üç teste ait başarıyla üretilmiş analizler yer alır. Çıktı başlığında “Gemini 3.8 Flash” yazmaktadır. Ancak testi çalıştıran Claude'un aktardığına göre başarılı analizler **gemini-3.5-flash** kullanılarak alınmıştır; `gemini-3.8-flash` denemelerinde 503 hatası görülmüştür. Başlık, çalıştırmada kullanılan modeli doğrulamaz.

Bu depo, yüklenen yerel Python dosyasında görülen gizli anahtar benzeri sabit değeri içermez. API anahtarı yalnızca `.env` üzerinden okunur. Yapay zekâ önerileri bağımsız güvenlik doğrulamasının yerine geçmez.
