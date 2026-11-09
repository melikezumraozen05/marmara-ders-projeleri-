"""TEST VERİSİ - Güvensiz serileştirme. Güvenilmeyen baytları açar."""
import pickle


def istek_govdesini_coz(request_body: bytes):
    # request_body: dış istemciden gelen, doğrulanmamış HTTP isteği gövdesi.
    return pickle.loads(request_body)
