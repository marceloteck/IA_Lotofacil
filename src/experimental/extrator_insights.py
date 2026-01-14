# src/experimental/extrator_insights.py

import json
import statistics
from collections import Counter

class ExtratorInsights:

    def __init__(self, jogos_premiados, perfil_vencedor):
        self.jogos = jogos_premiados
        self.perfil = set(perfil_vencedor)

    def extrair(self):
        somas = []
        pares = []
        repeticoes = []
        uso_perfil = []

        for jogo in self.jogos:
            soma = sum(jogo)
            qtd_pares = sum(1 for d in jogo if d % 2 == 0)
            repeticao = len(set(jogo) & self.perfil)
            perc_perfil = repeticao / len(jogo)

            somas.append(soma)
            pares.append(qtd_pares)
            repeticoes.append(repeticao)
            uso_perfil.append(perc_perfil)

        return {
            "faixa_soma": [
                int(statistics.mean(somas) - statistics.stdev(somas)),
                int(statistics.mean(somas) + statistics.stdev(somas))
            ],
            "media_pares": round(statistics.mean(pares), 2),
            "media_repeticao_perfil": round(statistics.mean(repeticoes), 2),
            "percentual_medio_perfil": round(statistics.mean(uso_perfil), 2),
            "total_jogos_analisados": len(self.jogos)
        }

    def salvar(self, caminho):
        dados = self.extrair()
        with open(caminho, "w", encoding="utf-8") as f:
            json.dump(dados, f, indent=4)
