# ==========================================================
# 🎯 FECHAMENTO AUTOMÁTICO INTELIGENTE
# ==========================================================

import itertools


def gerar_fechamento(base, tamanho_jogo=15, max_jogos=100):
    combinacoes = itertools.combinations(base, tamanho_jogo)

    jogos = []
    for comb in combinacoes:
        jogos.append(list(comb))
        if len(jogos) >= max_jogos:
            break

    return jogos
