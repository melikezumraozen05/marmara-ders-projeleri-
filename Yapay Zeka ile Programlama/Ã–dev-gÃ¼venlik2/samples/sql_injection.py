"""TEST VERİSİ - SQL Injection. Bu dosya analiz için okunur, çalıştırılmaz."""
import sqlite3


def kullanici_bul(kullanici_adi: str):
    conn = sqlite3.connect("kullanicilar.db")
    sorgu = "SELECT * FROM kullanicilar WHERE ad = '" + kullanici_adi + "'"
    return conn.execute(sorgu).fetchall()
