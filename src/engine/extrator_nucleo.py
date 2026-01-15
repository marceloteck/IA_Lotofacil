# ==========================================================
# 🧠 EXTRATOR DE NÚCLEO GLOBAL (EVOLUÍDO)
# ==========================================================

from collections import defaultdict
import random
from src.db.memoria_sqlite import carregar_jogos_memoria
from src.db.memoria_sqlite import carregar_frequencia_dezenas

PESOS = {
    11: 1.0,
    12: 2.0,
    13: 4.0,
    14: 6.0,
}

UNIVERSO = list(range(1, 26))


def extrair_nucleo_global():
    """
    Retorna:
    - nucleo: dezenas mais fortes
    - satelites: dezenas boas
    - descartaveis: dezenas fracas
    """

    jogos = carregar_jogos_memoria()  # [(dezenas, pontos), ...]
    score = defaultdict(float)

    for dezenas, pontos in jogos:
        if pontos not in PESOS:
            continue

        peso = PESOS[pontos]
        for d in dezenas:
            score[int(d)] += peso

    if not score:
        return {"nucleo": [], "satelites": [], "descartaveis": []}

    ordenadas = sorted(score.items(), key=lambda x: x[1], reverse=True)
    dezenas_ordenadas = [d for d, _ in ordenadas]

    return {
        "nucleo": dezenas_ordenadas[:6],
        "satelites": dezenas_ordenadas[6:14],
        "descartaveis": dezenas_ordenadas[14:]
    }


# ==========================================================
# 🚀 NOVO: GERADOR DE BASE 18 USANDO O NÚCLEO
# ==========================================================

def gerar_base_18_nucleo():
    """
    Gera uma base 18 de altíssima qualidade usando:
    - núcleo vencedor
    - satélites
    - frequência histórica
    - diversidade controlada
    """

    estrutura = extrair_nucleo_global()
    freq = carregar_frequencia_dezenas() or {}

    base = set()

    # 1️⃣ Núcleo (prioridade máxima)
    base.update(estrutura["nucleo"])

    # 2️⃣ Satélites
    if len(base) < 12:
        faltam = 12 - len(base)
        base.update(estrutura["satelites"][:faltam])

    # 3️⃣ Frequência histórica
    ordenadas_freq = sorted(freq.items(), key=lambda x: x[1], reverse=True)
    for d, _ in ordenadas_freq:
        if len(base) >= 18:
            break
        base.add(int(d))

    # 4️⃣ Diversidade (anti-vício)
    if len(base) < 18:
        restantes = list(set(UNIVERSO) - base)
        base.update(random.sample(restantes, 18 - len(base)))

    return sorted(base)
