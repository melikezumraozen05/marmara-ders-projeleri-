# Kod Güvenlik Analizörü — Seviye 2

**Ders:** Yapay Zeka ile Programlama  
**Temel:** Daha önceki `Security analyzer/security_analyzer.py` uygulamasının geliştirilmiş sürümü.  
**Model:** Gemini 3.8 Flash (`gemini-3.8-flash`), istenirse `GEMINI_MODEL` ile değiştirilebilir.

Bu uygulama, kullanıcının seçtiği Python dosyasını **çalıştırmadan** UTF-8 metin olarak okur, Gemini API ile statik güvenlik değerlendirmesi yapar ve doğrulanmış JSON yanıtını rapora dönüştürür. Modelin değerlendirmesi bir güvenlik uzmanı incelemesinin yerini tutmaz.

## 1. PDF'deki maddelere göre yapılanlar

| İstenen görev | Uygulamadaki karşılığı |
|---|---|
| `--file` ile dosya analizi | `argparse`, `read_python_file()` |
| Dosya, `.py`, UTF-8, boş içerik denetimi | `read_python_file()`; hatada **Gemini çağrısı yapılmaz** |
| Var olan 3 zafiyeti koruma | `samples/sql_injection.py`, `hardcoded_password.py`, `command_injection.py` |
| 2 yeni zafiyet | `samples/path_traversal.py`, `unsafe_deserialization.py` |
| Güvenli Python testi | `samples/safe_code.py` |
| Yalnızca JSON model yanıtı | `response_mime_type="application/json"` ve `json.loads()` |
| Zorunlu bulgu alanları | `type`, `severity`, `evidence`, `cause`, `impact`, `secure_code` |
| Risk özeti | Kritik, Yüksek, Orta, Düşük sayıları |
| Raporlama | `reports/analysis.json`; UTF-8; klasör otomatik oluşturulur |
| Hata kontrolü | API, eksik dosya, boş dosya, bozuk UTF-8, geçersiz JSON, eksik alan |
| Eski üç test | `py security_analyzer.py` |
| Altı test | `py security_analyzer.py --all` (her biri ayrıca `reports/<test>.json` olarak arşivlenir) |

## 2. Windows / PowerShell kurulum

1. ZIP dosyasını çıkarın. VS Code'da `Kod_Guvenlik_Analizoru_Seviye_2` klasörünü açın.
2. **Terminal > New Terminal** ile PowerShell terminalini açın ve aşağıdaki komutları sırayla çalıştırın:

```powershell
py -m pip install -r requirements.txt
Copy-Item .env.example .env
notepad .env
```

Not Defteri'nde `.env` dosyasının `GEMINI_API_KEY` satırına **kendi API anahtarınızı** girip kaydedin. Paylaşırken `.env` dosyasını **asla** ZIP'e veya GitHub'a koymayın. `GEMINI_MODEL=gemini-3.8-flash` varsayılandır. Kişisel kotanız veya model erişiminiz bunu desteklemiyorsa erişebildiğiniz modeli `.env` içinde seçebilirsiniz.

## 3. Çalıştırma

**Yeni: Tek dosya analiz etme**

```powershell
py security_analyzer.py --file samples/path_traversal.py
py security_analyzer.py --file samples/unsafe_deserialization.py
py security_analyzer.py --file samples/safe_code.py
```

**Eski üç senaryoyu çalıştırma (geriye dönük uyum):**

```powershell
py security_analyzer.py
```

**Altı senaryoyu analiz etme:**

```powershell
py security_analyzer.py --all
```

Her başarılı analiz `reports/analysis.json` dosyasını günceller. `--all` ve parametresiz çoklu çalıştırma, ayrıca her test için `reports/<test_adi>.json` kaydeder. Her çağrı yalnızca **tek bir** kaynak dosyayı modele iletir. Hatalı yanıt için yeni başarılı rapor yazılmaz; önceden oluşturulmuş bir rapor varsa olduğu gibi kalır.

