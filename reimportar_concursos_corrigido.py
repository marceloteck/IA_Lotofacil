import csv
from src.database.connection import get_conn

CSV_PATH = "data\planilhas\Lotofácil.csv"  # ajuste se necessário


def recriar_tabela():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("DROP TABLE IF EXISTS concursos")

    cur.execute("""
        CREATE TABLE concursos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            concurso INTEGER NOT NULL,
            d1 INTEGER, d2 INTEGER, d3 INTEGER, d4 INTEGER, d5 INTEGER,
            d6 INTEGER, d7 INTEGER, d8 INTEGER, d9 INTEGER, d10 INTEGER,
            d11 INTEGER, d12 INTEGER, d13 INTEGER, d14 INTEGER, d15 INTEGER
        )
    """)

    conn.commit()
    conn.close()
    print("✅ Tabela concursos recriada corretamente")


def importar_csv():
    conn = get_conn()
    cur = conn.cursor()

    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter=';')  # 👈 CORREÇÃO AQUI
        next(reader)  # pula cabeçalho

        total = 0
        for row in reader:
            if len(row) < 16:
                continue  # ignora linha quebrada

            concurso = int(row[0])
            dezenas = [int(x) for x in row[1:16]]

            cur.execute("""
                INSERT INTO concursos (
                    concurso,
                    d1,d2,d3,d4,d5,
                    d6,d7,d8,d9,d10,
                    d11,d12,d13,d14,d15
                ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            """, [concurso] + dezenas)

            total += 1

    conn.commit()
    conn.close()
    print(f"✅ {total} concursos importados corretamente")


if __name__ == "__main__":
    recriar_tabela()
    importar_csv()