def prateleira_existe(dados,) -> bool:
        nome = nome.strip().lower()

        return any(
            p["id"] != exclude_id and
            p["nome"].strip().lower() == nome
            for p in dados["prateleiras"]
        )
