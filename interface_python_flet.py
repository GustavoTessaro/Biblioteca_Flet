# ==============================================================================
# SMARTPANEL — Aplicativo Desktop/Mobile com Python + Flet
# ==============================================================================
# O Flet é uma biblioteca Python que permite criar aplicativos com interface
# gráfica (GUI) para desktop, web e mobile, aproveitando os widgets do Flutter.
#
# Para instalar:
#   pip install flet==0.81
#
# Para executar:
#   python smart_panel_comentado.py
# ==============================================================================


# ------------------------------------------------------------------------------
# IMPORTAÇÃO DA BIBLIOTECA
# ------------------------------------------------------------------------------
# "import flet as ft" carrega a biblioteca Flet e cria o apelido "ft".
# A partir daqui, escrevemos ft.Text() em vez de flet.Text().
# O apelido "ft" é uma convenção da comunidade Flet — assim como "np" para NumPy.
import flet as ft


# ------------------------------------------------------------------------------
# CONSTANTE GLOBAL — BREAKPOINT RESPONSIVO
# ------------------------------------------------------------------------------
# Constantes são variáveis cujos valores não mudam durante a execução.
# Por convenção, constantes em Python são escritas em MAIÚSCULAS.
#
# BREAKPOINT_MOBILE define a largura mínima (em pixels) para layout desktop.
# → Janela com largura < 600px  : layout MOBILE  (barra de navegação inferior)
# → Janela com largura >= 600px : layout DESKTOP (menu lateral)
#
# Centralizar esse valor aqui facilita a manutenção: se precisarmos mudar
# o breakpoint, alteramos só nesta linha, e o efeito se propaga por todo o app.
BREAKPOINT_MOBILE = 600   # unidade: pixels


# ==============================================================================
# FUNÇÃO: paleta(dark)
# ==============================================================================
# Esta função resolve um problema fundamental do Flet: widgets com "bgcolor"
# fixo (ex: bgcolor=ft.Colors.BLUE_50) NÃO mudam automaticamente ao trocar
# o tema — eles ficam sempre com aquela cor, independente do tema ativo.
#
# Solução: centralizar TODAS as cores do app aqui.
# A cada troca de tema, chamamos paleta(True) ou paleta(False), obtemos um
# novo dicionário e reconstruímos toda a interface com as cores corretas.
#
# Tipo dos parâmetros (type hints):
#   dark: bool  → aceita True (escuro) ou False (claro)
#   -> dict     → retorna um dicionário Python
# ==============================================================================
def paleta(dark: bool) -> dict:

    # Bloco executado quando dark=True (tema ESCURO ativo)
    if dark:
        return {

            # ------------------------------------------------------------------
            # SUPERFÍCIES — cores de fundo dos elementos visuais
            # ------------------------------------------------------------------
            # GREY_900 é o cinza mais escuro disponível no Flet (quase preto).
            # Usamos tons de cinza escuro para simular o "Material Dark Theme".
            "bg_page":    ft.Colors.GREY_900,   # fundo da janela inteira
            "bg_sidebar": ft.Colors.GREY_900,   # fundo do menu lateral
            "bg_card":    ft.Colors.GREY_800,   # fundo dos cards genéricos

            # with_opacity(opacidade, cor): aplica transparência à cor.
            # O valor 0.15 significa 15% de opacidade (quase transparente).
            # Isso cria um toque sutil de cor sem "estourar" o fundo escuro.
            # Exemplo: bg_card_blue no dark = azul muito transparente sobre cinza.
            "bg_card_blue":   ft.Colors.with_opacity(0.15, ft.Colors.BLUE_200),
            "bg_card_green":  ft.Colors.with_opacity(0.15, ft.Colors.GREEN_200),
            "bg_card_orange": ft.Colors.with_opacity(0.15, ft.Colors.ORANGE_200),
            "bg_dica":        ft.Colors.with_opacity(0.15, ft.Colors.AMBER_200),
            "bg_info_box":    ft.Colors.with_opacity(0.12, ft.Colors.BLUE_200),
            "bg_menu_ativo":  ft.Colors.with_opacity(0.18, ft.Colors.BLUE_200),

            # ------------------------------------------------------------------
            # BORDAS — linhas ao redor dos containers e cards
            # ------------------------------------------------------------------
            # No tema escuro, bordas mais escuras evitam contraste excessivo.
            "borda_padrao":     ft.Colors.GREY_700,
            "borda_blue":       ft.Colors.BLUE_800,
            "borda_green":      ft.Colors.GREEN_800,
            "borda_orange":     ft.Colors.ORANGE_800,
            "borda_dica":       ft.Colors.AMBER_700,
            "borda_info":       ft.Colors.BLUE_800,
            "borda_menu_ativo": ft.Colors.BLUE_700,
            "borda_sidebar":    ft.Colors.GREY_700,

            # ------------------------------------------------------------------
            # TEXTOS — cores dos textos em cada contexto
            # ------------------------------------------------------------------
            # No tema escuro, textos devem ser CLAROS para contrastar com o fundo.
            "txt_titulo":     ft.Colors.WHITE,      # títulos principais de cada página
            "txt_subtitulo":  ft.Colors.GREY_400,   # textos de apoio/descrição
            "txt_card_label": ft.Colors.GREY_400,   # rótulo no topo de cada card
            "txt_card_valor": ft.Colors.WHITE,      # valor/conteúdo dentro do card
            "txt_menu_ativo": ft.Colors.BLUE_300,   # item selecionado no menu
            "txt_menu_normal":ft.Colors.GREY_300,   # itens não selecionados no menu
            "txt_dica":       ft.Colors.AMBER_200,  # texto das caixas de dica (amarelas)
            "txt_semana":     ft.Colors.GREY_600,   # texto de rodapé/versão do app
            "txt_divider":    ft.Colors.GREY_700,   # cor das linhas divisórias (Divider)

            # ------------------------------------------------------------------
            # ÍCONES — cores dos ícones no menu lateral
            # ------------------------------------------------------------------
            "icone_menu_ativo": ft.Colors.BLUE_300,  # ícone do item ativo
            "icone_menu_norm":  ft.Colors.GREY_400,  # ícone dos itens inativos

            # ------------------------------------------------------------------
            # AVATAR — círculo com a inicial do nome do usuário
            # ------------------------------------------------------------------
            "avatar_bg": ft.Colors.BLUE_900,   # cor de fundo do círculo
            "avatar_fg": ft.Colors.BLUE_200,   # cor da letra dentro do círculo

            # ------------------------------------------------------------------
            # SOMBRA — efeito de profundidade/elevação nos cards
            # ------------------------------------------------------------------
            # 30% de opacidade no escuro cria sombra visível sem exagero.
            "sombra": ft.Colors.with_opacity(0.30, ft.Colors.BLACK),
        }

    # Bloco executado quando dark=False (tema CLARO ativo)
    else:
        return {

            # Superfícies claras — branco e cinza bem claro (GREY_50)
            "bg_page":        ft.Colors.WHITE,
            "bg_sidebar":     ft.Colors.GREY_50,
            "bg_card":        ft.Colors.WHITE,
            "bg_card_blue":   ft.Colors.BLUE_50,     # azul pastel
            "bg_card_green":  ft.Colors.GREEN_50,    # verde pastel
            "bg_card_orange": ft.Colors.ORANGE_50,   # laranja pastel
            "bg_dica":        ft.Colors.AMBER_50,    # âmbar pastel
            "bg_info_box":    ft.Colors.BLUE_50,
            "bg_menu_ativo":  ft.Colors.BLUE_50,

            # Bordas suaves — tons médios de cada cor
            "borda_padrao":     ft.Colors.BLUE_200,
            "borda_blue":       ft.Colors.BLUE_200,
            "borda_green":      ft.Colors.GREEN_200,
            "borda_orange":     ft.Colors.ORANGE_200,
            "borda_dica":       ft.Colors.AMBER_200,
            "borda_info":       ft.Colors.BLUE_100,
            "borda_menu_ativo": ft.Colors.BLUE_200,
            "borda_sidebar":    ft.Colors.GREY_200,

            # Textos escuros — legíveis sobre fundo claro
            "txt_titulo":     ft.Colors.BLACK,
            "txt_subtitulo":  ft.Colors.GREY_600,
            "txt_card_label": ft.Colors.GREY_600,
            "txt_card_valor": ft.Colors.BLACK,
            "txt_menu_ativo": ft.Colors.BLUE_700,
            "txt_menu_normal":ft.Colors.GREY_700,
            "txt_dica":       ft.Colors.AMBER_900,
            "txt_semana":     ft.Colors.GREY_400,
            "txt_divider":    ft.Colors.GREY_200,

            # Ícones
            "icone_menu_ativo": ft.Colors.BLUE_700,
            "icone_menu_norm":  ft.Colors.GREY_500,

            # Avatar
            "avatar_bg": ft.Colors.BLUE_100,
            "avatar_fg": ft.Colors.BLUE_700,

            # Sombra discreta — 7% de opacidade no claro é suficiente
            "sombra": ft.Colors.with_opacity(0.07, ft.Colors.BLACK),
        }


