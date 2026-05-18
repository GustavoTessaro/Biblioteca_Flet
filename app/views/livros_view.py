import flet as ft

from core.helpers import *
from services.cliente_service import *
from components.buttons import *
from components.layout import criar_layout_form
from data.storage import salvar_e_atualizar
from components.cards import mostrar_snack
from services.livro_service import livro_esta_emprestado, obter_livro_por_atributos

def view_livros(page, dados, estado, route_change):
        livro_titulo = ft.TextField(
            label="Título",
            expand=True
        )

        livro_autor = ft.TextField(
            label="Autor",
            expand=True
        )

        livro_prateleira = ft.Dropdown(
            label="Prateleira",
            width=250,
            options=[
                ft.dropdown.Option(
                    str(p["id"]),
                    p["nome"]
                )
                for p in dados["prateleiras"]
            ]
        )
        
        if estado["livro_edit_id"] and not obter_por_id(dados["livros"], estado["livro_edit_id"]):
            limpar_form_livro()

        async def adicionar_livro(e):
            titulo = livro_titulo.value.strip()
            autor = livro_autor.value.strip()
            prateleira_id = int(livro_prateleira.value) if livro_prateleira.value else None
            if not titulo or not autor or prateleira_id is None:
                await mostrar_snack("Todos os campos são obrigatórios.", ft.Colors.RED_700)
                return
            livro_existente = obter_livro_por_atributos(titulo, autor, prateleira_id)
            if livro_existente:
                livro_existente["quantidade"] = livro_existente.get("quantidade", 1) + 1
                limpar_form_livro()
                await salvar_e_atualizar(f"Livro existente encontrado. Quantidade atualizada para {livro_existente['quantidade']}.")
                return
            dados["livros"].append({
                "id": proximo_id(dados["livros"]),
                "titulo": titulo,
                "autor": autor,
                "prateleira_id": prateleira_id,
                "quantidade": 1,
            })
            limpar_form_livro()
            await salvar_e_atualizar("Livro cadastrado.")

        def editar_livro(livro_id):
            livro = obter_por_id(dados["livros"], livro_id)
            if not livro:
                return
            livro_titulo.value = livro["titulo"]
            livro_autor.value = livro["autor"]
            livro_prateleira.value = str(livro["prateleira_id"])
            estado["livro_edit_id"] = livro_id
            route_change() # ── ADICIONADO: Atualiza a tela para mudar o botão Salvar para Laranja

        async def salvar_livro_edit(e):
            if not estado["livro_edit_id"]:
                return
            livro = obter_por_id(dados["livros"], estado["livro_edit_id"])
            if not livro:
                limpar_form_livro()
                return
            titulo = livro_titulo.value.strip()
            autor = livro_autor.value.strip()
            prateleira_id = int(livro_prateleira.value) if livro_prateleira.value else None
            if not titulo or not autor or prateleira_id is None:
                await mostrar_snack("Todos os campos são obrigatórios.", ft.Colors.RED_700)
                return
            if obter_livro_por_atributos(titulo, autor, prateleira_id, exclude_id=livro["id"]):
                await mostrar_snack("Já existe um livro com esses dados.", ft.Colors.RED_700)
                return
            livro["titulo"] = titulo
            livro["autor"] = autor
            livro["prateleira_id"] = prateleira_id
            limpar_form_livro()
            await salvar_e_atualizar("Livro atualizado.")

        async def deletar_livro(livro_id):
            if livro_esta_emprestado(livro_id, dados) > 0:
                await mostrar_snack("Não pode deletar livro que está emprestado.", ft.Colors.RED_700)
                return
            dados["livros"][:] = [l for l in dados["livros"] if l["id"] != livro_id]
            if livro_id == estado["livro_edit_id"]:
                limpar_form_livro()
            await salvar_e_atualizar("Livro removido.")

        async def aumentar_quantidade(livro_id):
            livro = obter_por_id(dados["livros"], livro_id)
            if livro:
                livro["quantidade"] = livro.get("quantidade", 1) + 1
                await salvar_e_atualizar(f"Quantidade atualizada: {livro['quantidade']}")

        async def diminuir_quantidade(livro_id):
            livro = obter_por_id(dados["livros"], livro_id)
            if livro:
                if livro.get("quantidade", 1) <= 1:
                    await mostrar_snack("Quantidade mínima é 1. Use excluir para remover o livro.", ft.Colors.RED_700)
                    return
                livro["quantidade"] -= 1
                await salvar_e_atualizar(f"Quantidade atualizada: {livro['quantidade']}")

        def cancelar_edit(e):
            limpar_form_livro()
            route_change() # ── ALTERADO: Redesenha a tela limpando o estado de edição

        # Otimização: O botão de salvar só ativa a função se houver algo sendo editado
        btn_salvar = criar_botao_primario(
            "Editar",
            ft.Icons.SAVE,
            salvar_livro_edit if estado["livro_edit_id"] else None,
            bgcolor=ft.Colors.ORANGE if estado["livro_edit_id"] else ft.Colors.GREY
        )

        linhas = []
        for livro in dados["livros"]:
            async def on_delete_livro(e, lid=livro["id"]):
                await deletar_livro(lid)
            async def on_add(e, lid=livro["id"]):
                await aumentar_quantidade(lid)
            async def on_remove(e, lid=livro["id"]):
                await diminuir_quantidade(lid)
            emprestimos_abertos = livro_esta_emprestado(livro["id"], dados)
            quantidade = livro.get("quantidade", 1)
            emprestado = emprestimos_abertos >= quantidade
            prateleira = obter_por_id(dados["prateleiras"], livro["prateleira_id"])
            linhas.append(
                ft.ListTile(
                    title=ft.Text(livro["titulo"], weight="bold"),
                    subtitle=ft.Column([
                        ft.Text(f"Autor: {livro['autor']}", size=12),
                        ft.Text(f"Prateleira: {prateleira['nome'] if prateleira else 'Sem prateleira'}", size=12),
                    ], spacing=2),
                    trailing=ft.Row([
                        ft.Text(f"Qty: {quantidade} (Disp: {quantidade - emprestimos_abertos})", size=12),
                        ft.Text("Disponível" if emprestimos_abertos < quantidade else "Emprestado", color=ft.Colors.GREEN if emprestimos_abertos < quantidade else ft.Colors.RED),
                        criar_botao_primario("",ft.Icons.ADD,on_add,bgcolor=ft.Colors.BLUE),
                        criar_botao_primario("",ft.Icons.REMOVE,on_remove,bgcolor=ft.Colors.GREY),
                        criar_botao_primario("", ft.Icons.EDIT, lambda e, lid=livro["id"]: editar_livro(lid), bgcolor=ft.Colors.BLUE),
                        criar_botao_primario("", ft.Icons.DELETE, on_delete_livro, bgcolor=ft.Colors.RED) if not emprestado else ft.Container(),
                    ], spacing=5, tight=True), # ── ADICIONADO: tight=True evita bugs de tamanho na linha de ações
                )
            )

        lista = ft.Column([
            criar_layout_form([
                livro_titulo,
                livro_autor,
                livro_prateleira,
                criar_botao_primario("Cadastrar", ft.Icons.ADD, adicionar_livro, bgcolor=ft.Colors.GREEN),
            ], estado["mobile"], spacing=10),
            criar_layout_form([
                btn_salvar,
                criar_botao_secundario("Cancelar", ft.Icons.CANCEL, cancelar_edit, color=ft.Colors.GREY),
            ], estado["mobile"],spacing=10),
            ft.Divider(),
            ft.Text("Livros cadastrados", weight="bold"),
            *linhas,
        ], spacing=12)
        return ft.ListView([lista], expand=True, padding=20, spacing=20)
