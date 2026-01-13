import sqlite3
import os

DB_PATH = "data/lotofacil.db"


def conectar():
    os.makedirs("data", exist_ok=True)
    return sqlite3.connect(DB_PATH)


def garantir_tabela_memoria():
    con = conectar()
    cur = con.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS memoria_premiada (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            concurso INTEGER,
            dezenas TEXT NOT NULL,
            pontos INTEGER NOT NULL
        )
    """)

    con.commit()
    con.close()


def salvar_memoria(concurso, dezenas, pontos):
    if pontos < 11:
        return

    garantir_tabela_memoria()

    con = conectar()
    cur = con.cursor()

    dezenas_txt = ",".join(map(str, dezenas))

    cur.execute("""
        INSERT INTO memoria_premiada (concurso, dezenas, pontos)
        VALUES (?, ?, ?)
    """, (concurso, dezenas_txt, pontos))

    con.commit()
    con.close()


def carregar_memoria_premiada():
    garantir_tabela_memoria()

    con = conectar()
    cur = con.cursor()

    cur.execute("""
        SELECT dezenas, pontos
        FROM memoria_premiada
        WHERE pontos >= 11
    """)

    dados = []
    for dezenas, pontos in cur.fetchall():
        dados.append({
            "dezenas": list(map(int, dezenas.split(","))),
            "pontos": pontos
        })

    con.close()
    return dados


def carregar_frequencia_dezenas():
    garantir_tabela_memoria()

    con = conectar()
    cur = con.cursor()

    cur.execute("""
        SELECT dezenas
        FROM memoria_premiada
        WHERE pontos >= 11
    """)

    freq = {}
    for (dezenas,) in cur.fetchall():
        for n in map(int, dezenas.split(",")):
            freq[n] = freq.get(n, 0) + 1

    con.close()
    return freq
