def criar_card(titulo: str, conteudo: ft.Control, p: dict):
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
            border=ft.border.all(1, p["border"]),
            border_radius=12,
            shadow=ft.BoxShadow(
                blur_radius=8,
                color=p["shadow"],
                offset=ft.Offset(0, 2),
            ),
        )