# ==============================================================================
# SEÇÃO: COMPONENTES REUTILIZÁVEIS
# ==============================================================================
# "Componentizar" significa criar funções que geram widgets prontos para uso.
#
# Princípio DRY — Don't Repeat Yourself (Não Se Repita):
#   Se um mesmo bloco visual aparece em 3 lugares e você precisar mudar algo,
#   terá que alterar nos 3 lugares — fácil de esquecer e causar bugs.
#   Com componentes, altera uma vez e todos os usos são corrigidos.
#
# Todas as funções de componente abaixo recebem "p" (a paleta do tema atual)
# para que usem sempre as cores corretas, independente do tema ativo.
# ==============================================================================


# ------------------------------------------------------------------------------
# COMPONENTE: criar_card(titulo, conteudo, p, cor_borda_key)
# ------------------------------------------------------------------------------
# Gera um Container estilizado com título, borda arredondada e sombra.
# É o "envelope visual" usado para agrupar informações em cada seção.
#
# Parâmetros:
#   titulo        (str)        → rótulo exibido no topo do card
#   conteudo      (ft.Control) → qualquer widget Flet (Column, Row, etc.)
#   p             (dict)       → dicionário da paleta de cores
#   cor_borda_key (str)        → chave do dict p para escolher a cor da borda
#                                valor padrão: "borda_padrao"
#
# Retorno: ft.Container — widget pronto para ser adicionado à tela
# ------------------------------------------------------------------------------
def criar_card(titulo: str, conteudo: ft.Control, p: dict,
               cor_borda_key: str = "borda_padrao") -> ft.Container:

    return ft.Container(

        # ft.Column empilha os filhos verticalmente (um abaixo do outro)
        content=ft.Column([

            # Linha 1: título do card em negrito, cor discreta da paleta
            ft.Text(titulo, size=13, weight="bold", color=p["txt_card_label"]),

            # Linha 2: conteúdo variável — passado pelo chamador
            conteudo,

        ],
            spacing=10,   # espaço vertical entre título e conteúdo (em pixels)
            tight=True,   # Column encolhe ao tamanho dos filhos (sem espaço extra)
        ),

        padding=16,                                # espaço interno entre borda e conteúdo
        bgcolor=p["bg_card"],                      # cor de fundo vinda da paleta
        border=ft.border.all(1, p[cor_borda_key]), # borda de 1px nos 4 lados
        border_radius=12,                          # raio dos cantos arredondados

        # BoxShadow cria o efeito de "elevação" (card flutuando sobre o fundo)
        shadow=ft.BoxShadow(
            blur_radius=8,          # quão espalhada é a sombra (maior = mais difusa)
            spread_radius=0,        # expansão extra da sombra além do widget
            color=p["sombra"],      # cor com opacidade da paleta
            offset=ft.Offset(0, 2), # deslocamento: 0px horizontal, 2px para baixo
        ),
    )


# ------------------------------------------------------------------------------
# COMPONENTE: criar_botao_primario(texto, icone, on_click, expand)
# ------------------------------------------------------------------------------
# Gera um ElevatedButton (botão com fundo preenchido) com ícone + texto.
# Usado para a ação PRINCIPAL de um formulário (ex: "Enviar").
#
# Por que usamos content= com Row em vez de text= e icon= separados?
# No Flet 0.81, ElevatedButton não aceita text= e icon= como parâmetros diretos
# quando se quer layout customizado. Usamos content= com um Row para montar
# o layout interno manualmente: [ícone] [espaço] [texto].
#
# Parâmetros:
#   texto    → string exibida no botão
#   icone    → constante do Material Icons (ex: ft.Icons.SEND)
#   on_click → função chamada quando o usuário clica
#   expand   → se True, o botão se expande para ocupar toda a largura disponível
# ------------------------------------------------------------------------------
def criar_botao_primario(texto, icone, on_click, expand=False):

    return ft.ElevatedButton(

        # content= recebe um Row com ícone e texto lado a lado
        content=ft.Row(
            [
                ft.Icon(icone, size=16),    # ícone à esquerda, 16px
                ft.Text(texto, size=14),    # rótulo à direita, 14px
            ],
            spacing=6,   # espaço horizontal entre ícone e texto
            tight=True,  # Row ocupa apenas o espaço necessário
        ),

        on_click=on_click,   # referência à função handler (sem parênteses!)
        expand=expand,       # True = ocupa toda a largura do pai

        style=ft.ButtonStyle(
            # RoundedRectangleBorder define o formato dos cantos do botão
            shape=ft.RoundedRectangleBorder(radius=8),
        ),
    )


# ------------------------------------------------------------------------------
# COMPONENTE: criar_botao_secundario(texto, icone, on_click, expand)
# ------------------------------------------------------------------------------
# Gera um OutlinedButton (botão apenas com borda, sem fundo preenchido).
# Visualmente menos destacado que o primário — ideal para ações secundárias
# como "Limpar", "Cancelar" ou "Voltar".
#
# A estrutura interna é idêntica ao primário; apenas o tipo de botão muda.
# Isso reforça a consistência visual: mesma forma, hierarquia diferente.
# ------------------------------------------------------------------------------
def criar_botao_secundario(texto, icone, on_click, expand=False):

    return ft.OutlinedButton(

        content=ft.Row(
            [
                ft.Icon(icone, size=16),
                ft.Text(texto, size=14),
            ],
            spacing=6,
            tight=True,
        ),

        on_click=on_click,
        expand=expand,

        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=8),
        ),
    )


