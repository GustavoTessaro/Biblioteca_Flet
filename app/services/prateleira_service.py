def prateleira_existe(nome: str, exclude_id: int | None = None) -> bool:
        nome = nome.strip().lower()

        return any(
            p["id"] != exclude_id and
            p["nome"].strip().lower() == nome
            for p in dados["prateleiras"]
        )
