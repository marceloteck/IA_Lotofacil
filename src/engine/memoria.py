import sqlite3
from pathlib import Path

DB_PATH = Path("data/loto.db")

def inicializar_memoria():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS memoria_premiada (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            concurso_previsto INTEGER,
            pontos INTEGER,
            jogo TEXT
        )
    """)

    conn.commit()
    conn.close()


def salvar_jogo_premiado(concurso_previsto, jogo, pontos):
    if pontos < 11:
        return  # REGRA DE OURO

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO memoria_premiada (concurso_previsto, pontos, jogo)
        VALUES (?, ?, ?)
    """, (
        concurso_previsto,
        pontos,
        ",".join(map(str, jogo))
    ))

    conn.commit()
    conn.close()


def listar_melhores(min_pontos=11):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
        SELECT concurso_previsto, pontos, jogo
        FROM memoria_premiada
        WHERE pontos >= ?
        ORDER BY pontos DESC
    """, (min_pontos,))

    resultados = cur.fetchall()
    conn.close()

    return resultados