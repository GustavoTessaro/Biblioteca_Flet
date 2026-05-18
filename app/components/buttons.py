import flet as ft

from core.constants import BORDER_RADIUS

BUTTON_SHAPE = ft.RoundedRectangleBorder(
    radius=BORDER_RADIUS
)

def criar_botao_primario(texto: str, icone, on_click, expand=False, bgcolor=ft.Colors.BLUE_700, color=ft.Colors.WHITE, disabled=False):
        return ft.ElevatedButton(  # <── Alterado para ElevatedButton
            content=ft.Row([
                ft.Icon(icone, size=16),
                ft.Text(texto, size=14) if texto else ft.Container(), # Trata botões que só têm ícone
            ], spacing=6 if texto else 0, tight=True),
            on_click=on_click,
            expand=expand,
            disabled=disabled,
            style=ft.ButtonStyle(
                bgcolor=bgcolor,
                color=color,
                shape=BUTTON_SHAPE,
            ),
        )
        
def criar_botao_secundario(texto: str, icone, on_click, expand=False, color=ft.Colors.BLUE_700, disabled=False):
        return ft.OutlinedButton(  # <── Alterado para OutlinedButton
            content=ft.Row([
                ft.Icon(icone, size=16),
                ft.Text(texto, size=14) if texto else ft.Container(),
            ], spacing=6 if texto else 0, tight=True),
            on_click=on_click,
            expand=expand,
            disabled=disabled,
            style=ft.ButtonStyle(
                color=color,
                shape=BUTTON_SHAPE,
            ),
        )
