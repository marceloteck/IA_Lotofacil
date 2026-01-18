"""
🎯 SCORE 14/15
Calcula um score numérico de proximidade estatística
com base em memória, estatística e anti-caos.
"""

from collections import Counter

from src.engine.filtro_identidade import validar_jogo_historico


def score_memoria(jogo, memoria_1415):
    """
    Mede o quanto o jogo se parece com jogos 14/15 já memorizados.
    """
    if not memoria_1415:
        return 0

    jogo_set = set(jogo)
    soma = 0

    for jogo_mem in memoria_1415:
        intersecao = len(jogo_set & set(jogo_mem))
        soma += intersecao

    return soma / len(memoria_1415)


def score_estatistico(jogo, dezenas_quentes, dezenas_frias):
    """
    Score baseado em dezenas quentes e frias
    (viés controlado, não extremo).
    """
    quentes = len(set(jogo) & set(dezenas_quentes))
    frias = len(set(jogo) & set(dezenas_frias))

    return (quentes * 2) - (frias * 1)


def score_estrutura(jogo):
    """
    Avalia estrutura interna do jogo:
    - Pares / ímpares
    - Distribuição baixa/alta
    """
    pares = sum(1 for d in jogo if d % 2 == 0)
    impares = len(jogo) - pares

    baixos = sum(1 for d in jogo if d <= 12)
    altos = len(jogo) - baixos

    score = 0

    # equilíbrio estrutural
    if 6 <= pares <= 9:
        score += 3
    if 6 <= baixos <= 9:
        score += 3

    return score


def calcular_score_1415(
    jogo,
    memoria_1415,
    dezenas_quentes,
    dezenas_frias,
    historico_resultados
):
    """
    SCORE FINAL DE QUALIDADE 14/15
    """

    # ===============================
    # 🚫 FILTRO HISTÓRICO
    # ===============================
    valido, penalidade_hist = validar_jogo_historico(
        jogo, historico_resultados
    )

    if not valido:
        return -9999  # impossível

    # ===============================
    # 🧠 SCORES PARCIAIS
    # ===============================
    s_memoria = score_memoria(jogo, memoria_1415)
    s_est = score_estatistico(jogo, dezenas_quentes, dezenas_frias)
    s_estr = score_estrutura(jogo)

    # ===============================
    # ⚖️ SCORE FINAL
    # ===============================
    score_final = (
        (s_memoria * 1.5) +
        (s_est * 1.0) +
        (s_estr * 1.0) +
        penalidade_hist
    )

    return round(score_final, 2)