# ------------------------------------------------------------------------------
# COMPONENTE: criar_dica(mensagem, p)
# ------------------------------------------------------------------------------
# Gera uma caixa de destaque amarela com ícone de lâmpada.
# Serve para orientar o usuário com uma instrução ou sugestão rápida.
#
# Parâmetros:
#   mensagem → texto da dica a ser exibido
#   p        → dicionário da paleta de cores
# ------------------------------------------------------------------------------
def criar_dica(mensagem: str, p: dict) -> ft.Container:

    return ft.Container(

        # Row posiciona os filhos lado a lado horizontalmente
        content=ft.Row([

            # Ícone de lâmpada — cor âmbar fixa (não muda com o tema)
            ft.Icon(ft.Icons.LIGHTBULB_OUTLINE, color=ft.Colors.AMBER_700, size=16),

            # expand=True: o texto ocupa todo o espaço restante da Row
            # Isso evita que textos longos "empurrem" o ícone para fora
            ft.Text(mensagem, size=13, color=p["txt_dica"], expand=True),

        ], spacing=8),  # 8px entre ícone e texto

        # ft.Padding(esquerda, cima, direita, baixo) — espaços internos
        padding=ft.Padding(12, 10, 12, 10),

        bgcolor=p["bg_dica"],               # fundo âmbar claro (ou escuro no dark)
        border_radius=8,                    # cantos levemente arredondados
        border=ft.border.all(1, p["borda_dica"]),  # borda fina âmbar
    )


# ------------------------------------------------------------------------------
# COMPONENTE: criar_item_menu(label, icone_off, icone_on, ativo, on_click, p)
# ------------------------------------------------------------------------------
# Gera um item interativo do menu lateral.
# Aplica dois visuais distintos baseado no parâmetro "ativo":
#
#   ativo=True  → fundo azul, ícone preenchido, texto em negrito (SELECIONADO)
#   ativo=False → fundo transparente, ícone de contorno, texto normal
#
# Parâmetros:
#   label     → texto do item (ex: "Home", "Usuário")
#   icone_off → ícone de contorno — exibido quando o item NÃO está ativo
#   icone_on  → ícone preenchido — exibido quando o item ESTÁ ativo
#   ativo     → booleano: True se este item corresponde à rota atual
#   on_click  → função chamada ao clicar no item
#   p         → dicionário da paleta de cores
# ------------------------------------------------------------------------------
def criar_item_menu(label, icone_off, icone_on, ativo,
                    on_click, p: dict) -> ft.Container:

    return ft.Container(

        content=ft.Row([

            ft.Icon(
                # Operador ternário: condição if True else False
                # Se ativo=True → usa icone_on (preenchido)
                # Se ativo=False → usa icone_off (contorno)
                icone_on if ativo else icone_off,
                size=18,
                color=p["icone_menu_ativo"] if ativo else p["icone_menu_norm"],
            ),

            ft.Text(
                label,
                size=13,
                # Negrito quando ativo; peso normal quando inativo
                weight="bold" if ativo else "normal",
                color=p["txt_menu_ativo"] if ativo else p["txt_menu_normal"],
            ),

        ], spacing=10, tight=True),

        padding=ft.Padding(10, 9, 10, 9),  # padding assimétrico: mais horizontal

        border_radius=8,  # cantos arredondados do item

        # Fundo colorido apenas no item ativo; TRANSPARENT = sem cor de fundo
        bgcolor=p["bg_menu_ativo"] if ativo else ft.Colors.TRANSPARENT,

        # Borda apenas no item ativo (None = sem borda nos inativos)
        border=ft.border.all(1, p["borda_menu_ativo"]) if ativo else None,

        on_click=on_click,  # função chamada ao clicar

        # ink=True ativa o efeito "ripple" (ondinha de clique do Material Design)
        ink=True,
    )


