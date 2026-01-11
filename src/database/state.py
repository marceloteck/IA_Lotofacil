import json
import os

CAMINHO_ESTADO = "data/estado_motor.json"

ESTADO_PADRAO = {
    "tentativas": 0,
    "melhor_pontos": 0,
    "limite_tentativas": 600
}

def carregar_estado():
    if not os.path.exists("data"):
        os.makedirs("data")

    if not os.path.exists(CAMINHO_ESTADO):
        salvar_estado(
            ESTADO_PADRAO["tentativas"],
            ESTADO_PADRAO["melhor_pontos"],
            ESTADO_PADRAO["limite_tentativas"]
        )
        return ESTADO_PADRAO.copy()

    with open(CAMINHO_ESTADO, "r", encoding="utf-8") as f:
        return json.load(f)

def salvar_estado(tentativas, melhor_pontos, limite_tentativas=None):
    estado = {
        "tentativas": tentativas,
        "melhor_pontos": melhor_pontos,
        "limite_tentativas": limite_tentativas or ESTADO_PADRAO["limite_tentativas"]
    }

    with open(CAMINHO_ESTADO, "w", encoding="utf-8") as f:
        json.dump(estado, f, indent=4)
