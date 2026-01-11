from src.database.connection import get_conn

def init_db():
    conn = get_conn()
    cursor = conn.cursor()

    # Tabela de concursos
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS concursos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        concurso INTEGER,
        d1 INTEGER, d2 INTEGER, d3 INTEGER, d4 INTEGER, d5 INTEGER,
        d6 INTEGER, d7 INTEGER, d8 INTEGER, d9 INTEGER, d10 INTEGER,
        d11 INTEGER, d12 INTEGER, d13 INTEGER, d14 INTEGER, d15 INTEGER
    )
    """)

    # Tabela de frequências
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS frequencias (
        numero INTEGER PRIMARY KEY,
        quantidade INTEGER,
        peso REAL
    )
    """)

    # Estado do motor
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS estado_motor (
        id INTEGER PRIMARY KEY,
        tentativas INTEGER,
        melhor_pontos INTEGER
    )
    """)

    # Inicializa estado se não existir
    cursor.execute("SELECT COUNT(*) FROM estado_motor")
    if cursor.fetchone()[0] == 0:
        cursor.execute("""
        INSERT INTO estado_motor (id, tentativas, melhor_pontos)
        VALUES (1, 0, 0)
        """)

    conn.commit()
    conn.close()
    print("✅ Banco inicializado com sucesso")

if __name__ == "__main__":
    init_db()