# ==============================================================================
# FUNÇÃO PRINCIPAL: main(page)
# ==============================================================================
# No Flet, TODA a lógica do aplicativo vive dentro de main().
# O Flet chama essa função automaticamente ao iniciar, injetando o objeto
# "page" — que representa a janela/tela do app.
#
# Conceito de CLOSURE:
#   Funções definidas dentro de main() têm acesso a todas as variáveis
#   do escopo de main() (como "estado", "campo_nome", etc.) sem precisar
# ==============================================================================
def main(page: ft.Page):

    # --------------------------------------------------------------------------
    # CONFIGURAÇÕES INICIAIS DA PÁGINA
    # --------------------------------------------------------------------------

    page.title = "SmartPanel"       # aparece na barra de título do sistema operacional

    page.padding = 0                # remove a margem padrão ao redor da página
    page.spacing = 0                # remove o espaçamento padrão entre controles

    page.theme_mode = ft.ThemeMode.LIGHT  # inicia no tema claro

    # ft.Theme com color_scheme_seed gera automaticamente toda a paleta
    # Material Design a partir de uma única cor base.
    # O tema claro usa azul como cor semente.
    page.theme = ft.Theme(color_scheme_seed=ft.Colors.BLUE)

    # O tema escuro usa índigo — uma variante mais sóbria do azul.
    page.dark_theme = ft.Theme(color_scheme_seed=ft.Colors.INDIGO)


    # --------------------------------------------------------------------------
    # ESTADO DO APLICATIVO
    # --------------------------------------------------------------------------
    # "estado" é um dicionário que guarda todos os dados mutáveis do app —
    # valores que mudam durante o uso e afetam o que é exibido na tela.
    #
    # Por que usar dicionário em vez de variáveis simples?
    #   Funções internas (closures) podem LER variáveis do escopo externo,
    #   mas para MODIFICAR precisariam de "nonlocal" — o que polui o código.
    #   Com um dicionário, modificamos os VALORES das chaves diretamente
    #   (ex: estado["dark_mode"] = True), sem precisar de nonlocal.
    estado = {
        "dark_mode":      False,  # False = tema claro | True = tema escuro
        "notificacoes":   3,      # contador de notificações pendentes
        "usuario_logado": "",     # nome digitado pelo usuário (string vazia = anônimo)
        "rota":           "/",    # rota atual — "/" corresponde à página Home
        "mobile":         False,  # False = layout desktop | True = layout mobile
    }


    # --------------------------------------------------------------------------
    # CAMPOS DE FORMULÁRIO (criados fora das views)
    # --------------------------------------------------------------------------
    # Criamos campo_nome e campo_email AQUI (no escopo de main) e NÃO dentro
    # da função view_usuario.
    #
    # Motivo: se fossem criados dentro de view_usuario, seriam recriados do zero
    # cada vez que o usuário navegar para outra página e voltar — apagando
    # tudo que foi digitado. Aqui, eles persistem durante toda a sessão.

    campo_nome = ft.TextField(
        label="Seu nome",                        # rótulo flutuante acima do campo
        hint_text="Ex: João Silva",              # texto de exemplo (placeholder)
        prefix_icon=ft.Icons.PERSON_OUTLINE,     # ícone à esquerda, dentro do campo
        expand=True,                             # ocupa toda a largura disponível
        border_radius=8,                         # cantos arredondados do campo
    )

    campo_email = ft.TextField(
        label="E-mail",
        hint_text="Ex: joao@email.com",
        prefix_icon=ft.Icons.EMAIL_OUTLINED,
        expand=True,
        border_radius=8,
        # keyboard_type: dica ao sistema operacional para abrir o teclado correto
        # EMAIL abre teclado com "@" visível em dispositivos móveis
        keyboard_type=ft.KeyboardType.EMAIL,
    )

    # Widget de texto para exibir o resultado/feedback após clicar em "Enviar"
    # Começa vazio — será preenchido pelo handler processar()
    texto_result = ft.Text("")


    # --------------------------------------------------------------------------
    # FUNÇÃO AUXILIAR: mostrar_snack(msg, cor)
    # --------------------------------------------------------------------------
    # SnackBar é uma mensagem temporária que aparece na base da tela
    # por alguns segundos — padrão do Material Design para feedback rápido.
    #
    # Parâmetros:
    #   msg → texto a ser exibido
    #   cor → cor de fundo do snackbar (padrão: verde = sucesso)
    # --------------------------------------------------------------------------
    def mostrar_snack(msg: str, cor=ft.Colors.GREEN_700):

        # Criamos um novo SnackBar a cada chamada
        sb = ft.SnackBar(
            content=ft.Text(msg, color=ft.Colors.WHITE),  # texto sempre branco
            bgcolor=cor,      # cor de fundo configurável pelo chamador
            duration=2500,    # tempo de exibição em milissegundos (2,5 segundos)
        )

        # page.overlay é uma lista especial para widgets "flutuantes" —
        # elementos que ficam acima de todo o restante da interface
        # (dialogs, snackbars, bottom sheets, etc.)
        page.overlay.append(sb)

        sb.open = True    # define o snackbar como aberto/visível
        page.update()     # envia as mudanças para a tela (obrigatório no Flet)


    # ==========================================================================
    # HANDLERS — Funções de tratamento de eventos
    # ==========================================================================
    # Um "handler" é uma função chamada automaticamente quando um evento ocorre
    # (clique de botão, mudança de valor, redimensionamento, etc.).
    #
    # Convenção: handlers recebem o parâmetro "e" (evento), mesmo que não
    # precisem usá-lo. O "e" contém informações sobre o evento ocorrido
    # (ex: e.control.value = novo valor de um Switch após alteração).
    # ==========================================================================


    # --------------------------------------------------------------------------
    # HANDLER: processar(e)
    # --------------------------------------------------------------------------
    # Chamado quando o usuário clica no botão "Enviar" do formulário.
    # Valida os campos e exibe o resultado na tela.
    # --------------------------------------------------------------------------
    def processar(e):

        # .strip() remove espaços em branco do início e do fim da string
        # Evita que "   " (só espaços) seja aceito como nome válido
        nome  = campo_nome.value.strip()
        email = campo_email.value.strip()

        # Validação: nome é obrigatório
        if not nome:
            # "not nome" é True quando nome é string vazia "" ou apenas espaços
            texto_result.value = "⚠️ Preencha o nome."
            texto_result.color = ft.Colors.RED_600
            mostrar_snack("Campo obrigatório!", ft.Colors.RED_700)

        else:
            # Salva o nome no estado global para uso em outras views
            estado["usuario_logado"] = nome

            # f-string: sintaxe moderna para interpolação de strings
            # {nome} é substituído pelo valor da variável nome em tempo de execução
            # Operador ternário inline: adiciona o email se ele existir, ou "" se vazio
            texto_result.value = (
                f"👋 Olá, {nome}!"
                + (f"  •  📧 {email}" if email else "")
            )
            texto_result.color = ft.Colors.GREEN_700
            mostrar_snack(f"Bem-vindo(a), {nome}! ✅")

        # page.update() é OBRIGATÓRIO após qualquer mudança em widgets
        # que já estão na tela. Sem ele, a interface não se atualiza.
        page.update()


    # --------------------------------------------------------------------------
    # HANDLER: limpar(e)
    # --------------------------------------------------------------------------
    # Chamado ao clicar em "Limpar". Reseta o formulário para o estado inicial.
    # --------------------------------------------------------------------------
    def limpar(e):
        campo_nome.value         = ""   # apaga o conteúdo do campo nome
        campo_email.value        = ""   # apaga o conteúdo do campo email
        texto_result.value       = ""   # apaga o texto de resultado
        estado["usuario_logado"] = ""   # remove o nome salvo no estado
        mostrar_snack("Campos limpos.", ft.Colors.GREY_700)
        page.update()


    # --------------------------------------------------------------------------
    # HANDLER: toggle_theme_switch(e)
    # --------------------------------------------------------------------------
    # Chamado quando o Switch "Modo Escuro" na página de Configurações é alterado.
    # e.control.value contém o novo estado do Switch: True (ligado) ou False (desligado).
    # --------------------------------------------------------------------------
    def toggle_theme_switch(e):

        # Sincroniza o estado interno com o valor atual do Switch
        estado["dark_mode"] = e.control.value

        # Aplica o tema ao Flet — isso muda a aparência dos widgets nativos
        # (Switch, TextField, NavigationBar, etc.) que respondem ao ThemeMode
        page.theme_mode = (
            ft.ThemeMode.DARK if estado["dark_mode"] else ft.ThemeMode.LIGHT
        )

        # Reconstrói toda a interface para aplicar as cores da nova paleta
        route_change()


    # --------------------------------------------------------------------------
    # HANDLER: _toggle_tema_rapido()
    # --------------------------------------------------------------------------
    # Chamado pelo botão de sol/lua na AppBar (canto superior direito).
    # Inverte o tema atual sem precisar de um evento com valor explícito.
    #
    # O underscore (_) no início é uma convenção Python que indica que esta
    # função é "privada" — de uso interno, não deve ser chamada de fora.
    # --------------------------------------------------------------------------
    def _toggle_tema_rapido():

        # Operador "not" inverte o booleano: True → False, False → True
        estado["dark_mode"] = not estado["dark_mode"]

        page.theme_mode = (
            ft.ThemeMode.DARK if estado["dark_mode"] else ft.ThemeMode.LIGHT
        )

        route_change()  # reconstrói a interface com o novo tema


    # --------------------------------------------------------------------------
    # FUNÇÃO: navegar(rota)
    # --------------------------------------------------------------------------
    # Muda a página exibida ao atualizar a rota no estado e reconstruir a UI.
    # É chamada por todos os itens do menu e da navigation bar.
    # --------------------------------------------------------------------------
    def navegar(rota):
        estado["rota"] = rota  # define qual página deve ser exibida
        route_change()         # reconstrói a interface para a nova rota


    # ==========================================================================
    # VIEWS — Funções que constroem cada "página" do aplicativo
    # ==========================================================================
    # Cada view é uma função que:
    #   1. Recebe "p" (paleta) para usar as cores corretas do tema atual
    #   2. Monta e retorna um ft.ListView com o conteúdo da página
    #
    # Por que ListView e não Column?
    #   ListView adiciona scroll automático quando o conteúdo é maior que a tela.
    #   Column não tem scroll — o conteúdo seria cortado em telas pequenas.
    #
    # expand=True no ListView faz ele ocupar todo o espaço vertical disponível.
    # ==========================================================================


    # --------------------------------------------------------------------------
    # VIEW: view_home(p) — Página inicial / Dashboard
    # --------------------------------------------------------------------------
    def view_home(p: dict):

        # Lê o nome do usuário do estado; gera saudação personalizada ou genérica
        nome     = estado["usuario_logado"]
        saudacao = f"Olá, {nome}! " if nome else "Olá! "

        # ResponsiveRow: layout de grade que se adapta ao tamanho da tela.
        # Funciona com um sistema de 12 colunas (como o Bootstrap / CSS Grid).
        #
        # col={"xs": 12, "sm": 4} significa:
        #   xs (extra small) = telas até ~600px → ocupa 12/12 = largura total
        #   sm (small)       = telas acima ~600px → ocupa 4/12 = 1/3 da largura
        #
        # No mobile: cada card ocupa a tela toda (empilhados verticalmente)
        # No desktop: os 3 cards ficam lado a lado em uma única linha
        cards = ft.ResponsiveRow([

            # --- Card: Usuários ---
            ft.Container(
                content=ft.Column([
                    ft.Icon(ft.Icons.PEOPLE_ALT_OUTLINED, size=26, color=ft.Colors.BLUE_400),
                    ft.Text("Usuários", size=12, color=p["txt_card_label"]),
                    ft.Text("128", size=20, weight="bold", color=p["txt_card_valor"]),
                ],
                    # CrossAxisAlignment.CENTER centraliza os filhos horizontalmente
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=4,
                    tight=True,
                ),
                padding=14,
                border_radius=12,
                bgcolor=p["bg_card_blue"],
                border=ft.border.all(1, p["borda_blue"]),
                col={"xs": 12, "sm": 4},  # responsividade: mobile=full | desktop=1/3
            ),

            # --- Card: Tarefas ---
            ft.Container(
                content=ft.Column([
                    ft.Icon(ft.Icons.TASK_ALT, size=26, color=ft.Colors.GREEN_400),
                    ft.Text("Tarefas", size=12, color=p["txt_card_label"]),
                    ft.Text("42", size=20, weight="bold", color=p["txt_card_valor"]),
                ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=4,
                    tight=True,
                ),
                padding=14,
                border_radius=12,
                bgcolor=p["bg_card_green"],
                border=ft.border.all(1, p["borda_green"]),
                col={"xs": 12, "sm": 4},
            ),

            # --- Card: Alertas (valor dinâmico do estado) ---
            ft.Container(
                content=ft.Column([
                    ft.Icon(ft.Icons.NOTIFICATIONS_OUTLINED, size=26, color=ft.Colors.ORANGE_400),
                    ft.Text("Alertas", size=12, color=p["txt_card_label"]),
                    # str() converte o número inteiro para string (Text não aceita int)
                    ft.Text(str(estado["notificacoes"]), size=20, weight="bold",
                            color=p["txt_card_valor"]),
                ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=4,
                    tight=True,
                ),
                padding=14,
                border_radius=12,
                bgcolor=p["bg_card_orange"],
                border=ft.border.all(1, p["borda_orange"]),
                col={"xs": 12, "sm": 4},
            ),

        ],
            spacing=10,      # espaço horizontal entre colunas (quando lado a lado)
            run_spacing=10,  # espaço vertical entre linhas (quando empilhados)
        )

        # ListTile: widget de lista com três zonas: leading, title e subtitle.
        # leading = elemento à esquerda (ícone, avatar, etc.)
        # title   = texto principal
        # subtitle = texto secundário (menor, abaixo do title)
        # dense=True reduz a altura do item — mais compacto
        atividades = criar_card(
            "Atividades Recentes",
            ft.Column([
                ft.ListTile(
                    leading=ft.Icon(ft.Icons.CIRCLE, color=ft.Colors.GREEN_400, size=10),
                    title=ft.Text("Sistema iniciado com sucesso", size=13,
                                  color=p["txt_card_valor"]),
                    subtitle=ft.Text("Agora mesmo", size=11, color=p["txt_subtitulo"]),
                    dense=True,
                ),
                ft.ListTile(
                    leading=ft.Icon(ft.Icons.CIRCLE, color=ft.Colors.BLUE_400, size=10),
                    title=ft.Text("Semana 8 concluída", size=13, color=p["txt_card_valor"]),
                    subtitle=ft.Text("Hoje", size=11, color=p["txt_subtitulo"]),
                    dense=True,
                ),
                ft.ListTile(
                    leading=ft.Icon(ft.Icons.CIRCLE, color=ft.Colors.ORANGE_400, size=10),
                    title=ft.Text(
                        f"{estado['notificacoes']} notificações pendentes",
                        size=13, color=p["txt_card_valor"],
                    ),
                    subtitle=ft.Text("Hoje", size=11, color=p["txt_subtitulo"]),
                    dense=True,
                ),
            ], spacing=0, tight=True),
            p,  # passa a paleta para criar_card usar as cores corretas
        )

        # ft.ListView: lista com scroll automático
        # controls= recebe a lista de widgets exibidos de cima para baixo
        # spacing= espaço vertical entre cada item da lista
        # padding= margem interna (aplicada em todos os lados)
        # expand=True faz o ListView ocupar todo o espaço restante da tela
        return ft.ListView(
            controls=[
                ft.Text("🏠 Dashboard", size=22, weight="bold", color=p["txt_titulo"]),
                ft.Text(saudacao + "Bem-vindo ao SmartPanel.", size=14,
                        color=p["txt_subtitulo"]),
                ft.Divider(height=1, color=p["txt_divider"]),  # linha separadora
                cards,
                atividades,
            ],
            spacing=16,
            padding=20,
            expand=True,
        )


    # --------------------------------------------------------------------------
    # VIEW: view_usuario(p) — Página do formulário de cadastro
    # --------------------------------------------------------------------------
    def view_usuario(p: dict):

        # Agrupa campos e botões dentro de um card estilizado
        formulario = criar_card(
            "Dados do Usuário",
            ft.Column([
                campo_nome,   # TextField persistente (criado em main)
                campo_email,  # TextField persistente (criado em main)

                # Row coloca os dois botões lado a lado
                # expand=True em cada botão → dividem igualmente a largura disponível
                ft.Row([
                    criar_botao_primario("Enviar", ft.Icons.SEND, processar, expand=True),
                    criar_botao_secundario("Limpar", ft.Icons.CLEAR, limpar, expand=True),
                ], spacing=8),

                texto_result,  # exibe o feedback após o clique em Enviar
            ], spacing=12, tight=True),
            p,
        )

        return ft.ListView(
            controls=[
                ft.Text("👤 Usuário", size=22, weight="bold", color=p["txt_titulo"]),
                criar_dica("Preencha seu nome para personalizar o dashboard.", p),
                formulario,
            ],
            spacing=16,
            padding=20,
            expand=True,
        )


    # --------------------------------------------------------------------------
    # VIEW: view_config(p) — Página de configurações do aplicativo
    # --------------------------------------------------------------------------
    def view_config(p: dict):

        # --- Card: Aparência ---
        # Contém o Switch de alternância de tema escuro
        aparencia = criar_card(
            "Aparência",
            ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.DARK_MODE_OUTLINED, color=ft.Colors.INDIGO_400),
                    ft.Switch(
                        label="Modo Escuro",
                        value=estado["dark_mode"],         # espelha o estado atual
                        on_change=toggle_theme_switch,      # handler ao alternar
                        active_color=ft.Colors.INDIGO_400, # cor do Switch quando ligado
                    ),
                ], spacing=8),
                ft.Divider(height=1, color=p["txt_divider"]),
                ft.Row([
                    ft.Icon(ft.Icons.PALETTE_OUTLINED, color=ft.Colors.BLUE_400),
                    ft.Text("Tema: Azul (padrão)", size=14, color=p["txt_card_valor"]),
                ], spacing=8),
            ], spacing=10, tight=True),
            p,
            "borda_padrao",  # terceiro argumento: chave da cor da borda
        )

        # --- Card: Notificações ---
        notificacoes = criar_card(
            "Notificações",
            ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.NOTIFICATIONS_ACTIVE_OUTLINED,
                            color=ft.Colors.ORANGE_400),
                    ft.Switch(label="Ativar notificações", value=True,
                              active_color=ft.Colors.ORANGE_400),
                ], spacing=8),
                ft.Row([
                    ft.Icon(ft.Icons.VOLUME_UP_OUTLINED, color=ft.Colors.ORANGE_300),
                    ft.Switch(label="Sons do sistema", value=False,
                              active_color=ft.Colors.ORANGE_400),
                ], spacing=8),
            ], spacing=10, tight=True),
            p,
            "borda_orange",
        )

        # --- Card: Privacidade ---
        privacidade = criar_card(
            "Privacidade",
            ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.LOCK_OUTLINE, color=ft.Colors.GREEN_500),
                    ft.Switch(label="Salvar dados localmente", value=True,
                              active_color=ft.Colors.GREEN_500),
                ], spacing=8),
                ft.Row([
                    ft.Icon(ft.Icons.ANALYTICS_OUTLINED, color=ft.Colors.GREEN_400),
                    ft.Switch(label="Compartilhar analytics", value=False,
                              active_color=ft.Colors.GREEN_500),
                ], spacing=8),
            ], spacing=10, tight=True),
            p,
            "borda_green",
        )

        return ft.ListView(
            controls=[
                ft.Text("⚙️ Configurações", size=22, weight="bold", color=p["txt_titulo"]),
                aparencia,
                notificacoes,
                privacidade,
                # Rodapé com a versão do app — cor discreta da paleta
                ft.Text("SmartPanel v1.0 — Semanas 1 a 8", size=11, color=p["txt_semana"]),
            ],
            spacing=16,
            padding=20,
            expand=True,
        )
