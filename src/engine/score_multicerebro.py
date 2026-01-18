# src/engine/score_multicerebro.py

class ScoreMultiCerebro:
    """
    🧠 Motor de score multicritério
    Projetado para maximizar chance real de 14/15
    """

    def __init__(self, memoria):
        self.memoria = memoria
        self.freq = memoria.frequencia_dezenas()

    def score_final(self, jogo):
        detalhes = {}

        # 1️⃣ Frequência histórica ponderada
        score_freq = sum(self.freq.get(d, 0) for d in jogo)
        detalhes["frequencia"] = score_freq

        # 2️⃣ Paridade (ideal 7/8)
        pares = sum(1 for d in jogo if d % 2 == 0)
        impares = len(jogo) - pares
        score_paridade = 10 - abs(pares - impares)
        detalhes["paridade"] = score_paridade

        # 3️⃣ Distribuição por regiões
        faixas = [
            sum(1 for d in jogo if 1 <= d <= 5),
            sum(1 for d in jogo if 6 <= d <= 10),
            sum(1 for d in jogo if 11 <= d <= 15),
            sum(1 for d in jogo if 16 <= d <= 25),
        ]
        score_regiao = 10 - (max(faixas) - min(faixas))
        detalhes["regioes"] = score_regiao

        # 4️⃣ Sequências longas (repulsão)
        ordenado = sorted(jogo)
        seq = sum(
            1 for i in range(len(ordenado) - 1)
            if ordenado[i] + 1 == ordenado[i + 1]
        )
        score_seq = max(0, 10 - seq)
        detalhes["sequencias"] = score_seq

        # 🔥 SCORE FINAL REAL
        score_total = (
            score_freq * 0.35 +
            score_paridade * 1.6 +
            score_regiao * 1.4 +
            score_seq * 1.5
        )

        return score_total, detalhes
