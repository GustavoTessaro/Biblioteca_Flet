import json
import os
import asyncio
from datetime import date, timedelta

import flet as ft

BUTTON_SHAPE = ft.RoundedRectangleBorder(radius=BORDER_RADIUS)
STATUS_VALIDOS = [STATUS_ABERTO, STATUS_ATRASADO, STATUS_ENTREGUE]

def calcular_valor_multa(dias_atraso: int, valor_por_dia: float) -> float:
    return round(dias_atraso * valor_por_dia, 2)

def prateleira_tem_livros(prateleira_id: int, dados: dict) -> bool:
    return any(livro["prateleira_id"] == prateleira_id for livro in dados["livros"])

#endregion

def main(page: ft.Page):
    
    #region Configurações da Página e Estado
    page.title = "Biblioteca Flet"
    page.padding = 0
    page.spacing = 0
    page.window_maximized = True
    page.theme = ft.Theme(color_scheme_seed=ft.Colors.BLUE)
    page.dark_theme = ft.Theme(color_scheme_seed=ft.Colors.INDIGO)
    page.theme_mode = ft.ThemeMode.LIGHT

    dados = carregar_dados()
    verificar_atrasos_e_multas(dados)

    estado = {
        "rota": "/",
        "cliente_edit_id": None,
        "prateleira_edit_id": None,
        "livro_edit_id": None,
        "mobile": page.width < BREAKPOINT_MOBILE,
        "dark_mode": False,
    }
    
    #endregion

    #region TextFields e Dropdowns

    # TextField para clientes
    cliente_nome = ft.TextField(label="Nome do cliente", hint_text="Ex: João Alberto",  prefix_icon=ft.Icons.PERSON_OUTLINE, expand=True, border_radius=BORDER_RADIUS)
    cliente_email = ft.TextField(label="E-mail do cliente", hint_text="Ex: joao@email.com", prefix_icon=ft.Icons.EMAIL_OUTLINED, expand=True, border_radius=BORDER_RADIUS, keyboard_type=ft.KeyboardType.EMAIL)
    cliente_telefone = ft.TextField(label="Telefone", hint_text="Ex: (49) 9 9999-9999", prefix_icon=ft.Icons.PHONE_OUTLINED, expand=True, border_radius=BORDER_RADIUS, keyboard_type=ft.KeyboardType.PHONE)

    # TextField para prateleiras
    prateleira_nome = ft.TextField(label="Nome da prateleira", hint_text="Ex: Terror", prefix_icon=ft.Icons.TABLE_ROWS_OUTLINED, expand=True, border_radius=BORDER_RADIUS)
    prateleira_dias = ft.TextField(label="Dias de empréstimo", hint_text="Ex: 7", prefix_icon=ft.Icons.CALENDAR_TODAY_OUTLINED, expand=True, border_radius=BORDER_RADIUS)
    prateleira_multa = ft.TextField(label="Multa por dia", hint_text="Ex: 1.5", prefix_icon=ft.Icons.MONETIZATION_ON_OUTLINED, expand=True, border_radius=BORDER_RADIUS)

    # TextField para livros
    livro_titulo = ft.TextField(label="Título do livro", hint_text="Ex: Senhor dos Anéis", prefix_icon=ft.Icons.BOOK_OUTLINED, expand=True, border_radius=BORDER_RADIUS)
    livro_autor = ft.TextField(label="Autor", hint_text="Ex: J.R.R. Tolkien", prefix_icon=ft.Icons.CREATE_OUTLINED, expand=True, border_radius=BORDER_RADIUS)
    livro_prateleira = ft.Dropdown(label="Prateleira", leading_icon=ft.Icons.LAYERS_OUTLINED, expand=True)

    # Dropdown para empréstimos
    emprestimo_cliente = ft.Dropdown(label="Cliente", leading_icon=ft.Icons.PERSON_OUTLINE, expand=True)
    emprestimo_livro = ft.Dropdown(label="Livro disponível", leading_icon=ft.Icons.MENU_BOOK_OUTLINED, expand=True)

    #endregion

    async def mostrar_snack(msg: str, cor=ft.Colors.GREEN_700):

        snack = ft.SnackBar(
            content=ft.Text(
                msg,
                color=ft.Colors.WHITE
            ),
            bgcolor=cor,
            duration=2500,
        )

        page.overlay.clear()

        page.overlay.append(snack)

        snack.open = True

        page.update()

        await asyncio.sleep(1.2)

    def atualizar_dropdowns():
        livro_prateleira.options = [
            ft.dropdown.Option(str(prateleira["id"]), prateleira["nome"])
            for prateleira in dados["prateleiras"]
        ]
        emprestimo_cliente.options = [
            ft.dropdown.Option(str(cliente["id"]), cliente["nome"])
            for cliente in dados["clientes"]
        ]
        emprestimo_livro.options = [
            ft.dropdown.Option(str(livro["id"]), f"{livro['titulo']} ({livro['autor']})")
            for livro in dados["livros"]
            if not livro_esta_emprestado(livro["id"], dados)
        ]

    async def salvar_e_atualizar(msg: str = None):

        salvar_dados(dados)

        verificar_atrasos_e_multas(dados)

        atualizar_dropdowns()

        if msg:
            await mostrar_snack(msg)

        route_change()

    def navegar(rota: str):
        page.go(rota)

    def criar_layout_form(controles: list[ft.Control], spacing: int = 10):
        return ft.Column(controles, spacing=spacing) if estado["mobile"] else ft.Row(controles, spacing=spacing)

    def limpar_form_cliente():
        cliente_nome.value = ""
        cliente_email.value = ""
        cliente_telefone.value = ""
        estado["cliente_edit_id"] = None

    def limpar_form_prateleira():
        prateleira_nome.value = ""
        prateleira_dias.value = ""
        prateleira_multa.value = ""
        estado["prateleira_edit_id"] = None

    def limpar_form_livro():
        livro_titulo.value = ""
        livro_autor.value = ""
        livro_prateleira.value = None
        estado["livro_edit_id"] = None

    def renderizar_menu():
        opcoes = [
        ("/", "Home"),
        ("/clientes", "Clientes"),
        ("/prateleiras", "Prateleiras"),
        ("/livros", "Livros"),
        ("/emprestimos", "Empréstimos"),
        ("/multas", "Multas"),
        ]
        itens = []
        for rota, label in opcoes:
            ativo = rota == page.route 
            itens.append(
            ft.TextButton(
                content=ft.Text(label),
                on_click=lambda e, dest=rota: navegar(dest),
                style=ft.ButtonStyle(
                    color=ft.Colors.WHITE if ativo else ft.Colors.BLUE_700,
                    bgcolor=ft.Colors.BLUE_700 if ativo else ft.Colors.BLUE_50,
                    shape=BUTTON_SHAPE,
                ),
            )
        )
        return ft.Row(itens, wrap=True, spacing=10)

    titulos_paginas = {
        "/": "Início - Painel Geral",
        "/clientes": "Gerenciar Clientes",
        "/prateleiras": "Gerenciar Prateleiras",
        "/livros": "Catálogo de Livros",
        "/emprestimos": "Controle de Empréstimos",
        "/multas": "Histórico de Multas"
    }

    rotas_menu = [
        ("/",            "Home",         ft.Icons.HOME_OUTLINED,         ft.Icons.HOME),
        ("/clientes",    "Clientes",     ft.Icons.PERSON_OUTLINE,        ft.Icons.PERSON),
        ("/prateleiras", "Prateleiras",  ft.Icons.TABLE_ROWS_OUTLINED,   ft.Icons.TABLE_ROWS),
        ("/livros",      "Livros",       ft.Icons.BOOK_OUTLINED,         ft.Icons.BOOK),
        ("/emprestimos", "Empréstimos",  ft.Icons.UNDO_OUTLINED,         ft.Icons.UNDO),
        ("/multas",      "Multas",       ft.Icons.MONETIZATION_ON_OUTLINED, ft.Icons.MONETIZATION_ON),
    ]

    page.on_route_change = route_change
    page.on_resize = on_resize

    if not page.route or page.route == "/":
        page.route = "/"
    
    estado["rota"] = page.route

    route_change()

if __name__ == "__main__":
    ft.app(target=main, view=ft.WEB_BROWSER)


