from collections import Counter

def calcular_score_elite(
    jogo,
    dezenas_quentes,
    dezenas_frias,
    ultimo_resultado,
    perfil_vencedor=None
):
    """
    Retorna um score de 0 a 100 para um jogo.
    NÃO bloqueia, apenas pontua.
    """

    score = 0

    jogo_set = set(jogo)

    # 🔥 1️⃣ Dezenas quentes (peso alto)
    score += len(jogo_set & set(dezenas_quentes)) * 6

    # ❄️ 2️⃣ Penalidade por dezenas frias
    score -= len(jogo_set & set(dezenas_frias)) * 4

    # 🔁 3️⃣ Repetição do último concurso (controle)
    repetidas = jogo_set & set(ultimo_resultado)
    if 7 <= len(repetidas) <= 11:
        score += 10
    elif len(repetidas) > 13:
        score -= 10

    # 🧠 4️⃣ Perfil vencedor aprendido
    if perfil_vencedor:
        score += len(jogo_set & set(perfil_vencedor)) * 3

    # ⚖️ 5️⃣ Balanceamento par/ímpar
    pares = sum(1 for n in jogo if n % 2 == 0)
    if 6 <= pares <= 9:
        score += 8
    else:
        score -= 5

    # 🔢 6️⃣ Distribuição por dezenas (baixas/médias/altas)
    baixas = sum(1 for n in jogo if n <= 8)
    medias = sum(1 for n in jogo if 9 <= n <= 17)
    altas  = sum(1 for n in jogo if n >= 18)

    if 4 <= baixas <= 6 and 5 <= medias <= 7 and 4 <= altas <= 6:
        score += 10

    return max(0, min(score, 100))
