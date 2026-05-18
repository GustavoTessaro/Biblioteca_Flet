import flet as ft

def paleta(dark: bool) -> dict:

    if dark:
        return {
            "bg_page": ft.Colors.GREY_900,
            "bg_card": ft.Colors.GREY_800,
            "bg_sidebar": ft.Colors.GREY_900,

            "txt": ft.Colors.WHITE,
            "txt_sec": ft.Colors.GREY_400,

            "primary": ft.Colors.BLUE_300,
            "danger": ft.Colors.RED_300,
            "success": ft.Colors.GREEN_300,

            "border": ft.Colors.GREY_700,

            "menu_active": ft.Colors.BLUE_800,

            "shadow": ft.Colors.with_opacity(0.25, ft.Colors.BLACK),
        }

    return {
        "bg_page": ft.Colors.WHITE,
        "bg_card": ft.Colors.WHITE,
        "bg_sidebar": ft.Colors.GREY_50,

        "txt": ft.Colors.BLACK,
        "txt_sec": ft.Colors.GREY_700,

        "primary": ft.Colors.BLUE_700,
        "danger": ft.Colors.RED_700,
        "success": ft.Colors.GREEN_700,

        "border": ft.Colors.GREY_300,

        "menu_active": ft.Colors.BLUE_50,

        "shadow": ft.Colors.with_opacity(0.07, ft.Colors.BLACK),
    }
