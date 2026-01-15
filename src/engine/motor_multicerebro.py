import random
from collections import Counter
from src.db.memoria_sqlite import carregar_frequencia_dezenas
from src.engine.aprendiz import obter_perfil_vencedor

TOTAL_DEZENAS = 18
UNIVERSO = list(range(1, 26))

# ===============================
# PARÂMETROS DE INTELIGÊNCIA
# ===============================
MAX_PERFIL = 6          # máximo do perfil vencedor
MIN_NUCLEO = 4          # núcleo mínimo garantido
MAX_FREQ_DOMINANCIA = 10  # evita vício em poucas dezenas


def gerar_jogo():
    perfil = obter_perfil_vencedor() or []
    freq_dict = carregar_frequencia_dezenas() or {}

    jogo = set()

    # ===============================
    # 1️⃣ PERFIL VENCEDOR (núcleo)
    # ===============================
    if perfil:
        escolhidas = random.sample(perfil, min(MAX_PERFIL, len(perfil)))
        jogo.update(escolhidas)

    # ===============================
    # 2️⃣ FREQUÊNCIA COM PESO
    # ===============================
    if freq_dict:
        # ordena por frequência
        ordenadas = sorted(freq_dict.items(), key=lambda x: x[1], reverse=True)

        # limita dominância
        top_freq = ordenadas[:MAX_FREQ_DOMINANCIA]

        pool_frequente = []
        for dezena, peso in top_freq:
            pool_frequente.extend([int(dezena)] * peso)

        restantes = TOTAL_DEZENAS - len(jogo)
        if restantes > 0 and pool_frequente:
            amostra = set(random.sample(pool_frequente, min(restantes, len(pool_frequente))))
            jogo.update(amostra)

    # ===============================
    # 3️⃣ GARANTIA DE NÚCLEO
    # ===============================
    if len(jogo) < MIN_NUCLEO and perfil:
        faltantes = MIN_NUCLEO - len(jogo)
        extras = list(set(perfil) - jogo)
        if extras:
            jogo.update(random.sample(extras, min(faltantes, len(extras))))

    # ===============================
    # 4️⃣ ALEATORIEDADE INTELIGENTE
    # ===============================
    restantes = TOTAL_DEZENAS - len(jogo)
    if restantes > 0:
        pool = list(set(UNIVERSO) - jogo)
        jogo.update(random.sample(pool, restantes))

    # ===============================
    # 5️⃣ VALIDAÇÃO FINAL
    # ===============================
    if len(jogo) != TOTAL_DEZENAS:
        pool = list(set(UNIVERSO) - jogo)
        jogo.update(random.sample(pool, TOTAL_DEZENAS - len(jogo)))

    return sorted(jogo)
