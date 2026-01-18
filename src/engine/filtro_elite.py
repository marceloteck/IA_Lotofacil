import json
import os

ARQ_CALIBRACAO = "src/engine/calibracao_elite.json"


def carregar_calibracao():
    if not os.path.exists(ARQ_CALIBRACAO):
        return None
    with open(ARQ_CALIBRACAO, "r", encoding="utf-8") as f:
        return json.load(f)


def passa_filtro_elite(jogo, dezenas_quentes, dezenas_frias, ultimo_resultado):
    calibracao = carregar_calibracao()

    quentes = len(set(jogo) & set(dezenas_quentes))
    frias = len(set(jogo) & set(dezenas_frias))
    repetidas = len(set(jogo) & set(ultimo_resultado))
    pares = sum(1 for n in jogo if n % 2 == 0)
    soma = sum(jogo)

    # 🔁 MODO ANTIGO (fallback)
    if not calibracao:
        return (
            6 <= quentes <= 10 and
            3 <= frias <= 6 and
            6 <= repetidas <= 11 and
            6 <= pares <= 9
        )

    # 🧠 MODO CALIBRADO
    regras = {
        "quentes": quentes,
        "frias": frias,
        "repetidas": repetidas,
        "pares": pares,
        "soma": soma
    }

    for chave, valor in regras.items():
        cfg = calibracao.get(chave)
        if not cfg:
            continue
        if valor < cfg["min"] or valor > cfg["max"]:
            return False

    return True
