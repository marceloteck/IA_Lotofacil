import json
import random

ARQUIVO_PERFIL = "src/memory/perfil_vencedor.json"

def gerar_jogo_inteligente():
    with open(ARQUIVO_PERFIL, "r", encoding="utf-8") as f:
        perfil = json.load(f)

    freq = perfil["frequencia_dezenas"]
    dezenas = list(range(1, 26))

    pesos = [freq.get(str(d), 1) for d in dezenas]

    jogo = random.choices(dezenas, weights=pesos, k=15)
    return sorted(set(jogo))[:15]
