"""Yapay Zeka Destekli SQL Laboratuvari: Gemini, SQLite ve guvenlik testleri."""
import os
import random
import re
import sqlite3
import time
from datetime import datetime
from pathlib import Path

MODEL = os.getenv("GEMINI_MODEL", "gemini-3.6-flash")
RAPOR = Path(__file__).with_name("sql_asistan_raporu.txt")
SEHIRLER = ["İstanbul", "Ankara", "İzmir", "Bursa", "Antalya"]
YASAK = re.compile(r"\b(DROP|DELETE|UPDATE|INSERT|ALTER|CREATE|REPLACE|TRUNCATE|ATTACH|DETACH|PRAGMA|VACUUM)\b", re.I)
SISTEM = """SQLite veritabaninda yalnizca tek SELECT sorgusu uret.
Tablolar: musteriler(musteri_id, ad_soyad, sehir),
siparisler(siparis_id, musteri_id, tutar, tarih).
Sadece bu tablo ve sutunlari kullan. Aciklama ve markdown yazma."""


def veritabanini_olustur():
    rastgele = random.Random(2026)
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE musteriler (musteri_id INTEGER PRIMARY KEY, ad_soyad TEXT, sehir TEXT)")
    conn.execute("CREATE TABLE siparisler (siparis_id INTEGER PRIMARY KEY, musteri_id INTEGER, tutar REAL, tarih TEXT)")
    adlar = ["Ayşe", "Ece", "Elif", "Deniz", "Can", "Ahmet", "Zeynep", "Mehmet"]
    soyadlar = ["Yılmaz", "Kaya", "Demir", "Aydın", "Çelik", "Şahin", "Koç", "Arslan"]
    musteriler = [(i, f"{rastgele.choice(adlar)} {rastgele.choice(soyadlar)}", rastgele.choice(SEHIRLER)) for i in range(1, 1001)]
    siparisler = [(i, rastgele.randint(1, 1000), round(rastgele.uniform(100, 10000), 2), "2026-01-01") for i in range(1, 1001)]
    conn.executemany("INSERT INTO musteriler VALUES (?, ?, ?)", musteriler)
    conn.executemany("INSERT INTO siparisler VALUES (?, ?, ?, ?)", siparisler)
    conn.commit()
    # SQL metni kontrolune ek olarak veritabanini salt okunur yap.
    izinli = {sqlite3.SQLITE_SELECT, sqlite3.SQLITE_READ, sqlite3.SQLITE_FUNCTION}
    conn.set_authorizer(lambda islem, a, b, db, kaynak:
                        sqlite3.SQLITE_OK if islem in izinli else sqlite3.SQLITE_DENY)
    return conn


def clean_sql(metin):
    metin = (metin or "").strip()
    kod = re.fullmatch(r"```(?:sql|sqlite)?\s*\n?(.*?)\s*```", metin, flags=re.I | re.S)
    return (kod.group(1) if kod else metin).strip()


def guvenlik_kontrolu(sql):
    sql = sql.strip()
    if not re.match(r"^SELECT\b", sql, re.I):
        print("[GÜVENLİK ENGELİ] Yalnızca SELECT sorgularına izin veriliyor.")
        return False
    if YASAK.search(sql) or ";" in sql or "--" in sql or "/*" in sql or "*/" in sql:
        print("[GÜVENLİK ENGELİ] Yasaklı komut, yorum veya çoklu sorgu algılandı.")
        return False
    return True


def gemini_uret(client, talep, onceki_sql=None, hata=None):
    mesaj = SISTEM + "\nKullanıcı isteği: " + talep
    if hata:
        mesaj += f"\nÖnceki sorgu: {onceki_sql}\nSQLite hatası: {hata}\nHatalı sorguyu düzelt; sadece SELECT yaz."
    cevap = client.models.generate_content(model=MODEL, contents=mesaj)
    return clean_sql(cevap.text)


