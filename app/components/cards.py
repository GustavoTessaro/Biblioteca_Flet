import flet as ft

from core.theme import paleta

def criar_card(
    titulo: str,
    conteudo: ft.Control,
    p: dict | None = None
):

    if p is None:

        p = paleta(False)

    return ft.Container(
        content=ft.Column([
            ft.Text(
                titulo,
                size=13,
                weight="bold",
                color=p["txt"]
            ),

            conteudo,
        ]),

        padding=16,

        bgcolor=p["bg_card"],

        border=ft.border.all(
            1,
            p["border"]
        ),

        border_radius=12,

        shadow=ft.BoxShadow(
            blur_radius=8,
            color=p["shadow"],
            offset=ft.Offset(0, 2),
        ),
    )