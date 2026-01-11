import sqlite3
from pathlib import Path

DB_PATH = Path("data/lotofacil.db")


def carregar_concursos():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
        SELECT concurso, dezenas
        FROM concursos
        ORDER BY concurso ASC
    """)

    dados = []
    for concurso, dezenas in cur.fetchall():
        dezenas = list(map(int, dezenas.split(",")))
        dados.append((concurso, dezenas))

    conn.close()
    return dados
