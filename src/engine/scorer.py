from src.engine.brains.brain_patterns import score_padroes
from src.engine.brains.brain_diversity import diversidade


def score_total(base, outras, pontos_reais, score_heuristico):
    score = 0
    score += pontos_reais * 10
    score += score_heuristico * 2
    score += score_padroes(base)
    score += diversidade(base, outras)
    return score
