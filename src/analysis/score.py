def score_faixa(valor, faixas):
    return 1 if valor in faixas else 0


def calcular_score(metricas):
    score = 0

    score += score_faixa(metricas["impares"], {8, 9})
    score += score_faixa(metricas["primos"], {5, 6})
    score += score_faixa(metricas["multiplos_3"], {4, 6})
    score += score_faixa(metricas["fibonacci"], {3, 5})
    score += score_faixa(metricas["moldura"], {9, 10})
    score += score_faixa(metricas["repetidas"], {8, 10})

    return score
