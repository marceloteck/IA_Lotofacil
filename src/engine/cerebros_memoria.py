"""
🧠 CÉREBROS DE MEMÓRIA — IA HISTÓRICA
Avalia jogos com base em tudo que já deu 11–15 pontos.
"""

from collections import Counter
from typing import List, Tuple

from src.db.memoria_sqlite import carregar_memoria_premiada
from src.utils.logger import logger


class CerebrosMemoria:
    """
    Motor de avaliação baseado em memória premiada real.
    """

    def __init__(self):
        self.memoria = []
        self.contagem_dezenas = Counter()
        self._carregar_memoria()

    # --------------------------------------------------
    # 📥 CARGA DA MEMÓRIA
    # --------------------------------------------------
    def _carregar_memoria(self):
        registros = carregar_memoria_premiada()

        if not registros:
            logger.warning("⚠️ Memória premiada vazia")
            return

        for r in registros:
            dezenas = sorted(r["dezenas"])
            pontos = int(r["pontos"])

            self.memoria.append({
                "dezenas": dezenas,
                "pontos": pontos
            })

            # Peso maior para jogos melhores
            peso = pontos - 10  # 11→1, 15→5
            for d in dezenas:
                self.contagem_dezenas[d] += peso

        logger.info(
            f"🧠 Memória carregada | Jogos: {len(self.memoria)} | "
            f"Dezenas únicas: {len(self.contagem_dezenas)}"
        )

    # --------------------------------------------------
    # 🎯 SCORE PRINCIPAL
    # --------------------------------------------------
    def score_final(self, jogo: List[int]) -> Tuple[float, dict]:
        """
        Score baseado em alinhamento com a memória histórica
        """

        score = 0.0
        detalhes = {}

        # 🔢 Score por dezenas fortes na memória
        pontos_memoria = sum(
            self.contagem_dezenas.get(d, 0)
            for d in jogo
        )

        score += pontos_memoria
        detalhes["memoria_dezenas"] = pontos_memoria

        # 🔁 Similaridade com jogos premiados
        similaridades = []
        for m in self.memoria:
            inter = len(set(jogo) & set(m["dezenas"]))
            if inter >= 11:
                similaridades.append(inter)

        bonus_similaridade = sum(similaridades) * 2
        score += bonus_similaridade
        detalhes["similaridade"] = bonus_similaridade

        return score, detalhes


# --------------------------------------------------
# 🧠 SINGLETON GLOBAL
# --------------------------------------------------
_cerebro_global = None


def obter_cerebros_memoria() -> CerebrosMemoria:
    global _cerebro_global

    if _cerebro_global is None:
        _cerebro_global = CerebrosMemoria()

    return _cerebro_global
