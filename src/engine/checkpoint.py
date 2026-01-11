# src/engine/checkpoint.py

import json
import os

CHECKPOINT_PATH = "data/checkpoint.json"


def salvar_checkpoint(dados):
    os.makedirs("data", exist_ok=True)
    with open(CHECKPOINT_PATH, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4)


def carregar_checkpoint():
    if not os.path.exists(CHECKPOINT_PATH):
        return None
    with open(CHECKPOINT_PATH, "r", encoding="utf-8") as f:
        return json.load(f)
