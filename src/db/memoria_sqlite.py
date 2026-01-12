import sqlite3

DB_PATH = "data/lotofacil.db"

def carregar_memoria_premiada():
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()

    cur.execute("""
        SELECT dezenas, pontos
        FROM memoria_premiada
        WHERE pontos >= 11
    """)

    dados = []
    for dezenas, pontos in cur.fetchall():
        jogo = list(map(int, dezenas.split(",")))
        dados.append({
            "dezenas": jogo,
            "pontos": pontos
        })

    con.close()
    return dados
