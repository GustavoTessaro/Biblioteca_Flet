# Biblioteca Flet 📚

Sistema de gerenciamento de biblioteca desenvolvido em Python utilizando Flet, com interface moderna, responsiva e persistência local em JSON.

O projeto permite o gerenciamento completo de:

- Clientes
- Livros
- Prateleiras
- Empréstimos
- Multas

Além disso, o sistema possui:
- Tema claro/escuro
- Interface responsiva para desktop e mobile
- Controle automático de atrasos
- Geração automática de multas
- Persistência de dados local
- Componentes reutilizáveis

---

# 🖼️ Interface do Sistema

O sistema possui:

- Sidebar lateral no desktop
- Navigation Bar para mobile
- Cards informativos
- Sistema de notificações (SnackBar)
- Alternância entre tema claro e escuro

---

# 🚀 Tecnologias Utilizadas

- Python 3
- Flet
- JSON
- AsyncIO

---

# 📁 Estrutura do Projeto

```text
Biblioteca_Flet/
│
├── .gitignore
├── requirements.txt
├── run.py
│
└── app/
    ├── main.py
    │
    ├── components/
    │   ├── appbar.py
    │   ├── buttons.py
    │   ├── cards.py
    │   ├── layout.py
    │   ├── menu.py
    │   └── navigation.py
    │
    ├── core/
    │   ├── constants.py
    │   ├── helpers.py
    │   └── theme.py
    │
    ├── data/
    │   ├── salvarAtualizar.py
    │   └── storage.py
    │
    ├── services/
    │   ├── cliente_service.py
    │   ├── emprestimo_service.py
    │   ├── livro_service.py
    │   ├── multa_service.py
    │   └── prateleira_service.py
    │
    └── views/
        ├── clientes_view.py
        ├── emprestimos_view.py
        ├── home_view.py
        ├── livros_view.py
        ├── multas_view.py
        └── prateleiras_view.py
```

---

# ⚙️ Funcionalidades

## 👤 Clientes

- Cadastro de clientes
- Edição de clientes
- Exclusão de clientes
- Pesquisa dinâmica
- Validação de:
  - E-mail
  - Telefone
- Proteção contra exclusão de clientes com empréstimos ativos

---

## 📚 Livros

- Cadastro de livros
- Edição de livros
- Exclusão de livros
- Controle de quantidade
- Controle de disponibilidade
- Associação com prateleiras
- Pesquisa dinâmica
- Controle automático de exemplares emprestados

---

## 🗂️ Prateleiras

- Cadastro de prateleiras
- Configuração de:
  - prazo de empréstimo
  - multa por dia
- Edição
- Exclusão protegida
- Pesquisa dinâmica

---

## 🔄 Empréstimos

- Cadastro de empréstimos
- Controle de devolução
- Histórico de empréstimos
- Controle automático de status:
  - Aberto
  - Atrasado
  - Entregue
- Verificação automática de disponibilidade do livro
- Atualização automática de multas

---

## 💰 Multas

- Geração automática de multas
- Cálculo automático baseado em dias de atraso
- Controle de pagamento
- Histórico de multas
- Limpeza de histórico

---

# 🎨 Interface Responsiva

O sistema possui suporte para:

## 🖥️ Desktop
- Sidebar lateral
- Layout expandido
- Navegação completa

## 📱 Mobile
- Navigation Bar inferior
- Layout adaptável
- Componentes reorganizados automaticamente

---

# 🌙 Tema Claro e Escuro

O sistema possui alternância dinâmica entre:

- Light Mode
- Dark Mode

A paleta de cores é controlada centralmente pelo arquivo:

```python
core/theme.py
```

---

# 💾 Persistência de Dados

Os dados são armazenados localmente utilizando JSON:

```text
biblioteca_data.json
```

Estruturas persistidas:

- clientes
- livros
- prateleiras
- empréstimos
- multas

---

# 🧠 Arquitetura do Projeto

O projeto foi organizado utilizando separação de responsabilidades:

| Camada | Responsabilidade |
|---|---|
| components | Componentes reutilizáveis da interface |
| core | Constantes, helpers e tema |
| data | Persistência e atualização dos dados |
| services | Regras de negócio |
| views | Telas do sistema |

---

# 🔒 Regras de Negócio

## Clientes
- Não é possível excluir clientes com empréstimos ativos
- Não é permitido cadastrar clientes duplicados

## Livros
- Não é possível excluir livros emprestados
- Livros iguais aumentam quantidade automaticamente

## Prateleiras
- Não é possível excluir prateleiras com livros vinculados

## Empréstimos
- Um livro só pode ser emprestado se houver exemplares disponíveis
- Empréstimos atrasados geram multas automaticamente

## Multas
- Multas são calculadas automaticamente
- Empréstimos com multa pendente exigem quitação antes da devolução

---

# ▶️ Como Executar o Projeto

## 1️⃣ Clone o repositório

```bash
git clone <URL_DO_REPOSITORIO>
```

---

## 2️⃣ Execute o arquivo de configuração

```bash
python run.py
```

O script irá:
- criar a virtual environment
- instalar dependências
- configurar o ambiente automaticamente

---

## 3️⃣ Ative o ambiente virtual

### Windows

```bash
.\venv\Scripts\activate
```

### Linux / MacOS

```bash
source venv/bin/activate
```

---

## 4️⃣ Execute a aplicação

```bash
python app/main.py
```

---

# 📦 Dependências

Arquivo:

```text
requirements.txt
```

Dependência principal:

```text
flet
```

---

# 🛠️ Melhorias Futuras

- Banco de dados SQLite/PostgreSQL
- Sistema de autenticação
- Dashboard com gráficos
- Exportação de relatórios
- Upload de capas dos livros
- Sistema de reservas
- Notificações automáticas
- API REST
- Dockerização da aplicação

---

# 📖 Objetivo do Projeto

Este projeto foi desenvolvido com o objetivo de praticar:

- Desenvolvimento de interfaces modernas em Python
- Arquitetura modular
- Responsividade
- Persistência de dados
- Regras de negócio
- Organização de projetos reais
- Programação assíncrona com AsyncIO

---

# 👨‍💻 Autor

Desenvolvido por Gustavo Tessaro.
