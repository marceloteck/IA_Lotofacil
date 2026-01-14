# src/engine/seletor_jogos.py

from src.engine.motor_multicerebro import gerar_jogo
from src.engine.nn_cerebro import CerebroNeural
from src.utils.extrator_features import extrair_features
import random

class SeletorJogos:

    def __init__(self, usar_nn=True):
        self.usar_nn = usar_nn
        self.nn = CerebroNeural() if usar_nn else None

    def gerar_jogos_filtrados(self, total_gerados=30, total_selecionados=10):
        jogos = [gerar_jogo() for _ in range(total_gerados)]

        if not self.usar_nn:
            random.shuffle(jogos)
            return jogos[:total_selecionados]

        avaliados = []
        for jogo in jogos:
            features = extrair_features(jogo)
            score = self.nn.avaliar_jogo(features)
            avaliados.append((jogo, score))

        avaliados.sort(key=lambda x: x[1], reverse=True)

        # mantém diversidade (não pega só o topo)
        melhores = avaliados[:total_selecionados * 2]
        random.shuffle(melhores)

        return [j[0] for j in melhores[:total_selecionados]]
