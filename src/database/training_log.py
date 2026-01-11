from src.database.connection import get_conn

def init_training_log():
    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS training_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            concurso INTEGER,
            pontos INTEGER,
            score REAL,
            base TEXT
        )
    """)

    conn.commit()
    conn.close()


def salvar_log(concurso, pontos, score, base):
    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO training_log (concurso, pontos, score, base)
        VALUES (?, ?, ?, ?)
    """, (concurso, pontos, score, str(base)))

    conn.commit()
    conn.close()
