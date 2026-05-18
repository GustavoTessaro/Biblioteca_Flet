import json
import os

from core.constants import DATA_FILE


def carregar_dados() -> dict:
    if not os.path.exists(DATA_FILE):
        return {
            "clientes": [],
            "prateleiras": [],
            "livros": [],
            "emprestimos": [],
            "multas": [],
        }

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)
    except Exception:
        return {
            #Verificar Depois se o JSON estiver corrompido perde os dados silenciosamente. 
            "clientes": [],
            "prateleiras": [],
            "livros": [],
            "emprestimos": [],
            "multas": [],
        }

def salvar_dados(dados: dict):
    with open(DATA_FILE, "w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, indent=2, ensure_ascii=False)

async def salvar_e_atualizar(page, dados, route_change, msg: str = None):

        salvar_dados(dados)

        verificar_atrasos_e_multas(dados)

        atualizar_dropdowns()

        if msg:
            await mostrar_snack(msg)

        route_change()