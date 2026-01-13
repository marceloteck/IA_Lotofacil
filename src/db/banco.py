import sqlite3

DB_PATH = "data/lotofacil.db"


def carregar_concursos():
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()

    cur.execute("SELECT * FROM concursos ORDER BY concurso")

    concursos = []
    for row in cur.fetchall():
        concurso = row[0]
        dezenas = list(map(int, row[1:16]))
        concursos.append((concurso, dezenas))

    con.close()
    return concursos
