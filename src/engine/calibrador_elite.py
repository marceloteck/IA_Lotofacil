import json
import os
from statistics import mean
from collections import Counter

from src.db.memoria_sqlite import carregar_jogos_premiados
from src.utils.dados import carregar_resultados


ARQ_CALIBRACAO = "src/engine/calibracao_elite.json"


def analisar_jogo(jogo, ultimo_resultado, quentes, frias):
    return {
        "quentes": len(set(jogo) & quentes),
        "frias": len(set(jogo) & frias),
        "repetidas": len(set(jogo) & set(ultimo_resultado)),
        "pares": sum(1 for n in jogo if n % 2 == 0),
        "soma": sum(jogo)
    }


def calibrar_filtro_elite():
    print("🧪 Calibração Elite iniciada")

    jogos = carregar_jogos_premiados(min_pontos=14)
    resultados = carregar_resultados()

    if not jogos:
        print("⚠️ Nenhum jogo premiado encontrado para calibração")
        return

    ultimo_resultado = resultados[-1]["dezenas"]

    # 🔥 Frequência global
    freq = Counter()
    for r in resultados:
        freq.update(r["dezenas"])

    ordenadas = [n for n, _ in freq.most_common()]
    quentes = set(ordenadas[:10])
    frias = set(ordenadas[-10:])

    metricas = {
        "quentes": [],
        "frias": [],
        "repetidas": [],
        "pares": [],
        "soma": []
    }

    for jogo in jogos:
        dados = analisar_jogo(jogo["dezenas"], ultimo_resultado, quentes, frias)
        for k in metricas:
            metricas[k].append(dados[k])

    calibracao = {}
    for k, valores in metricas.items():
        calibracao[k] = {
            "min": min(valores),
            "max": max(valores),
            "media": round(mean(valores), 2)
        }

    os.makedirs(os.path.dirname(ARQ_CALIBRACAO), exist_ok=True)
    with open(ARQ_CALIBRACAO, "w", encoding="utf-8") as f:
        json.dump(calibracao, f, indent=4)

    print("✅ Calibração concluída")
    print(f"📁 Arquivo salvo em {ARQ_CALIBRACAO}")
