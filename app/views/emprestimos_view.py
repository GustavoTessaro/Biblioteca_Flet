import flet as ft

from core.helpers import *
from services.cliente_service import *
from components.buttons import *
from components.layout import criar_layout_form
from data.salvarAtualizar import salvar_e_atualizar
from components.cards import mostrar_snack
from services.livro_service import livro_esta_emprestado
from datetime import timedelta

def view_emprestimos(page, dados, estado, route_change, navegar):
        emprestimo_cliente = ft.Dropdown(
            label="Cliente",
            width=250,
            options=[
                ft.dropdown.Option(
                    str(c["id"]),
                    c["nome"]
                )
                for c in dados["clientes"]
            ]
        )

        emprestimo_livro = ft.Dropdown(
            label="Livro",
            width=250,
            options=[
                ft.dropdown.Option(
                    str(l["id"]),
                    l["titulo"]
                )
                for l in dados["livros"]
            ]
        )
        
        def atualizar_dropdown_emprestimo():
            emprestimo_cliente.options = [
                ft.dropdown.Option(str(cliente["id"]), cliente["nome"])
                for cliente in dados["clientes"]
            ]
            emprestimo_livro.options = [
                ft.dropdown.Option(str(livro["id"]), f"{livro['titulo']} ({livro['autor']})")
                for livro in dados["livros"]
                if not livro_esta_emprestado(livro["id"], dados)
            ]
        
        
        async def cadastrar_emprestimo(e):
            if not emprestimo_cliente.value or not emprestimo_livro.value:
                await mostrar_snack(page, "Escolha cliente e livro.", ft.Colors.RED_700)
                return
            cliente_id = int(emprestimo_cliente.value)
            livro_id = int(emprestimo_livro.value)
            livro = obter_por_id(dados["livros"], livro_id)
            prateleira = obter_por_id(dados["prateleiras"], livro["prateleira_id"]) if livro else None
            if not livro or not prateleira:
                await mostrar_snack(page, "Livro ou prateleira inválidos.", ft.Colors.RED_700)
                return
            emprestimos_abertos = livro_esta_emprestado(livro_id, dados)
            quantidade = livro.get("quantidade", 1)
            if emprestimos_abertos >= quantidade:
                await mostrar_snack(page, "Não há cópias disponíveis deste livro.", ft.Colors.RED_700)
                return

            hoje = date.today()
            dados["emprestimos"].append({
                "id": proximo_id(dados["emprestimos"]),
                "cliente_id": cliente_id,
                "livro_id": livro_id,
                "status": "Aberto",
                "data_emprestimo": formatar_data(hoje),
                "data_entrega": formatar_data(hoje + timedelta(days=prateleira["dias_e_prazo"])),
            })
            emprestimo_cliente.value = None
            emprestimo_livro.value = None
            await salvar_e_atualizar(page, dados, route_change, atualizar_dropdown_emprestimo,"Empréstimo cadastrado.")

        async def acionar_devolucao(emprestimo_id):
            emprestimo = obter_por_id(dados["emprestimos"], emprestimo_id)
            if not emprestimo:
                await mostrar_snack(page, "Empréstimo não encontrado.", ft.Colors.RED_700)
                return
            
            multa = next((m for m in dados["multas"] if m["emprestimo_id"] == emprestimo_id and m["status"] == "Pendente"), None)
            
            if multa:
                async def confirmar_devolucao(e):
                    await finalizar_devolucao(None, emprestimo_id, multa, dlg)

                dlg = ft.AlertDialog(
                    title=ft.Text(f"Devolução com Multa"),
                    content=ft.Column([
                        ft.Text(f"Este empréstimo tem uma multa de R${multa['valor']:.2f}"),
                        ft.Text("O cliente pagou a multa?"),
                    ], spacing=10, tight=True),
                    actions=[
                        ft.TextButton("Não (Ir para Multas)", on_click=lambda e: fechar_e_ir_para_multas(dlg)),
                        ft.TextButton("Sim (Finalizar Devolução)", on_click=confirmar_devolucao),
                    ],
                )
                # ── CORREÇÃO 1: Adiciona o diálogo no overlay de forma moderna
                page.dialog = dlg
                dlg.open = True
                page.update()
            else:
                await finalizar_devolucao(None, emprestimo_id, None, None)

        def fechar_e_ir_para_multas(dlg):
            dlg.open = False  # Fecha o aviso antes de mudar de tela
            page.update()
            navegar("/multas")

        async def finalizar_devolucao(e, emprestimo_id, multa_paga, dlg):
            emprestimo = obter_por_id(dados["emprestimos"], emprestimo_id)
            if emprestimo:
                emprestimo["status"] = "Entregue"
                if multa_paga:
                    multa_paga["status"] = "Pago"
                
                # ── CORREÇÃO 2: Se houver um diálogo aberto, fecha ele aqui
                if dlg:
                    dlg.open = False
                    page.update()
                
                await salvar_e_atualizar(page, dados, route_change, atualizar_dropdown_emprestimo,"Devolução registrada com sucesso.")

        linhas = []
        for emprestimo in dados["emprestimos"]:
            cliente = obter_por_id(dados["clientes"], emprestimo["cliente_id"])
            livro = obter_por_id(dados["livros"], emprestimo["livro_id"])

            async def on_devolver(e, eid=emprestimo["id"]):
                await acionar_devolucao(eid)

            linhas.append(
                ft.ListTile(
                    title=ft.Text(f"{livro['titulo'] if livro else 'Livro removido'}", weight="bold"),
                    subtitle=ft.Column([
                        ft.Text(f"Cliente: {cliente['nome'] if cliente else 'Removido'}", size=12),
                        ft.Text(f"Status: {emprestimo['status']}", size=12, weight="bold"),
                        ft.Text(f"Emprestado: {emprestimo['data_emprestimo']}", size=11),
                        ft.Text(f"Devolução prevista: {emprestimo['data_entrega']}", size=11),
                    ], spacing=2),
                    trailing=criar_botao_primario("Devolver", ft.Icons.UNDO, on_devolver, bgcolor=ft.Colors.ORANGE)
                    if emprestimo["status"] in [STATUS_ABERTO, STATUS_ATRASADO] else ft.Text("Concluído", color=ft.Colors.GREEN),
                )
            )

        lista = ft.Column([
            criar_layout_form([
                emprestimo_cliente,
                emprestimo_livro,
                criar_botao_primario("Cadastrar", ft.Icons.ADD, cadastrar_emprestimo, bgcolor=ft.Colors.GREEN),
            ], estado["mobile"], spacing=10),
            ft.Divider(),
            ft.Text("Empréstimos", weight="bold"),
            *linhas,
        ], spacing=12)
        return ft.ListView([lista], expand=True, padding=20, spacing=20)
