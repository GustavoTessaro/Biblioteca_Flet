_indice_rotas = ["/", "/clientes", "/livros", "/emprestimos", "/multas", "/prateleiras"]

def navigation_bar_mobile():
        rota_atual = estado["rota"]
        idx = _indice_rotas.index(rota_atual) if rota_atual in _indice_rotas else 0

        def ao_mudar(e):
            navegar(_indice_rotas[e.control.selected_index])

        return ft.NavigationBar(
            selected_index=idx,
            on_change=ao_mudar,
            destinations=[
                ft.NavigationBarDestination(icon=ft.Icons.HOME_OUTLINED, selected_icon=ft.Icons.HOME, label="Home"),
                ft.NavigationBarDestination(icon=ft.Icons.PERSON_OUTLINE, selected_icon=ft.Icons.PERSON, label="Clientes"),
                ft.NavigationBarDestination(icon=ft.Icons.BOOK_OUTLINED, selected_icon=ft.Icons.BOOK, label="Livros"),
                ft.NavigationBarDestination(icon=ft.Icons.UNDO_OUTLINED, selected_icon=ft.Icons.UNDO, label="Empréstimos"),
                ft.NavigationBarDestination(icon=ft.Icons.MONETIZATION_ON_OUTLINED, selected_icon=ft.Icons.MONETIZATION_ON, label="Multas"),
            ],
        )
