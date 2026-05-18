def view_home(dados):
        total_clientes = len(dados["clientes"])
        total_prateleiras = len(dados["prateleiras"])
        total_livros = len(dados["livros"])
        total_emprestimos = len(dados["emprestimos"])
        total_abertos = sum(1 for e in dados["emprestimos"] if e["status"] == "Aberto")
        total_atrasados = sum(1 for e in dados["emprestimos"] if e["status"] == "Atrasado")
        total_multas = sum(1 for m in dados["multas"] if m["status"] == "Pendente")

        cards = ft.Row(
            [
                criar_card("Clientes", ft.Text(str(total_clientes), size=24, weight="bold")),
                criar_card("Prateleiras", ft.Text(str(total_prateleiras), size=24, weight="bold")),
                criar_card("Livros", ft.Text(str(total_livros), size=24, weight="bold")),
                criar_card("Em aberto", ft.Text(str(total_abertos), size=24, weight="bold")),
                criar_card("Atrasados", ft.Text(str(total_atrasados), size=24, weight="bold")),
                criar_card("Multas", ft.Text(str(total_multas), size=24, weight="bold")),
            ],
            wrap=True,
            spacing=16,
        )
        return ft.ListView([cards], expand=True, padding=20, spacing=20)
