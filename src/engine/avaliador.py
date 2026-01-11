def contar_pontos(jogo, resultado_real):
    return len(set(jogo) & set(resultado_real))
