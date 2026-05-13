import json
import os
import asyncio
from datetime import date, timedelta

import flet as ft

DATA_FILE = "biblioteca_data.json"
BREAKPOINT_MOBILE = 600

_indice_rotas = ["/", "/clientes", "/livros", "/emprestimos", "/multas"]

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

#region Funções

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
            #Verificar Depois se o JSON estiver corrompido perde os dados silenciosamente. 
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

def livro_esta_emprestado(livro_id: int, dados: dict) -> bool:
    return any(
        emprestimo["livro_id"] == livro_id and emprestimo["status"] in ["Aberto", "Atrasado"]
        for emprestimo in dados["emprestimos"]
    )

def prateleira_tem_livros(prateleira_id: int, dados: dict) -> bool:
    return any(livro["prateleira_id"] == prateleira_id for livro in dados["livros"])

def cliente_tem_emprestimos_ativos(cliente_id: int, dados: dict) -> bool:
    return any(
        emprestimo["cliente_id"] == cliente_id and emprestimo["status"] in ["Aberto", "Atrasado"]
        for emprestimo in dados["emprestimos"]
    )

#endregion

def main(page: ft.Page):
    
    #region Configurações da Página e Estado
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
        "cliente_edit_id": None,
        "prateleira_edit_id": None,
        "livro_edit_id": None,
        "mobile": page.width < BREAKPOINT_MOBILE,
        "dark_mode": False,
    }
    
    #endregion

    #region TextFields e Dropdowns

    # TextField para clientes
    cliente_nome = ft.TextField(label="Nome do cliente", hint_text="Ex: João Alberto",  prefix_icon=ft.Icons.PERSON_OUTLINE, expand=True, border_radius=8)
    cliente_email = ft.TextField(label="E-mail do cliente", hint_text="Ex: joao@email.com", prefix_icon=ft.Icons.EMAIL_OUTLINED, expand=True, border_radius=8, keyboard_type=ft.KeyboardType.EMAIL)
    cliente_telefone = ft.TextField(label="Telefone", hint_text="Ex: (49) 9 9999-9999", prefix_icon=ft.Icons.PHONE_OUTLINED, expand=True, border_radius=8, keyboard_type=ft.KeyboardType.PHONE)

    # TextField para prateleiras
    prateleira_nome = ft.TextField(label="Nome da prateleira", hint_text="Ex: Terror", prefix_icon=ft.Icons.TABLE_ROWS_OUTLINED, expand=True, border_radius=8)
    prateleira_dias = ft.TextField(label="Dias de empréstimo", hint_text="Ex: 7", prefix_icon=ft.Icons.CALENDAR_TODAY_OUTLINED, expand=True, border_radius=8)
    prateleira_multa = ft.TextField(label="Multa por dia", hint_text="Ex: 1.5", prefix_icon=ft.Icons.MONETIZATION_ON_OUTLINED, expand=True, border_radius=8)

    # TextField para livros
    livro_titulo = ft.TextField(label="Título do livro", hint_text="Ex: Senhor dos Anéis", prefix_icon=ft.Icons.BOOK_OUTLINED, expand=True, border_radius=8)
    livro_autor = ft.TextField(label="Autor", hint_text="Ex: J.R.R. Tolkien", prefix_icon=ft.Icons.CREATE_OUTLINED, expand=True, border_radius=8)
    livro_prateleira = ft.Dropdown(label="Prateleira", leading_icon=ft.Icons.LAYERS_OUTLINED, expand=True)

    # Dropdown para empréstimos
    emprestimo_cliente = ft.Dropdown(label="Cliente", leading_icon=ft.Icons.PERSON_OUTLINE, expand=True)
    emprestimo_livro = ft.Dropdown(label="Livro disponível", leading_icon=ft.Icons.MENU_BOOK_OUTLINED, expand=True)

    #endregion

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
            if not livro_esta_emprestado(livro["id"], dados)
        ]

    def salvar_e_atualizar():
        salvar_dados(dados)
        verificar_atrasos_e_multas(dados)
        atualizar_dropdowns()
        route_change()

    def navegar(rota: str):
        page.go(rota)

    def criar_card(titulo: str, conteudo: ft.Control, p: dict | None = None):
        if p is None:
            p = paleta(estado["dark_mode"])

        return ft.Container(
            content=ft.Column([
                ft.Text(
                    titulo,
                    size=13,
                    weight="bold",
                    color=p["txt"]
                ),
                conteudo,
            ]),
            padding=16,
            bgcolor=p["bg_card"],
            border=ft.border.all(1, p["border"]),
            border_radius=12,
            shadow=ft.BoxShadow(
                blur_radius=8,
                color=p["shadow"],
                offset=ft.Offset(0, 2),
            ),
        )

    def criar_botao_primario(texto: str, icone, on_click, expand=False, bgcolor=ft.Colors.BLUE_700, color=ft.Colors.WHITE):
        return ft.ElevatedButton(  # <── Alterado para ElevatedButton
            content=ft.Row([
                ft.Icon(icone, size=16),
                ft.Text(texto, size=14) if texto else ft.Container(), # Trata botões que só têm ícone
            ], spacing=6 if texto else 0, tight=True),
            on_click=on_click,
            expand=expand,
            style=ft.ButtonStyle(
                bgcolor=bgcolor,
                color=color,
                shape=ft.RoundedRectangleBorder(radius=8),
            ),
        )
        
    def criar_botao_secundario(texto: str, icone, on_click, expand=False, color=ft.Colors.BLUE_700):
        return ft.OutlinedButton(  # <── Alterado para OutlinedButton
            content=ft.Row([
                ft.Icon(icone, size=16),
                ft.Text(texto, size=14),
            ], spacing=6, tight=True),
            on_click=on_click,
            expand=expand,
            style=ft.ButtonStyle(
                color=color,
                shape=ft.RoundedRectangleBorder(radius=8),
            ),
        )

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
            ativo = rota == page.route 
            itens.append(
            ft.TextButton(
                content=ft.Text(label),
                on_click=lambda e, dest=rota: navegar(dest),
                style=ft.ButtonStyle(
                    color=ft.Colors.WHITE if ativo else ft.Colors.BLUE_700,
                    bgcolor=ft.Colors.BLUE_700 if ativo else ft.Colors.BLUE_50,
                    shape=ft.RoundedRectangleBorder(radius=8),
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
                criar_card("Clientes", ft.Text(str(total_clientes), size=24, weight="bold")),
                criar_card("Prateleiras", ft.Text(str(total_prateleiras), size=24, weight="bold")),
                criar_card("Livros", ft.Text(str(total_livros), size=24, weight="bold")),
                criar_card("Em aberto", ft.Text(str(total_abertos), size=24, weight="bold")),
                criar_card("Atrasados", ft.Text(str(total_atrasados), size=24, weight="bold")),
                criar_card("Multas", ft.Text(str(total_multas), size=24, weight="bold")),
            ],
            wrap=True,
            spacing=16,
        )
        return ft.ListView([cards], expand=True, padding=20, spacing=20)

    def view_clientes():
        def adicionar_cliente(e):
            nome = cliente_nome.value.strip()
            email = cliente_email.value.strip()
            telefone = cliente_telefone.value.strip()
            if not nome:
                mostrar_snack("Digite o nome do cliente.", ft.Colors.RED_700)
                return
            dados["clientes"].append({
                "id": proximo_id(dados["clientes"]),
                "nome": nome,
                "email": email,
                "telefone": telefone,
            })
            cliente_nome.value = ""
            cliente_email.value = ""
            cliente_telefone.value = ""
            salvar_e_atualizar()
            mostrar_snack("Cliente cadastrado com sucesso.")

        def editar_cliente(cliente_id):
            cliente = obter_por_id(dados["clientes"], cliente_id)
            if not cliente:
                return
            cliente_nome.value = cliente["nome"]
            cliente_email.value = cliente.get("email", "")
            cliente_telefone.value = cliente.get("telefone", "")
            estado["cliente_edit_id"] = cliente_id
            route_change()

        def salvar_cliente_edit(e):
            if not estado["cliente_edit_id"]:
                return
            cliente = obter_por_id(dados["clientes"], estado["cliente_edit_id"])
            if not cliente:
                return
            cliente["nome"] = cliente_nome.value.strip()
            cliente["email"] = cliente_email.value.strip()
            cliente["telefone"] = cliente_telefone.value.strip()
            cliente_nome.value = ""
            cliente_email.value = ""
            cliente_telefone.value = ""
            estado["cliente_edit_id"] = None
            salvar_e_atualizar()
            mostrar_snack("Cliente atualizado.")

        def deletar_cliente(cliente_id):
            if cliente_tem_emprestimos_ativos(cliente_id, dados):
                mostrar_snack("Não pode deletar cliente com empréstimos ativos.", ft.Colors.RED_700)
                return
            dados["clientes"][:] = [c for c in dados["clientes"] if c["id"] != cliente_id]
            salvar_e_atualizar()
            mostrar_snack("Cliente removido.")

        def cancelar_edit(e):
            cliente_nome.value = ""
            cliente_email.value = ""
            cliente_telefone.value = ""
            estado["cliente_edit_id"] = None
            route_change()

        btn_salvar = criar_botao_primario(
            "Salvar",
            ft.Icons.SAVE,
            salvar_cliente_edit,
            bgcolor=ft.Colors.ORANGE if estado["cliente_edit_id"] else ft.Colors.GREY
        )

        linhas = []
        for cliente in dados["clientes"]:
            linhas.append(
                ft.ListTile(
                    title=ft.Text(cliente["nome"], weight="bold"),
                    subtitle=ft.Column([
                        ft.Text(f"Email: {cliente.get('email', 'N/A')}", size=12),
                        ft.Text(f"Telefone: {cliente.get('telefone', 'N/A')}", size=12),
                    ], spacing=4),
                    trailing=ft.Row([
                        criar_botao_primario("", ft.Icons.EDIT, lambda e, cid=cliente["id"]: editar_cliente(cid), bgcolor=ft.Colors.BLUE),
                        criar_botao_primario("", ft.Icons.DELETE, lambda e, cid=cliente["id"]: deletar_cliente(cid), bgcolor=ft.Colors.RED),
                    ], spacing=5, tight=True),
                    is_three_line=True,
                    min_vertical_padding=8,
                )
            )

        lista = ft.Column([
            ft.Row([
                cliente_nome,
                cliente_email,
                cliente_telefone,
                criar_botao_primario("Cadastrar", ft.Icons.ADD, adicionar_cliente, bgcolor=ft.Colors.GREEN),
            ], spacing=10),
            ft.Row([btn_salvar, criar_botao_secundario("Cancelar", ft.Icons.CANCEL, cancelar_edit, color=ft.Colors.GREY)], spacing=10),
            ft.Divider(),
            ft.Text("Clientes cadastrados", weight="bold"),
            *linhas,
        ], spacing=12)
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

        def editar_prateleira(prateleira_id):
            prateleira = obter_por_id(dados["prateleiras"], prateleira_id)
            if not prateleira:
                return
            prateleira_nome.value = prateleira["nome"]
            prateleira_dias.value = str(prateleira["dias_e_prazo"])
            prateleira_multa.value = str(prateleira["multa_por_dia"])
            estado["prateleira_edit_id"] = prateleira_id
            route_change()

        def salvar_prateleira_edit(e):
            if not estado["prateleira_edit_id"]:
                return
            prateleira = obter_por_id(dados["prateleiras"], estado["prateleira_edit_id"])
            if not prateleira:
                return
            dias = prateleira_dias.value.strip()
            if not dias.isdigit():
                mostrar_snack("Dias deve ser um número válido.", ft.Colors.RED_700)
                return
            prateleira["nome"] = prateleira_nome.value.strip()
            prateleira["dias_e_prazo"] = int(dias)
            prateleira["multa_por_dia"] = float(prateleira_multa.value.strip().replace(",", ".")) if prateleira_multa.value.strip() else 1.0
            prateleira_nome.value = ""
            prateleira_dias.value = ""
            prateleira_multa.value = ""
            estado["prateleira_edit_id"] = None
            salvar_e_atualizar()
            mostrar_snack("Prateleira atualizada.")

        def deletar_prateleira(prateleira_id):
            if prateleira_tem_livros(prateleira_id, dados):
                mostrar_snack("Não pode deletar prateleira que tem livros cadastrados.", ft.Colors.RED_700)
                return
            dados["prateleiras"][:] = [p for p in dados["prateleiras"] if p["id"] != prateleira_id]
            salvar_e_atualizar()
            mostrar_snack("Prateleira removida.")

        def cancelar_edit(e):
            prateleira_nome.value = ""
            prateleira_dias.value = ""
            prateleira_multa.value = ""
            estado["prateleira_edit_id"] = None
            route_change()

        btn_salvar = criar_botao_primario(
            "Salvar",
            ft.Icons.SAVE,
            salvar_prateleira_edit,
            bgcolor=ft.Colors.ORANGE if estado["prateleira_edit_id"] else ft.Colors.GREY
        )

        linhas = []
        for prateleira in dados["prateleiras"]:
            linhas.append(
                ft.ListTile(
                    title=ft.Text(prateleira["nome"], weight="bold"),
                    subtitle=ft.Text(
                        f"Prazo: {prateleira['dias_e_prazo']} dias · Multa/dia: R${prateleira['multa_por_dia']:.2f}",
                        size=12,
                    ),
                    trailing=ft.Row([
                        criar_botao_primario("", ft.Icons.EDIT, lambda e, pid=prateleira["id"]: editar_prateleira(pid), bgcolor=ft.Colors.BLUE),
                        criar_botao_primario("", ft.Icons.DELETE, lambda e, pid=prateleira["id"]: deletar_prateleira(pid), bgcolor=ft.Colors.RED),
                    ], spacing=5, tight=True),
                    min_vertical_padding=8,
                )
            )

        lista = ft.Column([
            ft.Row([
                prateleira_nome,
                prateleira_dias,
                prateleira_multa,
                criar_botao_primario("Cadastrar", ft.Icons.ADD, adicionar_prateleira, bgcolor=ft.Colors.GREEN),
            ], spacing=10),
            ft.Row([btn_salvar, criar_botao_secundario("Cancelar", ft.Icons.CANCEL, cancelar_edit, color=ft.Colors.GREY)], spacing=10),
            ft.Divider(),
            ft.Text("Prateleiras cadastradas", weight="bold"),
            *linhas,
        ], spacing=12)
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

        def editar_livro(livro_id):
            livro = obter_por_id(dados["livros"], livro_id)
            if not livro:
                return
            livro_titulo.value = livro["titulo"]
            livro_autor.value = livro["autor"]
            livro_prateleira.value = str(livro["prateleira_id"])
            estado["livro_edit_id"] = livro_id
            route_change() # ── ADICIONADO: Atualiza a tela para mudar o botão Salvar para Laranja

        def salvar_livro_edit(e):
            if not estado["livro_edit_id"]:
                return
            livro = obter_por_id(dados["livros"], estado["livro_edit_id"])
            if not livro:
                return
            livro["titulo"] = livro_titulo.value.strip()
            livro["autor"] = livro_autor.value.strip()
            livro["prateleira_id"] = int(livro_prateleira.value) if livro_prateleira.value else livro["prateleira_id"]
            livro_titulo.value = ""
            livro_autor.value = ""
            livro_prateleira.value = None
            estado["livro_edit_id"] = None
            salvar_e_atualizar()
            mostrar_snack("Livro atualizado.")

        def deletar_livro(livro_id):
            if livro_esta_emprestado(livro_id, dados):
                mostrar_snack("Não pode deletar livro que está emprestado.", ft.Colors.RED_700)
                return
            dados["livros"][:] = [l for l in dados["livros"] if l["id"] != livro_id]
            salvar_e_atualizar()
            mostrar_snack("Livro removido.")

        def cancelar_edit(e):
            livro_titulo.value = ""
            livro_autor.value = ""
            livro_prateleira.value = None
            estado["livro_edit_id"] = None
            route_change() # ── ALTERADO: Redesenha a tela limpando o estado de edição

        # Otimização: O botão de salvar só ativa a função se houver algo sendo editado
        btn_salvar = criar_botao_primario(
            "Salvar",
            ft.Icons.SAVE,
            salvar_livro_edit if estado["livro_edit_id"] else None,
            bgcolor=ft.Colors.ORANGE if estado["livro_edit_id"] else ft.Colors.GREY
        )

        linhas = []
        for livro in dados["livros"]:
            emprestado = livro_esta_emprestado(livro["id"], dados)
            prateleira = obter_por_id(dados["prateleiras"], livro["prateleira_id"])
            linhas.append(
                ft.ListTile(
                    title=ft.Text(livro["titulo"], weight="bold"),
                    subtitle=ft.Column([
                        ft.Text(f"Autor: {livro['autor']}", size=12),
                        ft.Text(f"Prateleira: {prateleira['nome'] if prateleira else 'Sem prateleira'}", size=12),
                    ], spacing=2),
                    trailing=ft.Row([
                        ft.Text("Emprestado" if emprestado else "Disponível", color=ft.Colors.RED if emprestado else ft.Colors.GREEN),
                        criar_botao_primario("", ft.Icons.EDIT, lambda e, lid=livro["id"]: editar_livro(lid), bgcolor=ft.Colors.BLUE) if not emprestado else ft.Container(),
                        criar_botao_primario("", ft.Icons.DELETE, lambda e, lid=livro["id"]: deletar_livro(lid), bgcolor=ft.Colors.RED) if not emprestado else ft.Container(),
                    ], spacing=5, tight=True), # ── ADICIONADO: tight=True evita bugs de tamanho na linha de ações
                )
            )

        lista = ft.Column([
            ft.Row([
                livro_titulo,
                livro_autor,
                livro_prateleira,
                criar_botao_primario("Cadastrar", ft.Icons.ADD, adicionar_livro, bgcolor=ft.Colors.GREEN),
            ], spacing=10),
            ft.Row([btn_salvar, criar_botao_secundario("Cancelar", ft.Icons.CANCEL, cancelar_edit, color=ft.Colors.GREY)], spacing=10),
            ft.Divider(),
            ft.Text("Livros cadastrados", weight="bold"),
            *linhas,
        ], spacing=12)
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

        def acionar_devolucao(emprestimo_id):
            emprestimo = obter_por_id(dados["emprestimos"], emprestimo_id)
            if not emprestimo:
                return
            
            multa = next((m for m in dados["multas"] if m["emprestimo_id"] == emprestimo_id and m["status"] == "Pendente"), None)
            
            if multa:
                # Criamos a estrutura do diálogo de forma isolada
                dlg = ft.AlertDialog(
                    title=ft.Text(f"Devolução com Multa"),
                    content=ft.Column([
                        ft.Text(f"Este empréstimo tem uma multa de R${multa['valor']:.2f}"),
                        ft.Text("O cliente pagou a multa?"),
                    ], spacing=10, tight=True),
                    actions=[
                        ft.TextButton("Não (Ir para Multas)", on_click=lambda e: fechar_e_ir_para_multas(dlg)),
                        ft.TextButton("Sim (Finalizar Devolução)", on_click=lambda e: finalizar_devolucao(e, emprestimo_id, multa, dlg)),
                    ],
                )
                # ── CORREÇÃO 1: Adiciona o diálogo no overlay de forma moderna
                page.dialog = dlg
                dlg.open = True
                page.update()
            else:
                finalizar_devolucao(None, emprestimo_id, None, None)

        def fechar_e_ir_para_multas(dlg):
            dlg.open = False  # Fecha o aviso antes de mudar de tela
            page.update()
            navegar("/multas")

        def finalizar_devolucao(e, emprestimo_id, multa_paga, dlg):
            emprestimo = obter_por_id(dados["emprestimos"], emprestimo_id)
            if emprestimo:
                emprestimo["status"] = "Entregue"
                if multa_paga:
                    multa_paga["status"] = "Pago"
                
                # ── CORREÇÃO 2: Se houver um diálogo aberto, fecha ele aqui
                if dlg:
                    dlg.open = False
                
                salvar_e_atualizar()
                mostrar_snack("Devolução registrada com sucesso.")

        linhas = []
        for emprestimo in dados["emprestimos"]:
            cliente = obter_por_id(dados["clientes"], emprestimo["cliente_id"])
            livro = obter_por_id(dados["livros"], emprestimo["livro_id"])
            linhas.append(
                ft.ListTile(
                    title=ft.Text(f"{livro['titulo'] if livro else 'Livro removido'}", weight="bold"),
                    subtitle=ft.Column([
                        ft.Text(f"Cliente: {cliente['nome'] if cliente else 'Removido'}", size=12),
                        ft.Text(f"Status: {emprestimo['status']}", size=12, weight="bold"),
                        ft.Text(f"Emprestado: {emprestimo['data_emprestimo']}", size=11),
                        ft.Text(f"Devolução prevista: {emprestimo['data_entrega']}", size=11),
                    ], spacing=2),
                    trailing=criar_botao_primario("Devolver", ft.Icons.UNDO, lambda e, eid=emprestimo['id']: acionar_devolucao(eid), bgcolor=ft.Colors.ORANGE)
                    if emprestimo["status"] in ["Aberto", "Atrasado"] else ft.Text("Concluído", color=ft.Colors.GREEN),
                )
            )

        lista = ft.Column([
            ft.Row([
                emprestimo_cliente,
                emprestimo_livro,
                criar_botao_primario("Cadastrar", ft.Icons.ADD, cadastrar_emprestimo, bgcolor=ft.Colors.GREEN),
            ], spacing=10),
            ft.Divider(),
            ft.Text("Empréstimos", weight="bold"),
            *linhas,
        ], spacing=12)
        return ft.ListView([lista], expand=True, padding=20, spacing=20)

    def view_multas():
        def marcar_multa_paga(multa_id):
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

    titulos_paginas = {
        "/": "Início - Painel Geral",
        "/clientes": "Gerenciar Clientes",
        "/prateleiras": "Gerenciar Prateleiras",
        "/livros": "Catálogo de Livros",
        "/emprestimos": "Controle de Empréstimos",
        "/multas": "Histórico de Multas"
    }

    rotas_menu = [
        ("/",            "Home",         ft.Icons.HOME_OUTLINED,         ft.Icons.HOME),
        ("/clientes",    "Clientes",     ft.Icons.PERSON_OUTLINE,        ft.Icons.PERSON),
        ("/prateleiras", "Prateleiras",  ft.Icons.TABLE_ROWS_OUTLINED,   ft.Icons.TABLE_ROWS),
        ("/livros",      "Livros",       ft.Icons.BOOK_OUTLINED,         ft.Icons.BOOK),
        ("/emprestimos", "Empréstimos",  ft.Icons.UNDO_OUTLINED,         ft.Icons.UNDO),
        ("/multas",      "Multas",       ft.Icons.MONETIZATION_ON_OUTLINED, ft.Icons.MONETIZATION_ON),
    ]

    def criar_item_menu(label: str, ic_off, ic_on, ativo: bool, on_click):
        return ft.Container(
            content=ft.Row([
                ft.Icon(ic_on if ativo else ic_off, color=ft.Colors.BLUE_700 if ativo else ft.Colors.BLACK, size=20),
                ft.Text(label, size=14, color=ft.Colors.BLUE_700 if ativo else ft.Colors.BLACK, weight="bold" if ativo else "normal"),
            ], spacing=12, tight=True),
            padding=ft.Padding(12, 10, 12, 10),
            border_radius=8,
            bgcolor=ft.Colors.BLUE_50 if ativo else ft.Colors.TRANSPARENT,
            on_click=on_click,
        )

    def menu_lateral():
        rota = estado["rota"]
        
        itens = [
            criar_item_menu(
                label, ic_off, ic_on,
                ativo=(rota == r),
                on_click=lambda e, dest=r: navegar(dest)
            )
            for r, label, ic_off, ic_on in rotas_menu
        ]

        perfil = ft.Container(
            content=ft.Row([
                ft.CircleAvatar(
                    content=ft.Text("ADM", size=10, weight="bold"),
                    bgcolor=ft.Colors.BLUE_700,
                    color=ft.Colors.WHITE,
                    radius=15,
                ),
                ft.Column([
                    ft.Text("Administrador", size=12, weight="bold", color=ft.Colors.BLACK),
                    ft.Text("● Online", size=10, color=ft.Colors.GREEN_400),
                ], spacing=0, tight=True, expand=True),
            ], spacing=8, tight=True),
            padding=ft.Padding(4, 8, 4, 0),
        )

        return ft.Container(
            width=215,
            bgcolor=ft.Colors.BLUE_50,
            border=ft.border.only(right=ft.BorderSide(1, ft.Colors.GREY_300)),
            padding=12,
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.MENU_BOOK, color=ft.Colors.BLUE_700, size=20),
                    ft.Text("BiblioFlet", size=16, weight="bold", color=ft.Colors.BLUE_700),
                ], spacing=8, tight=True),
                ft.Divider(height=16, color=ft.Colors.GREY_300),
                *itens,
                ft.Divider(height=16, color=ft.Colors.GREY_300),
                perfil,
            ], spacing=4, tight=True),
        )

    def toggle_theme():

        estado["dark_mode"] = not estado["dark_mode"]

        page.theme_mode = (
        ft.ThemeMode.DARK
        if estado["dark_mode"]
        else ft.ThemeMode.LIGHT
        )

        route_change()

    def navigation_bar_mobile():
        rota_atual = estado["rota"]
        idx = _indice_rotas.index(rota_atual) if rota_atual in _indice_rotas else 0

        def ao_mudar(e):
            # Como a sua função navegar agora usa asyncio, chamamos via task
            navegar(_indice_rotas[e.control.selected_index])

        return ft.NavigationBar(
            selected_index=idx,
            on_change=ao_mudar,
            destinations=[
                ft.NavigationBarDestination(icon=ft.Icons.HOME_OUTLINED, selected_icon=ft.Icons.HOME, label="Home"),
                ft.NavigationBarDestination(icon=ft.Icons.PERSON_OUTLINE, selected_icon=ft.Icons.PERSON, label="Clientes"),
                ft.NavigationBarDestination(icon=ft.Icons.BOOK_OUTLINED, selected_icon=ft.Icons.BOOK, label="Livros"),
                ft.NavigationBarDestination(icon=ft.Icons.UNDO_OUTLINED, selected_icon=ft.Icons.UNDO, label="Empréstimos"),
                ft.NavigationBarDestination(icon=ft.Icons.MONETIZATION_ON_OUTLINED, selected_icon=ft.Icons.MONETIZATION_ON, label="Multas"),
            ],
        )

    def construir_appbar():

        p = paleta(estado["dark_mode"])

        return ft.AppBar(
            leading=ft.Icon(
                ft.Icons.MENU_BOOK,
                color=p["txt"]
            ),

            leading_width=48,

            title=ft.Text(
                titulos_paginas.get(
                    estado["rota"],
                    "Sistema de Biblioteca"
                ),
                color=p["txt"],
                size=18,
                weight="bold",
            ),

            bgcolor=p["primary"],

            center_title=False,

            actions=[
                ft.IconButton(
                    icon=(
                        ft.Icons.DARK_MODE
                        if estado["dark_mode"]
                        else ft.Icons.LIGHT_MODE
                    ),

                    icon_color=ft.Colors.WHITE,

                    tooltip="Alternar tema",

                    on_click=lambda e: toggle_theme(),
                )
            ]
        )

    def route_change(e=None):
        p = paleta(estado["dark_mode"])
        
        if e is not None and hasattr(e, "route"):
            estado["rota"] = e.route

        atualizar_dropdowns()

        views_map = {
            "/": view_home,
            "/clientes": view_clientes,
            "/prateleiras": view_prateleiras,
            "/livros": view_livros,
            "/emprestimos": view_emprestimos,
            "/multas": view_multas
        }
        
        view_fn = views_map.get(estado["rota"], view_home)

        # ── CONFIGURAÇÃO DE LAYOUT RESPONSIVO ────────────────────────────────
        # Se for mobile, removemos o menu do topo para não duplicar a navegação
        if estado["mobile"]:
            # Layout Mobile (sem menu na tela, usa navigation_bar inferior nativa)
            conteudo_principal = ft.Container(
                content=view_fn(),
                padding=ft.Padding(20, 10, 20, 10),
                expand=True
            )
        else:
            # Layout Computador (Menu lateral à esquerda + Conteúdo à direita)
            conteudo_principal = ft.Row([
                menu_lateral(),  # ── PAINEL ESQUERDO FIXO
                ft.Container(
                    content=view_fn(),
                    padding=ft.Padding(20, 20, 20, 20),
                    expand=True  # Ocupa o resto do espaço da tela horizontalmente
                )
            ], spacing=0, expand=True)


        # Atualiza a pilha de visualização aplicando a barra inferior condicionalmente
        page.views.clear()
        page.views.append(
            ft.View(
                route=estado["rota"],
                appbar=construir_appbar(),
                controls=[conteudo_principal],
                # Se for mobile, injeta a NavigationBar na propriedade nativa da View
                navigation_bar=navigation_bar_mobile() if estado["mobile"] else None,
                padding=0,
                spacing=0
            )
        )
        page.update()

    def on_resize(e: ft.PageResizeEvent):
        # Calcula se mudou para tamanho mobile dinamicamente
        novo_mobile = e.width < BREAKPOINT_MOBILE
        if novo_mobile != estado["mobile"]:
            estado["mobile"] = novo_mobile
            route_change()

    page.on_route_change = route_change
    page.on_resize = on_resize

    if not page.route or page.route == "/":
        page.route = "/"
    
    estado["rota"] = page.route

    route_change()

if __name__ == "__main__":
    ft.app(target=main, view=ft.WEB_BROWSER)


