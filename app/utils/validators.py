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

def prateleira_existe(nome: str, exclude_id: int | None = None) -> bool:
        nome = nome.strip().lower()

        return any(
            p["id"] != exclude_id and
            p["nome"].strip().lower() == nome
            for p in dados["prateleiras"]
        )
