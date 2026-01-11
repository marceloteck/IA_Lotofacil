# src/generator/generator.py

import random
from src.analysis.patterns import (
    contar_impares,
    contar_primos,
    contar_multiplos_3,
    contar_fibonacci,
    contar_moldura,
)
from src.generator.constraints import CONSTRAINTS
from src.generator.diversity import diversidade

UNIVERSO = list(range(1, 26))


def jogo_valido(jogo):
    return (
        CONSTRAINTS["impares"][0] <= contar_impares(jogo) <= CONSTRAINTS["impares"][1]
        and CONSTRAINTS["primos"][0] <= contar_primos(jogo) <= CONSTRAINTS["primos"][1]
        and CONSTRAINTS["multiplos_3"][0]
        <= contar_multiplos_3(jogo)
        <= CONSTRAINTS["multiplos_3"][1]
        and CONSTRAINTS["fibonacci"][0]
        <= contar_fibonacci(jogo)
        <= CONSTRAINTS["fibonacci"][1]
        and CONSTRAINTS["moldura"][0]
        <= contar_moldura(jogo)
        <= CONSTRAINTS["moldura"][1]
    )


def gerar_jogo_18(jogos_anteriores=None, tentativas=500):
    if jogos_anteriores is None:
        jogos_anteriores = []

    for _ in range(tentativas):
        jogo = sorted(random.sample(UNIVERSO, 18))

        if not jogo_valido(jogo):
            continue

        if not diversidade(jogo, jogos_anteriores):
            continue

        return jogo

    return None
