"""TEST VERİSİ - Path Traversal. Kullanıcının verdiği dosya adı denetlenmiyor."""
from pathlib import Path


def kullanici_dosyasi_oku(filename: str) -> str:
    base_dir = Path("uploads")
    # Kullanıcı '../../.env' gibi bir ad verebilir; dizin sınırı denetlenmiyor.
    target = base_dir / filename
    with open(target, "r", encoding="utf-8") as file:
        return file.read()
