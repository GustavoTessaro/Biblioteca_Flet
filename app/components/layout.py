import flet as ft

def criar_layout_form(
    controles: list[ft.Control],
    mobile: bool,
    spacing: int = 10
):
    if mobile:
        return ft.Column(
            controles,
            spacing=spacing
        )

    return ft.Row(
        controles,
        spacing=spacing
    )