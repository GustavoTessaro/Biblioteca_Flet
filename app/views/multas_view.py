import flet as ft
import asyncio

from core.helpers import *
from services.cliente_service import *
from components.buttons import *
from data.salvarAtualizar import salvar_e_atualizar
from components.cards import mostrar_snack

def view_multas(page, dados, estado, route_change):

        campo_pesquisa = ft.TextField(
            label="Pesquisar multas",
            prefix_icon=ft.Icons.SEARCH,
            on_change=lambda e: atualizar_lista_multas(),
        )

        lista_multas = ft.Column(spacing=10)

        async def marcar_multa_paga(multa_id):
            multa = obter_por_id(dados["multas"], multa_id)

            if multa:
                multa["status"] = "Pago"

                await salvar_e_atualizar(
                    page,
                    dados,
                    route_change,
                    None,
                    "Multa marcada como paga."
                )

                atualizar_lista_multas()
                page.update()

        async def limpar_multas_pagas(e):

            multas_filtradas = []

            for multa in dados["multas"]:

                emprestimo = obter_por_id(
                    dados["emprestimos"],
                    multa["emprestimo_id"]
                )

                if (
                    multa["status"] == "Pago"
                    and emprestimo
                    and emprestimo["status"] != "Entregue"
                ):
                    multas_filtradas.append(multa)

                elif multa["status"] != "Pago":
                    multas_filtradas.append(multa)

            dados["multas"][:] = multas_filtradas

            await salvar_e_atualizar(
                page,
                dados,
                route_change,
                None,
                "Histórico de multas pagas de empréstimos devolvidos removido."
            )

            atualizar_lista_multas()

        def criar_callback(mid):
            return lambda e: page.run_task(marcar_multa_paga, mid)

        def atualizar_lista_multas():
            texto = campo_pesquisa.value.lower().strip()

            lista_multas.controls.clear()

            multas_filtradas = []

            for multa in dados["multas"]:

                cliente = obter_por_id(
                    dados["clientes"],
                    multa["cliente_id"]
                )

                livro = obter_por_id(
                    dados["livros"],
                    multa["livro_id"]
                )

                nome_cliente = (
                    cliente["nome"].lower()
                    if cliente else ""
                )

                titulo_livro = (
                    livro["titulo"].lower()
                    if livro else ""
                )

                status = multa["status"].lower()

                if (
                    texto == ""
                    or texto in nome_cliente
                    or texto in titulo_livro
                    or texto in status
                ):
                    multas_filtradas.append(
                        (multa, cliente, livro)
                    )

            if not multas_filtradas:
                lista_multas.controls.append(
                    ft.Text(
                        "Nenhuma multa encontrada.",
                        color=ft.Colors.GREY
                    )
                )

            for multa, cliente, livro in multas_filtradas:

                lista_multas.controls.append(
                    ft.ListTile(
                        title=ft.Text(
                            cliente['nome']
                            if cliente else 'Cliente removido',
                            weight="bold"
                        ),

                        subtitle=ft.Column([
                            ft.Text(
                                f"Livro: {livro['titulo'] if livro else 'Livro removido'}",
                                size=12
                            ),

                            ft.Text(
                                f"Multa: R${multa['valor']:.2f}",
                                size=12,
                                weight="bold"
                            ),

                            ft.Text(
                                f"Dias de atraso: {multa['dias_atraso']}",
                                size=11
                            ),

                            ft.Text(
                                f"Status: {multa['status']}",
                                size=11
                            ),

                        ], spacing=2),

                        trailing=(
                            criar_botao_primario(
                                "Quitar",
                                ft.Icons.CHECK,
                                criar_callback(multa['id']),
                                bgcolor=ft.Colors.GREEN
                            )

                            if multa["status"] == "Pendente"

                            else ft.Text(
                                "Pago",
                                color=ft.Colors.GREEN
                            )
                        ),
                    )
                )

            page.update()

        atualizar_lista_multas()

        return ft.ListView([
            ft.Column(
                [
                    ft.Text(
                        "Multas geradas",
                        weight="bold",
                        size=16
                    ),

                    campo_pesquisa,

                    criar_botao_secundario(
                        "Limpar Histórico",
                        ft.Icons.DELETE_SWEEP,
                        limpar_multas_pagas,
                        color=ft.Colors.RED,
                    ),

                    ft.Divider(),

                    lista_multas,
                ],
                spacing=12
            )
        ],
        expand=True,
        padding=20,
        spacing=20)