"""TEST VERİSİ - Komut enjeksiyonu. Bu dosya çalıştırılmamalıdır."""
import os


def dosya_listele(klasor_adi: str):
    os.system("ls " + klasor_adi)
