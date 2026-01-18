"""
🔥 SELETOR EXTREMO — IA ANTI-CAOS
Seleciona apenas os jogos mais alinhados com 14/15 reais.
"""

from time import time
from typing import List, Tuple

from src.engine.score_1415 import calcular_score_1415
from src.engine.cerebros_memoria import obter_cerebros_memoria
from src.engine.estatisticas import calcular_dezenas_quentes_frias
from src.utils.dados import carregar_resultados
from src.utils.logger import logger

from collections import Counter
from time import time

class SeletorExtremo:

    def __init__(self, top_n=10, score_minimo=-999, timeout_segundos=10):
        self.top_n = top_n
        self.score_minimo = score_minimo
        self.timeout_segundos = timeout_segundos

        # 🧠 Memória principal (14/15 reais)
        self.cerebros = obter_cerebros_memoria()
        self.memoria_1415 = self.cerebros.memoria  # lista de jogos históricos

        # 📊 Frequência GLOBAL (calculada UMA ÚNICA VEZ)
        logger.info("🧮 Calculando frequência global das dezenas (cache)")
        

        self.freq_global = Counter()
        inicio = time()

        for idx, jogo in enumerate(self.memoria_1415, 1):
            self.freq_global.update(jogo)

            if idx % 5000 == 0:
                logger.info(
                    f"🧮 Frequência | Processados {idx}/{len(self.memoria_1415)} "
                    f"| Tempo: {round(time() - inicio, 2)}s"
                )

            

        # 🔥 Dezenas quentes e frias
        self.dezenas_quentes, self.dezenas_frias = calcular_dezenas_quentes_frias()

        # 🕰️ Histórico recente (anti-clone / similaridade)
        resultados = carregar_resultados()
        self.historico = [r["dezenas"] for r in resultados[-300:]]

        logger.info(
            f"🧠 Seletor extremo pronto | "
            f"Memória: {len(self.memoria_1415)} jogos | "
            f"Histórico recente: {len(self.historico)}"
        )


    def selecionar(self, jogos: List[List[int]]) -> List[Tuple[List[int], float]]:
        inicio = time()
        avaliados = []

        logger.info(f"🧠 Seletor extremo iniciado | Jogos recebidos: {len(jogos)}")

        for idx, jogo in enumerate(jogos, 1):
            if time() - inicio > self.timeout_segundos:
                logger.warning("⏱️ Timeout atingido no seletor extremo")
                break

            score = calcular_score_1415(
                jogo=jogo,
                memoria_1415=self.memoria_1415,
                dezenas_quentes=self.dezenas_quentes,
                dezenas_frias=self.dezenas_frias,
                historico_resultados=self.historico
            )

            if score >= self.score_minimo:
                avaliados.append((jogo, score))

            if idx % 1 == 0:
                logger.info(f"⏳ Avaliados {idx}/{len(jogos)} | Aprovados {len(avaliados)}")


        avaliados.sort(key=lambda x: x[1], reverse=True)
        return avaliados[: self.top_n]


def selecionar_top_jogos(jogos, top_n=10, score_minimo=-999, timeout_segundos=10):
    seletor = SeletorExtremo(top_n, score_minimo, timeout_segundos)
    resultado = seletor.selecionar(jogos)
    return [j for j, _ in resultado]
