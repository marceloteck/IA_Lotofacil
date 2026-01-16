# ==========================================================
# 🎯 GERADOR FINAL DE JOGOS — MODO PRODUÇÃO
# Com Filtro ELITE (14 e 15 pontos)
# ==========================================================

import random

from src.engine.aprendiz import obter_perfil_vencedor
from src.db.memoria_sqlite import carregar_frequencia_dezenas

from src.engine.filtro_elite import passa_filtro_elite

from src.engine.avaliador import Avaliador

# ----------------------------------------------------------
# CONFIGURAÇÕES
# ----------------------------------------------------------

UNIVERSO = list(range(1, 26))

TOTAL_JOGOS_15 = 10
TOTAL_JOGOS_18 = 7

TENTATIVAS_MAX = 500  # evita loop infinito


# ----------------------------------------------------------
# GERADOR BASE (NÃO MEXER — JÁ FUNCIONA)
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

def gerar_jogos_finais(
    dezenas_quentes,
    dezenas_frias,
    ultimo_resultado
):
    """
    Gera jogos finais já filtrados pelo FILTRO ELITE
    Não interfere no treinamento
    """

    jogos_15 = []
    jogos_18 = []

    tentativas = 0

    # ===============================
    # 🎯 JOGOS DE 15 DEZENAS
    # ===============================
    while len(jogos_15) < TOTAL_JOGOS_15 and tentativas < TENTATIVAS_MAX:
        jogo = gerar_jogo_custom(15)

        if passa_filtro_elite(
            jogo,
            dezenas_quentes,
            dezenas_frias,
            ultimo_resultado
        ):
            if jogo not in jogos_15:
                jogos_15.append(jogo)

        tentativas += 1

    # ===============================
    # 🎯 JOGOS DE 18 DEZENAS
    # ===============================
    tentativas = 0

    while len(jogos_18) < TOTAL_JOGOS_18 and tentativas < TENTATIVAS_MAX:
        jogo = gerar_jogo_custom(18)

        if passa_filtro_elite(
            jogo,
            dezenas_quentes,
            dezenas_frias,
            ultimo_resultado
        ):
            if jogo not in jogos_18:
                jogos_18.append(jogo)

        tentativas += 1

    return jogos_15, jogos_18
