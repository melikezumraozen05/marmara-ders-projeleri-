"""TEST VERİSİ - Kaynak koda gömülü örnek parola. Gerçek sır içermez."""

DB_PASSWORD = "ORNEK_GERCEK_OLMAYAN_PAROLA_123"


def baglanti_bilgileri():
    return {"sunucu": "localhost", "parola": DB_PASSWORD}