## 4. Rapor yapısı

```json
{
  "file": "samples/path_traversal.py",
  "finding_count": 1,
  "findings": [
    {
      "type": "Path Traversal",
      "severity": "Yüksek",
      "evidence": "target = base_dir / filename",
      "cause": "Kullanıcı girdisi ile oluşan yol güvenli kök dizin içinde doğrulanmıyor.",
      "impact": "Üst dizinlerdeki dosyalar yetkisiz okunabilir.",
      "secure_code": "resolve() ve is_relative_to() ile dizin sınırını doğrula."
    }
  ],
  "risk_summary": {"Kritik": 0, "Yüksek": 1, "Orta": 0, "Düşük": 0}
}
```

**Önemli:** ZIP'in içindeki hazır `reports/analysis.json` yalnızca **örnek/çevrimdışı test raporudur**, gerçek Gemini analizinin sonucu değildir. Gerçek sonuç için yukarıdaki `--file` komutunu API anahtarınızla çalıştırın.

## 5. Çevrimdışı otomatik testler

Bu testler **API anahtarı veya internet olmadan** uygulamanın dosya okuma, JSON denetleme ve raporlama işlemlerini sınar. Gemini'nin gerçek doğruluk performansını kanıtlamaz.

```powershell
py -m unittest discover -s tests -v
```

Testler: altı senaryo, geçersiz uzantı, bulunamayan dosya, klasör yolu, boş dosya, bozuk UTF-8, okunamayan dosya, API hatası, geçersiz JSON, eksik JSON alanları, geçersiz risk seviyesi ve kaynak kodun çalıştırılmaması.

## 6. Beklenen inceleme ve yanlış pozitif notları

| Dosya | Beklenen model bulgusu | Kodda görülmesi gereken yer | Güvenli yaklaşım |
|---|---|---|---|
| `sql_injection.py` | SQL Injection | `conn.execute(sorgu)` ve `kullanici_adi` birleştirmesi | SQL parametreleri (`?`) |
| `hardcoded_password.py` | Sabit Parola | `DB_PASSWORD = ...` | Gizli bilgiyi ortam değişkeni / secrets manager'dan al |
| `command_injection.py` | Komut enjeksiyonu | `os.system("ls " + klasor_adi)` | `shell=False` ile argüman listesi, girdiyi doğrulama |
| `path_traversal.py` | Path Traversal | `target = base_dir / filename` | `resolve()` + `is_relative_to()` ile izinli dizinde kaldığını doğrulama |
| `unsafe_deserialization.py` | Güvensiz serileştirme | `pickle.loads(request_body)` | Güvenilmeyen veri için JSON ve şema doğrulaması |
| `safe_code.py` | **0 bulgu** | İşlevlerde riskli örüntü yok | Mevcut güvenli kullanım korunur |

Modelin **gerçek** yanıtları alındığında `safe_code.py` üzerinde yanlış pozitif olup olmadığına ayrıca bakın. Bu tabloda listelenen sonuçlar **beklentidir**; API testlerinin gerçekleştirildiğini iddia etmez. Analizör `import`, `exec`, `eval` veya kaynak kod için `subprocess` çalıştırmaz.

## 7. Hata durumları

- Dosya yok: `HATA: Dosya bulunamadı`.
- Dosya boş: `HATA: Dosya boş`.
- Dosya UTF-8 değil: `HATA: Dosya UTF-8 olarak okunamadı`.
- API erişilemez: kısa Türkçe API hata açıklaması.
- Yanıt JSON değil veya zorunlu alan eksik: hata döner; **o yanıttan rapor oluşturulmaz**.

**Teslim:** `security_analyzer.py`, `requirements.txt`, `samples/` içindeki altı `.py` örneği ve `reports/analysis.json`. İsteğe bağlı `README.md` ve `tests/` değerlendirmeyi kolaylaştırır.
