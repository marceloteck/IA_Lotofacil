def calcular_pontos_reais(jogo, resultado):
    """
    Calcula acertos reais entre jogo gerado e resultado oficial.
    """
    return len(set(jogo) & set(resultado))
