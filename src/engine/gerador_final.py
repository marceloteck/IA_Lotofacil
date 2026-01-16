# ==========================================================
# 🎯 GERADOR FINAL DE JOGOS — MODO PRODUÇÃO
# ==========================================================

import random

from src.engine.aprendiz import obter_perfil_vencedor
from src.db.memoria_sqlite import carregar_frequencia_dezenas
from src.engine.filtro_elite import passa_filtro_elite
from src.engine.score_elite import calcular_score_elite

# ----------------------------------------------------------
# CONFIGURAÇÕES
# ----------------------------------------------------------

UNIVERSO = list(range(1, 26))

TOTAL_JOGOS_15 = 10
TOTAL_JOGOS_18 = 7
TENTATIVAS_MAX = 500


# ----------------------------------------------------------
# GERADOR BASE (ROBUSTO)
# ----------------------------------------------------------

def gerar_jogo_custom(tamanho):
    perfil = obter_perfil_vencedor()
    freq = carregar_frequencia_dezenas()

    jogo = set()

    # 🔹 Perfil vencedor (até 40%)
    if perfil:
        qtd = min(int(tamanho * 0.4), len(perfil))
        jogo.update(random.sample(perfil, qtd))

    # 🔹 Frequência histórica
    if freq:
        ordenadas = sorted(freq.items(), key=lambda x: x[1], reverse=True)
        frequentes = [int(n) for n, _ in ordenadas]

        restantes = tamanho - len(jogo)
        if restantes > 0:
            jogo.update(random.sample(frequentes, min(restantes, len(frequentes))))

    # 🔹 Aleatório controlado
    restantes = tamanho - len(jogo)
    if restantes > 0:
        pool = list(set(UNIVERSO) - jogo)
        jogo.update(random.sample(pool, restantes))

    return sorted(jogo)


# ----------------------------------------------------------
# GERADOR FINAL + FILTRO ELITE
# ----------------------------------------------------------

def gerar_jogos_finais(dezenas_quentes, dezenas_frias, ultimo_resultado):
    """
    Gera jogos finais filtrados e ranqueados
    """

    jogos_15 = []
    jogos_18 = []

    perfil = obter_perfil_vencedor()

    # ===============================
    # 🎯 JOGOS DE 15 DEZENAS
    # ===============================
    candidatos_15 = []
    tentativas = 0

    while len(candidatos_15) < 50 and tentativas < TENTATIVAS_MAX:
        jogo = gerar_jogo_custom(15)

        if passa_filtro_elite(jogo, dezenas_quentes, dezenas_frias, ultimo_resultado):
            score = calcular_score_elite(
                jogo,
                dezenas_quentes,
                dezenas_frias,
                ultimo_resultado,
                perfil
            )
            candidatos_15.append((score, jogo))

        tentativas += 1

    candidatos_15.sort(reverse=True)
    jogos_15 = [j for _, j in candidatos_15[:TOTAL_JOGOS_15]]

    # ===============================
    # 🎯 JOGOS DE 18 DEZENAS
    # ===============================
    candidatos_18 = []
    tentativas = 0

    while len(candidatos_18) < 40 and tentativas < TENTATIVAS_MAX:
        jogo = gerar_jogo_custom(18)

        if passa_filtro_elite(jogo, dezenas_quentes, dezenas_frias, ultimo_resultado):
            score = calcular_score_elite(
                jogo,
                dezenas_quentes,
                dezenas_frias,
                ultimo_resultado,
                perfil
            )
            candidatos_18.append((score, jogo))

        tentativas += 1

    candidatos_18.sort(reverse=True)
    jogos_18 = [j for _, j in candidatos_18[:TOTAL_JOGOS_18]]

    return jogos_15, jogos_18
