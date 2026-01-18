"""
🧠 FILTRO DE IDENTIDADE HISTÓRICA
Bloqueia repetição exata e penaliza similaridade extrema.
"""

def validar_jogo_historico(jogo, historico_resultados):
    """
    Retorna:
    - valido (bool)
    - penalidade (int)
    """

    jogo_set = set(jogo)
    max_repeticao = 0

    for dezenas in historico_resultados:
        dezenas_set = set(dezenas)

        if jogo_set == dezenas_set:
            return False, -9999  # bloqueio total

        repetidas = len(jogo_set & dezenas_set)
        if repetidas > max_repeticao:
            max_repeticao = repetidas

    # Penalização progressiva
    if max_repeticao >= 15:
        return False, -9999
    elif max_repeticao == 14:
        return True, -20
    elif max_repeticao == 13:
        return True, -10
    elif max_repeticao == 12:
        return True, -4
    else:
        return True, 0
