import re

from core.constants import STATUS_ABERTO, STATUS_ATRASADO

def cliente_existe(dados, nome, email, telefone, exclude_id=None) -> bool:
        nome = nome.strip().lower()
        email = email.strip().lower()
        telefone = telefone.strip()
        return any(
            c["id"] != exclude_id and (
                c["nome"].strip().lower() == nome or
                c["email"].strip().lower() == email or
                c["telefone"].strip() == telefone
            )
            for c in dados["clientes"]
        )

def cliente_tem_emprestimos_ativos(cliente_id: int, dados: dict) -> bool:
    return any(
        emprestimo["cliente_id"] == cliente_id and emprestimo["status"] in [STATUS_ABERTO, STATUS_ATRASADO]
        for emprestimo in dados["emprestimos"]
    )
    
def email_valido(email: str) -> bool:
    padrao = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(padrao, email.strip()) is not None


def telefone_valido(telefone: str) -> str | None:
    apenas_numeros = re.sub(r"\D", "", telefone)

    tamanho = len(apenas_numeros)

    if tamanho == 10:
        return f"({apenas_numeros[:2]}) {apenas_numeros[2:6]}-{apenas_numeros[6:]}"
    
    elif tamanho == 11:
        return f"({apenas_numeros[:2]}) {apenas_numeros[2]} {apenas_numeros[3:7]}-{apenas_numeros[7:]}"
    
    return None
