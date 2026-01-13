import sqlite3
import os

DB_PATH = "data/lotofacil.db"


def carregar_resultados():
    """
    Carrega concursos do banco SQLite de forma inteligente.
    Detecta automaticamente como as dezenas estão armazenadas.
    Retorna:
    [
        {
            "concurso": int,
            "dezenas": [int, int, ..., int]
        }
    ]
    """

    if not os.path.exists(DB_PATH):
        raise FileNotFoundError(f"Banco não encontrado: {DB_PATH}")

    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()

    # 1️⃣ Descobrir estrutura da tabela concursos
    cur.execute("PRAGMA table_info(concursos)")
    colunas = [c[1] for c in cur.fetchall()]

    if "concurso" not in colunas:
        raise RuntimeError("Tabela concursos não possui coluna 'concurso'")

    # 2️⃣ Caso 1: dezenas em colunas separadas (n1, n2, ...)
    colunas_numericas = [
        c for c in colunas
        if c.lower().startswith(("n", "d", "bola"))
    ]

    resultados = []

    if len(colunas_numericas) >= 15:
        colunas_numericas = sorted(colunas_numericas)

        query = f"""
            SELECT concurso, {",".join(colunas_numericas)}
            FROM concursos
            ORDER BY concurso DESC
        """
        cur.execute(query)

        for row in cur.fetchall():
            concurso = row[0]
            dezenas = list(map(int, row[1:]))

            resultados.append({
                "concurso": concurso,
                "dezenas": dezenas
            })

    # 3️⃣ Caso 2: dezenas em uma única coluna texto
    else:
        coluna_texto = None
        for c in colunas:
            if c.lower() in ("dezenas", "numeros", "resultado"):
                coluna_texto = c
                break

        if not coluna_texto:
            raise RuntimeError(
                "Não foi possível identificar colunas de dezenas na tabela concursos"
            )

        cur.execute(f"""
            SELECT concurso, {coluna_texto}
            FROM concursos
            ORDER BY concurso DESC
        """)

        for concurso, texto in cur.fetchall():
            dezenas = list(map(int, texto.replace(";", ",").split(",")))

            resultados.append({
                "concurso": concurso,
                "dezenas": dezenas
            })

    con.close()

    if not resultados:
        raise RuntimeError("Nenhum concurso carregado do banco")

    return resultados
