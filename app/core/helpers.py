def formatar_data(valor: date) -> str:
    return valor.isoformat()

def parse_data(texto: str) -> date:
    return date.fromisoformat(texto)

def parse_float(texto: str, default: float | None = None) -> float | None:
    if not texto or not texto.strip():
        return default
    try:
        return float(texto.strip().replace(",", "."))
    except ValueError:
        return None

def proximo_id(lista: list) -> int:
    if not lista:
        return 1
    return max(item["id"] for item in lista) + 1

def obter_por_id(lista: list, id_valor: int) -> dict | None:
    return next((item for item in lista if item["id"] == id_valor), None)