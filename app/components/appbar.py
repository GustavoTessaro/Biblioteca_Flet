import flet as ft

from core.theme import paleta

def toggle_theme(page, estado, route_change):

        estado["dark_mode"] = not estado["dark_mode"]

        page.theme_mode = (
        ft.ThemeMode.DARK
        if estado["dark_mode"]
        else ft.ThemeMode.LIGHT
        )

        route_change()


def construir_appbar(page, estado, titulos_paginas, route_change):

        p = paleta(estado["dark_mode"])

        return ft.AppBar(
            leading=ft.Icon(
                ft.Icons.MENU_BOOK,
                color=p["txt"]
            ),

            leading_width=48,

            title=ft.Text(
                titulos_paginas.get(
                    estado["rota"],
                    "Sistema de Biblioteca"
                ),
                color=p["txt"],
                size=18,
                weight="bold",
            ),

            bgcolor=p["primary"],

            center_title=False,

            actions=[
                ft.IconButton(
                    icon=(
                        ft.Icons.DARK_MODE
                        if estado["dark_mode"]
                        else ft.Icons.LIGHT_MODE
                    ),

                    icon_color=ft.Colors.WHITE,

                    tooltip="Alternar tema",

                    on_click=lambda e: toggle_theme(page, estado, route_change),
                )
            ]
        )

