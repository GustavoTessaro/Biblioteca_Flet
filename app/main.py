import flet as ft

# =========================
# CORES
# =========================

from core.constants import *
from core.helpers import *
from core.theme import paleta

# =========================
# DATA
# =========================

from data.storage import carregar_dados, salvar_dados

# =========================
# SERVICES
# =========================

from services.cliente_service import cliente_existe, cliente_tem_emprestimos_ativos
from services.emprestimo_service import verificar_atrasos_e_multas, obter_status_emprestimo
from services.livro_service import livro_esta_emprestado, obter_livro_por_atributos
from services.multa_service import calcular_valor_multa
from services.prateleira_service import prateleira_existe

# =========================
# COMPONENTS
# =========================

from components.appbar import construir_appbar
from components.buttons import (criar_botao_primario,criar_botao_secundario)
from components.cards import criar_card
from components.menu import menu_lateral
from components.navigation import navigation_bar_mobile

# =========================
# VIEWS
# =========================

from views.home_view import view_home
from views.clientes_view import view_clientes
from views.prateleiras_view import view_prateleiras
from views.livros_view import view_livros
from views.emprestimos_view import view_emprestimos
from views.multas_view import view_multas


def main(page: ft.Page):

    # =========================
    # PAGE CONFIG
    # =========================

    page.title = "Biblioteca Flet"

    page.padding = 0
    page.spacing = 0

    page.window_maximized = True

    page.theme = ft.Theme(color_scheme_seed=ft.Colors.BLUE)

    page.dark_theme = ft.Theme(color_scheme_seed=ft.Colors.INDIGO)

    page.theme_mode = ft.ThemeMode.LIGHT

    # =========================
    # DATA
    # =========================

    dados = carregar_dados()

    verificar_atrasos_e_multas(dados)

    # =========================
    # APP STATE
    # =========================

    estado = {
        "rota": "/",
        "cliente_edit_id": None,
        "prateleira_edit_id": None,
        "livro_edit_id": None,
        "mobile": page.width < BREAKPOINT_MOBILE,
        "dark_mode": False,
    }

    # =========================
    # ROUTES
    # =========================

    titulos_paginas = {
        "/": "Início - Painel Geral",
        "/clientes": "Gerenciar Clientes",
        "/prateleiras": "Gerenciar Prateleiras",
        "/livros": "Catálogo de Livros",
        "/emprestimos": "Controle de Empréstimos",
        "/multas": "Histórico de Multas"
    }

    rotas_menu = [
        ("/", "Home", ft.Icons.HOME_OUTLINED, ft.Icons.HOME),
        ("/clientes", "Clientes", ft.Icons.PERSON_OUTLINE, ft.Icons.PERSON),
        ("/prateleiras", "Prateleiras", ft.Icons.TABLE_ROWS_OUTLINED, ft.Icons.TABLE_ROWS),
        ("/livros", "Livros", ft.Icons.BOOK_OUTLINED, ft.Icons.BOOK),
        ("/emprestimos", "Empréstimos", ft.Icons.UNDO_OUTLINED, ft.Icons.UNDO),
        ("/multas", "Multas", ft.Icons.MONETIZATION_ON_OUTLINED, ft.Icons.MONETIZATION_ON),
    ]

    # =========================
    # NAVIGATION
    # =========================

    def navegar(rota: str):
        page.go(rota)

    # =========================
    # ROUTER
    # =========================

    def route_change(e=None):

        if e and hasattr(e, "route"):
            estado["rota"] = e.route

        views_map = {
            "/": lambda: view_home(dados),
            "/clientes": lambda: view_clientes(
                page,
                dados,
                estado,
                route_change
            ),
            "/prateleiras": lambda: view_prateleiras(
                page,
                dados,
                estado,
                route_change
            ),
            "/livros": lambda: view_livros(
                page,
                dados,
                estado,
                route_change
            ),
            "/emprestimos": lambda: view_emprestimos(
                page,
                dados,
                estado,
                route_change,
                navegar
            ),
            "/multas": lambda: view_multas(
                page,
                dados,
                estado,
                route_change
            ),
        }

        view_fn = views_map.get(estado["rota"], lambda: view_home(dados))

        # =========================
        # MOBILE
        # =========================

        if estado["mobile"]:

            conteudo_principal = ft.Container(
                content=view_fn(),
                padding=ft.Padding(20, 10, 20, 10),
                expand=True
            )
            

        # =========================
        # DESKTOP
        # =========================

        else:

            conteudo_principal = ft.Row(
                [
                    menu_lateral(
                        estado,
                        rotas_menu,
                        navegar
                    ),

                    ft.Container(
                        content=view_fn(),
                        padding=20,
                        expand=True
                    )
                ],
                spacing=0,
                expand=True
            )

        # =========================
        # VIEW
        # =========================

        page.views.clear()

        page.views.append(
            ft.View(
                route=estado["rota"],

                appbar=construir_appbar(
                    page,
                    estado,
                    titulos_paginas,
                    route_change
                ),

                controls=[conteudo_principal],

                navigation_bar=(
                    navigation_bar_mobile(
                        estado,
                        navegar
                    )
                    if estado["mobile"]
                    else None
                ),

                padding=0,
                spacing=0
            )
        )

        page.update()

    # =========================
    # RESPONSIVE
    # =========================

    def on_resize(e):

        novo_mobile = e.width < BREAKPOINT_MOBILE

        if novo_mobile != estado["mobile"]:

            estado["mobile"] = novo_mobile

            route_change()

    # =========================
    # EVENTS
    # =========================

    page.on_route_change = route_change

    page.on_resize = on_resize

    # =========================
    # START
    # =========================

    if not page.route:

        page.route = "/"

    estado["rota"] = page.route

    route_change()


# =========================
# APP START
# =========================

if __name__ == "__main__":

    ft.app(
        target=main,
        view=ft.WEB_BROWSER
    )