from src.analysis.patterns import *
from src.analysis.score import calcular_score


def analisar_jogo(dezenas, dezenas_anteriores=None):
    """
    Analisa métricas estruturais do jogo.
    NÃO calcula pontos reais.
    """

    metricas = {
        "impares": contar_impares(dezenas),
        "primos": contar_primos(dezenas),
        "multiplos_3": contar_multiplos_3(dezenas),
        "fibonacci": contar_fibonacci(dezenas),
        "moldura": contar_moldura(dezenas),
        "repetidas": contar_repetidas(dezenas, dezenas_anteriores),
    }

    metricas["score_heuristico"] = calcular_score(metricas)

    return metricas


def calcular_pontos_reais(jogo, resultado):
    return len(set(jogo) & set(resultado))
