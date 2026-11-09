"""TEST VERİSİ - Yalnızca güvenli ve basit Python kodu."""
import json
from pathlib import Path


def kullanici_ayarlarini_oku(config_path: Path) -> dict:
    """Yalnızca JSON veri okur; eval veya pickle kullanmaz."""
    with config_path.open("r", encoding="utf-8") as file:
        data = json.load(file)
    if not isinstance(data, dict):
        raise ValueError("Ayarlar JSON nesnesi olmalı")
    return data


def pozitif_sayilarin_toplami(sayilar: list[int]) -> int:
    return sum(sayi for sayi in sayilar if isinstance(sayi, int) and sayi > 0)
