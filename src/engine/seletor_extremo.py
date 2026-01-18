"""
🔥 SELETOR EXTREMO — IA ANTI-CAOS
Elimina brutalmente jogos ruins e mantém
os mais alinhados com 14/15 pontos reais.
"""

from typing import List, Tuple
from time import time

from src.engine.score_1415 import calcular_score_1415
from src.engine.cerebros_memoria import obter_cerebros_memoria
from src.utils.dados import carregar_resultados
from src.utils.logger import logger


class SeletorExtremo:
    """
    Motor seletivo de alto nível.
    Não gera jogos — apenas decide quais sobrevivem.
    """

    def __init__(
        self,
        top_n: int = 10,
        score_minimo: float = -999,
        timeout_segundos: int = 10
    ):
        self.top_n = top_n
        self.score_minimo = score_minimo
        self.timeout_segundos = timeout_segundos

        self.cerebros = obter_cerebros_memoria()
        self.historico = [
            r["dezenas"] for r in carregar_resultados()
        ]

    # --------------------------------------------------
    # 🔥 SELEÇÃO PRINCIPAL
    # --------------------------------------------------
    def selecionar(self, jogos):
        """
        Recebe lista de jogos e retorna os TOP N:
        [(jogo, score_final), ...]
        """

        inicio = time()
        avaliados = []

        total = len(jogos)
        logger.info(f"🧠 Seletor extremo iniciado | Jogos recebidos: {total}")

        for idx, jogo in enumerate(jogos, start=1):
            # ⏱️ Proteção contra travamento
            if time() - inicio > self.timeout_segundos:
                logger.warning("⏱️ Timeout atingido no seletor extremo")
                break

            # 🔥 SCORE ÚNICO E OFICIAL
            score_final, detalhes = self.cerebros.score_final(jogo)

            if score_final >= self.score_minimo:
                avaliados.append((jogo, score_final))

            # Log leve
            if idx % 100 == 0 or idx == total:
                logger.debug(
                    f"🧠 Avaliados: {idx}/{total} | "
                    f"Aprovados: {len(avaliados)}"
                )

        if not avaliados:
            logger.warning("⚠️ Nenhum jogo passou no filtro mínimo")
            return []

        # 🏆 ORDENAÇÃO FINAL
        avaliados.sort(key=lambda x: x[1], reverse=True)
        selecionados = avaliados[: self.top_n]

        logger.info(
            f"✅ Seleção concluída | "
            f"Sobreviventes: {len(selecionados)} / {total}"
        )

        return selecionados



# --------------------------------------------------
# 🚀 FUNÇÃO DE ATALHO
# --------------------------------------------------
def selecionar_top_jogos(
    jogos: List[List[int]],
    top_n: int = 10,
    score_minimo: float = -999,
    timeout_segundos: int = 10
) -> List[List[int]]:

    seletor = SeletorExtremo(
        top_n=top_n,
        score_minimo=score_minimo,
        timeout_segundos=timeout_segundos
    )

    resultado = seletor.selecionar(jogos)
    return [jogo for jogo, _ in resultado]
