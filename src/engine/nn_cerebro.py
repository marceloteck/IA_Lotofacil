# src/engine/nn_cerebro.py

import joblib
import numpy as np

class CerebroNeural:

    def __init__(self, modelo_path="data/modelo_nn.pkl"):
        self.modelo = joblib.load(modelo_path)

    def avaliar_jogo(self, features: dict) -> float:
        ordem = [
            "soma", "pares", "impares", "repeticao_anterior",
            "perc_perfil", "freq_media", "dispersao", "entropia"
        ]

        vetor = np.array([[features[k] for k in ordem]])
        score = self.modelo.predict_proba(vetor)[0][1]
        return round(float(score), 4)
