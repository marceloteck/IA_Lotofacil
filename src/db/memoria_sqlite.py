import sqlite3
import os
from collections import Counter

# --- CORREÇÃO DE DIRETÓRIO ---
# Pega o caminho absoluto da pasta onde ESTE arquivo está
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Se este script estiver dentro de 'src/database', precisamos subir níveis para chegar na raiz
# Se ele já estiver na raiz, use apenas: PROJECT_ROOT = BASE_DIR
# Vamos assumir que ele está em 'src/database/', então subimos dois níveis:
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, "..", ".."))

# Define o caminho final do banco de dados
DB_PATH = os.path.join(PROJECT_ROOT, "data", "lotofacil.db")
DATA_DIR = os.path.join(PROJECT_ROOT, "data")


def conectar():
    # Cria a pasta 'data' de forma absoluta antes de conectar
    os.makedirs(DATA_DIR, exist_ok=True)
    return sqlite3.connect(DB_PATH)


def garantir_tabela():
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


def salvar_jogo_premiado(concurso, dezenas, pontos):
    if pontos < 11:
        return False 

    garantir_tabela()

    con = conectar()
    cur = con.cursor()

    dezenas_txt = ",".join(map(str, dezenas))

    cur.execute("""
        INSERT INTO memoria_premiada (concurso, dezenas, pontos)
        VALUES (?, ?, ?)
    """, (concurso, dezenas_txt, pontos))

    con.commit()
    con.close()

    return True


def carregar_memoria_premiada():
    garantir_tabela()

    con = conectar()
    cur = con.cursor()

    cur.execute("""
        SELECT dezenas, pontos
        FROM memoria_premiada
        WHERE pontos >= 11
    """)

    jogos = []
    for dezenas, pontos in cur.fetchall():
        jogos.append({
            "dezenas": list(map(int, dezenas.split(","))),
            "pontos": pontos
        })

    con.close()
    return jogos


def carregar_frequencia_dezenas():
    garantir_tabela()

    con = conectar()
    cur = con.cursor()

    cur.execute("""
        SELECT dezenas
        FROM memoria_premiada
        WHERE pontos >= 11
    """)

    contador = Counter()

    for (dezenas,) in cur.fetchall():
        nums = map(int, dezenas.split(","))
        contador.update(nums)

    con.close()

    return dict(contador)