def rapor_yaz(kayitlar):
    satirlar = [
        "AKILLI SQL ASİSTANI PERFORMANS VE GÜVENLİK RAPORU",
        "-" * 52,
        "Çalıştırma Tarihi : " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Veritabanı Hacmi : 1.000 Müşteri / 1.000 Sipariş",
        "Toplam Test Talebi : " + str(len(kayitlar)),
        "Başarılı İcra : " + str(sum(k["durum"] == "BAŞARILI" for k in kayitlar)),
        "Engellenen Saldırı : " + str(sum(k["durum"] == "ENGELLENDİ" for k in kayitlar)),
        "Hata Düzeltme Sayısı : " + str(sum(k["duzeltildi"] for k in kayitlar)),
        "", "TEST DETAYLARI:"
    ]
    for i, k in enumerate(kayitlar, 1):
        satirlar.append(
            f"[TEST {i}] {k['talep']} | {k['durum']} | Deneme: {k['deneme']} | "
            f"Toplam süre: {k['toplam']:.4f} sn | SQL: {k['sql']} | Not: {k['not']}"
        )
    satirlar.extend(["", "DEĞERLENDİRME:",
                     "Toplam süre API isteğini ve SQLite yürütmesini kapsar.",
                     "Sadece bu oturumdaki gerçek sonuçlar raporlanır."])
    RAPOR.write_text("\n".join(satirlar) + "\n", encoding="utf-8")


def sql_asistani_calistir(conn, client, talep, kayitlar):
    import pandas as pd
    baslangic = time.perf_counter()
    onceki_sql, hata = None, None
    kayit = dict(talep=talep, durum="HATA", deneme=0, toplam=0.0,
                 sql="", duzeltildi=False, notlar="")
    for deneme in range(1, 4):
        kayit["deneme"] = deneme
        sql = ""
        try:
            print(f"[GEMINI] Sorgu üretiliyor ({deneme}/3)...")
            sql = gemini_uret(client, talep, onceki_sql, hata)
            kayit["sql"] = sql
            print("[SQL]", sql)
            if not guvenlik_kontrolu(sql):
                kayit["durum"] = "ENGELLENDİ"
                kayit["notlar"] = "Güvenlik filtresi"
                break
            baslangic_sql = time.perf_counter()
            imlec = conn.execute(sql)
            tablo = pd.DataFrame(imlec.fetchall(), columns=[c[0] for c in imlec.description])
            sql_suresi = time.perf_counter() - baslangic_sql
            print(f"[SONUÇ] SQL süresi: {sql_suresi:.5f} saniye")
            print(tablo.head(30).to_string(index=False))
            if len(tablo) > 30:
                print(f"... toplam {len(tablo)} satır (ilk 30 gösterildi)")
            kayit["durum"] = "BAŞARILI"
            kayit["duzeltildi"] = deneme > 1
            kayit["notlar"] = f"{len(tablo)} satır, SQL süresi {sql_suresi:.5f} sn"
            break
        except sqlite3.Error as exc:
            hata = str(exc)
            onceki_sql = sql
            kayit["notlar"] = hata
            print("[SQL HATASI]", hata)
            if deneme < 3:
                print("[SELF-CORRECTION] Hata Gemini'ye geri gönderilecek.")
        except Exception as exc:
            kayit["notlar"] = f"API/sistem hatası: {exc}"
            print("[SİSTEM HATASI]", exc)
            break
    kayit["toplam"] = time.perf_counter() - baslangic
    kayit["not"] = kayit.pop("notlar")
    print(f"[TOPLAM SÜRE] {kayit['toplam']:.4f} saniye | {kayit['durum']}")
    kayitlar.append(kayit)
    rapor_yaz(kayitlar)
    return kayit


def main():
    anahtar = os.getenv("GEMINI_API_KEY")
    if not anahtar:
        print("[HATA] GEMINI_API_KEY ortam değişkeni ayarlanmalı.")
        return
    try:
        from google import genai
        client = genai.Client(api_key=anahtar)
        import pandas  # gerekli kutuphaneyi erken kontrol et
    except ImportError:
        print("[HATA] python -m pip install google-genai pandas")
        return
    conn = veritabanini_olustur()
    kayitlar = []
    print("[BİLGİ] 1.000 müşteri ve 1.000 sipariş yüklendi.")
    try:
        while True:
            talep = input("\nSoru girin (çıkış: q): ").strip()
            if talep.lower() == "q":
                break
            if talep:
                sql_asistani_calistir(conn, client, talep, kayitlar)
    except (KeyboardInterrupt, EOFError):
        print("\nProgram sonlandırıldı.")
    finally:
        conn.close()
        rapor_yaz(kayitlar)
        print("[BİLGİ] Rapor kaydedildi:", RAPOR)


if __name__ == "__main__":
    main()
