import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai import errors, types

SISTEM_MESAJI = """
Sen kıdemli bir Yazılım Mimarı ve Performans Uzmanısın.

Kullanıcının gönderdiği kötü yazılmış Python kodunu iyileştir.

1. Değişken isimlerini anlamlı hale getir.
2. Gereksiz döngüleri kaldır, mümkünse O(n) çözüm kullan.
3. Type hint ekle. Girdi bir tam sayı listesidir.
4. Mevcut işlevselliği ve sonuç sırasını koru:
   Tekrarlanan sayıları yalnızca bir kez,
   listedeki ilk görünme sıralarına göre döndür.
5. Yalnızca düzeltilmiş Python kodunu ver.
   Markdown veya ek açıklama yazma.
"""


def kod_optimize_et(spagetti_kod: str) -> None:
    klasor = Path(__file__).resolve().parent
    load_dotenv(klasor / ".env", encoding="utf-8-sig")

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        print("API anahtarı bulunamadı. .env dosyasını kontrol et.")
        return

    print("=" * 60)
    print("YAPAY ZEKA DESTEKLİ KOD İYİLEŞTİRME VE OPTİMİZASYON")
    print("=" * 60)

    print("\n[AŞAMA 1] OPTİMİZE EDİLECEK KOD:")
    print(spagetti_kod)
    print("\n[AŞAMA 2] YAPAY ZEKAYA BAĞLANILIYOR...\n")

    try:
        with genai.Client(api_key=api_key) as client:
            response = client.models.generate_content(
                model="gemini-3.8-flash",
                contents=spagetti_kod,
                config=types.GenerateContentConfig(
                    system_instruction=SISTEM_MESAJI,
                    temperature=0.2,
                ),
            )

        temiz_kod = response.text

        if not temiz_kod:
            print("Model boş yanıt döndürdü.")
            return

        print("[AŞAMA 3] İYİLEŞTİRİLMİŞ KOD:\n")
        print(temiz_kod)

    except errors.APIError as hata:
        print(f"API hatası: {hata}")


kotu_kod = """
def bul(l):
    r = []
    for i in range(len(l)):
        for j in range(i + 1, len(l)):
            if l[i] == l[j] and l[i] not in r:
                r.append(l[i])
    return r
"""


if __name__ == "__main__":
    kod_optimize_et(kotu_kod) 