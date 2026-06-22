import json
import os
import sqlite3

from core.constants import DATA_FILE

APP_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
DB_FILE = os.path.join(APP_ROOT, "biblioteca.db")

conexao = sqlite3.connect(DB_FILE, check_same_thread=False)
cursor = conexao.cursor()

cursor.execute("PRAGMA foreign_keys = ON;")

cursor.execute("""
CREATE TABLE IF NOT EXISTS clientes(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT,
    telefone TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS prateleiras(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    dias_e_prazo INTEGER NOT NULL,
    multa_por_dia REAL NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS livros(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo TEXT NOT NULL,
    autor TEXT NOT NULL,
    prateleira_id INTEGER NOT NULL,
    quantidade INTEGER NOT NULL,
    FOREIGN KEY(prateleira_id) REFERENCES prateleiras(id) ON DELETE CASCADE
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS emprestimos(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente_id INTEGER NOT NULL,
    livro_id INTEGER NOT NULL,
    status TEXT NOT NULL,
    data_emprestimo TEXT NOT NULL,
    data_entrega TEXT NOT NULL,
    FOREIGN KEY(cliente_id) REFERENCES clientes(id) ON DELETE CASCADE,
    FOREIGN KEY(livro_id) REFERENCES livros(id) ON DELETE CASCADE
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS multas(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    emprestimo_id INTEGER NOT NULL,
    cliente_id INTEGER NOT NULL,
    livro_id INTEGER NOT NULL,
    dias_atraso INTEGER NOT NULL,
    valor REAL NOT NULL,
    status TEXT NOT NULL,
    FOREIGN KEY(emprestimo_id) REFERENCES emprestimos(id) ON DELETE CASCADE,
    FOREIGN KEY(cliente_id) REFERENCES clientes(id) ON DELETE CASCADE,
    FOREIGN KEY(livro_id) REFERENCES livros(id) ON DELETE CASCADE
)
""")

conexao.commit()

TABLES = {
    "clientes": ("id", "nome", "email", "telefone"),
    "prateleiras": ("id", "nome", "dias_e_prazo", "multa_por_dia"),
    "livros": ("id", "titulo", "autor", "prateleira_id", "quantidade"),
    "emprestimos": ("id", "cliente_id", "livro_id", "status", "data_emprestimo", "data_entrega"),
    "multas": ("id", "emprestimo_id", "cliente_id", "livro_id", "dias_atraso", "valor", "status"),
}


def _query_rows(table: str, columns: tuple[str, ...]) -> list[dict]:
    cursor.execute(f"SELECT {', '.join(columns)} FROM {table}")
    return [dict(zip(columns, row)) for row in cursor.fetchall()]


def _has_existing_data() -> bool:
    for table in TABLES:
        cursor.execute(f"SELECT 1 FROM {table} LIMIT 1")
        if cursor.fetchone():
            return True
    return False


def _delete_all_rows() -> None:
    cursor.execute("PRAGMA foreign_keys = OFF;")
    for table in ("multas", "emprestimos", "livros", "prateleiras", "clientes"):
        cursor.execute(f"DELETE FROM {table}")
    cursor.execute("PRAGMA foreign_keys = ON;")


def _insert_rows(table: str, columns: tuple[str, ...], rows: list[dict]) -> None:
    if not rows:
        return
    placeholders = ", ".join("?" for _ in columns)
    query = f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({placeholders})"
    values = [tuple(item.get(column) for column in columns) for item in rows]
    cursor.executemany(query, values)


def _migrate_json_to_db() -> None:
    if not os.path.exists(DATA_FILE):
        return

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)
    except (OSError, json.JSONDecodeError):
        return

    if not isinstance(dados, dict):
        return

    salvar_dados(dados)


def carregar_dados() -> dict:
    if os.path.exists(DATA_FILE) and not _has_existing_data():
        _migrate_json_to_db()

    return {
        table: _query_rows(table, columns)
        for table, columns in TABLES.items()
    }


def salvar_dados(dados: dict) -> None:
    _delete_all_rows()

    _insert_rows("clientes", TABLES["clientes"], dados.get("clientes", []))
    _insert_rows("prateleiras", TABLES["prateleiras"], dados.get("prateleiras", []))
    _insert_rows("livros", TABLES["livros"], dados.get("livros", []))
    _insert_rows("emprestimos", TABLES["emprestimos"], dados.get("emprestimos", []))
    _insert_rows("multas", TABLES["multas"], dados.get("multas", []))

    conexao.commit()
