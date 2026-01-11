import sqlite3
from src.database.connection import get_conn

def init_learning():
    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS aprendizado (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        concurso INTEGER,
        pontos INTEGER,
        base TEXT
    )
    """)

    conn.commit()
    conn.close()


def salvar_aprendizado(concurso, pontos, base):
    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO aprendizado (concurso, pontos, base)
    VALUES (?, ?, ?)
    """, (concurso, pontos, str(sorted(base))))

    conn.commit()
    conn.close()
