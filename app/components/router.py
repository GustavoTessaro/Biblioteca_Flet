def route_change(e=None):
        p = paleta(estado["dark_mode"])
        
        if e is not None and hasattr(e, "route"):
            estado["rota"] = e.route

        atualizar_dropdowns()

        views_map = {
            "/": view_home,
            "/clientes": view_clientes,
            "/prateleiras": view_prateleiras,
            "/livros": view_livros,
            "/emprestimos": view_emprestimos,
            "/multas": view_multas
        }
        
        view_fn = views_map.get(estado["rota"], view_home)

        # ── CONFIGURAÇÃO DE LAYOUT RESPONSIVO ────────────────────────────────
        # Se for mobile, removemos o menu do topo para não duplicar a navegação
        if estado["mobile"]:
            # Layout Mobile (sem menu na tela, usa navigation_bar inferior nativa)
            conteudo_principal = ft.Container(
                content=view_fn(),
                padding=ft.Padding(20, 10, 20, 10),
                expand=True
            )
        else:
            # Layout Computador (Menu lateral à esquerda + Conteúdo à direita)
            conteudo_principal = ft.Row([
                menu_lateral(),  # ── PAINEL ESQUERDO FIXO
                ft.Container(
                    content=view_fn(),
                    padding=ft.Padding(20, 20, 20, 20),
                    expand=True  # Ocupa o resto do espaço da tela horizontalmente
                )
            ], spacing=0, expand=True)


        # Atualiza a pilha de visualização aplicando a barra inferior condicionalmente
        page.views.clear()
        page.views.append(
            ft.View(
                route=estado["rota"],
                appbar=construir_appbar(),
                controls=[conteudo_principal],
                # Se for mobile, injeta a NavigationBar na propriedade nativa da View
                navigation_bar=navigation_bar_mobile() if estado["mobile"] else None,
                padding=0,
                spacing=0
            )
        )
        page.update()
