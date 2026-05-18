def prateleira_existe(dados, exclude_id=None) -> bool:
        nome = nome.strip().lower()

        return any(
            p["id"] != exclude_id and
            p["nome"].strip().lower() == nome
            for p in dados["prateleiras"]
        )

def prateleira_tem_livros(prateleira_id: int, dados: dict) -> bool:
    return any(livro["prateleira_id"] == prateleira_id for livro in dados["livros"])