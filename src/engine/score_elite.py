from collections import Counter

def calcular_score_elite(
    jogo,
    dezenas_quentes,
    dezenas_frias,
    ultimo_resultado,
    perfil_vencedor
):
    score = 0

    jogo = set(jogo)
    ultimo = set(ultimo_resultado or [])
    perfil = set(perfil_vencedor or [])

    # ==================================================
    # 🔥 1️⃣ NÚCLEO REPETIDO (MUITO IMPORTANTE)
    # ==================================================
    intersecao_ultimo = len(jogo & ultimo)

    if 8 <= intersecao_ultimo <= 10:
        score += 30
    elif 6 <= intersecao_ultimo <= 11:
        score += 15
    else:
        score -= 10

    # ==================================================
    # 🔥 2️⃣ PERFIL VENCEDOR HISTÓRICO
    # ==================================================
    score += len(jogo & perfil) * 3

    # ==================================================
    # 🔥 3️⃣ DEZENAS QUENTES
    # ==================================================
    quentes = len(jogo & set(dezenas_quentes))
    score += quentes * 2.5

    # ==================================================
    # ⚖️ 4️⃣ DEZENAS FRIAS (CONTROLE FINO)
    # ==================================================
    frias = len(jogo & set(dezenas_frias))

    if frias <= 2:
        score += 8
    elif frias <= 4:
        score += 2
    else:
        score -= 15

    # ==================================================
    # ⚖️ 5️⃣ PARES / ÍMPARES
    # ==================================================
    pares = len([n for n in jogo if n % 2 == 0])

    if 7 <= pares <= 8:
        score += 6
    elif 6 <= pares <= 9:
        score += 3
    else:
        score -= 5

    # ==================================================
    # ❌ 6️⃣ SEQUÊNCIAS LONGAS
    # ==================================================
    seq = 0
    max_seq = 0
    for n in sorted(jogo):
        if n - 1 in jogo:
            seq += 1
            max_seq = max(max_seq, seq)
        else:
            seq = 0

    if max_seq >= 4:
        score -= max_seq * 3

    return round(score, 2)

