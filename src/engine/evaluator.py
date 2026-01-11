def contar_acertos(base, concurso_real):
    """
    base: set ou list com 18 dezenas
    concurso_real: set com 15 dezenas
    """
    return len(set(base) & set(concurso_real))
