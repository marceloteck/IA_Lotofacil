import sqlite3
from pathlib import Path
from datetime import datetime

DB_PATH = Path("data/lotofacil.db")

def conectar():
    return sqlite3.connect(DB_PATH)

def salvar_concurso(concurso, dezenas, data=None):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT OR IGNORE INTO concursos (concurso, dezenas, data)
    VALUES (?, ?, ?)
    """, (concurso, ",".join(map(str, dezenas)), data))

    conn.commit()
    conn.close()

def salvar_tentativa(concurso, tentativa, dezenas, acertos, score, tempo_exec):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO tentativas
    (concurso, tentativa, dezenas, acertos, score, tempo_exec, timestamp)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        concurso,
        tentativa,
        ",".join(map(str, dezenas)),
        acertos,
        score,
        tempo_exec,
        datetime.now().isoformat()
    ))

    conn.commit()
    conn.close()

def salvar_checkpoint(concurso_atual, tentativa_atual):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT OR REPLACE INTO checkpoint
    (id, concurso_atual, tentativa_atual, inicio_timestamp)
    VALUES (1, ?, ?, ?)
    """, (
        concurso_atual,
        tentativa_atual,
        datetime.now().isoformat()
    ))

    conn.commit()
    conn.close()

def carregar_checkpoint():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT concurso_atual, tentativa_atual FROM checkpoint WHERE id=1")
    row = cursor.fetchone()
    conn.close()

    if row:
        return row[0], row[1]
    return None, None
