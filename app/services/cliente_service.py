def cliente_existe(nome: str, email: str, telefone: str, exclude_id: int | None = None) -> bool:
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
