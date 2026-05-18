import asyncio

import flet as ft

from core.theme import paleta

async def mostrar_snack(page: ft.Page, msg: str, cor=ft.Colors.GREEN_700):

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