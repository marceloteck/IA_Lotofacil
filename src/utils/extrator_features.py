# src/utils/extrator_features.py

import numpy as np
from src.engine.aprendiz import obter_perfil_vencedor

def extrair_features(jogo, jogo_anterior=None):
    perfil = set(obter_perfil_vencedor())

    soma = sum(jogo)
    pares = sum(1 for d in jogo if d % 2 == 0)
    impares = 15 - pares

    repeticao = len(set(jogo) & set(jogo_anterior)) if jogo_anterior else 0
    perc_perfil = len(set(jogo) & perfil) / len(jogo) if perfil else 0

    dispersao = float(np.std(jogo))
    entropia = len(set(jogo)) / 25

    return {
        "soma": soma,
        "pares": pares,
        "impares": impares,
        "repeticao_anterior": repeticao,
        "perc_perfil": round(perc_perfil, 3),
        "freq_media": 0.0,   # pode evoluir depois
        "dispersao": round(dispersao, 3),
        "entropia": round(entropia, 3)
    }
