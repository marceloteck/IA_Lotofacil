# src/experimental/treinar_nn.py

import joblib
import numpy as np
from sklearn.neural_network import MLPClassifier
from src.db.memoria_sqlite import carregar_memoria_completa
from src.utils.extrator_features import extrair_features

def carregar_dados_treino():
    X = []
    y = []

    registros = carregar_memoria_completa()  
    # deve retornar: concurso, dezenas, pontos

    for concurso, dezenas, pontos in registros:
        features = extrair_features(dezenas)

        X.append(list(features.values()))
        y.append(1 if pontos >= 11 else 0)

    return np.array(X), np.array(y)

def treinar_nn():
    X, y = carregar_dados_treino()

    if len(X) < 50:
        print("❌ Dados insuficientes para treinar a rede neural")
        return

    modelo = MLPClassifier(
        hidden_layer_sizes=(16, 8),
        activation="relu",
        solver="adam",
        max_iter=500,
        random_state=42
    )

    modelo.fit(X, y)

    joblib.dump(modelo, "data/modelo_nn.pkl")
    print("✅ Modelo neural treinado e salvo com sucesso")

if __name__ == "__main__":
    treinar_nn()
