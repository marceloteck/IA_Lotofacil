from src.engine.brains.brain_stats import gerar_base_stats
from src.engine.brains.brain_explorer import gerar_base_exploracao
from src.engine.scorer import score_total
from src.database.state import carregar_estado, salvar_estado
from src.analysis.analyzer import analisar_jogo
from src.analysis.pontos import calcular_pontos_reais
from src.database.connection import get_conn

TODAS = list(range(1, 26))


def executar_motor(resultado_real):
    print("🚀 Motor Multicérebro iniciado")

    estado = carregar_estado()
    tentativa = estado["tentativas"]
    limite = estado["limite_tentativas"]

    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute("SELECT numero FROM frequencias ORDER BY peso DESC")
    freq_rank = [int(r[0]) for r in cursor.fetchall()]

    melhor_pontos = 0
    melhor_score = 0
    melhor_base = None

    while tentativa < limite:
        tentativa += 1

        base_stats = gerar_base_stats(freq_rank)
        base_exploracao = gerar_base_exploracao(TODAS)

        metricas = analisar_jogo(base_stats)
        pontos_reais = calcular_pontos_reais(base_stats, resultado_real)

        score = score_total(
            base_stats,
            [base_exploracao],
            pontos_reais,
            metricas["score_heuristico"]
        )

        if pontos_reais > melhor_pontos or score > melhor_score:
            melhor_pontos = pontos_reais
            melhor_score = score
            melhor_base = base_stats

            print(f"⭐ Novo melhor: {melhor_pontos} pontos | score {melhor_score}")

        salvar_estado(tentativa, melhor_pontos)

        if pontos_reais >= 11:
            break

    conn.close()

    return {
        "pontos": melhor_pontos,
        "score": melhor_score,
        "base": melhor_base
    }
