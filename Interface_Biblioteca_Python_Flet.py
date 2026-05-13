import json
import os
from datetime import date, timedelta

import flet as ft

DATA_FILE = "biblioteca_data.json"
BREAKPOINT_MOBILE = 600


def carregar_dados() -> dict:
    if not os.path.exists(DATA_FILE):
        return {
            "clientes": [],
            "prateleiras": [],
            "livros": [],
            "emprestimos": [],
            "multas": [],
        }

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)
    except Exception:
        return {
            "clientes": [],
            "prateleiras": [],
            "livros": [],
            "emprestimos": [],
            "multas": [],
        }


def salvar_dados(dados: dict):
    with open(DATA_FILE, "w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, indent=2, ensure_ascii=False)


def formatar_data(valor: date) -> str:
    return valor.isoformat()


def parse_data(texto: str) -> date:
    return date.fromisoformat(texto)


def proximo_id(lista: list) -> int:
    if not lista:
        return 1
    return max(item["id"] for item in lista) + 1


def obter_por_id(lista: list, id_valor: int) -> dict | None:
    return next((item for item in lista if item["id"] == id_valor), None)


def calcular_valor_multa(dias_atraso: int, valor_por_dia: float) -> float:
    return round(dias_atraso * valor_por_dia, 2)


def obter_status_emprestimo(emprestimo: dict, hoje: date) -> str:
    if emprestimo["status"] == "Entregue":
        return "Entregue"
    data_entrega = parse_data(emprestimo["data_entrega"])
    if hoje > data_entrega:
        return "Atrasado"
    return "Aberto"


def verificar_atrasos_e_multas(dados: dict):
    hoje = date.today()
    for emprestimo in dados["emprestimos"]:
        if emprestimo["status"] != "Entregue":
            novo_status = obter_status_emprestimo(emprestimo, hoje)
            emprestimo["status"] = novo_status

            if novo_status == "Atrasado":
                livro = obter_por_id(dados["livros"], emprestimo["livro_id"])
                prateleira = obter_por_id(dados["prateleiras"], livro["prateleira_id"]) if livro else None
                if livro and prateleira:
                    dias_atraso = (hoje - parse_data(emprestimo["data_entrega"])).days
                    valor = calcular_valor_multa(dias_atraso, prateleira.get("multa_por_dia", 1.0))

                    multa_existente = next(
                        (m for m in dados["multas"] if m["emprestimo_id"] == emprestimo["id"]),
                        None,
                    )
                    if multa_existente:
                        if multa_existente["status"] == "Pendente":
                            multa_existente["dias_atraso"] = dias_atraso
                            multa_existente["valor"] = valor
                    else:
                        dados["multas"].append({
                            "id": proximo_id(dados["multas"]),
                            "emprestimo_id": emprestimo["id"],
                            "cliente_id": emprestimo["cliente_id"],
                            "livro_id": emprestimo["livro_id"],
                            "dias_atraso": dias_atraso,
                            "valor": valor,
                            "status": "Pendente",
                        })

    salvar_dados(dados)


def main(page: ft.Page):
    page.title = "Biblioteca Flet"
    page.padding = 0
    page.spacing = 0
    page.window_maximized = True
    page.theme = ft.Theme(color_scheme_seed=ft.Colors.BLUE)
    page.dark_theme = ft.Theme(color_scheme_seed=ft.Colors.INDIGO)
    page.theme_mode = ft.ThemeMode.LIGHT

    dados = carregar_dados()
    verificar_atrasos_e_multas(dados)

    estado = {
        "rota": "/",
    }

    cliente_nome = ft.TextField(label="Nome do cliente", expand=True, border_radius=8)
    cliente_email = ft.TextField(label="E-mail do cliente", expand=True, border_radius=8)

    prateleira_nome = ft.TextField(label="Nome da prateleira", expand=True, border_radius=8)
    prateleira_dias = ft.TextField(label="Dias de empréstimo", hint_text="7", expand=True, border_radius=8)
    prateleira_multa = ft.TextField(label="Multa por dia", hint_text="1.5", expand=True, border_radius=8)

    livro_titulo = ft.TextField(label="Título do livro", expand=True, border_radius=8)
    livro_autor = ft.TextField(label="Autor", expand=True, border_radius=8)
    livro_prateleira = ft.Dropdown(label="Prateleira", expand=True)

    emprestimo_cliente = ft.Dropdown(label="Cliente", expand=True)
    emprestimo_livro = ft.Dropdown(label="Livro disponível", expand=True)

    def mostrar_snack(msg: str, cor=ft.Colors.GREEN_700):
        snackbar = ft.SnackBar(content=ft.Text(msg, color=ft.Colors.WHITE), bgcolor=cor, duration=2500)
        page.snack_bar = snackbar
        snackbar.open = True
        page.update()

    def atualizar_dropdowns():
        livro_prateleira.options = [
            ft.dropdown.Option(str(prateleira["id"]), prateleira["nome"])
            for prateleira in dados["prateleiras"]
        ]
        emprestimo_cliente.options = [
            ft.dropdown.Option(str(cliente["id"]), cliente["nome"])
            for cliente in dados["clientes"]
        ]
        emprestimo_livro.options = [
            ft.dropdown.Option(str(livro["id"]), f"{livro['titulo']} ({livro['autor']})")
            for livro in dados["livros"]
            if not any(
                emprestimo["livro_id"] == livro["id"] and emprestimo["status"] in ["Aberto", "Atrasado"]
                for emprestimo in dados["emprestimos"]
            )
        ]

    def salvar_e_atualizar():
        salvar_dados(dados)
        verificar_atrasos_e_multas(dados)
        atualizar_dropdowns()
        route_change()

    def navegar(rota: str):
        estado["rota"] = rota
        route_change()

    def criar_card(titulo: str, conteudo: ft.Control) -> ft.Container:
        return ft.Container(
            content=ft.Column([ft.Text(titulo, size=13, weight="bold"), conteudo], spacing=10, tight=True),
            padding=16,
            bgcolor=ft.Colors.WHITE,
            border=ft.Border.all(1, ft.Colors.GREY_300),
            border_radius=12,
            shadow=ft.BoxShadow(color=ft.Colors.GREY_300, blur_radius=10, offset=ft.Offset(0, 2)),
        )

    def criar_botao(texto: str, on_click, cor=ft.Colors.BLUE):
        return ft.ElevatedButton(content=ft.Text(texto), on_click=on_click, bgcolor=cor, color=ft.Colors.WHITE)

    def renderizar_menu():
        opcoes = [
            ("/", "Home"),
            ("/clientes", "Clientes"),
            ("/prateleiras", "Prateleiras"),
            ("/livros", "Livros"),
            ("/emprestimos", "Empréstimos"),
            ("/multas", "Multas"),
        ]
        itens = []
        for rota, label in opcoes:
            ativo = rota == estado["rota"]
            itens.append(
                ft.TextButton(
                    content=ft.Text(label),
                    on_click=lambda e, dest=rota: navegar(dest),
                    style=ft.ButtonStyle(
                        color=ft.Colors.WHITE if ativo else ft.Colors.BLACK,
                        bgcolor=ft.Colors.BLUE_700 if ativo else ft.Colors.BLUE_50,
                    ),
                )
            )
        return ft.Row(itens, wrap=True, spacing=10)

    def view_home():
        total_clientes = len(dados["clientes"])
        total_prateleiras = len(dados["prateleiras"])
        total_livros = len(dados["livros"])
        total_emprestimos = len(dados["emprestimos"])
        total_abertos = sum(1 for e in dados["emprestimos"] if e["status"] == "Aberto")
        total_atrasados = sum(1 for e in dados["emprestimos"] if e["status"] == "Atrasado")
        total_multas = sum(1 for m in dados["multas"] if m["status"] == "Pendente")

        cards = ft.Row(
            [
                criar_card("Clientes cadastrados", ft.Text(str(total_clientes), size=24, weight="bold")),
                criar_card("Prateleiras", ft.Text(str(total_prateleiras), size=24, weight="bold")),
                criar_card("Livros cadastrados", ft.Text(str(total_livros), size=24, weight="bold")),
                criar_card("Empréstimos em aberto", ft.Text(str(total_abertos), size=24, weight="bold")),
                criar_card("Empréstimos atrasados", ft.Text(str(total_atrasados), size=24, weight="bold")),
                criar_card("Multas pendentes", ft.Text(str(total_multas), size=24, weight="bold")),
            ],
            wrap=True,
            spacing=16,
        )
        return ft.ListView([cards], expand=True, padding=20, spacing=20)

    def view_clientes():
        def adicionar_cliente(e):
            nome = cliente_nome.value.strip()
            email = cliente_email.value.strip()
            if not nome:
                mostrar_snack("Digite o nome do cliente.", ft.Colors.RED_700)
                return
            dados["clientes"].append({
                "id": proximo_id(dados["clientes"]),
                "nome": nome,
                "email": email,
            })
            cliente_nome.value = ""
            cliente_email.value = ""
            salvar_e_atualizar()
            mostrar_snack("Cliente cadastrado com sucesso.")

        lista = ft.Column([
            ft.Row([
                cliente_nome,
                cliente_email,
                criar_botao("Cadastrar", adicionar_cliente, ft.Colors.GREEN),
            ], spacing=10),
            ft.Divider(),
            ft.Text("Clientes cadastrados", weight="bold"),
            *[
                ft.ListTile(
                    title=ft.Text(cliente["nome"]),
                    subtitle=ft.Text(cliente["email"] or "Sem e-mail"),
                )
                for cliente in dados["clientes"]
            ],
        ], spacing=16)
        return ft.ListView([lista], expand=True, padding=20, spacing=20)

    def view_prateleiras():
        def adicionar_prateleira(e):
            nome = prateleira_nome.value.strip()
            dias = prateleira_dias.value.strip()
            multa = prateleira_multa.value.strip()
            if not nome or not dias.isdigit():
                mostrar_snack("Preencha nome e dias de empréstimo válidos.", ft.Colors.RED_700)
                return
            dados["prateleiras"].append({
                "id": proximo_id(dados["prateleiras"]),
                "nome": nome,
                "dias_e_prazo": int(dias),
                "multa_por_dia": float(multa.replace(",", ".")) if multa else 1.0,
            })
            prateleira_nome.value = ""
            prateleira_dias.value = ""
            prateleira_multa.value = ""
            salvar_e_atualizar()
            mostrar_snack("Prateleira cadastrada.")

        lista = ft.Column([
            ft.Row([
                prateleira_nome,
                prateleira_dias,
                prateleira_multa,
                criar_botao("Cadastrar", adicionar_prateleira, ft.Colors.GREEN),
            ], spacing=10),
            ft.Divider(),
            ft.Text("Prateleiras cadastradas", weight="bold"),
            *[
                ft.ListTile(
                    title=ft.Text(prateleira["nome"]),
                    subtitle=ft.Text(f"Prazo: {prateleira['dias_e_prazo']} dias · Multa/dia: R${prateleira['multa_por_dia']:.2f}"),
                )
                for prateleira in dados["prateleiras"]
            ],
        ], spacing=16)
        return ft.ListView([lista], expand=True, padding=20, spacing=20)

    def view_livros():
        def adicionar_livro(e):
            titulo = livro_titulo.value.strip()
            autor = livro_autor.value.strip()
            prateleira_id = int(livro_prateleira.value) if livro_prateleira.value else None
            if not titulo or not autor or prateleira_id is None:
                mostrar_snack("Preencha título, autor e prateleira.", ft.Colors.RED_700)
                return
            dados["livros"].append({
                "id": proximo_id(dados["livros"]),
                "titulo": titulo,
                "autor": autor,
                "prateleira_id": prateleira_id,
            })
            livro_titulo.value = ""
            livro_autor.value = ""
            livro_prateleira.value = None
            salvar_e_atualizar()
            mostrar_snack("Livro cadastrado.")

        linhas = []
        for livro in dados["livros"]:
            emprestado = any(
                emprestimo["livro_id"] == livro["id"] and emprestimo["status"] in ["Aberto", "Atrasado"]
                for emprestimo in dados["emprestimos"]
            )
            prateleira = obter_por_id(dados["prateleiras"], livro["prateleira_id"])
            linhas.append(
                ft.ListTile(
                    title=ft.Text(livro["titulo"]),
                    subtitle=ft.Text(f"Autor: {livro['autor']} · Prateleira: {prateleira['nome'] if prateleira else 'Sem prateleira'}"),
                    trailing=ft.Text("Emprestado" if emprestado else "Disponível", color=ft.Colors.RED if emprestado else ft.Colors.GREEN),
                )
            )

        lista = ft.Column([
            ft.Row([
                livro_titulo,
                livro_autor,
                livro_prateleira,
                criar_botao("Cadastrar", adicionar_livro, ft.Colors.GREEN),
            ], spacing=10),
            ft.Divider(),
            ft.Text("Livros cadastrados", weight="bold"),
            *linhas,
        ], spacing=16)
        return ft.ListView([lista], expand=True, padding=20, spacing=20)

    def view_emprestimos():
        def cadastrar_emprestimo(e):
            if not emprestimo_cliente.value or not emprestimo_livro.value:
                mostrar_snack("Escolha cliente e livro.", ft.Colors.RED_700)
                return
            cliente_id = int(emprestimo_cliente.value)
            livro_id = int(emprestimo_livro.value)
            livro = obter_por_id(dados["livros"], livro_id)
            prateleira = obter_por_id(dados["prateleiras"], livro["prateleira_id"]) if livro else None
            if not livro or not prateleira:
                mostrar_snack("Livro ou prateleira inválidos.", ft.Colors.RED_700)
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
            salvar_e_atualizar()
            mostrar_snack("Empréstimo cadastrado.")

        def entregar_emprestimo(e, emprestimo_id: int):
            emprestimo = obter_por_id(dados["emprestimos"], emprestimo_id)
            if emprestimo:
                emprestimo["status"] = "Entregue"
                salvar_e_atualizar()
                mostrar_snack("Livro entregue.")

        linhas = []
        for emprestimo in dados["emprestimos"]:
            cliente = obter_por_id(dados["clientes"], emprestimo["cliente_id"])
            livro = obter_por_id(dados["livros"], emprestimo["livro_id"])
            linhas.append(
                ft.ListTile(
                    title=ft.Text(f"{livro['titulo'] if livro else 'Livro removido'}"),
                    subtitle=ft.Text(
                        f"Cliente: {cliente['nome'] if cliente else 'Removido'} · "
                        f"Status: {emprestimo['status']} · Emprestado: {emprestimo['data_emprestimo']} · "
                        f"Entrega: {emprestimo['data_entrega']}"
                    ),
                    trailing=ft.Row([
                        criar_botao("Entregar", lambda e, id=emprestimo['id']: entregar_emprestimo(e, id), ft.Colors.ORANGE)
                        if emprestimo["status"] in ["Aberto", "Atrasado"] else ft.Text("Concluído", color=ft.Colors.GREEN)
                    ], spacing=5),
                )
            )

        lista = ft.Column([
            ft.Row([
                emprestimo_cliente,
                emprestimo_livro,
                criar_botao("Cadastrar", cadastrar_emprestimo, ft.Colors.GREEN),
            ], spacing=10),
            ft.Divider(),
            ft.Text("Empréstimos", weight="bold"),
            *linhas,
        ], spacing=16)
        return ft.ListView([lista], expand=True, padding=20, spacing=20)

    def view_multas():
        def pagar_multa(e, multa_id: int):
            multa = obter_por_id(dados["multas"], multa_id)
            if multa:
                multa["status"] = "Pago"
                salvar_e_atualizar()
                mostrar_snack("Multa marcada como paga.")

        linhas = []
        for multa in dados["multas"]:
            cliente = obter_por_id(dados["clientes"], multa["cliente_id"])
            livro = obter_por_id(dados["livros"], multa["livro_id"])
            linhas.append(
                ft.ListTile(
                    title=ft.Text(f"{cliente['nome'] if cliente else 'Cliente removido'}"),
                    subtitle=ft.Text(
                        f"Livro: {livro['titulo'] if livro else 'Livro removido'} · "
                        f"Valor: R${multa['valor']:.2f} · Dias de atraso: {multa['dias_atraso']}"
                    ),
                    trailing=ft.Row([
                        criar_botao("Pagar", lambda e, id=multa['id']: pagar_multa(e, id), ft.Colors.GREEN)
                        if multa["status"] == "Pendente" else ft.Text("Pago", color=ft.Colors.GREEN)
                    ], spacing=5),
                )
            )

        return ft.ListView([
            ft.Column([
                ft.Text("Multas geradas", weight="bold"),
                *linhas,
            ], spacing=16)
        ], expand=True, padding=20, spacing=20)

    def route_change():
        atualizar_dropdowns()
        page.controls.clear()
        page.add(
            ft.Column([
                ft.Container(
                    content=ft.Column([
                        ft.Text("Sistema de Biblioteca", size=24, weight="bold"),
                        renderizar_menu(),
                    ], tight=True),
                    padding=ft.Padding(20, 20, 20, 10),
                ),
                ft.Divider(),
                {"/": view_home,
                 "/clientes": view_clientes,
                 "/prateleiras": view_prateleiras,
                 "/livros": view_livros,
                 "/emprestimos": view_emprestimos,
                 "/multas": view_multas}[estado["rota"]](),
            ], spacing=0)
        )
        page.update()

    route_change()


if __name__ == "__main__":
    ft.app(target=main)

