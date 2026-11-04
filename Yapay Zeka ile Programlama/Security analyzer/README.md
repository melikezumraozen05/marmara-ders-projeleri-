# Security analyzer — Kod Güvenlik Analizörü

**Ders:** Yapay Zeka ile Programlama

## Proje hakkında
Python kodlarında aşağıdaki üç güvenlik açığını yapay zekâ ile analiz etme ödevi:

1. SQL Injection
2. Sabit Parola Kullanımı (Hardcoded Credentials)
3. Komut Enjeksiyonu (OS Command Injection)

Analiz raporunda açığın tanımı, nedeni, olası etkileri ve güvenli kod önerisi bulunur.

## Test sonuçları hakkında
Üç test için başarılı analiz çıktıları kullanıcı tarafından VS Code ekran görüntüleriyle doğrulandı. Claude'un aktardığı bilgiye göre bu **başarılı analizler `gemini-3.5-flash`** ile alınmıştır. `gemini-3.8-flash` denemelerinde 503 hatası görülmüştür; 3.8 başlığı gerçek kullanılan modeli kanıtlamaz.

## Dosyalar
Güncellenmiş `security_analyzer.py`, gerçek `test_ciktisi.txt`, görseller ve video, yerel proje sürümünden teslim klasörüne aktarılacaktır.

## Güvenlik
Gerçek API anahtarını içeren `.env` dosyası ve diğer gizli bilgiler **GitHub'a yüklenmez**.
