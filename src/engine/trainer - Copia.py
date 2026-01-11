from src.database.connection import get_conn
from src.engine.motor_multicerebro import gerar_jogo
from src.analysis.analyzer import calcular_pontos_reais


def treinar_sequencial():
    print("🧠 Treinamento sequencial iniciado\n")

    conn = get_conn()
    cur = conn.cursor()

    # 🔹 pegar concursos em ordem crescente (antigo → recente)
    cur.execute("""
        SELECT concurso, d1,d2,d3,d4,d5,
               d6,d7,d8,d9,d10,
               d11,d12,d13,d14,d15
        FROM concursos
        ORDER BY concurso ASC
    """)
    rows = cur.fetchall()
    conn.close()

    total = len(rows)

    for i in range(total - 1):
        concurso_atual = rows[i]
        concurso_futuro = rows[i + 1]

        num_atual = concurso_atual[0]
        num_futuro = concurso_futuro[0]

        resultado_real = list(concurso_futuro[1:])

        print(f"📘 Concurso {num_atual} → tentando prever {num_futuro}")

        jogo_previsto = gerar_jogo()

        pontos = calcular_pontos_reais(jogo_previsto, resultado_real)

        print("🎯 Resultado concurso", num_futuro)
        print("   ➜ Jogo:", sorted(jogo_previsto))
        print("   ➜ Pontos:", pontos)
        print("-" * 60)
