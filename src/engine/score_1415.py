"""
🔥 SCORE 14–15 REAL
Score matemático focado em padrões vencedores reais.
"""

from collections import Counter
from src.engine.filtro_identidade import validar_jogo_historico


def calcular_score_1415(
    jogo,
    memoria_1415,            # lista de jogos [[...], [...]]
    dezenas_quentes,
    dezenas_frias,
    historico_resultados
):
    # ---------------------------
    # PROTEÇÕES
    # ---------------------------
    if not isinstance(jogo, (list, tuple)) or len(jogo) != 15:
        return -9999

    score = 0.0

    # ----------------------------------
    # 1️⃣ FILTRO HISTÓRICO (ANTI-CLONE)
    # ----------------------------------
    valido, penal_hist = validar_jogo_historico(jogo, historico_resultados)
    if not valido:
        return -9999

    score += penal_hist

    # ----------------------------------
    # 2️⃣ FREQUÊNCIA HISTÓRICA REAL
    # ----------------------------------
    freq = Counter()
    for j in memoria_1415:
        freq.update(j)

    score_freq = sum(freq.get(d, 0) for d in jogo)
    score += score_freq * 0.004  # ⚠️ PESO REDUZIDO (antes estava matando tudo)

    # ----------------------------------
    # 3️⃣ DEZENAS QUENTES / FRIAS
    # ----------------------------------
    quentes = len(set(jogo) & set(dezenas_quentes))
    frias = len(set(jogo) & set(dezenas_frias))

    score += quentes * 2.0
    score -= frias * 1.0

    # ----------------------------------
    # 4️⃣ PAR / ÍMPAR (ideal 7/8)
    # ----------------------------------
    pares = sum(1 for d in jogo if d % 2 == 0)
    impares = 15 - pares
    score += max(0, 10 - abs(pares - impares) * 1.5)

    # ----------------------------------
    # 5️⃣ SEQUÊNCIAS LONGAS (PENALIZA)
    # ----------------------------------
    ordenado = sorted(jogo)
    seq = sum(
        1 for i in range(len(ordenado) - 1)
        if ordenado[i] + 1 == ordenado[i + 1]
    )

    score -= seq * 1.2  # ⚠️ suavizado

    return round(score, 3)