#   passá-las como parâmetros. Isso é chamado de "closure" em Python.


    # --------------------------------------------------------------------------
    # VIEW: view_sobre(p) — Página com o histórico de desenvolvimento
    # --------------------------------------------------------------------------
    def view_sobre(p: dict):

        # Lista de tuplas com os dados de cada semana do projeto.
        # Tupla: estrutura imutável de Python — ideal para dados fixos/constantes.
        # Cada tupla tem: (rótulo da semana, descrição, cor do badge)
        itens = [
            ("Semana 1", "Tela única: texto + botão",              ft.Colors.GREEN_600),
            ("Semana 2", "Campos e interatividade real",           ft.Colors.GREEN_600),
            ("Semana 3", "Row, Column, Container",                 ft.Colors.YELLOW_700),
            ("Semana 4", "Menu lateral com navegação visual",      ft.Colors.YELLOW_700),
            ("Semana 5", "Navegação real com rotas",               ft.Colors.ORANGE_600),
            ("Semana 6", "AppBar, ícones e SnackBar",              ft.Colors.ORANGE_600),
            ("Semana 7", "Componentização e código escalável",     ft.Colors.BLUE_600),
            ("Semana 8", "Dark mode, refinamento e produto final", ft.Colors.RED_600),
        ]

        # List comprehension: forma compacta de criar uma lista em Python.
        # Equivale a um loop for que coleta resultados em uma lista.
        #
        # Sintaxe: [expressão for variavel in iteravel]
        # Para cada tupla (s, d, c) em itens, cria um Container visual.
        # "s, d, c" = desempacotamento: cada elemento da tupla vira uma variável.
        lista = ft.Column([
            ft.Container(
                content=ft.Row([

                    # Badge colorido com o nome da semana
                    ft.Container(
                        content=ft.Text(s, size=11, weight="bold",
                                        color=ft.Colors.WHITE),
                        bgcolor=c,                       # cor da variável c da tupla
                        padding=ft.Padding(8, 4, 8, 4),
                        border_radius=6,
                        width=80,                        # largura fixa para alinhar badges
                    ),

                    # Descrição da semana — expand=True para ocupar o resto da linha
                    ft.Text(d, size=13, expand=True, color=p["txt_card_valor"]),

                ],
                    spacing=10,
                    # CrossAxisAlignment.CENTER alinha verticalmente ao centro
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                padding=ft.Padding(10, 8, 10, 8),
                border_radius=8,
                bgcolor=p["bg_card"],
                border=ft.border.all(1, p["borda_padrao"]),
            )
            for s, d, c in itens   # loop: desempacota cada tupla em s, d, c
        ], spacing=6, tight=True)

        return ft.ListView(
            controls=[
                ft.Text("📚 Sobre o Projeto", size=22, weight="bold",
                        color=p["txt_titulo"]),
                ft.Text(
                    "Progressão de 8 semanas construindo o SmartPanel com Python + Flet.",
                    size=14, color=p["txt_subtitulo"],
                ),
                ft.Divider(color=p["txt_divider"]),
                lista,
                # Box informativo com tecnologia e disciplina do projeto
                ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.Icon(ft.Icons.CODE, color=ft.Colors.BLUE_500, size=16),
                            ft.Text("Python + Flet 0.81", size=13,
                                    color=p["txt_card_valor"]),
                        ], spacing=8),
                        ft.Row([
                            ft.Icon(ft.Icons.SCHOOL_OUTLINED, color=ft.Colors.BLUE_500,
                                    size=16),
                            ft.Text("Disciplina: Tecnologia da Informação", size=13,
                                    color=p["txt_card_valor"]),
                        ], spacing=8),
                    ], spacing=8, tight=True),
                    padding=16,
                    border_radius=12,
                    bgcolor=p["bg_info_box"],
                    border=ft.border.all(1, p["borda_info"]),
                ),
            ],
            spacing=16,
            padding=20,
            expand=True,
        )


    # ==========================================================================
    # DEFINIÇÃO DAS ROTAS E MENU LATERAL
    # ==========================================================================

    # Lista de tuplas descrevendo cada item de navegação:
    # (caminho da rota, rótulo, ícone inativo, ícone ativo)
    rotas_menu = [
        ("/",        "Home",          ft.Icons.HOME_OUTLINED,     ft.Icons.HOME),
        ("/usuario", "Usuário",       ft.Icons.PERSON_OUTLINED,   ft.Icons.PERSON),
        ("/config",  "Configurações", ft.Icons.SETTINGS_OUTLINED, ft.Icons.SETTINGS),
        ("/sobre",   "Sobre",         ft.Icons.INFO_OUTLINE,      ft.Icons.INFO),
    ]


    # --------------------------------------------------------------------------
    # FUNÇÃO: menu_lateral(p) — Painel de navegação lateral (layout desktop)
    # --------------------------------------------------------------------------
    def menu_lateral(p: dict):

        rota = estado["rota"]              # rota atual, para destacar o item correto
        nome = estado.get("usuario_logado", "")  # .get() retorna "" se a chave não existir

        # Se nome estiver preenchido: pega a primeira letra em maiúsculo
        # Se nome estiver vazio: usa "?" como placeholder do avatar
        avatar_label = nome[0].upper() if nome else "?"

        # List comprehension que gera os itens de menu a partir de rotas_menu.
        # Para cada tupla, chama criar_item_menu com os parâmetros corretos.
        #
        # ATENÇÃO — "lambda e, dest=r: navegar(dest)":
        #   Em loops Python, closures capturam a VARIÁVEL, não o valor no momento.
        #   Se usarmos "lambda e: navegar(r)", todos os lambdas usariam o último "r".
        #   O argumento padrão "dest=r" CONGELA o valor atual de "r" naquele item.
        #   Isso garante que cada botão navegue para sua própria rota.
        itens = [
            criar_item_menu(
                label, ic_off, ic_on,
                ativo=(rota == r),                          # True se for a rota atual
                on_click=lambda e, dest=r: navegar(dest),   # captura o valor de r
                p=p,
            )
            for r, label, ic_off, ic_on in rotas_menu      # desempacota cada tupla
        ]

        # Seção de perfil do usuário na parte inferior do menu lateral
        perfil = ft.Container(
            content=ft.Row([

                # CircleAvatar: círculo com inicial do nome do usuário
                ft.CircleAvatar(
                    content=ft.Text(avatar_label, size=11, weight="bold"),
                    bgcolor=p["avatar_bg"],  # cor de fundo do círculo
                    color=p["avatar_fg"],    # cor da letra dentro do círculo
                    radius=15,              # raio do círculo em pixels
                ),

                # Coluna com nome e status do usuário
                ft.Column([
                    # "nome or 'Visitante'": se nome for "" (falsy), usa "Visitante"
                    ft.Text(nome or "Visitante", size=12, weight="bold",
                            color=p["txt_card_valor"]),
                    ft.Text("● Online", size=10, color=ft.Colors.GREEN_400),
                ], spacing=0, tight=True, expand=True),

            ], spacing=8, tight=True),
            padding=ft.Padding(4, 8, 4, 0),
        )

        # Container principal do menu lateral
        return ft.Container(
            width=215,  # largura fixa em pixels

            bgcolor=p["bg_sidebar"],

            # border.only aplica borda apenas nos lados especificados
            # Aqui, só o lado direito tem borda (separa menu do conteúdo)
            border=ft.border.only(right=ft.BorderSide(1, p["borda_sidebar"])),

            padding=12,

            content=ft.Column([

                # Cabeçalho do menu: ícone + nome do app
                ft.Row([
                    ft.Icon(ft.Icons.DASHBOARD_OUTLINED, color=ft.Colors.BLUE_400, size=20),
                    ft.Text("SmartPanel", size=15, weight="bold", color=ft.Colors.BLUE_400),
                ], spacing=8, tight=True),

                ft.Divider(height=8, color=p["txt_divider"]),  # linha divisória

                # *itens — operador de desempacotamento (spread operator):
                # Transforma a lista [item1, item2, ...] em argumentos individuais
                # da Column, como se fossem escritos: item1, item2, ...
                *itens,

                ft.Divider(height=8, color=p["txt_divider"]),

                perfil,  # seção de perfil no rodapé do menu

            ], spacing=4, tight=True),
        )


    # --------------------------------------------------------------------------
    # ÍNDICE DE ROTAS — para o NavigationBar mobile
    # --------------------------------------------------------------------------
    # NavigationBar trabalha com ÍNDICES numéricos (0, 1, 2, 3),
    # não com strings de rota. Esta lista faz a conversão:
    # índice 0 → "/", índice 1 → "/usuario", etc.
    _indice_rotas = ["/", "/usuario", "/config", "/sobre"]


    # --------------------------------------------------------------------------
    # FUNÇÃO: navigation_bar_mobile() — Barra de navegação inferior (mobile)
    # --------------------------------------------------------------------------
    def navigation_bar_mobile():

        rota_atual = estado["rota"]

        # list.index(valor) retorna o índice da primeira ocorrência do valor
        # A condição "if rota_atual in _indice_rotas" evita ValueError
        # caso a rota não exista na lista (retorna 0 = Home como padrão)
        idx = _indice_rotas.index(rota_atual) if rota_atual in _indice_rotas else 0

        # Função interna: converte índice numérico de volta para rota string
        def ao_mudar(e):
            # e.control.selected_index = índice do item clicado pelo usuário
            navegar(_indice_rotas[e.control.selected_index])

        return ft.NavigationBar(
            selected_index=idx,    # índice do item visualmente destacado
            on_change=ao_mudar,    # handler chamado ao trocar de item

            # NavigationBarDestination define cada item da barra:
            # icon         = ícone quando o item NÃO está selecionado
            # selected_icon = ícone quando o item ESTÁ selecionado
            # label         = texto abaixo do ícone
            destinations=[
                ft.NavigationBarDestination(
                    icon=ft.Icons.HOME_OUTLINED, selected_icon=ft.Icons.HOME,
                    label="Home"),
                ft.NavigationBarDestination(
                    icon=ft.Icons.PERSON_OUTLINED, selected_icon=ft.Icons.PERSON,
                    label="Usuário"),
                ft.NavigationBarDestination(
                    icon=ft.Icons.SETTINGS_OUTLINED, selected_icon=ft.Icons.SETTINGS,
                    label="Config"),
                ft.NavigationBarDestination(
                    icon=ft.Icons.INFO_OUTLINE, selected_icon=ft.Icons.INFO,
                    label="Sobre"),
            ],
        )


    # --------------------------------------------------------------------------
    # DICIONÁRIO DE TÍTULOS DA APPBAR
    # --------------------------------------------------------------------------
    # Mapeia cada rota ao título exibido na barra superior.
    # Usar dicionário é mais limpo que um if/elif para cada rota.
    titulos = {
        "/":        "Dashboard",
        "/usuario": "Perfil do Usuário",
        "/config":  "Configurações",
        "/sobre":   "Sobre o Projeto",
    }


    # --------------------------------------------------------------------------
    # FUNÇÃO: construir_appbar() — Barra superior do aplicativo
    # --------------------------------------------------------------------------
    # AppBar é recriada a cada route_change() para refletir:
    #   - O título correto da página atual
    #   - O ícone correto do botão de tema (sol ou lua)
    #   - A cor correta conforme o tema (azul claro ou azul escuro)
    # --------------------------------------------------------------------------
    def construir_appbar():
        return ft.AppBar(

            # leading: widget exibido à esquerda da AppBar (antes do título)
            leading=ft.Icon(ft.Icons.DASHBOARD_OUTLINED, color=ft.Colors.WHITE),
            leading_width=48,  # largura reservada para o widget leading

            # title: widget centralizado na AppBar
            # .get(chave, padrao): retorna o valor ou "SmartPanel" se não encontrar
            title=ft.Text(
                titulos.get(estado["rota"], "SmartPanel"),
                color=ft.Colors.WHITE,
                size=16,
                weight="bold",
            ),

            # Cor da AppBar: azul mais escuro no dark mode, mais claro no light
            bgcolor=(
                ft.Colors.BLUE_800 if estado["dark_mode"] else ft.Colors.BLUE_700
            ),

            # actions: lista de widgets exibidos à DIREITA da AppBar
            actions=[

                # Botão de notificações
                ft.IconButton(
                    icon=ft.Icons.NOTIFICATIONS_OUTLINED,
                    icon_color=ft.Colors.WHITE,
                    tooltip="Notificações",  # texto exibido ao passar o mouse
                    on_click=lambda e: mostrar_snack(
                        f"🔔 {estado['notificacoes']} notificações pendentes.",
                        ft.Colors.BLUE_700,
                    ),
                ),

                # Botão de alternância de tema (sol = claro | lua = escuro)
                ft.IconButton(
                    # Ternário: se dark_mode=True mostra ícone de sol, senão de lua
                    # (o ícone indica para qual tema o botão vai MUDAR, não o atual)
                    icon=(
                        ft.Icons.LIGHT_MODE_OUTLINED
                        if estado["dark_mode"]
                        else ft.Icons.DARK_MODE_OUTLINED
                    ),
                    icon_color=ft.Colors.WHITE,
                    tooltip="Alternar tema",
                    # lambda e: adapta o handler (on_click exige função com parâmetro)
                    on_click=lambda e: _toggle_tema_rapido(),
                ),

                # Espaçador: afasta o último botão da borda direita da janela
                ft.Container(width=6),
            ],
        )


    # --------------------------------------------------------------------------
    # MAPA DE VIEWS — associa rotas às funções construtoras
    # --------------------------------------------------------------------------
    # Em vez de um if/elif longo, usamos um dicionário para mapear
    # cada rota à sua função de view correspondente.
    # views_map["/"] retorna a função view_home (sem chamá-la ainda).
    views_map = {
        "/":        view_home,
        "/usuario": view_usuario,
        "/config":  view_config,
        "/sobre":   view_sobre,
    }


    # ==========================================================================
    # FUNÇÃO CENTRAL: route_change(e)
    # ==========================================================================
    # Esta é a função mais importante do app — o "coração" da navegação.
    # Ela é chamada em 4 situações:
    #   1. Inicialização do app (chamada direta no final de main)
    #   2. Troca de página (via navegar())
    #   3. Alternância de tema (via toggle_theme_switch ou _toggle_tema_rapido)
    #   4. Redimensionamento que cruza o breakpoint (via on_resize)
    #
    # A cada chamada, ela reconstrói TODA a interface do zero com:
    #   → As cores corretas do tema atual (via paleta())
    #   → O layout correto (mobile ou desktop)
    #   → A view correta para a rota atual
    # ==========================================================================
    def route_change(e=None):

        # Se chamada pelo evento on_route_change do Flet, "e" terá o atributo
        # "route". hasattr() verifica se o atributo existe antes de acessá-lo.
        if e is not None and hasattr(e, "route"):
            estado["rota"] = e.route

        rota   = estado["rota"]    # página a ser exibida
        mobile = estado["mobile"]  # layout a ser usado

        # Gera o dicionário de cores adequado ao tema atual
        p = paleta(estado["dark_mode"])

        # .get(chave, padrao): busca a função da view no mapa
        # Se a rota não existir, usa view_home como fallback (página padrão)
        view_fn = views_map.get(rota, view_home)

        # Define a cor de fundo da janela inteira
        page.bgcolor = p["bg_page"]

        if mobile:
            # ── LAYOUT MOBILE ─────────────────────────────────────────────────
            # Sem menu lateral; a barra de navegação fica na parte inferior.
            conteudo = view_fn(p)   # chama a função da view passando a paleta

            page.views.clear()      # remove todas as views anteriores da pilha

            # ft.View encapsula uma "tela completa" do app com seus componentes
            page.views.append(
                ft.View(
                    route=rota,
                    controls=[conteudo],                      # conteúdo principal
                    appbar=construir_appbar(),                 # barra superior
                    navigation_bar=navigation_bar_mobile(),   # barra inferior
                    bgcolor=p["bg_page"],
                    padding=0,
                    spacing=0,
                )
            )

        else:
            # ── LAYOUT DESKTOP ────────────────────────────────────────────────
            # Menu lateral à esquerda + conteúdo da página à direita.
            # ft.Row posiciona os dois painéis lado a lado.
            conteudo = ft.Row([
                menu_lateral(p),   # painel esquerdo: navegação
                view_fn(p),        # painel direito: conteúdo da rota atual
            ], expand=True, spacing=0)

            page.views.clear()
            page.views.append(
                ft.View(
                    route=rota,
                    controls=[conteudo],
                    appbar=construir_appbar(),
                    bgcolor=p["bg_page"],
                    padding=0,
                    spacing=0,
                )
            )

        # page.update() renderiza todas as mudanças acumuladas de uma só vez
        page.update()


    # --------------------------------------------------------------------------
    # HANDLER: on_resize(e) — Responde ao redimensionamento da janela
    # --------------------------------------------------------------------------
    # Chamado automaticamente pelo Flet sempre que o usuário redimensiona a janela.
    # Implementa o "layout responsivo": troca de mobile↔desktop conforme necessário.
    #
    # Otimização importante: só reconstrói a interface se o estado de
    # mobile MUDOU (cruzou o breakpoint). Sem essa verificação, a interface
    # seria reconstruída a cada pixel de redimensionamento — muito ineficiente.
    # --------------------------------------------------------------------------
    def on_resize(e: ft.PageResizeEvent):

        # e.width: largura atual da janela em pixels
        # Calcula se a largura atual caracteriza layout mobile
        novo_mobile = e.width < BREAKPOINT_MOBILE

        # Compara com o estado anterior para evitar reconstruções desnecessárias
        if novo_mobile != estado["mobile"]:
            estado["mobile"] = novo_mobile  # atualiza o estado
            route_change()                  # reconstrói com o novo layout


    # ==========================================================================
    # REGISTRO DOS EVENTOS DA PÁGINA
    # ==========================================================================
    # Associamos nossas funções handler aos eventos do objeto page.
    # O Flet chama automaticamente essas funções quando os eventos ocorrem.
    # Note que passamos a REFERÊNCIA da função (sem parênteses), não o resultado.
    page.on_resize       = on_resize       # dispara ao redimensionar a janela
    page.on_route_change = route_change    # dispara ao mudar de rota via page.go()


    # ==========================================================================
    # INICIALIZAÇÃO DO APP
    # ==========================================================================
    # Chamamos route_change() manualmente para construir a tela inicial.
    # Sem essa chamada, o app iniciaria com a janela completamente em branco.
    # Não usamos page.go("/") aqui pois isso pode causar conflitos no Flet 0.81.
    route_change()


# ==============================================================================
# PONTO DE ENTRADA DO PROGRAMA
# ==============================================================================
# ft.run(main) inicializa o framework Flet, cria a janela do sistema operacional
# e chama a função main() injetando o objeto page como argumento.
#
# Esta linha SEMPRE deve ser a última do arquivo — nada é executado após ela
# durante a sessão normal do aplicativo.
# ==============================================================================
ft.run(main)