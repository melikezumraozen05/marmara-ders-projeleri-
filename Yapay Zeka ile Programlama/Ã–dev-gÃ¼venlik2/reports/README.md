# Raporların kaynağı

`analysis.json` dosyası, `samples/path_traversal.py` üzerinde **sahte/örnek Gemini JSON yanıtı kullanılarak** uygulamanın rapor üretim fonksiyonuyla oluşturulmuş teslim biçimi örneğidir. Gerçek Gemini API analizi değildir.

Gerçek değerlendirme için proje kökündeki `.env` dosyasına kendi `GEMINI_API_KEY` değerinizi girin ve şunu çalıştırın:

```powershell
py security_analyzer.py --file samples/path_traversal.py
```

Bu komut başarılıysa `reports/analysis.json` gerçek model yanıtıyla yeniden oluşturulur.
