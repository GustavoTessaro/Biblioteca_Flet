BREAKPOINT_MOBILE = 600

def on_resize(e: ft.PageResizeEvent):
        # Calcula se mudou para tamanho mobile dinamicamente
        novo_mobile = e.width < BREAKPOINT_MOBILE
        if novo_mobile != estado["mobile"]:
            estado["mobile"] = novo_mobile
            route_change()
