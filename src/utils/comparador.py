def contar_acertos(jogo, resultado_real):
    return len(set(jogo) & set(resultado_real))
