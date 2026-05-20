import flet as ft

from core.helpers import *
from services.cliente_service import *
from components.buttons import *
from components.layout import criar_layout_form
from data.salvarAtualizar import salvar_e_atualizar
from components.cards import mostrar_snack
from services.prateleira_service import prateleira_existe, prateleira_tem_livros

def view_prateleiras(page, dados, estado, route_change):
        prateleira_nome = ft.TextField(
            label="Nome",
            expand=True
        )

        prateleira_dias = ft.TextField(
            label="Dias de empréstimo",
            width=180
        )

        prateleira_multa = ft.TextField(
            label="Multa por dia",
            width=180
        )
        
        def limpar_form_prateleira():
            prateleira_nome.value = ""
            prateleira_dias.value = ""
            prateleira_multa.value = ""
            estado["prateleira_edit_id"] = None
            atualizar_estado_botoes()
        
        if estado["prateleira_edit_id"] and not obter_por_id(dados["prateleiras"], estado["prateleira_edit_id"]):
            limpar_form_prateleira()
            
        def atualizar_estado_botoes():
            btn_cadastrar.disabled = bool(estado.get("prateleira_edit_id"))
            btn_cadastrar.bgcolor = (ft.Colors.GREEN if not estado.get("prateleira_edit_id")else ft.Colors.GREY)
            btn_salvar.disabled = not bool(estado.get("prateleira_edit_id"))
            btn_salvar.bgcolor = (ft.Colors.ORANGE if estado.get("prateleira_edit_id") else ft.Colors.GREY)

        async def adicionar_prateleira(e):
            nome = prateleira_nome.value.strip()
            dias = prateleira_dias.value.strip()
            multa_texto = prateleira_multa.value.strip()
            multa_valor = parse_float(prateleira_multa.value)
            if not nome or not dias or not multa_texto:
                await mostrar_snack(page, "Todos os campos são obrigatórios.", ft.Colors.RED_700)
                return
            if not dias.isdigit() or int(dias) <= 0:
                await mostrar_snack(page, "Preencha nome e dias de empréstimo válidos.", ft.Colors.RED_700)
                return
            if multa_valor is None:
                await mostrar_snack(page, "Multa por dia deve ser um número válido.", ft.Colors.RED_700)
                return
            if prateleira_existe(dados, nome):
                await mostrar_snack(page, "Já existe uma prateleira com esses dados.", ft.Colors.RED_700)
                return
            dados["prateleiras"].append({
                "id": proximo_id(dados["prateleiras"]),
                "nome": nome,
                "dias_e_prazo": int(dias),
                "multa_por_dia": multa_valor,
            })
            limpar_form_prateleira()
            await salvar_e_atualizar(page, dados, route_change, None, "Prateleira cadastrada.")

        def editar_prateleira(prateleira_id):
            prateleira = obter_por_id(dados["prateleiras"], prateleira_id)
            if not prateleira:
                return
            prateleira_nome.value = prateleira["nome"]
            prateleira_dias.value = str(prateleira["dias_e_prazo"])
            prateleira_multa.value = str(prateleira["multa_por_dia"])
            estado["prateleira_edit_id"] = prateleira_id
            atualizar_estado_botoes()
            page.update()

        async def salvar_prateleira_edit(e):
            if not estado["prateleira_edit_id"]:
                return
            prateleira = obter_por_id(dados["prateleiras"], estado["prateleira_edit_id"])
            if not prateleira:
                limpar_form_prateleira()
                return
            nome = prateleira_nome.value.strip()
            dias = prateleira_dias.value.strip()
            multa_texto = prateleira_multa.value.strip()
            multa_valor = parse_float(prateleira_multa.value)
            if not nome or not dias or not multa_texto:
                await mostrar_snack(page, "Todos os campos são obrigatórios.", ft.Colors.RED_700)
                return
            if not dias.isdigit() or int(dias) <= 0:
                await mostrar_snack(page, "Dias deve ser um número válido.", ft.Colors.RED_700)
                return
            if multa_valor is None:
                await mostrar_snack(page, "Multa por dia deve ser um número válido.", ft.Colors.RED_700)
                return
            if prateleira_existe(dados, nome, exclude_id=prateleira["id"]):
                await mostrar_snack(page, "Já existe uma prateleira com esses dados.", ft.Colors.RED_700)
                return
            prateleira["nome"] = nome
            prateleira["dias_e_prazo"] = int(dias)
            prateleira["multa_por_dia"] = multa_valor
            limpar_form_prateleira()
            await salvar_e_atualizar(page, dados, route_change, None, "Prateleira atualizada.")

        async def deletar_prateleira(prateleira_id):
            if prateleira_tem_livros(prateleira_id, dados):
                await mostrar_snack(page, "Não pode deletar prateleira que tem livros cadastrados.", ft.Colors.RED_700)
                return
            dados["prateleiras"][:] = [p for p in dados["prateleiras"] if p["id"] != prateleira_id]
            if prateleira_id == estado["prateleira_edit_id"]:
                limpar_form_prateleira()
            await salvar_e_atualizar(page, dados, route_change, None, "Prateleira removida.")

        def cancelar_edit(e):
            limpar_form_prateleira()
            page.update()

        btn_salvar = criar_botao_primario(
            "Editar",
            ft.Icons.SAVE,
            salvar_prateleira_edit,
            bgcolor=ft.Colors.ORANGE if estado.get("prateleira_edit_id") else ft.Colors.GREY,
            expand=False,
            disabled=not bool(estado.get("prateleira_edit_id"))
        )
        
        btn_cadastrar = criar_botao_primario(
            "Cadastrar",
            ft.Icons.ADD,
            adicionar_prateleira,
            bgcolor=ft.Colors.GREEN,
            expand=False,
            disabled=bool(estado.get("prateleira_edit_id"))
        )
        
        campo_pesquisa = ft.TextField(
            label="Pesquisar prateleiras",
            prefix_icon=ft.Icons.SEARCH,
            on_change=lambda e: atualizar_lista_prateleiras(),
        )

        lista_prateleiras = ft.Column(spacing=10)

        def atualizar_lista_prateleiras():

            texto = campo_pesquisa.value.lower().strip()

            lista_prateleiras.controls.clear()

            prateleiras_filtradas = []

            for prateleira in dados["prateleiras"]:

                nome = prateleira["nome"].lower()

                dias = str(prateleira["dias_e_prazo"])

                multa = str(prateleira["multa_por_dia"])

                if (
                    texto == ""
                    or texto in nome
                    or texto in dias
                    or texto in multa
                ):
                    prateleiras_filtradas.append(prateleira)

            if not prateleiras_filtradas:

                lista_prateleiras.controls.append(
                    ft.Text(
                        "Nenhuma prateleira encontrada.",
                        color=ft.Colors.GREY
                    )
                )

            for prateleira in prateleiras_filtradas:

                async def on_delete_prateleira(
                    e,
                    pid=prateleira["id"]
                ):
                    await deletar_prateleira(pid)

                lista_prateleiras.controls.append(
                    ft.ListTile(
                        title=ft.Text(
                            prateleira["nome"],
                            weight="bold"
                        ),

                        subtitle=ft.Text(
                            (
                                f"Prazo: "
                                f"{prateleira['dias_e_prazo']} dias "
                                f"· Multa/dia: "
                                f"R${prateleira['multa_por_dia']:.2f}"
                            ),
                            size=12,
                        ),

                        trailing=ft.Row([
                            criar_botao_primario(
                                "",
                                ft.Icons.EDIT,
                                lambda e, pid=prateleira["id"]:
                                    editar_prateleira(pid),
                                bgcolor=ft.Colors.BLUE
                            ),

                            criar_botao_primario(
                                "",
                                ft.Icons.DELETE,
                                on_delete_prateleira,
                                bgcolor=ft.Colors.RED
                            ),

                        ], spacing=5, tight=True),

                        min_vertical_padding=8,
                    )
                )

            page.update()

        atualizar_lista_prateleiras()

        lista = ft.Column([
            criar_layout_form([
                prateleira_nome,
                prateleira_dias,
                prateleira_multa,
                btn_cadastrar,
            ], estado["mobile"], spacing=10),
            criar_layout_form([
                btn_salvar,
                criar_botao_secundario("Cancelar", ft.Icons.CANCEL, cancelar_edit, color=ft.Colors.RED),
            ],estado["mobile"], spacing=10),
            ft.Divider(),
            ft.Text("Prateleiras cadastradas", weight="bold"),
            campo_pesquisa,
            lista_prateleiras,
        ], spacing=12)
        return ft.ListView([lista], expand=True, padding=20, spacing=20)
