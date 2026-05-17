def livro_esta_emprestado(livro_id: int, dados: dict) -> int:
    return sum(
        1 for emprestimo in dados["emprestimos"]
        if emprestimo["livro_id"] == livro_id and emprestimo["status"] in [STATUS_ABERTO, STATUS_ATRASADO]
    )
    
def obter_livro_por_atributos(titulo: str, autor: str, prateleira_id: int, exclude_id: int | None = None) -> dict | None:
        titulo = titulo.strip().lower()
        autor = autor.strip().lower()
        return next(
            (
                l for l in dados["livros"]
                if l["id"] != exclude_id and
                   l["titulo"].strip().lower() == titulo and
                   l["autor"].strip().lower() == autor and
                   l["prateleira_id"] == prateleira_id
            ),
            None,
        )
