import flet as ft

from core.helpers import *
from services.cliente_service import *
from components.buttons import *
from components.layout import criar_layout_form
from data.salvarAtualizar import salvar_e_atualizar
from components.cards import mostrar_snack

def view_clientes(page, dados, estado, route_change):
        cliente_nome = ft.TextField(
            label="Nome",
            expand=True
        )

        cliente_email = ft.TextField(
            label="Email",
            expand=True,
            keyboard_type=ft.KeyboardType.EMAIL
        )

        cliente_telefone = ft.TextField(
            label="Telefone",
            expand=True,
            keyboard_type=ft.KeyboardType.PHONE
        )
        
        def limpar_form_cliente():
            cliente_nome.value = ""
            cliente_email.value = ""
            cliente_telefone.value = ""
            estado["cliente_edit_id"] = None
            atualizar_estado_botoes()
        
        def atualizar_estado_botoes():
            btn_cadastrar.disabled = bool(estado.get("cliente_edit_id"))
            btn_cadastrar.bgcolor = ft.Colors.GREEN if not estado.get("cliente_edit_id") else ft.Colors.GREY
            btn_salvar.disabled = not bool(estado.get("cliente_edit_id"))
            btn_salvar.bgcolor = ft.Colors.ORANGE if estado.get("cliente_edit_id") else ft.Colors.GREY

        if estado["cliente_edit_id"] and not obter_por_id(dados["clientes"], estado["cliente_edit_id"]):
            limpar_form_cliente()

        async def adicionar_cliente(e):
            nome = cliente_nome.value.strip()
            email = cliente_email.value.strip()
            telefone = telefone_valido(cliente_telefone.value)
            if not telefone:
                await mostrar_snack(page, "Telefone inválido.", ft.Colors.RED_700)
                return
            if not nome or not email:
                await mostrar_snack(page, "Todos os campos são obrigatórios.", ft.Colors.RED_700)
                return
            if cliente_existe(dados, nome, email, telefone):
                await mostrar_snack(page, "Já existe um cliente com nome, e-mail ou telefone iguais.", ft.Colors.RED_700)
                return
            if not email_valido(email):
                await mostrar_snack(page, "E-mail inválido.", ft.Colors.RED_700)
                return
            dados["clientes"].append({
                "id": proximo_id(dados["clientes"]),
                "nome": nome,
                "email": email,
                "telefone": telefone,
            })
            limpar_form_cliente()
            await salvar_e_atualizar(page, dados, route_change, None, "Cliente cadastrado com sucesso.")

        def editar_cliente(cliente_id):
            cliente = obter_por_id(dados["clientes"], cliente_id)
            if not cliente:
                return
            cliente_nome.value = cliente["nome"]
            cliente_email.value = cliente.get("email", "")
            cliente_telefone.value = cliente.get("telefone", "")
            estado["cliente_edit_id"] = cliente_id
            atualizar_estado_botoes()
            page.update()

        async def salvar_cliente_edit(e):
            if not estado["cliente_edit_id"]:
                return
            cliente = obter_por_id(dados["clientes"], estado["cliente_edit_id"])
            if not cliente:
                limpar_form_cliente()
                return
            nome = cliente_nome.value.strip()
            email = cliente_email.value.strip()
            telefone = cliente_telefone.value.strip()
            if not nome or not email or not telefone:
                await mostrar_snack(page, "Todos os campos são obrigatórios.", ft.Colors.RED_700)
                return
            if cliente_existe(dados, nome, email, telefone, exclude_id=cliente["id"]):
                await mostrar_snack(page, "Já existe um cliente com nome, e-mail ou telefone iguais.", ft.Colors.RED_700)
                return
            if not email_valido(email):
                await mostrar_snack(page, "E-mail inválido.", ft.Colors.RED_700)
                return
            if not telefone:
                await mostrar_snack(page, "Telefone inválido.", ft.Colors.RED_700)
                return
            cliente["nome"] = nome
            cliente["email"] = email
            cliente["telefone"] = telefone
            limpar_form_cliente()
            await salvar_e_atualizar(page, dados, route_change, None, "Cliente atualizado.")

        async def deletar_cliente(cliente_id):
            if cliente_tem_emprestimos_ativos(cliente_id, dados):
                await mostrar_snack(page, "Não pode deletar cliente com empréstimos ativos.", ft.Colors.RED_700)
                return
            dados["clientes"][:] = [c for c in dados["clientes"] if c["id"] != cliente_id]
            if cliente_id == estado["cliente_edit_id"]:
                limpar_form_cliente()
            await salvar_e_atualizar(page, dados, route_change, None, "Cliente removido.")

        def cancelar_edit(e):
            limpar_form_cliente()
            page.update()

        btn_cadastrar = criar_botao_primario(
            "Cadastrar",
            ft.Icons.ADD,
            adicionar_cliente,
            bgcolor=ft.Colors.GREEN,
            expand=False,
            disabled=bool(estado.get("cliente_edit_id"))
        )

        btn_salvar = criar_botao_primario(
            "Salvar",
            ft.Icons.SAVE,
            salvar_cliente_edit,
            bgcolor=ft.Colors.ORANGE if estado.get("cliente_edit_id") else ft.Colors.GREY,
            expand=False,
            disabled=not bool(estado.get("cliente_edit_id"))
        )

        campo_pesquisa = ft.TextField(
            label="Pesquisar clientes",
            prefix_icon=ft.Icons.SEARCH,
            on_change=lambda e: atualizar_lista_clientes(),
        )

        lista_clientes = ft.Column(spacing=10)
        
        def atualizar_lista_clientes():
            texto = campo_pesquisa.value.lower().strip()

            lista_clientes.controls.clear()

            clientes_filtrados = [
                cliente for cliente in dados["clientes"]
                if (
                    texto in cliente["nome"].lower()
                    or texto in cliente.get("email", "").lower()
                    or texto in cliente.get("telefone", "").lower()
                )
            ]

            for cliente in clientes_filtrados:

                async def on_delete_cliente(e, cid=cliente["id"]):
                    await deletar_cliente(cid)

                lista_clientes.controls.append(
                    ft.ListTile(
                        title=ft.Text(cliente["nome"], weight="bold"),
                        subtitle=ft.Column([
                            ft.Text(f"Email: {cliente.get('email', 'N/A')}", size=12),
                            ft.Text(f"Telefone: {cliente.get('telefone', 'N/A')}", size=12),
                        ], spacing=4),
                        trailing=ft.Row([
                            criar_botao_primario(
                                "",
                                ft.Icons.EDIT,
                                lambda e, cid=cliente["id"]: editar_cliente(cid),
                                bgcolor=ft.Colors.BLUE
                            ),
                            criar_botao_primario(
                                "",
                                ft.Icons.DELETE,
                                on_delete_cliente,
                                bgcolor=ft.Colors.RED
                            ),
                        ], spacing=5, tight=True),
                        is_three_line=True,
                        min_vertical_padding=8,
                    )
                )

            page.update()

        atualizar_lista_clientes()

        linhas = []
        for cliente in dados["clientes"]:
            async def on_delete_cliente(e, cid=cliente["id"]):
                await deletar_cliente(cid)
            linhas.append(
                ft.ListTile(
                    title=ft.Text(cliente["nome"], weight="bold"),
                    subtitle=ft.Column([
                        ft.Text(f"Email: {cliente.get('email', 'N/A')}", size=12),
                        ft.Text(f"Telefone: {cliente.get('telefone', 'N/A')}", size=12),
                    ], spacing=4),
                    trailing=ft.Row([
                        criar_botao_primario("", ft.Icons.EDIT, lambda e, cid=cliente["id"]: editar_cliente(cid), bgcolor=ft.Colors.BLUE),
                        criar_botao_primario("", ft.Icons.DELETE, on_delete_cliente, bgcolor=ft.Colors.RED),
                    ], spacing=5, tight=True),
                    is_three_line=True,
                    min_vertical_padding=8,
                )
            )

        lista = ft.Column([
            criar_layout_form([
                cliente_nome,
                cliente_email,
                cliente_telefone,
                btn_cadastrar,
            ], estado["mobile"], spacing=10),
            criar_layout_form([
                btn_salvar,
                criar_botao_secundario("Cancelar", ft.Icons.CANCEL, cancelar_edit, color=ft.Colors.RED),
            ], estado["mobile"], spacing=10),
            ft.Divider(),
            ft.Text("Clientes cadastrados", weight="bold"),
            campo_pesquisa,
            lista_clientes,
        ], spacing=12)
        return ft.ListView([lista], expand=True, padding=20, spacing=20)
