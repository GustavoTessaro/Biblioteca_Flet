import flet as ft

from core.helpers import *
from services.cliente_service import *
from components.buttons import *
from data.salvarAtualizar import salvar_e_atualizar
from components.cards import mostrar_snack

def view_multas(page, dados, estado, route_change):
        async def marcar_multa_paga(multa_id):
            multa = obter_por_id(dados["multas"], multa_id)
            if multa:
                multa["status"] = "Pago"
                await salvar_e_atualizar(page, dados, route_change, None, "Multa marcada como paga.")
                await mostrar_snack("Multa marcada como paga.")

        linhas = []
        for multa in dados["multas"]:
            cliente = obter_por_id(dados["clientes"], multa["cliente_id"])
            livro = obter_por_id(dados["livros"], multa["livro_id"])
            linhas.append(
                ft.ListTile(
                    title=ft.Text(f"{cliente['nome'] if cliente else 'Cliente removido'}", weight="bold"),
                    subtitle=ft.Column([
                        ft.Text(f"Livro: {livro['titulo'] if livro else 'Livro removido'}", size=12),
                        ft.Text(f"Multa: R${multa['valor']:.2f}", size=12, weight="bold"),
                        ft.Text(f"Dias de atraso: {multa['dias_atraso']}", size=11),
                    ], spacing=2),
                    trailing=criar_botao_primario("Quitar", ft.Icons.CHECK, lambda e, mid=multa['id']: marcar_multa_paga(mid), bgcolor=ft.Colors.GREEN)
                    if multa["status"] == "Pendente" else ft.Text("Pago", color=ft.Colors.GREEN),
                )
            )

        return ft.ListView([
            ft.Column(
                [
                    ft.Text("Multas geradas", weight="bold", size=16),
                    ft.Divider(),
                ] + (linhas if linhas else [ft.Text("Nenhuma multa pendente.", color=ft.Colors.GREY)]),
                spacing=12
            )
        ], expand=True, padding=20, spacing=20)
