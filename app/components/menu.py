from app.core.constants import BORDER_RADIUS
import flet as ft

def criar_item_menu(label: str, ic_off, ic_on, ativo: bool, on_click):
        return ft.Container(
            content=ft.Row([
                ft.Icon(ic_on if ativo else ic_off, color=ft.Colors.BLUE_700 if ativo else ft.Colors.BLACK, size=20),
                ft.Text(label, size=14, color=ft.Colors.BLUE_700 if ativo else ft.Colors.BLACK, weight="bold" if ativo else "normal"),
            ], spacing=12, tight=True),
            padding=ft.Padding(12, 10, 12, 10),
            border_radius=BORDER_RADIUS,
            bgcolor=ft.Colors.BLUE_50 if ativo else ft.Colors.TRANSPARENT,
            on_click=on_click,
        )


def menu_lateral(estado, rotas_menu, navegar):
        rota = estado["rota"]
        
        itens = [
            criar_item_menu(
                label, ic_off, ic_on,
                ativo=(rota == r),
                on_click=lambda e, dest=r: navegar(dest)
            )
            for r, label, ic_off, ic_on in rotas_menu
        ]

        perfil = ft.Container(
            content=ft.Row([
                ft.CircleAvatar(
                    content=ft.Text("ADM", size=10, weight="bold"),
                    bgcolor=ft.Colors.BLUE_700,
                    color=ft.Colors.WHITE,
                    radius=15,
                ),
                ft.Column([
                    ft.Text("Administrador", size=12, weight="bold", color=ft.Colors.BLACK),
                    ft.Text("● Online", size=10, color=ft.Colors.GREEN_400),
                ], spacing=0, tight=True, expand=True),
            ], spacing=8, tight=True),
            padding=ft.Padding(4, 8, 4, 0),
        )

        return ft.Container(
            width=215,
            bgcolor=ft.Colors.BLUE_50,
            border=ft.border.only(right=ft.BorderSide(1, ft.Colors.GREY_300)),
            padding=12,
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.MENU_BOOK, color=ft.Colors.BLUE_700, size=20),
                    ft.Text("BiblioFlet", size=16, weight="bold", color=ft.Colors.BLUE_700),
                ], spacing=8, tight=True),
                ft.Divider(height=16, color=ft.Colors.GREY_300),
                *itens,
                ft.Divider(height=16, color=ft.Colors.GREY_300),
                perfil,
            ], spacing=4, tight=True),
        )
