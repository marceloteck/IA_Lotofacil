import sqlite3
from pathlib import Path

DB_PATH = Path("data/lotofacil.db")


def carregar_concursos():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # 🔎 Detecta estrutura real da tabela
    cur.execute("PRAGMA table_info(concursos)")
    info = cur.fetchall()

    if not info:
        raise RuntimeError("❌ Tabela concursos não encontrada")

    colunas = [c[1] for c in info]

    # 🧠 Detecta coluna do concurso
    col_concurso = None
    for c in info:
        nome = c[1].lower()
        if "concurs" in nome:
            col_concurso = c[1]
            break

    if col_concurso is None:
        col_concurso = colunas[1]  # fallback seguro

    # 🔢 Detecta dezenas automaticamente
    col_dezenas = [c for c in colunas if c != col_concurso]
    col_dezenas = col_dezenas[:15]

    sql = f"""
        SELECT {col_concurso}, {",".join(col_dezenas)}
        FROM concursos
        ORDER BY {col_concurso} ASC
    """

    cur.execute(sql)

    concursos = []
    for row in cur.fetchall():
        concursos.append(
            (int(row[0]), list(map(int, row[1:])))
        )

    conn.close()
    return concursos
