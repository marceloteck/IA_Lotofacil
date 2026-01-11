from src.database.connection import get_conn

def normalizar(valor):
    if isinstance(valor, int):
        return valor
    if isinstance(valor, bytes):
        if len(valor) == 8:
            return int.from_bytes(valor, byteorder="little", signed=False)
        return int(valor.decode(errors="ignore"))
    return valor


def debug_concursos(limit=30):
    print("\n🔎 ANALISANDO TABELA concursos\n")

    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, concurso,
               d1,d2,d3,d4,d5,
               d6,d7,d8,d9,d10,
               d11,d12,d13,d14,d15
        FROM concursos
        ORDER BY id
        LIMIT ?
    """, (limit,))

    rows = cursor.fetchall()
    conn.close()

    if not rows:
        print("❌ Tabela concursos está vazia")
        return

    concursos = []

    for row in rows:
        id_db = row[0]
        concurso_raw = row[1]
        concurso = normalizar(concurso_raw)

        dezenas = [normalizar(d) for d in row[2:]]

        concursos.append(concurso)

        print(f"ID {id_db:4} | Concurso: {concurso_raw!r} -> {concurso}")
        print(f"     Dezenas: {dezenas}")

        # valida dezenas
        for d in dezenas:
            if not isinstance(d, int) or d < 1 or d > 25:
                print("     ❌ DEZENA INVÁLIDA DETECTADA")

    print("\n📊 VERIFICAÇÃO DE SEQUÊNCIA DOS CONCURSOS\n")

    for i in range(1, len(concursos)):
        diff = concursos[i] - concursos[i - 1]
        if diff != 1:
            print(
                f"⚠️ Salto anormal entre concursos: "
                f"{concursos[i-1]} → {concursos[i]} (Δ = {diff})"
            )

    print("\n✅ Diagnóstico concluído")


def debug_frequencias():
    print("\n🔎 ANALISANDO TABELA frequencias\n")

    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute("SELECT numero, quantidade, peso FROM frequencias ORDER BY numero")
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        print("❌ Tabela frequencias está vazia")
        return

    for numero, qtd, peso in rows:
        numero_n = normalizar(numero)
        print(f"Número {numero_n} | qtd={qtd} | peso={peso}")

        if not isinstance(numero_n, int) or numero_n < 1 or numero_n > 25:
            print("❌ NÚMERO INVÁLIDO NA FREQUÊNCIA")


if __name__ == "__main__":
    debug_concursos()
    debug_frequencias()
