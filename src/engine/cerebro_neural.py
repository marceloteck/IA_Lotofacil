# ==========================================================
# 🤖 CÉREBRO NEURAL CONSULTIVO (SIMPLIFICADO)
# ==========================================================

def avaliar_base(base):
    pares = len([x for x in base if x % 2 == 0])
    impares = len(base) - pares

    equilibrio = 1 - abs(pares - impares) / len(base)

    score = round(0.6 * equilibrio + 0.4, 2)

    return {
        "score": score,
        "equilibrio": equilibrio,
        "aprovado": score >= 0.75
    }
