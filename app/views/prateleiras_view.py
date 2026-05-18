import flet as ft

from core.helpers import *
from services.cliente_service import *
from components.buttons import *

def view_prateleiras(page, dados, estado, route_change):
        if estado["prateleira_edit_id"] and not obter_por_id(dados["prateleiras"], estado["prateleira_edit_id"]):
            limpar_form_prateleira()

        async def adicionar_prateleira(e):
            nome = prateleira_nome.value.strip()
            dias = prateleira_dias.value.strip()
            multa_texto = prateleira_multa.value.strip()
            multa_valor = parse_float(prateleira_multa.value)
            if not nome or not dias or not multa_texto:
                await mostrar_snack("Todos os campos são obrigatórios.", ft.Colors.RED_700)
                return
            if not dias.isdigit() or int(dias) <= 0:
                await mostrar_snack("Preencha nome e dias de empréstimo válidos.", ft.Colors.RED_700)
                return
            if multa_valor is None:
                await mostrar_snack("Multa por dia deve ser um número válido.", ft.Colors.RED_700)
                return
            if prateleira_existe(nome):
                await mostrar_snack("Já existe uma prateleira com esses dados.", ft.Colors.RED_700)
                return
            dados["prateleiras"].append({
                "id": proximo_id(dados["prateleiras"]),
                "nome": nome,
                "dias_e_prazo": int(dias),
                "multa_por_dia": multa_valor,
            })
            limpar_form_prateleira()
            await salvar_e_atualizar("Prateleira cadastrada.")

        def editar_prateleira(prateleira_id):
            prateleira = obter_por_id(dados["prateleiras"], prateleira_id)
            if not prateleira:
                return
            prateleira_nome.value = prateleira["nome"]
            prateleira_dias.value = str(prateleira["dias_e_prazo"])
            prateleira_multa.value = str(prateleira["multa_por_dia"])
            estado["prateleira_edit_id"] = prateleira_id
            route_change()

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
                await mostrar_snack("Todos os campos são obrigatórios.", ft.Colors.RED_700)
                return
            if not dias.isdigit() or int(dias) <= 0:
                await mostrar_snack("Dias deve ser um número válido.", ft.Colors.RED_700)
                return
            if multa_valor is None:
                await mostrar_snack("Multa por dia deve ser um número válido.", ft.Colors.RED_700)
                return
            if prateleira_existe(nome, exclude_id=prateleira["id"]):
                await mostrar_snack("Já existe uma prateleira com esses dados.", ft.Colors.RED_700)
                return
            prateleira["nome"] = nome
            prateleira["dias_e_prazo"] = int(dias)
            prateleira["multa_por_dia"] = multa_valor
            limpar_form_prateleira()
            await salvar_e_atualizar("Prateleira atualizada.")

        async def deletar_prateleira(prateleira_id):
            if prateleira_tem_livros(prateleira_id, dados):
                await mostrar_snack("Não pode deletar prateleira que tem livros cadastrados.", ft.Colors.RED_700)
                return
            dados["prateleiras"][:] = [p for p in dados["prateleiras"] if p["id"] != prateleira_id]
            if prateleira_id == estado["prateleira_edit_id"]:
                limpar_form_prateleira()
            await salvar_e_atualizar("Prateleira removida.")

        def cancelar_edit(e):
            limpar_form_prateleira()
            route_change()

        btn_salvar = criar_botao_primario(
            "Salvar",
            ft.Icons.SAVE,
            salvar_prateleira_edit,
            bgcolor=ft.Colors.ORANGE if estado["prateleira_edit_id"] else ft.Colors.GREY
        )

        linhas = []
        for prateleira in dados["prateleiras"]:
            async def on_delete_prateleira(e, pid=prateleira["id"]):
                await deletar_prateleira(pid)
            linhas.append(
                ft.ListTile(
                    title=ft.Text(prateleira["nome"], weight="bold"),
                    subtitle=ft.Text(
                        f"Prazo: {prateleira['dias_e_prazo']} dias · Multa/dia: R${prateleira['multa_por_dia']:.2f}",
                        size=12,
                    ),
                    trailing=ft.Row([
                        criar_botao_primario("", ft.Icons.EDIT, lambda e, pid=prateleira["id"]: editar_prateleira(pid), bgcolor=ft.Colors.BLUE),
                        criar_botao_primario("", ft.Icons.DELETE, on_delete_prateleira, bgcolor=ft.Colors.RED),
                    ], spacing=5, tight=True),
                    min_vertical_padding=8,
                )
            )

        lista = ft.Column([
            criar_layout_form([
                prateleira_nome,
                prateleira_dias,
                prateleira_multa,
                criar_botao_primario("Cadastrar", ft.Icons.ADD, adicionar_prateleira, bgcolor=ft.Colors.GREEN),
            ], spacing=10),
            criar_layout_form([
                btn_salvar,
                criar_botao_secundario("Cancelar", ft.Icons.CANCEL, cancelar_edit, color=ft.Colors.GREY),
            ], spacing=10),
            ft.Divider(),
            ft.Text("Prateleiras cadastradas", weight="bold"),
            *linhas,
        ], spacing=12)
        return ft.ListView([lista], expand=True, padding=20, spacing=20)
